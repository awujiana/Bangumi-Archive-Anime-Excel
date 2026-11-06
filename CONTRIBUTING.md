<div align="center">

<p align="center">
  <a href="LICENSE"><img alt="协议 CC BY-SA 4.0" src="https://img.shields.io/badge/协议-CC%20BY--SA%204.0-lightgrey?style=flat"></a>
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat"></a>
</p>

<h1>贡献指南</h1>

<strong>欢迎参与「Bangumi 动画存档数据」的共建</strong>

</div>

---

感谢你关注 **Bangumi-Archive-Anime-Excel** 并愿意贡献。本仓库是**数据仓库**，主要产出为 JSONL 分片数据与每周差异摘要。

> 维护者：awujiana ｜ 许可协议：以仓库 `LICENSE` 为准（CC BY-SA 4.0）

## 📚 目录

- [我能如何参与](#我能如何参与)
- [提交 Issue 前](#提交-issue-前)
- [提交 Pull Request 前](#提交-pull-request-前)
- [命名规范（不缩写）](#命名规范不缩写)
- [数据与文档约定](#数据与文档约定)
- [行为准则](#行为准则)
- [许可证](#许可证)

## 🤝 我能如何参与

- **提交 Issue**：反馈数据缺失、字段异常、分片下载失败或文档错误。
- **完善文档**：改进 README、数据字典与使用说明。
- **改进数据管线**：优化字段分组、差异摘要与清单生成（须保持清单与分片一致）。
- **报告来源问题**：上游 `bangumi/Archive` 的数据问题请同时注明上游期次。

## 🐞 提交 Issue 前

1. 先搜索确认问题未被重复提出。
2. 说明期次（`data/anime.manifest.json` 的日期）与涉及的字段 / 分片。
3. 附上校验信息（分片名、`bytes`、`sha256`）与复现步骤。
4. 说明是「缺数据」「字段错」「下载失败」还是「文档问题」。

## 🔀 提交 Pull Request 前

1. 从 `main` 切出特性分支，命名如 `fix/manifest-sha` 或 `docs/data-dict`。
2. 遵循本仓库的 README 输出规范：居中徽章、双名标题、底部三节。
3. **数据仓库不加 AI 辅助生成声明**。
4. 改动分片或清单时，必须同步 `data/anime.manifest.json` 的 `bytes` / `sha256` / 记录数。
5. 命名一律全拼、禁止缩写、名称不重复。
6. 提交信息清晰说明「做了什么 / 为什么」。

## 📝 命名规范（不缩写）

### 总则

- **一律全拼，禁止缩写**：`cfg`→`config`、`msg`→`message`、`err`→`error`、`idx`→`index`。
- **名称不重复**：同目录文件名唯一（大小写不敏感）。
- **名称即语义**：禁止 `data1`、`temp`、`misc` 等泛化名。

### 文件命名

| 类型 | 规则 | 示例 |
| --- | --- | --- |
| 数据分片 | `<主题>.<字段>.jsonlines.gz` | `anime.base.jsonlines.gz` |
| 清单 | `kebab-case.json` | `anime.manifest.json` |
| Excel | `kebab-case-YYYY-MM-DD.xlsx` | `ani-bangumi-type2-2026-08-04.xlsx` |
| 文档 | `kebab-case.md` | `readme.md` |

## 📋 数据与文档约定

- 正文以简体中文为主，专有名词（JSONL / gzip / sha256）保留英文原文。
- 对比 / 字段类信息优先使用表格。
- **清单是唯一入口**：分片名、字段、字节数、`sha256` 以 `data/anime.manifest.json` 为准。
- **完整性可校验**：每片同时给出压缩后字节数与 SHA-256。
- **不裁剪原始字段**：顶层字段保真，按分片归组。

## 🤗 行为准则

请保持友善、专业、就事论事。尊重不同经验水平的贡献者，不人身攻击、不贬低他人工作。

## 📄 许可证

本仓库基于 **CC BY-SA 4.0** 发布；向本仓库提交贡献，即表示你同意以该协议发布你的贡献。详见 [LICENSE](LICENSE)。

[![CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
