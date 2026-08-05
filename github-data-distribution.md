# GitHub 仓库数据下发指南

本文档说明如何配置 GitHub 仓库，使其作为本插件的数据下发源。插件通过读取仓库中的 `latest.json` 配置文件，自动发现并下载最新版本的数据包。

## 工作流程

```
插件 ──① 读取──▶ latest.json (raw URL)
                   │
                   │ ② 解析出 browser_download_url
                   ▼
            ③ 下载 Release Asset (zip)
                   │
                   │ ④ 解压 → JSONL
                   ▼
            ⑤ 解析 JSONL → 写入 Excel
```

## 仓库结构

```
your-repo/
├── latest.json              ← 版本指针（必须，raw 可访问）
├── data/
│   └── bangumi.jsonl        ← 直接 JSONL 模式（可选，小文件）
└── releases/                ← Release Assets 模式（大文件推荐）
    └── (通过 GitHub Release 上传)
```

## latest.json 配置格式

`latest.json` 是仓库根目录的一个 JSON 文件，内容为 GitHub Release Asset 对象。插件读取此文件后，通过 `browser_download_url` 字段定位并下载最新数据包。

```json
{
  "browser_download_url": "https://github.com/{owner}/{repo}/releases/download/{tag}/{filename}.zip",
  "content_type": "application/zip",
  "created_at": "2026-07-21T21:04:41Z",
  "digest": "sha256:e1120169088407c66a94dacacda4dffaabe0e2e08cbcc8238c880f6c0140dd57",
  "id": 485155893,
  "label": "",
  "name": "dump-2026-07-21.210441Z.zip",
  "node_id": "RA_kwDOGogJqs4c6uQ1",
  "size": 419054508,
  "updated_at": "2026-07-21T21:05:00Z",
  "url": "https://api.github.com/repos/{owner}/{repo}/releases/assets/485155893"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `browser_download_url` | string | **核心字段**。数据包实际下载地址，插件用此 URL 下载数据 |
| `content_type` | string | MIME 类型，通常为 `application/zip` |
| `created_at` | string | Release Asset 创建时间（ISO 8601） |
| `digest` | string | SHA-256 校验值，格式 `sha256:{hash}`，用于完整性校验 |
| `id` | number | GitHub Release Asset ID |
| `label` | string | Asset 标签（可为空） |
| `name` | string | 文件名，如 `dump-2026-07-21.210441Z.zip` |
| `size` | number | 文件大小（字节） |
| `updated_at` | string | 最后更新时间（ISO 8601） |
| `url` | string | GitHub API Asset 资源地址 |

## 数据包格式

下载的 zip 包解压后，必须是一个 **JSONL** 文件（每行一个 JSON 对象）。

### JSONL 单条记录格式

```jsonl
{"sid":"8","name":"Code Geass 反叛的鲁路修R2","updatedAt":"2026-07-21","date":"2008-04-06","meta_tags":["机战","TV","日本","原创","战斗"],"nsfw":false,"播放结束":"2008年9月28日","动画制作公司":"サンライズ","话数":"25","片长":"","制片国家":"","语言":"","类型":"","导演":"谷口悟朗","音乐":"中川幸太郎、黒石ひとみ","人物设定":"木村貴宏","机械设定":"寺岡賢司","原作":"","脚本":"","分镜":"","演出":"","原案":"故事原案：大河内一楼、谷口悟朗","系列构成":"大河内一楼","在线播放平台":"","关联的动漫ID":"85 | 344 | 793"}
```

### 字段定义

输出字段共 25 个，分 3 类。BGM 插件识别全部字段。

**基础字段**（3 个，BGM 插件 `GithubRemoteEntry` 接口）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `sid` | string | 是 | Bangumi subject ID（主键，用于比对去重） |
| `name` | string | 否 | 条目名称 |
| `updatedAt` | string | 否 | 远程更新日期，格式 `YYYY-MM-DD`（仅日期，不含时间） |

**dump 顶层扩展**（3 个）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `date` | string | 否 | 开播日期 |
| `meta_tags` | string[] | 否 | 标签/分级数组（写入 Excel「标签/分级」列，`\|` 分隔） |
| `nsfw` | bool | 否 | 是否 NSFW |

**infobox 解析扩展**（19 个，中文命名）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `话数` | string | 集数（写入 Excel「集数」列） |
| `播放结束` | string | 完播日（写入 Excel「完播日」列） |
| `动画制作公司` | string | 制作公司（写入 Excel「制作公司」列） |
| `片长` | string | 时长/分钟 |
| `制片国家` | string | 同名映射 |
| `语言` | string | 同名映射 |
| `类型` | string | 同名映射 |
| `导演` | string | 同名映射 |
| `音乐` | string | 同名映射 |
| `人物设定` | string | 同名映射 |
| `机械设定` | string | 同名映射 |
| `原作` | string | 同名映射 |
| `脚本` | string | 同名映射 |
| `分镜` | string | 同名映射 |
| `演出` | string | 同名映射 |
| `原案` | string | 同名映射 |
| `系列构成` | string | 同名映射 |
| `在线播放平台` | string | 同名映射 |
| `关联的动漫ID` | string | 关联 subject_id 列表，`' \| '` 分隔 |

### 不输出字段（已移除以减少冗余）

`url`（从 sid 构造）/ `type`（恒为 2=动画）/ `tags`（与 meta_tags 冗余）/ `episode`（恒为 0，用 话数 替代）/ `platform` / `score`（数据源平均分）/ `comment`（dump 不含）

> 插件解析时仅要求 `sid` 为字符串类型，其余字段均为可选。空行与非法行会被跳过并记录警告日志，不中断整体解析。

## 插件配置

在 WPS Excel 加载项面板中填写以下配置：

| 配置项 | 值 | 说明 |
|---|---|---|
| 同步源 | GitHub | 选择 GitHub 同步源 |
| owner | `你的用户名` | GitHub 仓库所有者 |
| repo | `你的仓库名` | 仓库名称 |
| branch | `main` | 分支名（默认 main） |
| path | `latest.json` | 仓库中配置文件的路径 |

插件会从以下 URL 读取配置：

```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}
```

## 发布新版本流程

### 1. 准备数据

将数据导出为 JSONL 文件，压缩为 zip：

```bash
zip data.zip bangumi.jsonl
```

### 2. 创建 GitHub Release

```bash
# 创建 tag
git tag -a v2026-07-21 -m "数据更新 2026-07-21"

