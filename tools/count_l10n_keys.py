# -*- coding: utf-8 -*-
"""重算本模组的「键数」与「1.7 相对 1.6 的修订数」—— README / About 里那些数字的唯一出处。

用法：
    python tools/count_l10n_keys.py
    python tools/count_l10n_keys.py --base16 D:/RimWorld-1.6 \
        --base17 "D:/steam/steamapps/common/RimWorld" \
        --lang-dir "Languages/ChineseSimplified (简体中文)"

默认参数指向本机安装；换机器时三个路径都能覆盖。

口径（与 README / About 逐句对应）：
  · 键数 = Keyed 的唯一 key 数 + DefInjected 的唯一 path 数（Strings 是文件数、LanguageInfo 是字段，单列）
  · 修订 = 同一 key 在 1.6 与 1.7 官方包里文本不同
  · 「标量 / 列表」按**单个文件内**该 key 的条目数判定（>1 即整列表注入，见审查模板 B.13），
    不是按「跨 DLC 合并后的值个数」—— 后者会把「同一个 key 在多个 DLC 的同名文件里各出现一次」误判成列表
  · 「纯空白 / 实质」按去掉所有空白后是否仍不同来分

只读：不写任何文件。
"""
import argparse
import collections
import os
import re
import sys
import tarfile
import xml.etree.ElementTree as ET

BS = chr(92)                       # 反斜杠（不写字面量，避免被 shell 吃掉一层）
PACKS = ['Core', 'Royalty', 'Ideology', 'Biotech', 'Anomaly', 'Odyssey']
TARNAME = 'ChineseSimplified (简体中文).tar'


def load_tars(base):
    """读 6 个 DLC 的中文 tar，返回 [(包名, 相对路径, 字节)]。"""
    out = []
    for pk in PACKS:
        path = '%s/Data/%s/Languages/%s' % (base.replace(BS, '/'), pk, TARNAME)
        if not os.path.exists(path):
            sys.exit('找不到官方语言包：%s' % path)
        with tarfile.open(path) as tf:
            for m in tf.getmembers():
                if m.isfile():
                    out.append((pk, m.name.replace(BS, '/'), tf.extractfile(m).read()))
    return out


def load_dir(root):
    """读本仓库的语言目录，返回 {相对路径: 字节}。"""
    d = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            fp = os.path.join(dp, f)
            d[os.path.relpath(fp, root).replace(BS, '/')] = open(fp, 'rb').read()
    return d


def parse_pairs(rel, data):
    """把一个语言文件摊平成 [(key, text)]；.txt 按行、.png 跳过。"""
    if rel.lower().endswith('.png'):
        return []
    if rel.lower().endswith('.txt'):
        t = data.decode('utf-8-sig', errors='ignore')
        return [(rel, ln.strip()) for ln in t.splitlines() if ln.strip()]
    try:
        root = ET.fromstring(data)
    except Exception:
        return None
    out = []

    def walk(el, prefix):
        for c in el:
            tag = prefix + c.tag
            if len(c):
                walk(c, tag + '.')
            else:
                out.append((tag, (c.text or '').strip()))

    walk(root, '')
    return out


def top_of(rel):
    if rel.lower().endswith('.txt'):
        return 'Strings'
    return rel.split('/')[0] if '/' in rel else 'ROOT'


def index(items):
    """返回 ({类别: {key: [texts]}}, {key: 单文件内最大条目数}, 解析失败数)"""
    buckets = collections.defaultdict(lambda: collections.defaultdict(list))
    max_per_file = collections.defaultdict(int)
    bad = 0
    for _tag, rel, data in items:
        pr = parse_pairs(rel, data)
        if pr is None:
            bad += 1
            continue
        cat = top_of(rel)
        per_file = collections.defaultdict(int)
        for key, text in pr:
            buckets[cat][key].append(text)
            per_file[key] += 1
        for key, n in per_file.items():
            max_per_file[key] = max(max_per_file[key], n)
    for cat in buckets:
        for key in buckets[cat]:
            buckets[cat][key].sort()
    return buckets, max_per_file, bad


def flat(v):
    return chr(1).join(v)


