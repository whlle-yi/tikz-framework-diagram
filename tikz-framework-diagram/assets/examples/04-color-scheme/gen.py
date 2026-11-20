#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彩色方案样例：三层架构，每层一个色系。

演示 09-color.md 的色板与映射规则：浅色填充 + 深色描边 + 黑字。
    python gen.py && xelatex fig.tex
"""

# ---- 色板（与 09-color.md 一致）----
MAIN = ("mainDeep", "mainLight")   # 主色系：结构 / 模型
TEAL = ("tealDeep", "tealLight")   # 辅助：数据
WARM = ("warmDeep", "warmLight")   # 辅助：应用
INK  = "black"                  # 正文文字

OUT = []
def w(s): OUT.append(s)
LW = 0.7


def hexcolor(name, h):
    return f"\\definecolor{{{name}}}{{HTML}}{{{h[1:]}}}"


def node(cx, cy, text, fs=8.3, color=INK, bold=False):
    b = r"\bfseries " if bold else ""
    w(f"\\node[align=center,inner sep=0pt,outer sep=0pt,"
      f"font=\\fontsize{{{fs}}}{{{fs * 1.4:.2f}}}\\selectfont,text={color}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{text}}};")


def box(x0, y0, x1, y1, text="", fill="white", stroke=INK, fs=8.3, r=0, bold=False):
    st = f"draw={stroke},line width={LW}pt,fill={fill}"
    if r:
        st += f",rounded corners={r/72:.4f}cm"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    if text:
        node((x0 + x1) / 2, (y0 + y1) / 2, text, fs, stroke, bold)


def dashed(x0, y0, x1, y1, stroke):
    w(f"\\draw[dashed,dash pattern=on 1.7pt off 1.3pt,line width=0.7pt,draw={stroke}] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def varrow(cx, y0, y1, sw, hw, hh, stroke):
    yh = y1 - hh
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- "
      f"({cx+sw/2:.1f},{yh:.1f}) -- ({cx+hw/2:.1f},{yh:.1f}) -- "
      f"({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")


def arrow(x0, x1, y, stroke):
    w(f"\\draw[line width={LW}pt,draw={stroke},-{{Latex[length=1.4mm,width=1.0mm]}}] "
      f"({x0:.1f},{y:.1f}) -- ({x1:.1f},{y:.1f});")


def chars(cx, y0, y1, text, color, fs=8.3):
    n = len(text)
    pitch = (y1 - y0 - 24) / n
    for i, ch in enumerate(text):
        node(cx, y0 + 12 + pitch * (i + 0.5), ch, fs, color)


# ---- 版面 ----
LAYERS = [
    ("数据层", TEAL, ["多源采集", "清洗对齐", "特征构建"]),
    ("模型层", MAIN, ["训练调度", "效果评估", "轻量化"]),
    ("应用层", WARM, ["系统集成", "现场验证", "成果输出"]),
]
Y0 = [40, 232, 424]
H = 150           # 层高
CONT_X = (60, 876)
LAB_X = (68, 150)
BOX_X = [(160, 380), (404, 624), (648, 868)]
BOX_H = 70

for i, (label, (deep, light), items) in enumerate(LAYERS):
    y0 = Y0[i]
    y1 = y0 + H
    dashed(CONT_X[0], y0, CONT_X[1], y1, deep)
    # 左侧竖排标签
    box(LAB_X[0], y0 + 10, LAB_X[1], y1 - 10, "", light, deep, r=8)
    chars((LAB_X[0] + LAB_X[1]) / 2, y0 + 10, y1 - 10, label, deep, 9.2)
    # 三个内容框
    for (bx0, bx1), txt in zip(BOX_X, items):
        cy = (y0 + y1) / 2
        box(bx0, cy - BOX_H / 2, bx1, cy + BOX_H / 2, txt, "white", deep)
    # 框间细箭头
    for j in range(2):
        arrow(BOX_X[j][1], BOX_X[j + 1][0], (y0 + y1) / 2, deep)

# 层间块箭头
for i in range(2):
    varrow((CONT_X[0] + CONT_X[1]) / 2, Y0[i] + H + 6, Y0[i + 1] - 6, 34, 66, 14,
           LAYERS[i + 1][1][0])

HEAD = r"""% !TEX program = xelatex
% 彩色方案样例：三层架构
\documentclass[tikz,border=8pt]{standalone}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\definecolor{mainDeep}{HTML}{2A4370}
\definecolor{mainLight}{HTML}{D6E0EE}
\definecolor{tealDeep}{HTML}{2C736E}
\definecolor{tealLight}{HTML}{D3E7E4}
\definecolor{warmDeep}{HTML}{B0702F}
\definecolor{warmLight}{HTML}{F4E6D4}
\begin{document}
\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]
"""
FOOT = "\n\\end{tikzpicture}\n\\end{document}\n"
open("fig.tex", "w", encoding="utf-8").write(HEAD + "\n".join(OUT) + FOOT)
print("written fig.tex")
