# Bangumi-Archive-Anime-Excel

> Bangumi 动画存档数据下发仓库 · 提供 JSONL 数据源与差异摘要供 BGM 插件同步使用

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-2da44e.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Data Update](https://img.shields.io/badge/更新频率-每周三-2da44e.svg)](https://github.com/bangumi/Archive)
[![Last Update](https://img.shields.io/badge/更新日期-2026-09-08-2da44e.svg)](data/bangumi.jsonlines)
[![Records](https://img.shields.io/badge/记录数-30836-2da44e.svg)](data/bangumi.jsonlines)

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
本项目的Releases页面仅包含以下三类 Excel 文件:

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `ani-bangumi-type2-YYYY-MM-DD.xlsx` | 主数据文件 | 完整原始导出字段(73 列),按日期归档的全量动画条目数据 |
| `type2_subject_YYMMDD_vs_YYMMDD.xlsx` | 差异对比文件 | 相邻期次之间的差异记录(新增、删除、修改),命名格式为"新日期_vs_旧日期" |
| `ani-bangumi-type2-YYYY-MM-DD-template.xlsx` | 模板转换文件 | 在主数据文件基础上精简的 41 列模板,面向用户填写收藏信息 |

### 数据预览图
ani-bangumi-type2-YYYY-MM-DD.xlsx
[![Archive提取为Excel预览图](https://free.picui.cn/free/2026/06/30/6a437e24cbe7f.png)]

ani-bangumi-type2-YYYY-MM-DD-template.xlsx
[![Archive模板转换为Excel预览图](https://free.picui.cn/free/2026/06/30/6a437e5e7ba36.png)]


---

## 📂 目录结构

```
Bangumi-Archive-Anime-Excel/
├── data/
│   └── bangumi.jsonlines                # BGM 插件数据源（~8 MB，30836 条）
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
├── LICENSE
└── README.md
```

> 本仓库**只存放数据**（JSONL 数据源与差异摘要），不存放任何处理脚本；
> 流水线与运维脚本统一位于业务仓库 [`Archive/scripts/`](../Archive/scripts)。

> **注意**：`*.xlsx` 文件仅在本地使用，不上传到 GitHub。

---

## 📊 数据文件说明

### 1. `data/bangumi.jsonlines`（核心数据源）

BGM 插件通过 raw URL 读取的动画数据，采用「**表头 + 值数组**」两段式 JSON Lines 格式。

- **大小**：约 8 MB（8,017,440 字节）
- **记录数**：30836 条
- **编码**：UTF-8 无 BOM，LF 换行
- **更新频率**：每周三（跟随 Bangumi 官方 dump 节奏）
- **最近更新**：2026-09-08
- **访问地址**：
  ```
  https://raw.githubusercontent.com/awujiana/Bangumi-Archive-Anime-Excel/main/data/bangumi.jsonlines
  ```

> **为什么扩展名是 `.jsonlines` 而不是 `.jsonl`？**
> GitHub raw CDN 是否对文件做 gzip 压缩**只取决于扩展名**，与文件大小无关（已实测）。
> `.jsonl` 会被当作 `application/octet-stream` 原样传输，16 MB 全量下载；
> 而 `.jsonlines` / `.json` / `.md` / `.txt` 会被识别为文本并透明压缩。
> 实测本文件经 CDN 压缩后只需传输 **约 2.6 MB（−84%）**，浏览器自动解压，客户端零额外代码。

#### 数据格式：表头 + 值数组

第 1 行是**表头**（字段名数组），其后每行是与表头**等长**的**值数组**：

```jsonl
["sid","name","updatedAt","date","meta_tags","nsfw","播放结束","动画制作公司","话数","片长","制片国家","语言","类型","导演","音乐","人物设定","机械设定","原作","脚本","分镜","演出","原案","系列构成","在线播放平台","关联的动漫ID"]
["8","Code Geass 反叛的鲁路修R2","2026-09-08","2008-04-06",["机战","TV","日本","原创","战斗"],false,"2008年9月28日","サンライズ、david production、スタジオガッツ；作画协力：GONZO","25","","","","","谷口悟朗","中川幸太郎、黒石ひとみ","木村貴宏","寺岡賢司、沙倉拓実；Knightmare设计：安田朗、中田栄治、阿久津潤一","","","","","故事原案：大河内一楼、谷口悟朗","大河内一楼","","85 | 344 | 793 | 1081 | 3219 | 8813 | 8816 | 8817 | 8819 | 8820 | 17967 | 32214 | 33389 | 35866 | 51042 | 73715 | 78546 | 91493 | 99952 | 102098 | 110909 | 118733 | 118734 | 118735 | 118736 | 118737 | 118738 | 120756 | 120758 | 141050 | 145943 | 188684 | 188685 | 199228 | 199229 | 199230 | 199231 | 231875 | 231982 | 231989 | 237827 | 239861 | 306532 | 309324 | 321523 | 336526 | 377946 | 391213 | 391214 | 391873 | 400807 | 405346 | 452308 | 667009 | 667019"]
```

- 仍然是合法的 JSON Lines：**每行一个合法的 JSON 值**（这里是数组）。
- 值数组的顺序与长度**严格对应表头**；缺失字段补默认值（字符串补 `""`、`meta_tags` 补 `[]`、`nsfw` 补 `false`）。
- 字段名只在表头出现一次，不再随 3 万条记录重复，因此文件体积比「每行一个完整对象」**减半**，且完全无损。
- 消费端解析约定：**首个非空行必须是纯字符串数组（表头）**，其后每行必须是等长数组。

#### 字段说明

本数据集包含以下字段，全面记录每部动画的详细信息：

##### 基础信息字段

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| **id** | 条目ID | 数字 | 初始版本 |
| **type** | 作品类型 | 数字 | 初始版本（固定为2，表示动画） |
| **name** | 条目名 | 字符串 | 初始版本 |
| **name_cn** | 条目简体中文名 | 字符串 | 初始版本 |
| **platform** | 条目平台 | 字符串 | 初始版本 |
| **summary** | 条目简介 | 长文本 | 初始版本 |
| **nsfw** | 是否为NSFW | 布尔值 | 初始版本 |
| **date** | 发行日期 | 日期（YYYY-MM-DD） | 初始版本 |
| **favorite** | 收藏状态 | 字符串 | 初始版本 |
| **series** | 是否为系列作品 | 布尔值 | 初始版本 |

##### 原始信息字段

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| **infobox** | 条目原始wiki字符串 | 长文本/HTML | 初始版本（2024-08-30起正确处理HTML转义） |

##### 评分与排名字段

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| **tags** | 标签（部分） | 字符串/数组 | 2023-07-27 |
| **score** | 评分 | 数字（0-10） | 2023-07-27 |
| **score_details** | 评分细节 | 字符串/JSON | 2023-07-27 |
| **rank** | 类别内排名 | 数字 | 2023-07-27 |

##### 元数据字段

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| **meta_tags** | 公共标签 | 字符串/数组 | 2025-04-18 |

##### infobox解析字段 <span style="color:#2da44e"> 新增 2026-06-19</span>

以下字段从infobox原始wiki字符串中解析提取为独立列：

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| <span style="color:#2da44e">**制片国家**</span> | 制片国家/地区 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**语言**</span> | 作品语言 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**类型**</span> | 作品类型标签 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**导演**</span> | 导演 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**音乐**</span> | 音乐制作 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**人物设定**</span> | 人物设定 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**机械设定**</span> | 机械设定 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**原作**</span> | 原作 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**脚本**</span> | 脚本 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**分镜**</span> | 分镜 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**演出**</span> | 演出 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**原案**</span> | 原案 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**系列构成**</span> | 系列构成 | 字符串 | 2026-06-19 |
| <span style="color:#2da44e">**在线播放平台**</span> | 在线播放平台 | 字符串 | 2026-06-19 |

##### 关联数据字段 <span style="color:#2da44e"> 新增 2026-06-19</span>

| 字段名 | 含义 | 数据类型 | 来源版本 |
|--------|------|----------|----------|
| <span style="color:#2da44e">**关联的动漫ID**</span> | 关联的动画条目ID | 字符串（多个ID以` \| `分隔） | 2026-06-19 |

#### <span style="color:#2da44e"> 新增 2026-07-05</span> infobox字段解析说明

infobox字段包含条目原始wiki字符串，其中可能包含以下信息（通过解析可提取）：

- 话数
- 片长
- 制片国家/地区
- 语言
- 官方网站
- 放送开始时间
- 播放结束时间
- 动画制作公司
- 导演
- 音乐
- 链接
- 其他
- Copyright
- 人物设定
- 机械设定
- 原作
- 企画
- 制片人
- 动画制片人
- 脚本
- 分镜
- 演出
- 作画监督
- 美术监督
- 色彩设计
- 摄影监督
- 音响监督
- 主题歌作曲
- 主题歌作词
- 主题歌演出
- 主题歌编曲
- 原画
- 第二原画
- 补间动画
- 动画检查
- 3DCG
- CG导演
- 配音
- 监制
- 摄影
- 制片
- 音乐制作
- 道具设计
- 原案
- 系列构成
- 编剧
- 美术设计
- 背景美术
- 音响
- 音效
- 效果
- 录音
- 剪辑

注意：这些详细信息包含在infobox字段中，本数据集的Excel格式已将其解析为独立字段（详见上方"infobox解析字段"章节）。

### 2. `differences/`（差异摘要）

每周 dump 对比生成的差异摘要，保留新增/删除的小文件和可视化报告。

| 文件 | 说明 |
|------|------|
| `diff_report.html` | 差异对比报告（浏览器可读） |
| `diff_summary.json` | 差异统计数据 |
| `type2_subject_*_added.jsonlines` | 新增条目列表 |
| `type2_subject_*_deleted.jsonlines` | 删除条目列表 |
| `差异数据_type2_*.html` | 差异可视化页面 |

---

## 🔄 数据更新流程

1. **Bangumi 官方**每周三凌晨发布 wiki 数据 dump
2. **Archive 项目**下载 dump 并处理：
   - 解析 infobox、生成 Excel 全量存档与差异报告
   - 执行 `convert_dump_to_jsonl.py` 生成 `bangumi.jsonlines`（表头 + 值数组）
   - 执行 `sync_to_awujiana.py` 同步差异摘要到本仓库
3. **本仓库**由 Archive 项目的 `push_anime_data_repository.py` 自动提交：
   - 先执行 `Archive/scripts/update_badges.py`，把本 README 的徽章与统计信息对齐到最新的 `bangumi.jsonlines`
   - 再 `git add` + `git commit` + `git push` 更新到 GitHub
4. **BGM 插件**通过 raw URL 拉取最新 `bangumi.jsonlines`

> 本 README 中所有数字（记录数、大小、更新日期）均由业务仓库的 `Archive/scripts/update_badges.py` 从 `data/bangumi.jsonlines` 自动生成，无需手工维护。
> 手动校验是否已对齐：`python scripts/update_badges.py --check`（在 Archive 仓库根目录执行，过期时退出码为 1）。

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
