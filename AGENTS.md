# AGENTS.md

> 本文件供 **AI 编码 / 写作 agent** 阅读，用于了解本仓库的结构、约定与禁忌，从而在自动改动时保持风格一致。
> 人类贡献者请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目概述

- **名称**：Bangumi 动画存档数据（中文名）
- **GitHub 仓库名（英文名）**：Bangumi-Archive-Anime-Excel
- **类型**：数据仓库（CC BY-SA 4.0，**不加** AI 声明）
- **维护者**：awujiana
- **一句话**：Bangumi Archive 的数据下发仓库，提供 JSONL 分片数据源与每周差异摘要，供 My Bangumi Database for WPS 插件免 token 同步。

## 仓库结构

| 路径 | 用途 | 是否发布 |
| --- | --- | --- |
| `data/anime.manifest.json` | 清单：分片名、字段、字节数、`sha256`、记录数、更新日期 | ✅ |
| `data/*.jsonlines.gz` | 6 个字段分片（base / infobox / meta / relations / stats / summary） | ✅ |
| `xlsx/*.xlsx` | 主数据（75 列）与模板（42 列）Excel | ✅ |
| `differences/` | 相邻期次差异摘要 | ✅ |
| `README.md` / `CONTRIBUTING.md` / `AGENTS.md` / `CHANGELOG.md` | 文档 | ✅ |
| `LICENSE` | CC BY-SA 4.0 说明 | ✅ |

## 必须遵守的约定

1. **命名规范（不缩写）**：分片 `<主题>.<字段>.jsonlines.gz`、清单 `kebab-case.json`、Excel `kebab-case-YYYY-MM-DD.xlsx`，全拼无缩写、名称不重复。
2. **项目核心不变量**：
   - **清单是唯一入口**：分片名 / 字段 / `bytes` / `sha256` / 记录数以 `data/anime.manifest.json` 为准。
   - **完整性可校验**：每片给出压缩后字节数与 SHA-256，下载后可逐字节比对。
   - **不裁剪原始字段**：原始 dump 顶层字段保真，37 个字段按分片归组。
   - **免 token**：插件直连 raw URL，不调用 Bangumi API，规避 token 与限流。
   - **每周三更新**：随上游 `bangumi/Archive` 的 dump 同步。
3. **技术禁令**：不得引入需要 token 的访问方式；不得在未同步清单的情况下改动分片；不得添加 AI 辅助生成声明（数据仓库）。
4. **README 风格**：居中徽章 → 双名标题（中文 `<h1>` 在上、英文 `<h2>` 在下）→ 目录 → 正文 → 关联标签 → 底部三节。
5. **协议**：CC BY-SA 4.0（`LICENSE` 指向官方 legalcode，不内嵌全文）。
6. **提交信息**：说明「做了什么 / 为什么」。
7. **提交身份**：`git config user.name` 必须是 `awujiana`，`user.email` 必须是 `bingshanlengtie@qq.com`。
8. **维护**：每次改动同步 `CHANGELOG.md` 与 `data/anime.manifest.json`。

## 改动前检查

- 改分片 / 清单：核对 `anime.manifest.json` 的 `bytes` / `sha256` / 记录数与实际分片一致。
- 改 Excel：确认 75 列主数据与 42 列模板的字段映射未漂移。
- 改文档：同步 `CHANGELOG.md`。
- 提交：`git status` 确认不含临时文件。

## 不要做的事

- 不要添加 AI 辅助生成声明（本仓库为数据仓库）。
- 不要手写 `⚠️ Warning` 代替 `> [!WARNING]`。
- 不要缩写命名、不要同名文件。
- 不要在未更新清单的情况下替换分片。
- 不要引入 token / API 依赖。
- 不要删除 `AGENTS.md` / `CONTRIBUTING.md` / `CHANGELOG.md`。
