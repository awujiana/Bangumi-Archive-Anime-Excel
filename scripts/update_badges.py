#!/usr/bin/env python3
"""Update README.md badges with current data statistics.

Usage:
    python scripts/update_badges.py [--readme README_PATH] [--jsonl JSONL_PATH]

This script:
1. Counts the number of records in data/bangumi.jsonl
2. Updates the record count badge in README.md
3. Updates the date badge in README.md
"""

import re
import sys
import argparse
from datetime import date
from pathlib import Path


def count_lines(file_path: Path) -> int:
    """Count the number of lines in a file efficiently."""
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for _ in f:
            count += 1
    return count


def update_readme(readme_path: Path, record_count: int) -> bool:
    """Update README.md with new badge values. Returns True if file was modified."""
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        return False

    content = readme_path.read_text(encoding='utf-8')
    original = content

    # Update record count badge
    # Pattern: img.shields.io/badge/记录数-<number>-2da44e
    content = re.sub(
        r'(img\.shields\.io/badge/记录数-)\d+(-2da44e)',
        rf'\g<1>{record_count}\g<2>',
        content,
    )

    # Update date badge
    today_str = date.today().strftime('%Y-%m-%d')
    # Pattern: img.shields.io/badge/更新日期-<date>-2da44e
    content = re.sub(
        r'(img\.shields\.io/badge/更新日期-)[0-9-]+(-2da44e)',
        rf'\g<1>{today_str}\g<2>',
        content,
    )

    if content == original:
        print("No changes needed - badges are up to date")
        return False

    readme_path.write_text(content, encoding='utf-8')
    print(f"Updated README.md: record count = {record_count}, date = {today_str}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Update README.md badges with data statistics',
    )
    parser.add_argument(
        '--readme',
        default='README.md',
        help='Path to README.md (default: README.md)',
    )
    parser.add_argument(
        '--jsonl',
        default='data/bangumi.jsonl',
        help='Path to JSONL data file (default: data/bangumi.jsonl)',
    )
    args = parser.parse_args()

    readme_path = Path(args.readme)
    jsonl_path = Path(args.jsonl)

    if not jsonl_path.exists():
        print(f"Error: {jsonl_path} not found")
        return 1

    record_count = count_lines(jsonl_path)
    print(f"Found {record_count} records in {jsonl_path}")

    updated = update_readme(readme_path, record_count)
    return 0 if updated else 1


if __name__ == '__main__':
    sys.exit(main())