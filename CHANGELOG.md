# 更新日志

本文件记录 `Bangumi 动画存档数据`（Bangumi-Archive-Anime-Excel）的重要变更，版本号遵循语义化版本 `MAJOR.MINOR.PATCH`。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [未发布]

### 新增

- 新增 awujiana 风格 `CONTRIBUTING.md`、`AGENTS.md`、`CHANGELOG.md`。
- README 增加「🏷 关联标签」节，并补齐双名标题（中文名 + 英文仓库名）。

### 改进

- 统一 README 底部三节与居中徽章风格。

## [1.0.0] - 2026-11-03

### 新增

- 数据下发仓库首次成型：6 个字段分片 + `anime.manifest.json` 清单 + 每周差异摘要。
- 主数据（75 列）与模板（42 列）Excel 归档。

### 已知限制

- 数据随上游 `bangumi/Archive` 每周三 dump 同步，存在滞后。
- 插件读取依赖 raw URL，需网络可达。

## 更早的版本

本仓库在 `2026-11-06` 之前已有数据与 README，但未建立 `CHANGELOG.md`，此处不做追溯编造。
