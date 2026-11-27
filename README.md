# 原版中文补全（1.7 专用）· RimWorld CoreZh GNH

RimWorld **1.7 官方简体中文的完整备份**，与官方语言包**逐字一致**。

| 项 | 值 |
|---|---|
| packageId | `gnh.cn.cys.corezh` |
| 适用版本 | **RimWorld 1.7**（1.6 正式版自带官方中文，不需要它） |
| 类型 | 纯语言包，**不含程序集** |
| 当前版本 | v2.0.3 |
| 仓库 | <https://github.com/1579486875/RimWorld-CoreZh-GNH> |

---

## 与官方的关系：逐字一致，0 差异

这不是重译，而是与 1.7 官方语言包**逐键比对后确认完全相同**的副本。

| 指标 | 数值 |
|---|---|
| 官方六个 DLC 中文包合计键数 | 34,094 |
| 本模组收录键数 | **34,075** |
| 收录部分与官方**完全相同** | **34,075（100%）** |
| 与官方**不同** | **0** |
| 仅本模组有 | 0 |
| 仅官方有（未收录） | 19 |

### 未收录的 19 个键是什么

全部是**桌面显示与显卡设置**项：`Gpu` / `Gpu_Automatic` / `Gpu_InUse` / `GpuChangedRestart` / `Monitor` / `Monitor_Automatic` / `DisplayMode` / `DisplayMode_Windowed` / `DisplayMode_ExclusiveFullscreen` / `RespectSystemScaling` / `RespectSystemScaling_Tooltip` / `TextureCompressionAlwaysOn_Tooltip` / `BakingModAssetPacks` / `BakingModAssetPacksFor` / `ModAssetPackBakeFailed` / `UploadBuildAssetPack` / `UploadBuildAssetPackTip` / `UploadSkipSourceTextures` / `UploadSkipSourceTexturesTip`。

实测这 19 个键在**原版中文里已有正确译文**（「显卡」「显示器」「显示模式」「遵循系统显示缩放」等），因此**不需要覆盖**。

> 换言之：启用本模组，看到的就是官方中文。没有改写、没有旧版遗留、不会把任何一处官方译文盖回旧写法。

---

## 为什么会有这个模组

1.7 测试版早期曾出现「语言目录里没有中文」的情况，当时做了这个备份。

**官方中文现在正常，所以当前环境不需要启用本模组。**
它的价值只有一个：万一某个版本又把官方中文删掉，启用它就能立刻补回来。

---

## 启用它会发生什么（实测）

### ✅ 键集覆盖：无副作用

| 机制 | 反编译结论（`Verse.LoadedLanguage`，1.7） | 影响 |
|---|---|---|
| **Keyed** | `keyedReplacements.SetOrAdd(key, ...)` —— 同键**覆盖** | 无 |
| **DefInjected** | 同键覆盖 | 无 |
| **Keyed 文件内重复键** | 会报 `Duplicate keyed translation key` | 本包 **0 处重复**（已逐文件校验） |
| **DefInjected 文件内重复键** | 同上 | 本包 **0 处重复**（已逐文件校验） |

### ⚠ 唯一副作用：Strings 名单翻倍

`LoadedLanguage.LoadFromFile_Strings` 对同名文件是 **`value.Add(item2)` 追加**，不是替换：

```csharp
if (stringFiles.TryGetValue(text2, out var value)) {
    foreach (string item2 in list) value.Add(item2);   // ← 追加
    return;
}
```

本包 97 个 `Strings` 文件（人名 / 地名 / 词根）与官方 **97 个全部同名**，内容**规范化换行后 100% 相同**（合计 10,581 行）。

→ 启用后这 10,581 行会被**再追加一份**，对应名单条目翻倍。

- **不影响正确性**：`NameBank` 是随机选取，同一名字出现两次时抽中概率不变（2/2N = 1/N）。
- **影响内存**：多占一份字符串。
- **为什么仍然保留**：本模组的定位是「官方中文消失时的备份」，那时官方 Strings 不存在，本包的 Strings 就是唯一来源。删掉它就失去了备份的意义。

---

## 收录内容

| 类别 | 文件数 | 内容 |
|---|---|---|
| `Keyed` | 91 | 界面、提示、按钮 |
| `DefInjected` | 1,470（151 个目录） | 物品、生物、基因、研究、事件、心情、戒律、仪式、书籍等 |
| `Strings` | 97 | 人名 / 地名 / 词根 |
| `LanguageInfo.xml` + 图标 | 2 | 官方元数据（含译者名单） |

覆盖 **Core + Royalty + Ideology + Biotech + Anomaly + Odyssey** 六个来源。

XML 完整性：**1,562 个文件全部解析通过（0 失败）**。

---

## 翻译来源与著作权

**这是官方译文，不是机翻。** 内容与 **1.7 官方语言包**
（`Data\<DLC>\Languages\ChineseSimplified (简体中文).tar`）**逐键一致**，
并保留官方的 `LanguageInfo.xml`（内含译者名单）与语言图标。

- 译文著作权归 **Ludeon Studios 及官方译者**所有；本仓库仅作「跨版本备份」用途，非商业、未作改写。
- 本仓库的打包与校验工作以 MIT License 发布（见 [LICENSE](LICENSE)）。
- 如官方中文可用，**请直接使用官方版本**，可以停用本模组。

---

## 安装

1. 把本仓库整个目录放进 RimWorld 的 `Mods\` 目录（或从 Releases 下载压缩包解压进去）
2. 在游戏内模组列表里**排到最后**（它是语言包，越晚加载越好）
3. 游戏设置 → 语言 → 选「简体中文 (ChineseSimplified)」

---

## 校验方法

本 README 里的所有数字都可以复验：

```powershell
# 1. XML 完整性（应 1562 通过 / 0 失败）
python -c "import glob,xml.etree.ElementTree as ET;fs=glob.glob(r'Languages/ChineseSimplified (简体中文)/**/*.xml',recursive=True);[ET.parse(f) for f in fs];print(len(fs),'ok')"

# 2. 与官方逐键比对（应 完全相同 34075 / 不同 0）
#    脚本见仓库 工具\ 目录
```

---

## 版本史

| 版本 | 变更 |
|---|---|
| **v2.0.3** | 与 1.7 官方包逐键对齐：修复 187 处旧版遗留差异（术语、def 语义变化、空格与引号），现与官方 **0 差异**；重写描述 |
| v2.0.2 | 补全书类 RulePack（书籍描述 / 书名生成器），全库 100% 中文 |
| v2.0.1 | 首次入库并修掉「丢 7,786 个键」的缺陷 |

---

作者　　　　大赢经直插白皮赢道
AI 协作　　 代码与校验脚本由 AI 助手辅助编写；设计与实机验证由作者完成
