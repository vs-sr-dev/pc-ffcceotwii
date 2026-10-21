"""Name a stripped DOL's functions from kin: other stripped DOLs, already
named, built with the same or nearly the same SDK libraries.

Echoes of Time's SDK (2008) is no other port's, but six ports have named
DOLs whose libraries are close: Castlevania Judgment and Arc Rise Fantasia
(2007-08), Crystal Bearers and Monster Hunter Tri (2009), Conduit 2 (2010),
Dragon Quest Swords (2007). Three passes, each kin in turn, the first kin
given first:

  by hash   a function here whose words hash as one there, with immediates
            and branch targets masked (Dolphin's checksum, tools/sigmatch.py),
            and of the same size, is the same function
  by place  a kin's name between two such matches that moved by the same
            distance, where a function of the same size and hash is
  by order  between two such matches that follow each other in both DOLs,
            with as many functions between them on each side, the functions
            paired in order where their instructions are alike (opcodes
            only, --min-ratio of them): a library built again with small
            changes, as this game's 2008 WPAD against 2007's and 2009's

Spans are the recompiler's own units on both sides. Only one-to-one matches
are kept: a hash that lands on two functions in either DOL says nothing.

    python tools/kinmatch.py build/extract/sys/main.dol \
        --kin <port>/build/extract/sys/main.dol <port>/build/names.tsv \
        [--kin ...] --out build/kin_guess.tsv
"""
import argparse
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # wiikit/

from wiikit.dol import Image
from wiikit.recomp.discover import symbolise
from tools.sigmatch import checksum


def spans(img):
    units, _ = symbolise(img, log=lambda m: None)
    starts = sorted(s for s, _ in units)
    out = []
    for seg in img.text_segments():
        inside = [s for s in starts if seg.vaddr <= s < seg.vaddr + len(seg.data)]
        for a, b in zip(inside, inside[1:] + [seg.vaddr + len(seg.data)]):
            words = struct.unpack_from(f">{(b - a) // 4}I", seg.data, a - seg.vaddr)
            out.append((a, b - a, checksum(words)))
            SHAPES[(id(img), a)] = shape(words)
    return out


SHAPES = {}


def shape(words):
    """The function's instructions with registers and immediates gone: the
    primary opcode and, where there is one, the extended opcode."""
    out = []
    for w in words:
        op = w >> 26
        out.append((op << 10) | ((w >> 1) & 0x3FF) if op in (4, 19, 31, 59, 63) else op << 10)
    return out


def similar(x, y):
    import difflib
    if not (0.8 <= len(x) / max(1, len(y)) <= 1.25):
        return 0.0
    return difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dol")
    ap.add_argument("--kin", nargs=2, action="append", required=True, metavar=("DOL", "NAMES"))
    ap.add_argument("--min-size", type=int, default=0x10)
    ap.add_argument("--min-ratio", type=float, default=0.8)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    global KIMG, MIMG
    MIMG = Image(a.dol)
    mine = spans(MIMG)
    here = collections.Counter((s, c) for _, s, c in mine)
    found = {}
    for kdol, knames in a.kin:
        names = {}
        with open(knames, encoding="utf-8") as f:
            next(f)
            for line in f:
                p = line.rstrip("\n").split("\t")
                names[int(p[0], 16)] = p[1]
        KIMG = Image(kdol)
        kin = spans(KIMG)
        there = collections.Counter((s, c) for _, s, c in kin)
        by_key = {(s, c): names[ad] for ad, s, c in kin if ad in names and there[(s, c)] == 1}
        tag = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(knames))))
        delta = {}                               # kin address -> this DOL's, for unique matches
        kin_at = {ad: (s, c) for ad, s, c in kin}
        mine_at = {ad: (s, c) for ad, s, c in mine}
        for ad, s, c in mine:
            if s >= a.min_size and here[(s, c)] == 1 and (s, c) in by_key:
                found.setdefault(ad, (by_key[(s, c)], tag))
        unique_kin = {(s, c): ad for ad, s, c in kin if there[(s, c)] == 1}
        for ad, s, c in mine:
            if s >= a.min_size and here[(s, c)] == 1 and (s, c) in unique_kin:
                delta[unique_kin[(s, c)]] = ad - unique_kin[(s, c)]
        # The rest by place: a kin's name between two unique matches that moved
        # by the same amount, where this DOL has a function of the same size
        # and hash at the same distance (the WPAD.o thunks, the setters).
        anchors = sorted(delta)
        import bisect
        for kad, n in names.items():
            if kad not in kin_at or kad in delta:
                continue
            i = bisect.bisect_left(anchors, kad)
            if i == 0 or i == len(anchors):
                continue
            lo, hi = anchors[i - 1], anchors[i]
            if delta[lo] != delta[hi]:
                continue
            ad = kad + delta[lo]
            if mine_at.get(ad) == kin_at[kad]:
                found.setdefault(ad, (n, tag + " (by place)"))
        # The rest by order: between two unique matches that follow each other
        # in both DOLs, the same number of functions on each side, paired in
        # order where their instructions are alike (a library built again
        # with small changes: the 2008 WPAD and KPAD against 2007's or 2009's).
        kin_list = [ad for ad, _, _ in kin]
        mine_list = [ad for ad, _, _ in mine]
        kin_ix = {ad: i for i, ad in enumerate(kin_list)}
        mine_ix = {ad: i for i, ad in enumerate(mine_list)}
        pairs = sorted((kin_ix[k], mine_ix[k + d]) for k, d in delta.items())
        kimg, mimg = KIMG, MIMG
        for (k0, m0), (k1, m1) in zip(pairs, pairs[1:]):
            if m1 <= m0 or k1 - k0 != m1 - m0 or k1 - k0 < 2 or k1 - k0 > 40:
                continue
            for j in range(1, k1 - k0):
                kad, ad = kin_list[k0 + j], mine_list[m0 + j]
                if kad not in names or ad in found:
                    continue
                r = similar(SHAPES[(id(kimg), kad)], SHAPES[(id(mimg), ad)])
                if r >= a.min_ratio:
                    found[ad] = (names[kad], f"{tag} (by order, {r:.2f})")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("addr\tsize\tname\tkin\n")
        for ad in sorted(found):
            f.write(f"{ad:08X}\t-\t{found[ad][0]}\t{found[ad][1]}\n")
    print(f"{len(found)} functions named by kin -> {a.out}")


if __name__ == "__main__":
    main()
