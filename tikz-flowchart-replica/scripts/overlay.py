#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""红蓝叠色比对：原图 vs 我的渲染结果。

颜色语义
--------
红 = 只有我的图有    蓝 = 只有原图有    黑 = 两者重合

用法
----
# 1) 先用 183dpi 渲染 PDF（1 单位 ≈ 1 像素）
python -c "import pymupdf; pymupdf.open('fig.pdf')[0].get_pixmap(dpi=183).save('out.png')"

# 2) 叠色
python overlay.py 素材/1.jpg out.png --orig 141,38,1076,1417 --out overlay.png

参数 --orig 给原图上要参与比对的矩形区域，其左上角应与绘图坐标的原点一致
（即生成器里最小的 x / 最小的 y）。--border 与 standalone 的 border 保持一致。
"""
import argparse
import sys

import numpy as np
from PIL import Image


def dark_bbox(a, thr=250):
    ys, xs = np.where(a < thr)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max()


def main():
    ap = argparse.ArgumentParser(description="红蓝叠色比对")
    ap.add_argument("original")
    ap.add_argument("render")
    ap.add_argument("--orig", required=True,
                    help="原图比对区域 x0,y0,x1,y1（左上角=绘图原点）")
    ap.add_argument("--border", type=float, default=6, help="standalone 的 border(pt)")
    ap.add_argument("--dpi", type=float, default=183, help="渲染 dpi")
    ap.add_argument("--anchor", default="auto",
                    help="渲染图上内容左上角像素坐标，auto=自动取暗像素包围盒")
    ap.add_argument("--out", default="overlay.png")
    ap.add_argument("--diff", action="store_true", help="额外输出纯色差异图（更易读）")
    args = ap.parse_args()

    x0, y0, x1, y1 = [int(v) for v in args.orig.split(",")]
    W, H = x1 - x0, y1 - y0
    if W <= 0 or H <= 0:
        sys.exit("--orig 区域无效")

    O = np.array(Image.open(args.original).convert("L"))
    M = np.array(Image.open(args.render).convert("L"))
    oc = O[y0:y1, x0:x1]

    if args.anchor == "auto":
        bb = dark_bbox(M)
        if bb is None:
            sys.exit("渲染图没有内容")
        ax, ay = bb[0], bb[1]
    else:
        ax, ay = [int(v) for v in args.anchor.split(",")]

    scale = args.dpi / 182.88          # 每单位对应的渲染像素
    border_px = args.border * 2.54 * scale
    # 内容左上角应对齐到 border_px（自动锚点已包含线宽，直接用）
    sx = int(round(ax + (0 - 0) + (border_px - border_px)))
    mc = M[int(ay):int(ay + H * scale), int(ax):int(ax + W * scale)]
    if mc.size == 0:
        sys.exit("裁切超出渲染图范围，检查 --orig / --dpi")
    mc = np.array(Image.fromarray(mc).resize((W, H), Image.BILINEAR))

    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[..., 0] = oc                      # 红通道 = 原图
    img[..., 1] = np.minimum(oc, mc)      # 公共部分
    img[..., 2] = mc                      # 蓝通道 = 我的
    Image.fromarray(img).save(args.out)
    print(f"overlay -> {args.out}   ({W}x{H}, scale={scale:.4f})")

    if args.diff:
        d = np.zeros((H, W, 3), dtype=np.uint8)
        only_o = (oc < 170) & (mc >= 170)
        only_m = (mc < 170) & (oc >= 170)
        d[only_o] = (40, 90, 255)         # 蓝：原图独有（我漏画）
        d[only_m] = (255, 60, 40)         # 红：我独有（多画/错位）
        both = (oc < 170) & (mc < 170)
        d[both] = (200, 200, 200)
        out2 = args.out.rsplit(".", 1)[0] + "_diff.png"
        Image.fromarray(d).save(out2)
        rare = int(only_o.sum()) / max(1, int((oc < 170).sum())) * 100
        print(f"diff    -> {out2}   原图独有像素占比 {rare:.1f}%")


if __name__ == "__main__":
    main()
