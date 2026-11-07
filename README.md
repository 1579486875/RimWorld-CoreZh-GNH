# 原版中文补全（1.7 专用）· RimWorld CoreZh GNH

把 **RimWorld 1.7 测试版删掉的原版官方简体中文**补回来。

| 项 | 值 |
|---|---|
| packageId | `gnh.cn.cys.corezh` |
| 适用版本 | **RimWorld 1.7 测试版**（1.6 正式版自带官方中文，不需要它） |
| 类型 | 纯语言包，**不含程序集** |
| 当前版本 | v2.0.1 |

## 为什么需要它 —— ⚠ 立项前提已失效

**本模组当初的立项前提是「1.7 测试版把语言目录砍到只剩 English」。该前提在 1.7.4995 上已不成立，1.7.5000 上同样不成立。**
实测（2026-11-07，RimWorld 1.7.5000 rev1275）：`Data\{Core,Royalty,Ideology,Biotech,Anomaly,Odyssey}\Languages\` 下
**`ChineseSimplified (简体中文).tar` 六个全都在**，官方简体中文是可用的。

因此 —— **当前环境不需要启用本模组。** 它现在唯一的价值是「万一某个版本又把官方中文删掉，打开它就能立刻补回来」。
保留仓库、保持不启用，是本轮复审给出的处置。

### 启用它会带来什么（三条实测副作用）

1. **键集不增反退**：本包 34,071 键（Keyed 8,192 + DefInjected 25,879）与 1.7 官方
   **DefInjected 完全同集（0 缺 0 多）**、**Keyed 缺 19 个 1.7 新增键**
   （`Gpu` / `Monitor` / `DisplayMode` / `RespectSystemScaling` / `UploadBuildAssetPack` 等图形与模组上传界面）
   → 作为「补全包」在 1.7 上**真实补入 0 键**。
2. **116 个键会被盖回 1.6 旧版**（99 个在 Ideology；截至 1.7.5000 实测），其中 `CelebratedDate_Consumable.outcomeChances.1.description`
   在 1.6 是 `{0 枯燥乏味。…`（**缺右花括号**），1.7 已修成 `{0}` —— 启用会重新引入这一处格式串破损
   （运行时 `string.Format` 有抛 `FormatException` 的风险）。
3. **人名池会翻倍**：97 个 `Strings` 文件与 1.7 官方**零差异**（10,421 行全已在池中），
   而 `Verse.LoadedLanguage.LoadFromFile_Strings` 对同名 key 是 **`list.Add` 追加**而不是替换
   → 启用后这 10,421 行会被**再追加一份**。

> 上面三条都来自 2026-11-07 的逐字节比对（1.6 六个 tar ↔ 1.7 六个 tar ↔ 本包），可复验。

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

## 数字怎么重算

本 README 与 `About/About.xml` 里的键数、修订数、Strings 行数，都可以用仓库自带的脚本复算：

```bash
python tools/count_l10n_keys.py
```

默认读本机 `D:\RimWorld-1.6`（1.6 官方包）、`D:\steam\steamapps\common\RimWorld`（1.7 官方包）
与本仓库的 `Languages\ChineseSimplified (简体中文)\`；三个路径分别用
`--base16` / `--base17` / `--lang-dir` 覆盖。

输出与本文的数字一一对应：

| 脚本输出 | 对应本文哪句话 |
|---|---|
| `合计(键)` | 「34,071 键（Keyed 8,192 + DefInjected 25,879）」 |
| `合计(全量)` | 「全量 34,175 项」（= 键数 + Strings 97 个文件 + LanguageInfo 7 个字段） |
| `Strings 行数` | 「10,421 行」 |
| `修订总数` + `标量 / 列表` | 「修订过 116 个键（112 标量 + 4 列表）」 |
| `纯空白 / 实质` | 「96 条纯空白/排版、20 条实质」 |
| `按 DLC` | 「99 个在 Ideology」 |

> ⚠ **这些数字随官方语言包变动。** 1.7 的 `ChineseSimplified (简体中文).tar` 在 2026-11-06 就变过一次
> （Core 的 SHA256 `7139c2a2…` → `f59cb7f9…`，修订数从上一轮记录的 115 变成 116）。
> 官方再发新版时，重跑一次脚本、把结果同步到 README 与 `About/About.xml` 即可。

## 变更记录

### v2.0.1 — 2026-10-16（重要修复）

**修掉一个「丢了 7,786 个键」的缺陷。** 原先从 6 个官方 tar 提取时，
**多个 DLC 里同名的语言文件只保留了第一个**，导致 Ideology / Biotech / Anomaly / Odyssey / Royalty 的部分文本整批回退英文。

- **机制**（反编译取证）：`Verse.LoadedLanguage.TryRegisterFileIfNew` 对**同一个模组内、相对路径相同**的语言文件只加载第一个 ——
  `string item = filePath.Substring(dir.Item3.Length); if (tmpAlreadyLoadedFiles[dir.Item2].Contains(item)) return false;`
- **修法**：**重命名**而不是重写键 —— 首个 DLC 版保持原名，其余追加 `_<DLC>` 后缀
  （如 `Abilities.xml` / `Abilities_Ideology.xml` / `Abilities_Biotech.xml` / `Abilities_Anomaly.xml` / `Abilities_Odyssey.xml`）
- **结果**：新增 **417 个文件**（DefInjected 356 + Keyed 61），全部是官方 tar 成员的**逐字节副本**；
  文件数 1244 → **1660**（另有 `About.xml` 与 `LangIcon.png` 各 1 个，不计入语言文件）；按游戏口径模拟，加载到的键 26,292 → **35,006 = 6 个 tar 的键全集（缺 0、多 0）**
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
