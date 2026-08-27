# 项目长期记忆 (Bangumi-Archive-Anime-Excel)

## Git 工作流注意事项
- 整合远程提交用 **merge 不要用 rebase**：本仓库 `git checkout/reset/rebase` 到远程提交时会把 `differences/` 下旧周差异文件夹整目录从工作树删除（文件/树都在，checkout 写不回磁盘，疑似 Windows + autocrlf + 编辑器占用）。rebase 会被 git 拒绝保护；用 `git merge <remote>` 安全。
- `origin/main` 引用会被 IDE 后台自动 fetch 清成 [gone]，手动 update-ref 也会被冲掉；属表象，推送时 IDE 自建。
- 本机到 GitHub 的 HTTPS（schannel）网络不稳，fetch/pull 常 early EOF / 握手失败；可只 fetch 单分支 `git fetch origin main`，成功率较高。
- 仓库未设 .gitattributes，`core.autocrlf=true`，数据文件(data/bangumi.jsonl 等)有 LF→CRLF 归一化告警；如频繁 checkout 异常，建议 core.autocrlf=false 或加 .gitattributes。
