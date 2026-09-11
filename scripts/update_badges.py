#!/usr/bin/env python3
"""把 README.md 中的统计信息对齐到当前数据文件（bangumi.jsonl）。

Usage:
    python scripts/update_badges.py [--readme README_PATH] [--jsonl JSONL_PATH] [--check]

一次同步以下全部位置：

1. 徽章 `记录数-<N>-2da44e`          <- 记录条数
2. 徽章 `更新日期-<YYYY-MM-DD>-2da44e` <- 最后一条记录的 updatedAt
   （缺失时自动插入到「更新频率」徽章之后；「更新频率-每周三」徽章本身不改动）
3. 正文 `- **大小**：约 N MB（M 字节）`
4. 正文 `- **记录数**：N 条`
5. 正文 `- **最近更新**：YYYY-MM-DD`
6. 目录树注释 `# BGM 插件数据源（~N MB，M 条）`

日期取自数据文件本身（最后一条记录的 updatedAt），而不是运行脚本的当天，
这样即使补跑流水线也不会把「更新日期」写成错误的日期。

`--check` 只检查不写入：README 与数据不一致时退出码为 1，便于 CI / 预提交校验。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import NamedTuple

# 数据源路径（相对仓库根目录）
DEFAULT_README = 'README.md'
DEFAULT_JSONL = 'data/bangumi.jsonl'

# 回溯最后若干条记录以查找 updatedAt（正常情况下最后一条就有）
_TAIL_SCAN_LINES = 10


class Stats(NamedTuple):
    """从数据文件解析出的统计信息。"""

    record_count: int
    size_bytes: int
    size_mb: int
    last_updated: str


# ---------------------------------------------------------------- 数据文件解析

def count_records(jsonl_path: Path) -> int:
    """统计 JSONL 中的有效记录数（忽略空行）。"""
    count = 0
    with open(jsonl_path, 'r', encoding='utf-8') as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def read_last_updated(jsonl_path: Path) -> str | None:
    """读取最后一条记录里的 updatedAt（倒序回溯若干行）。"""
    tail: deque[str] = deque(maxlen=_TAIL_SCAN_LINES)
    with open(jsonl_path, 'r', encoding='utf-8') as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                tail.append(stripped)

    for line in reversed(tail):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            value = record.get('updatedAt')
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def collect_stats(jsonl_path: Path) -> Stats:
    """收集 README 需要的全部统计信息。"""
    record_count = count_records(jsonl_path)
    size_bytes = jsonl_path.stat().st_size
    size_mb = round(size_bytes / (1024 * 1024))
    last_updated = read_last_updated(jsonl_path) or ''
    return Stats(record_count, size_bytes, size_mb, last_updated)


# ---------------------------------------------------------------- README 重写

BADGE_COUNT_RE = re.compile(r'(img\.shields\.io/badge/记录数-)\d+(-2da44e)')
BADGE_DATE_RE = re.compile(r'(img\.shields\.io/badge/更新日期-)[0-9-]+(-2da44e)')
BADGE_DATE_LINE = '[![Last Update](https://img.shields.io/badge/更新日期-{date}-2da44e.svg)](data/bangumi.jsonl)'
BADGE_FREQ_MARKER = 'img.shields.io/badge/更新频率-'

BODY_SIZE_RE = re.compile(r'(?m)^(- \*\*大小\*\*：)约\s*[\d.]+\s*MB.*$')
BODY_COUNT_RE = re.compile(r'(?m)^(- \*\*记录数\*\*：)\d+(\s*条)\s*$')
BODY_UPDATED_RE = re.compile(r'(?m)^(- \*\*最近更新\*\*：)\d{4}-\d{2}-\d{2}\s*$')
BODY_FREQ_RE = re.compile(r'(?m)^- \*\*更新频率\*\*：[^\n]*$')

TREE_RE = re.compile(r'(BGM 插件数据源（~)\d+( MB，)\d+( 条）)')


def _ensure_date_badge(content: str, last_updated: str) -> str:
    """更新「更新日期」徽章；不存在时插入到「更新频率」徽章之后。"""
    if BADGE_DATE_RE.search(content):
        return BADGE_DATE_RE.sub(rf'\g<1>{last_updated}\g<2>', content)

    lines = content.split('\n')
    for index, line in enumerate(lines):
        if BADGE_FREQ_MARKER in line:
            lines.insert(index + 1, BADGE_DATE_LINE.format(date=last_updated))
            return '\n'.join(lines)
    return content


def _ensure_updated_body_line(content: str, last_updated: str) -> str:
    """更新正文「最近更新」条目；不存在时插入到「更新频率」条目之后。"""
    if BODY_UPDATED_RE.search(content):
        return BODY_UPDATED_RE.sub(rf'\g<1>{last_updated}', content)

    match = BODY_FREQ_RE.search(content)
    if not match:
        return content
    insert_at = match.end()
    return f'{content[:insert_at]}\n- **最近更新**：{last_updated}{content[insert_at:]}'


def render_readme(content: str, stats: Stats) -> str:
    """返回对齐后的 README 内容（不落盘）。"""
    # 1) 记录数徽章
    content = BADGE_COUNT_RE.sub(rf'\g<1>{stats.record_count}\g<2>', content)

    # 2) 更新日期徽章（仅在拿到有效日期时改动）
    if stats.last_updated:
        content = _ensure_date_badge(content, stats.last_updated)

    # 3) 正文大小
    content = BODY_SIZE_RE.sub(
        rf'\g<1>约 {stats.size_mb} MB（{stats.size_bytes:,} 字节）', content
    )

    # 4) 正文记录数
    content = BODY_COUNT_RE.sub(rf'\g<1>{stats.record_count}\g<2>', content)

    # 5) 正文最近更新
    if stats.last_updated:
        content = _ensure_updated_body_line(content, stats.last_updated)

    # 6) 目录树注释
    content = TREE_RE.sub(
        rf'\g<1>{stats.size_mb}\g<2>{stats.record_count}\g<3>', content
    )

    return content


def update_readme(readme_path: Path, stats: Stats, check_only: bool = False) -> tuple[bool, bool]:
    """对齐 README。

    返回 ``(needs_update, changed)``：
    - ``needs_update``：README 与数据文件不一致
    - ``changed``：本次是否实际写入了文件（``check_only`` 时恒为 False）
    """
    if not readme_path.is_file():
        raise FileNotFoundError(f'找不到 README 文件: {readme_path}')

    original = readme_path.read_text(encoding='utf-8')
    updated = render_readme(original, stats)

    if updated == original:
        return False, False

    if check_only:
        return True, False

    readme_path.write_text(updated, encoding='utf-8')
    return True, True


# ---------------------------------------------------------------- CLI

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='把 README.md 的徽章与统计信息对齐到当前 bangumi.jsonl',
    )
    parser.add_argument('--readme', default=DEFAULT_README, help=f'README 路径（默认 {DEFAULT_README}）')
    parser.add_argument('--jsonl', default=DEFAULT_JSONL, help=f'JSONL 数据路径（默认 {DEFAULT_JSONL}）')
    parser.add_argument('--check', action='store_true', help='只检查不写入，过期时退出码为 1')
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    readme_path = Path(args.readme)
    jsonl_path = Path(args.jsonl)

    if not jsonl_path.is_file():
        print(f'[错误] 找不到数据文件: {jsonl_path}')
        return 2

    stats = collect_stats(jsonl_path)
    print(
        f'数据文件: {jsonl_path} | 记录数: {stats.record_count} | '
        f'大小: {stats.size_bytes:,} 字节（约 {stats.size_mb} MB） | '
        f'最近更新: {stats.last_updated or "未知"}'
    )

    try:
        needs_update, changed = update_readme(readme_path, stats, check_only=args.check)
    except FileNotFoundError as error:
        print(f'[错误] {error}')
        return 2

    if args.check:
        if needs_update:
            print(f'[过期] {readme_path} 与数据文件不一致，请运行本脚本同步')
            return 1
        print(f'[一致] {readme_path} 已与数据文件对齐')
        return 0

    if not changed:
        print(f'[跳过] {readme_path} 已是最新，无需改动')
        return 0

    print(f'[完成] 已更新 {readme_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