def norm(s):
    return re.sub(r'\s+', '', s)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    ap = argparse.ArgumentParser(description='重算 CoreZh 的键数与修订数')
    ap.add_argument('--base16', default='D:/RimWorld-1.6', help='1.6 安装根目录')
    ap.add_argument('--base17', default='D:/steam/steamapps/common/RimWorld', help='1.7 安装根目录')
    ap.add_argument('--lang-dir', default=os.path.join(repo, 'Languages', 'ChineseSimplified (简体中文)'),
                    help='本模组的语言目录')
    a = ap.parse_args()

    print('1.6 安装 : %s' % a.base16)
    print('1.7 安装 : %s' % a.base17)
    print('本模组   : %s' % a.lang_dir)
    print()

    m16 = load_tars(a.base16)
    m17 = load_tars(a.base17)
    a2 = load_dir(a.lang_dir)
    i16, mx16, bad16 = index(m16)
    i17, mx17, bad17 = index(m17)
    ia2, _mxA2, badA2 = index([('A2', r, d) for r, d in a2.items()])
    print('成员数: 1.6=%d  1.7=%d  本模组文件=%d   XML 解析失败: %d/%d/%d'
          % (len(m16), len(m17), len(a2), bad16, bad17, badA2))

    print()
    print('=== ① 键数 ===')
    print('%-14s %8s %8s %8s' % ('类别', '1.6', '1.7', '本模组'))
    tot = {'1.6': 0, '1.7': 0, 'A2': 0}
    for cat in ('Keyed', 'DefInjected', 'Strings', 'ROOT'):
        n16, n17, nA2 = len(i16.get(cat, {})), len(i17.get(cat, {})), len(ia2.get(cat, {}))
        print('%-14s %8d %8d %8d' % (cat, n16, n17, nA2))
        if cat in ('Keyed', 'DefInjected'):
            tot['1.6'] += n16
            tot['1.7'] += n17
            tot['A2'] += nA2
    print('%-14s %8d %8d %8d   <- 「键数」口径（Keyed + DefInjected）' % ('合计(键)', tot['1.6'], tot['1.7'], tot['A2']))
    all16 = sum(len(i16.get(c, {})) for c in i16)
    all17 = sum(len(i17.get(c, {})) for c in i17)
    allA2 = sum(len(ia2.get(c, {})) for c in ia2)
    print('%-14s %8d %8d %8d   <- 含 Strings / ROOT 的全量' % ('合计(全量)', all16, all17, allA2))
    rows = {'1.6': 0, '1.7': 0, 'A2': 0}
    for _t, r, d in m16:
        if r.endswith('.txt'):
            rows['1.6'] += len([l for l in d.decode('utf-8-sig', errors='ignore').splitlines() if l.strip()])
    for _t, r, d in m17:
        if r.endswith('.txt'):
            rows['1.7'] += len([l for l in d.decode('utf-8-sig', errors='ignore').splitlines() if l.strip()])
    for r, d in a2.items():
        if r.endswith('.txt'):
            rows['A2'] += len([l for l in d.decode('utf-8-sig', errors='ignore').splitlines() if l.strip()])
    print('%-14s %8d %8d %8d   <- Strings 非空行数（README 里的「10,421 行」）'
          % ('Strings 行数', rows['1.6'], rows['1.7'], rows['A2']))

    print()
    print('=== ② 1.6 → 1.7 修订（同 key 文本不同）===')
    by_pack = collections.Counter()
    total = scalar = listed = blank = real = 0
    for cat in ('Keyed', 'DefInjected'):
        s16, s17 = set(i16.get(cat, {})), set(i17.get(cat, {}))
        common = s16 & s17
        diff = sorted(k for k in common if i16[cat][k] != i17[cat][k])
        for k in diff:
            total += 1
            if mx16.get(k, 1) > 1 or mx17.get(k, 1) > 1:
                listed += 1
            else:
                scalar += 1
            if norm(flat(i16[cat][k])) == norm(flat(i17[cat][k])):
                blank += 1
            else:
                real += 1
        print('  %-12s 1.6 有 %d / 1.7 有 %d / 共有 %d；新增 %d、删除 %d、文本不同 %d'
              % (cat, len(s16), len(s17), len(common), len(s17 - s16), len(s16 - s17), len(diff)))
    # 按 DLC 分布
    for pk, rel, data in m16:
        if (pk, rel) not in {(p2, r2) for p2, r2, _ in m17}:
            continue
        d17 = dict(((p2, r2), dd) for p2, r2, dd in m17)
        if d17[(pk, rel)] == data:
            continue
        pa, pb = parse_pairs(rel, data), parse_pairs(rel, d17[(pk, rel)])
        if pa is None or pb is None:
            continue
        da, db = collections.defaultdict(list), collections.defaultdict(list)
        for k, v in pa:
            da[k].append(v)
        for k, v in pb:
            db[k].append(v)
        n = sum(1 for k in da if k in db and sorted(da[k]) != sorted(db[k]))
        if n:
            by_pack[pk] += n

    print()
    print('  ★ 修订总数 = %d' % total)
    print('     标量 / 列表 : %d / %d' % (scalar, listed))
    print('     纯空白 / 实质: %d / %d' % (blank, real))
    print('     按 DLC      : ' + '  '.join('%s=%d' % (pk, by_pack[pk]) for pk in PACKS))
    check = sum(by_pack.values())
    print('     （按 DLC 累加 = %d，与总数%s）' % (check, '一致' if check == total else '不一致 —— 请查脚本'))

    print()
    print('=== ③ 本模组 vs 1.6 / 1.7 双向比对 ===')
    for cat in ('Keyed', 'DefInjected', 'Strings', 'ROOT'):
        A = set(ia2.get(cat, {}))
        for tag, idx in (('1.6', i16), ('1.7', i17)):
            B = set(idx.get(cat, {}))
            if not A and not B:
                continue
            miss, extra = B - A, A - B
            vd = sum(1 for k in (A & B) if ia2[cat][k] != idx[cat][k])
            print('  %-12s vs %s: 本模组 %d / 基准 %d ; 缺 %d 多 %d 同键文本不同 %d'
                  % (cat, tag, len(A), len(B), len(miss), len(extra), vd))

    print()
    print('提示：这些数字随官方语言包变动。官方更新后重跑本脚本，'
          '把结果同步到 README 与 About/About.xml 即可。')


if __name__ == '__main__':
    main()
