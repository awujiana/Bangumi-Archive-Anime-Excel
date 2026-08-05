# Bangumi-Archive-Anime-Excel

> Bangumi 动画存档数据下发仓库 · 提供 JSONL 数据源与差异摘要供 BGM 插件同步使用

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-2da44e.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Data Update](https://img.shields.io/badge/更新频率-每周三-2da44e.svg)](https://github.com/bangumi/Archive)
[![Records](https://img.shields.io/badge/记录数-30610-2da44e.svg)](data/bangumi.jsonl)

---

## 📖 项目简介

本仓库是 [Bangumi Archive](https://github.com/bangumi/Archive) 数据处理链路的**数据下发仓库**，由上游 [Archive 项目](../Archive) 每周处理后同步而来。

**数据链路**：

```
Bangumi 官方 Archive (每周三 dump)
        ↓
Archive 项目 (处理 dump、生成 Excel 与差异)
        ↓ convert_dump_to_jsonl.py + sync_to_awujiana.py
本仓库 (Bangumi-Archive-Anime-Excel)
        ↓ raw URL
BGM 插件 (读取 JSONL → 写入 Excel → 同步 Bangumi API)
```

---

## 📂 目录结构

```
Bangumi-Archive-Anime-Excel/
├── data/
│   └── bangumi.jsonl                    # BGM 插件数据源（~16 MB，30610 条）
├── differences/                         # 差异摘要（每周对比）
│   ├── 2026-07-21_to_2026-07-28/
│   │   ├── diff_report.html             # 差异报告（浏览器可读）
│   │   ├── diff_summary.json            # 差异统计
│   │   ├── type2_subject_*_added.jsonlines      # 新增条目
│   │   ├── type2_subject_*_deleted.jsonlines    # 删除条目
│   │   └── 差异数据_type2_*.html         # 差异可视化
│   └── 2026-07-28_to_2026-08-04/
│       └── ...
├── config/
│   └── field_mappings.json              # 字段映射配置
├── .gitignore
├── LICENSE
└── README.md
```

> **注意**：`*.xlsx` 文件已通过 `.gitignore` 排除，仅在本地使用，不上传到 GitHub。

---

## 📊 数据文件说明

### 1. `data/bangumi.jsonl`（核心数据源）

BGM 插件通过 raw URL 读取的 JSONL 格式动画数据。

- **大小**：约 16 MB
- **记录数**：30610 条
- **编码**：UTF-8 无 BOM，LF 换行
- **更新频率**：每周三（跟随 Bangumi 官方 dump 节奏）
- **访问地址**：
  ```
  https://raw.githubusercontent.com/awujiana/Bangumi-Archive-Anime-Excel/main/data/bangumi.jsonl
  ```

#### 单条记录示例

```json
{
  "sid": "8",
  "name": "Code Geass 反叛的鲁路修R2",
  "updatedAt": "2026-08-04",
  "date": "2008-04-06",
  "meta_tags": ["机战", "TV", "日本", "原创", "战斗"],
  "nsfw": false,
  "播放结束": "2008年9月28日",
  "动画制作公司": "サンライズ",
  "话数": "25",
  "导演": "谷口悟朗",
  "音乐": "中川幸太郎、黒石ひとみ",
  "人物设定": "木村貴宏",
  "原作": "大河内一楼、谷口悟朗",
  "系列构成": "大河内一楼",
  "关联的动漫ID": "85 | 344 | 793 | 1081 | 3219 | 8813"
}
```

#### 字段说明（25 个字段）

| 类别 | 字段 | 类型 | 说明 |
|------|------|------|------|
| **基础** | `sid` | string | Bangumi 条目 ID |
| **基础** | `name` | string | 名称（优先中文名，回退日文名） |
| **基础** | `updatedAt` | string | 数据更新日期（YYYY-MM-DD） |
| **顶层** | `date` | string | 开播日期 |
| **顶层** | `meta_tags` | string[] | 标签/分级 |
| **顶层** | `nsfw` | bool | 是否 NSFW |
| **infobox** | `播放结束` | string | 完播日期 |
| **infobox** | `动画制作公司` | string | 制作公司 |
| **infobox** | `话数` | string | 集数 |
| **infobox** | `片长` | string | 单集时长（分钟） |
| **infobox** | `制片国家` | string | 制片国家/地区 |
| **infobox** | `语言` | string | 作品语言 |
| **infobox** | `类型` | string | 作品类型 |
| **infobox** | `导演` | string | 导演 |
| **infobox** | `音乐` | string | 音乐制作 |
| **infobox** | `人物设定` | string | 人物设定 |
| **infobox** | `机械设定` | string | 机械设定 |
| **infobox** | `原作` | string | 原作 |
| **infobox** | `脚本` | string | 脚本 |
| **infobox** | `分镜` | string | 分镜 |
| **infobox** | `演出` | string | 演出 |
| **infobox** | `原案` | string | 原案 |
| **infobox** | `系列构成` | string | 系列构成 |
| **infobox** | `在线播放平台` | string | 在线播放平台 |
| **关联** | `关联的动漫ID` | string | 关联条目 ID（` \| ` 分隔） |

### 2. `differences/`（差异摘要）

每周 dump 对比生成的差异摘要，保留新增/删除的小文件和可视化报告。

| 文件 | 说明 |
|------|------|
| `diff_report.html` | 差异对比报告（浏览器可读） |
| `diff_summary.json` | 差异统计数据 |
| `type2_subject_*_added.jsonlines` | 新增条目列表 |
| `type2_subject_*_deleted.jsonlines` | 删除条目列表 |
| `差异数据_type2_*.html` | 差异可视化页面 |

> **注意**：`modified.jsonlines` / `modified.json`（约 70-90 MB/周期）体积过大，不上传到 GitHub，仅保留本地。

---

## 🔄 数据更新流程

1. **Bangumi 官方**每周三凌晨发布 wiki 数据 dump
2. **Archive 项目**下载 dump 并处理：
   - 解析 infobox、生成 Excel 全量存档与差异报告
   - 执行 `convert_dump_to_jsonl.py` 生成 `bangumi.jsonl`
   - 执行 `sync_to_awujiana.py` 同步差异摘要到本仓库
3. **本仓库**通过 `git push` 更新到 GitHub
4. **BGM 插件**通过 raw URL 拉取最新 `bangumi.jsonl`

---

## 🔗 相关项目

| 项目 | 仓库 | 说明 |
|------|------|------|
| Archive 项目 | 本地 `../Archive` | 数据处理流水线（上游） |
| Bangumi 官方 Archive | [bangumi/Archive](https://github.com/bangumi/Archive) | 原始数据源 |
| BGM 插件 | — | Excel 加载项，读取 JSONL 并同步 Bangumi API |

---

## 📜 许可协议

本数据集遵循 [知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)。

- ✅ **允许**：个人使用、学习、研究、非商业分享、数据分析
- ❌ **禁止**：商业用途、未署名使用、移除许可声明

数据来源：[Bangumi Archive](https://github.com/bangumi/Archive)

---

## 📧 联系方式

如有疑问或反馈，请联系：**bingshanlengtie@qq.com**
