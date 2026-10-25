# 原版中文补全（1.7 专用）· RimWorld CoreZh GNH

把 **RimWorld 1.7 测试版删掉的原版官方简体中文**补回来。

| 项 | 值 |
|---|---|
| packageId | `gnh.cn.cys.corezh` |
| 适用版本 | **RimWorld 1.7 测试版**（1.6 正式版自带官方中文，不需要它） |
| 类型 | 纯语言包，**不含程序集** |
| 当前版本 | v2.0.1 |

## 为什么需要它

RimWorld **1.7 测试版（Waylith 引擎）把 `Data\Core\Languages` 与全部 5 个 DLC 的语言目录砍到只剩 English** ——
官方简体中文连同其余 27 种语言一起被移除。后果是：原版界面、物品、生物、研究、事件的名称与描述**全部回退成英文**；
而模组自带的中文不受影响，所以看起来是「一半中文一半英文」。

本模组把这些官方中文原样补回来。

## 收录内容（共 1,660 个语言文件）

| 类别 | 内容 |
|---|---|
| `Keyed` | 界面与提示（91 个文件） |
| `DefInjected` | 物品 / 生物 / 基因 / 研究 / 事件 / 心情 / 戒律等（1470 个文件、151 个目录） |
| `Strings` | 人名 / 地名 / 词根（97 个文件） |

覆盖 **Core + Royalty + Ideology + Biotech + Anomaly + Odyssey** 六个来源。

## 翻译来源与著作权

**这是官方译文，不是机翻。** 内容直接取自 **1.6 正式版**的官方语言包
（`Data\<DLC>\Languages\ChineseSimplified (简体中文).tar`），**逐字节原样收录**，
并保留官方的 `LanguageInfo.xml`（内含译者名单）与语言图标。

- 译文著作权归 **Ludeon Studios 及官方译者**所有；本仓库仅作「跨版本补齐」用途，非商业、不作修改。
- 本仓库的打包与修复工作以 MIT License 发布（见 [LICENSE](LICENSE)）。
- 如官方在 1.7 正式版恢复中文，或你已能拿到官方 1.7 语言包，**请优先使用官方版本**，可以删掉本模组。

## 已知限制

- **1.6 → 1.7 之间新增的文本不在其中**，那部分仍显示英文（例如主菜单那句 "All translations of RimWorld are Fan-made…"）。
  要补全需从 1.7 的官方语言包提取。
- 本模组在 **1.6 正式版**下**不需要也不建议启用**（官方中文本来就在）。

## 安装

1. 把本仓库整个目录放进 RimWorld 的 `Mods\` 目录（或从 Releases 下载压缩包解压进去）
2. 在游戏内模组列表里**排到最后**（它是语言包，越晚加载越好）
3. 游戏设置 → 语言 → 选「简体中文 (ChineseSimplified)」

## 变更记录

### v2.0.1 — 2026-10-16（重要修复）

**修掉一个「丢了 7,786 个键」的缺陷。** 原先从 6 个官方 tar 提取时，
**多个 DLC 里同名的语言文件只保留了第一个**，导致 Ideology / Biotech / Anomaly / Odyssey / Royalty 的部分文本整批回退英文。

- **机制**（反编译取证）：`Verse.LoadedLanguage.TryRegisterFileIfNew` 对**同一个模组内、相对路径相同**的语言文件只加载第一个 ——
  `string item = filePath.Substring(dir.Item3.Length); if (tmpAlreadyLoadedFiles[dir.Item2].Contains(item)) return false;`
- **修法**：**重命名**而不是重写键 —— 首个 DLC 版保持原名，其余追加 `_<DLC>` 后缀
  （如 `Abilities.xml` / `Abilities_Ideology.xml` / `Abilities_Biotech.xml` / `Abilities_Anomaly.xml` / `Abilities_Odyssey.xml`）
- **结果**：新增 **417 个文件**（DefInjected 356 + Keyed 61），全部是官方 tar 成员的**逐字节副本**；
  文件数 1244 → **1661**；按游戏口径模拟，加载到的键 26,292 → **35,006 = 6 个 tar 的键全集（缺 0、多 0）**
- **只增不改**：原有 1244 个文件除 `About.xml` 的版本号外零改动、零丢失

### v2.0.0 — 2026-10-13

- 首次发布：从 1.6 正式版的 6 个官方语言包提取，收录 1244 个文件

## 复现方式

本仓库内容可由官方 1.6 正式版的 tar 完全复现（不改一个字节）：

```python
import tarfile, os
# Data\Core\Languages\ChineseSimplified (简体中文).tar 等 6 个文件
tf = tarfile.open(tar_path)
tf.extractall(dest)          # 取出后按上面「变更记录」的规则重命名同名文件即可
```
