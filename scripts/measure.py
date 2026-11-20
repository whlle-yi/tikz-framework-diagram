#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""位图几何测量工具：为 TikZ 复刻量取坐标。

用法示例
--------
python measure.py hlines img.jpg --x0 300 --x1 920
python measure.py vlines img.jpg --y0 200 --y1 460
python measure.py edges  img.jpg --y0 215 --y1 260          # 一排框的左右边界
python measure.py ink    img.jpg --x0 330 --y0 75 --x1 450 --y1 110
python measure.py row    img.jpg --y 313 --x0 300 --x1 920
python measure.py col    img.jpg --x 611 --y0 170 --y1 250
python measure.py art    img.jpg --x0 300 --y0 118 --x1 920 --y1 250
python measure.py dashed img.jpg                            # 覆盖率 0.3~0.8 的虚线条
"""
import argparse
import sys

import numpy as np
from PIL import Image


def load(path):
    return np.array(Image.open(path).convert("L"))


def runs_of(idx, gap=2):
    """把升序索引聚成连续游程。"""
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - p <= gap:
            p = v
        else:
            out.append((int(s), int(p)))
            s = p = v
    out.append((int(s), int(p)))
    return out


def merge(items, tol=2, join=12):
    """合并相邻行/列上的同类线段（抗抗锯齿造成的 1~2px 分裂）。"""
    res = []
    for a, s0, s1 in items:
        for r in res:
            if abs(a - r[0]) <= tol and not (s1 < r[1] - join or s0 > r[2] + join):
                r[0] = min(r[0], a)
                r[1] = min(r[1], s0)
                r[2] = max(r[2], s1)
                break
        else:
            res.append([a, s0, s1])
    return res


# ---------------------------------------------------------------- commands
def cmd_hlines(a, args):
    sub = a[:, args.x0:args.x1] < args.dark
    items = []
    for y in range(sub.shape[0]):
        for s0, s1 in runs_of(np.where(sub[y])[0], args.gap):
            if s1 - s0 >= args.minlen:
                items.append((y, s0 + args.x0, s1 + args.x0))
    for y, s0, s1 in merge(sorted(items)):
        print(f"H y={y:<5d} x={s0}..{s1}  w={s1 - s0}")


def cmd_vlines(a, args):
    sub = a[:, args.x0:args.x1] < args.dark
    sub = sub[args.y0:args.y1]
    items = []
    for x in range(sub.shape[1]):
        for s0, s1 in runs_of(np.where(sub[:, x])[0], args.gap):
            if s1 - s0 >= args.minlen:
                items.append((x + args.x0, s0 + args.y0, s1 + args.y0))
    for x, s0, s1 in merge(sorted(items)):
        print(f"V x={x:<5d} y={s0}..{s1}  h={s1 - s0}")


def cmd_edges(a, args):
    """一排方框的左右边界：区间内竖线覆盖率接近 1 的列。"""
    sub = a[args.y0:args.y1, args.x0:args.x1] < args.dark
    cov = sub.sum(axis=0) / max(1, (args.y1 - args.y0))
    hit = [args.x0 + i for i, v in enumerate(cov) if v > args.cov]
    cols = [int(np.mean(g)) for g in runs_of(np.array(hit), 2)] if hit else []
    print("edges:", cols)
    if len(cols) >= 2:
        pairs = [f"{cols[i]}-{cols[i + 1]}" for i in range(0, len(cols) - 1, 2)]
        print("boxes:", ", ".join(pairs))


def cmd_dashed(a, args):
    """虚线/点线：覆盖率落在 0.30~0.80 的整列。"""
    sub = a[args.y0:args.y1, :] < args.dark
    cov = sub.sum(axis=0) / max(1, (args.y1 - args.y0))
    hit = [i for i, v in enumerate(cov) if args.lo < v < args.hi]
    for g in runs_of(np.array(hit), 2) if hit else []:
        c = int(np.mean(g))
        print(f"dashed col x={c}  coverage={cov[c]:.2f}")


def cmd_ink(a, args):
    s = a[args.y0:args.y1, args.x0:args.x1] < args.dark
    xs = np.where(s.any(axis=0))[0]
    ys = np.where(s.any(axis=1))[0]
    if len(xs) == 0:
        print("no ink")
        return
    x0, x1 = args.x0 + int(xs.min()), args.x0 + int(xs.max())
    y0, y1 = args.y0 + int(ys.min()), args.y0 + int(ys.max())
    print(f"ink x={x0}..{x1} (w={x1 - x0})  y={y0}..{y1} (h={y1 - y0})")
    print(f"center=({(x0 + x1) / 2:.1f},{(y0 + y1) / 2:.1f})")
    if args.chars:
        w = (x1 - x0) / args.chars
        print(f"per-char w={w:.1f}px  ->  font ~{w * 0.3937:.2f}pt")


def cmd_row(a, args):
    print(runs_of(np.where(a[args.y, args.x0:args.x1] < args.dark)[0], args.gap)
          and [(s + args.x0, e + args.x0) for s, e in
               runs_of(np.where(a[args.y, args.x0:args.x1] < args.dark)[0], args.gap)])


def cmd_col(a, args):
    r = runs_of(np.where(a[args.y0:args.y1, args.x] < args.dark)[0], args.gap)
    print([(s + args.y0, e + args.y0) for s, e in r])


def cmd_art(a, args):
    sx, sy = max(1, args.sx), max(1, args.sy)
    sub = (a[args.y0:args.y1, args.x0:args.x1] < args.dark).astype(float)
    for j in range(0, sub.shape[0] - sy + 1, sy):
        line = ""
        for i in range(0, sub.shape[1] - sx + 1, sx):
            m = sub[j:j + sy, i:i + sx].mean()
            line += "#" if m > .55 else ("+" if m > .25 else ("." if m > .07 else " "))
        print(f"{args.y0 + j:5d} {line}")


def main():
    p = argparse.ArgumentParser(description="位图几何测量（TikZ 复刻用）")
    p.add_argument("cmd", choices=["hlines", "vlines", "edges", "dashed", "ink", "row", "col", "art"])
    p.add_argument("image")
    p.add_argument("--x0", type=int, default=0)
    p.add_argument("--x1", type=int, default=10 ** 6)
    p.add_argument("--y0", type=int, default=0)
    p.add_argument("--y1", type=int, default=10 ** 6)
    p.add_argument("--x", type=int)
    p.add_argument("--y", type=int)
    p.add_argument("--dark", type=int, default=165, help="暗像素阈值")
    p.add_argument("--minlen", type=int, default=60, help="线段最小长度")
    p.add_argument("--gap", type=int, default=2, help="游程间断容忍")
    p.add_argument("--cov", type=float, default=0.75, help="edges: 覆盖率阈值")
    p.add_argument("--lo", type=float, default=0.30, help="dashed: 覆盖率下限")
    p.add_argument("--hi", type=float, default=0.80, help="dashed: 覆盖率上限")
    p.add_argument("--chars", type=int, default=0, help="ink: 字数，用于推算字号")
    p.add_argument("--sx", type=int, default=5)
    p.add_argument("--sy", type=int, default=4)
    args = p.parse_args()

    a = load(args.image)
    args.y1 = min(args.y1, a.shape[0])
    args.x1 = min(args.x1, a.shape[1])

    if args.cmd in ("row",) and args.y is None:
        sys.exit("row 需要 --y")
    if args.cmd in ("col",) and args.x is None:
        sys.exit("col 需要 --x")

    {"hlines": cmd_hlines, "vlines": cmd_vlines, "edges": cmd_edges, "dashed": cmd_dashed,
     "ink": cmd_ink, "row": cmd_row, "col": cmd_col, "art": cmd_art}[args.cmd](a, args)


if __name__ == "__main__":
    main()