# 推送 tag
git push origin v2026-07-21

# 使用 gh CLI 创建 Release 并上传 asset
gh release create v2026-07-21 data.zip \
  --title "数据更新 2026-07-21" \
  --notes "最新 bangumi 数据 dump"
```

### 3. 更新 latest.json

从 GitHub API 获取刚上传的 Asset 信息，更新 `latest.json`：

```bash
# 获取 Release Asset 信息
gh api repos/{owner}/{repo}/releases/latest --jq '.assets[0]'
```

将输出的 JSON 写入仓库根目录的 `latest.json`，然后提交推送：

```bash
git add latest.json
git commit -m "chore: update latest.json → v2026-07-21"
git push origin main
```

### 4. 验证

在 WPS Excel 中点击「GitHub 同步」，插件会：
1. 从 raw URL 读取 `latest.json`
2. 解析 `browser_download_url`
3. 下载 zip 并解压
4. 解析 JSONL 并写入 Excel

## 两种模式对比

| 特性 | 直接 JSONL 模式 | Release Asset 模式 |
|---|---|---|
| 适用场景 | 小文件（< 100MB） | 大文件（> 100MB） |
| path 配置 | `data/bangumi.jsonl` | `latest.json` |
| 数据格式 | 直接 JSONL | zip 压缩包（内含 JSONL） |
| 版本管理 | 无（直接覆盖） | 有（Release tag 历史） |
| 下载方式 | raw.githubusercontent.com | github.com/releases/download |
| 限流 | 60 次/小时（未认证） | Release 下载不限流 |

## 注意事项

1. **仓库必须为 public**，否则 raw URL 和 Release 下载均需认证
2. **latest.json 必须放在 raw 可访问的路径**（即仓库文件，而非 Release Asset）
3. **zip 包内只能有一个 JSONL 文件**，插件自动解压并读取
4. **digest 字段用于校验**，插件下载后会验证 SHA-256（如配置了校验）
5. **未认证限流**：raw URL 读取限 60 次/小时/IP，Release 下载不限流
