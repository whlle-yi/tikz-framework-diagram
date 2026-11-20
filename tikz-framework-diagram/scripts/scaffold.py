#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TikZ 流程图生成器骨架。

用法：复制此文件为 gen.py，把层级清单填成数据表，然后
    python gen.py && xelatex -interaction=nonstopmode -halt-on-error fig.tex
不要手改生成的 .tex（会被下次覆盖），所有修改都改这个脚本。

单位约定：坐标用 1/72cm 为一格（写整数最省事）；y 取负向下。
"""

# ---------------------------------------------------------------- 基础
PX2PT = 72 / 2.54 / 72          # 1 unit = 1/72cm = 0.3937pt
def pt(px): return px * PX2PT   # 像素 -> pt（字号/行距/圆角换算用）

LW = 0.7                         # 主线条宽
OUT = []                         # 收集生成的 TikZ 代码


def w(s): OUT.append(s)


def node(cx, cy, text, fs=8.3, style="", bold=False):
    """单行文字节点，居中于 (cx,cy)。"""
    b = r"\bfseries " if bold else ""
    w(f"\\node[align=center,inner sep=0pt,outer sep=0pt,"
      f"font=\\fontsize{{{fs}}}{{{fs * 1.4:.2f}}}\\selectfont,{style}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{text}}};")


def mlines(cx, cy, lines, fs=8.3, pitch=30):
    """多行文字：逐行独立定位，行距 pitch 用实测量（像素）。"""
    n = len(lines)
    for i, t in enumerate(lines):
        y = cy + (i - (n - 1) / 2.0) * pitch
        node(cx, y, t, fs)


def chars_at(cx, y_first, pitch, text, fs=8.3):
    """竖排文字：逐字定位，y_first 为首字中心，pitch 为相邻字中心差。"""
    for i, ch in enumerate(text):
        node(cx, y_first + pitch * i, ch, fs)


def box(x0, y0, x1, y1, text="", fs=8.3, r=0, lw=LW, pitch=30):
    """矩形框（r>0 为圆角，单位像素）。text 可为 str 或 list[str]。"""
    st = f"draw=black,line width={lw}pt,fill=white"
    if r:
        st += f",rounded corners={r / 72:.4f}cm"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    if not text:
        return
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if isinstance(text, list):
        mlines(cx, cy, text, fs, pitch)
    else:
        node(cx, cy, text, fs)


def line(x0, y0, x1, y1, lw=LW):
    w(f"\\draw[line width={lw}pt] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")


def dashed(x0, y0, x1, y1, on=1.7, off=1.3, lw=0.7):
    w(f"\\draw[dashed,dash pattern=on {on}pt off {off}pt,line width={lw}pt] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def check_arrow(L, sw, hw, hh, name="块箭头"):
    """箭头比例硬约束：L 总长 / sw 轴宽 / hw 头宽 / hh 头长（栅格单位）。"""
    assert hh >= 0.5 * hw, f"{name}: 头长 {hh} < 头宽 {hw}/2，会画成一根针"
    assert hw >= 1.8 * sw, f"{name}: 头宽 {hw} 相对轴宽 {sw} 不够"
    shaft = L - hh
    assert shaft >= 0.9 * hh, f"{name}: 箭轴 {shaft} < 0.9×头长 {hh}，头尾都太短"


def varrow(cx, y0, y1, sw=26, hw=62, hh=36):
    """向下空心块箭头。默认比例见 01-style.md；区块间距取 76–84。"""
    check_arrow(y1 - y0, sw, hw, hh)
    yh = y1 - hh
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- "
      f"({cx+sw/2:.1f},{yh:.1f}) -- ({cx+hw/2:.1f},{yh:.1f}) -- "
      f"({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")


def cylinder(cx, y0, y1, rx, ry, text, fs=8.3):
    """数据库圆柱。用贝塞尔画下弧——y 翻转后 arc 的方向会反。"""
    k = 0.5523 * ry
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({cx-rx:.1f},{y0:.1f}) -- ({cx-rx:.1f},{y1:.1f}) "
      f".. controls ({cx-rx:.1f},{y1+k:.1f}) and ({cx+rx:.1f},{y1+k:.1f}) .. "
      f"({cx+rx:.1f},{y1:.1f}) -- ({cx+rx:.1f},{y0:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({cx:.1f},{y0:.1f}) ellipse ({rx:.1f} and {ry:.1f});")
    if text:
        node(cx, (y0 + y1) / 2 + ry * 0.6, text, fs)


def box3d(x0, x1, ytop, ybot, dx, dy, title, body, tfs=8.4):
    """立体卡片：正面矩形 + 顶面(标题) + 右侧面(灰)。dx,dy 为 3D 偏移量。"""
    w(f"\\fill[fill=white,draw=black,line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) -- ({x0+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1+dx:.1f},{ytop-dy:.1f}) -- ({x1:.1f},{ytop:.1f}) -- cycle;")
    w(f"\\fill[fill=cfold,draw=black,line width={LW}pt] "
      f"({x1:.1f},{ytop:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1+dx:.1f},{ybot-dy:.1f}) -- ({x1:.1f},{ybot:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) rectangle ({x1:.1f},{ybot:.1f});")
    node((x0 + x1) / 2 + dx / 2, ytop - dy / 2, title, tfs, bold=True)
    mlines((x0 + x1) / 2, (ytop + ybot) / 2 + 3, body, 8.3, 30)


def label_box(x0, y0, x1, y1, text, y_first, pitch, content_x, fs=8.3):
    """竖排标签框 + 右向块箭头（箭尾与框共边）。

    通道 = content_x - x1，按 ≥ 86 留；轴长 32、头长 42，尖端距内容区 ≥ 10。
    必须分三段画；末段不要 cycle，否则会斜拉一条线穿过框内。
    """
    cy = (y0 + y1) / 2
    sh, hd = 12, 25
    xsh, xhd = x1 + 32, x1 + 74
    assert xhd + 10 <= content_x, "标签箭头戳进了内容区"
    w(f"\\draw[line width={LW}pt] ({x0:.1f},{y1:.1f}) -- ({x0:.1f},{y0:.1f}) -- "
      f"({x1:.1f},{y0:.1f}) -- ({x1:.1f},{cy-sh:.1f});")
    w(f"\\draw[line width={LW}pt,fill=white] ({x1:.1f},{cy-sh:.1f}) -- ({xsh:.1f},{cy-sh:.1f}) -- "
      f"({xsh:.1f},{cy-hd:.1f}) -- ({xhd:.1f},{cy:.1f}) -- ({xsh:.1f},{cy+hd:.1f}) -- "
      f"({xsh:.1f},{cy+sh:.1f}) -- ({x1:.1f},{cy+sh:.1f});")
    w(f"\\draw[line width={LW}pt] ({x1:.1f},{cy+sh:.1f}) -- ({x1:.1f},{y1:.1f}) -- ({x0:.1f},{y1:.1f});")
    chars_at((x0 + x1) / 2, y_first, pitch, text, fs)


def tree(trunk_x, centers, child_edge, side="right", parent=None, parent_y=None):
    """树形支架：横干 + 每个子节点一条 stub，可选父节点接入。"""
    line(trunk_x, min(centers), trunk_x, max(centers))
    for cy in centers:
        line(trunk_x, cy, child_edge, cy)
    if parent is not None:
        line(parent, parent_y, trunk_x, parent_y)


def fit_blocks(pairs, pad_max=42):
    """容器必须贴着内容包：逐个检查（名称, 内容底边, 容器底边），超了就报错。

    先排内容、再套容器；反过来一定会留出一大块空白。
    """
    for name, content_bot, box_bot in pairs:
        gap = box_bot - content_bot
        if gap > pad_max:
            raise AssertionError(f"{name}: 容器底部留白 {gap} > {pad_max}")
        if gap < 0:
            raise AssertionError(f"{name}: 内容超出容器 {gap}")


# ---------------------------------------------------------------- 模板
HEADER = r"""% !TEX program = xelatex
\documentclass[tikz,border=6pt]{standalone}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,positioning}
\definecolor{cfold}{HTML}{CBCBCB}
\begin{document}
\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]
"""
FOOTER = "\n\\end{tikzpicture}\n\\end{document}\n"


def build(path="fig.tex"):
    open(path, "w", encoding="utf-8").write(HEADER + "\n".join(OUT) + FOOTER)
    print(f"written {path}")


# ---------------------------------------------------------------- 示例
if __name__ == "__main__":
    # 一个最小可用示例：虚线容器 + 标签框 + 两个框 + 树形支架 + 空心箭头
    dashed(141, 38, 1076, 366)
    label_box(156, 52, 217, 357, "数据源头归集与预处理", 88.5, 25.7, 320)
    box(320, 190, 647, 350, ["缺失值填充、异常值剔除、", "数据降噪、归一化归一处理"])
    box(695, 190, 1053, 350, ["样本标签标定、数据集分层、", "训练 / 验证 / 测试集拆分"])
    cylinder(399.5, 61, 128, 90.5, 9, "工况实测数据库")
    line(399.5, 149, 512.5, 149)
    line(512.5, 149, 512.5, 169)
    varrow(605, 366, 444)   # 通道 78 → 头长 36 + 箭轴 42
    build()
