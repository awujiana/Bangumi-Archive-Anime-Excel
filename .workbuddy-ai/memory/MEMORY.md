# Bangumi-Archive-Anime-Excel · 项目长期记忆

## 定位与协议

- 纯**数据下发仓库**：只放 `data/`（6 个 JSONL 分片 + 清单）、`differences/`（周差异）、README、LICENSE；
  处理脚本全部在业务仓库 `D:\编程\awujiana\Archive\scripts\`。
- 协议 **CC BY-SA 4.0**（2026-10-26 由 AGPL-3.0 改来）：允许商用，要求署名 + 相同方式共享。
  `LICENSE` 存 CC 官方法律文本全文（逐字不改，便于 GitHub 识别）。
- 作者署名 **awujian**，联系方式 bingshanlengtie@qq.com。

## ⚠️ README 改写的硬约束

每周三由 `Archive/scripts/push_data_repository.py` → `update_badges.py` 自动改写 README。
以下 6 处格式一旦变动就**静默失效**（不报错，只是不再更新），重构时须原样保留：

1. `img.shields.io/badge/记录数-<N>-2da44e`
2. `img.shields.io/badge/更新日期-<YYYY--MM--DD>-2da44e`（连字符须 `--` 转义，否则渲染 404 图）
3. `- **大小**：约 N MB（...字节，解压后 X MiB）`
4. `- **记录数**：N 条`
5. `- **最近更新**：YYYY-MM-DD`
6. 目录树注释 `BGM 插件数据源（~N MB，M 条`

许可徽章不在其管理范围，可自由改。

## README 结构（awujian-readme-style v2.0，2026-10-26 重构）

居中徽章区（协议/语言/作者/格式 + 更新频率/更新日期/记录数/Stars，共 8 枚）
→ `<h1>` + `<strong>` 一句话 → `---` → `## 📚 目录`
→ 正文 12 节 → 底部三节（关联仓库 / 作者联系方式 / 开源协议）。

- **不加 AI 辅助生成 `[!WARNING]` 声明**（用户 2026-10-26 决定）：本仓库是纯数据仓库、
  不含可执行代码，该声明的前提（AI 参与的代码生成）不成立。规范里那条是"有 AI 参与才加"，
  不要照搬。

- TOC 一律用 `<a id="sec-N"></a>` 稳定锚点；**不要**依赖 emoji 自动锚点（VS16 会失效）。
- 章节 emoji：🚀 项目简介 / ✨ 核心特色 / 📷 展示图 / 📂 目录结构 / 📊 数据文件说明 /
  🔄 数据更新流程 / ⚠️ 注意事项 / 💬 反馈建议 / 🙏 参考与致谢 / 🔗 关联仓库 /
  📮 作者联系方式 / 📄 开源协议。

## 常用命令

- 推送（本机 GCM 弹窗在非交互 shell 下必失败）：
  ```bash
  git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin main
  ```
- 提交信息：Conventional Commits + 中文摘要，正文用 `-` 列表写校验结论。
