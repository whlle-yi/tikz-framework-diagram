#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""示例 05：城市内涝实时预警系统 —— 多图元组合，单色与彩色两版。

图元：数据库圆柱、立体折角卡片、胶囊标题、分层虚线容器、左侧竖排标签、
      内嵌右向块箭头、层间空心块箭头、双向箭头、1→4 树形支架、结论条。
    python gen.py && xelatex fig.tex
"""
OUT = []
def w(s): OUT.append(s)
LW = 0.7

# ---------------- 基础图元 ----------------
def node(cx, cy, t, fs=8.3, color="black", bold=False):
    b = r"\bfseries " if bold else ""
    w(f"\\node[align=center,inner sep=0pt,outer sep=0pt,"
      f"font=\\fontsize{{{fs}}}{{{fs*1.4:.2f}}}\\selectfont,text={color}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{t}}};")


def two(cx, cy, t1, t2, fs1=8.3, fs2=6.6, color="black", gap=1.2):
    body = ("{\\fontsize{%.2f}{%.2f}\\selectfont\\bfseries %s}\\\\[%.2fpt]"
            "{\\fontsize{%.2f}{%.2f}\\selectfont %s}") % (
        fs1, fs1 * 1.15, t1, gap, fs2, fs2 * 1.2, t2)
    w("\\node[align=center,inner sep=0pt,outer sep=0pt,text=%s] at (%.1f,%.1f) {%s};"
      % (color, cx, cy, body))


def rect(x0, y0, x1, y1, r=0, fill="white", stroke="black", lw=LW):
    st = f"draw={stroke},line width={lw}pt,fill={fill}"
    if r:
        st += f",rounded corners={r/72:.4f}cm"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def dashed(x0, y0, x1, y1, stroke):
    w(f"\\draw[dashed,dash pattern=on 2.0pt off 1.6pt,line width=0.7pt,draw={stroke}] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def check_arrow(L, sw, hw, hh, name="块箭头"):
    assert hh >= 0.5 * hw, f"{name}: 头长 {hh} < 头宽 {hw}/2"
    assert hw >= 1.8 * sw, f"{name}: 头宽 {hw} 相对轴宽 {sw} 不够"
    shaft = L - hh
    assert shaft >= 0.9 * hh, f"{name}: 箭轴 {shaft} < 0.9×头长 {hh}"


def varrow(cx, y0, y1, stroke, sw=26, hw=62, hh=36):
    check_arrow(y1 - y0, sw, hw, hh)
    yh = y1 - hh
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{yh:.1f}) -- "
      f"({cx+hw/2:.1f},{yh:.1f}) -- ({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")


def label_box(x0, y0, x1, y1, text, stroke, content_x=172):
    """左侧竖排标签 + 内嵌右向块箭头（箭尾与框共边）。

    轴长 32、头长 42；尖端停在内容区左侧 ≥ 10 处。
    """
    cy = (y0 + y1) / 2
    sh, hd = 12, 25          # 轴半高 / 头半高
    xsh, xhd = x1 + 32, x1 + 74
    assert xhd + 10 <= content_x, f"标签箭头戳进内容区: {xhd} vs {content_x}"
    w(f"\\draw[line width={LW}pt,draw={stroke}] ({x0:.1f},{y1:.1f}) -- ({x0:.1f},{y0:.1f}) -- "
      f"({x1:.1f},{y0:.1f}) -- ({x1:.1f},{cy-sh:.1f});")
    w(f"\\draw[line width={LW}pt,fill=white,draw={stroke}] ({x1:.1f},{cy-sh:.1f}) -- "
      f"({xsh:.1f},{cy-sh:.1f}) -- ({xsh:.1f},{cy-hd:.1f}) -- ({xhd:.1f},{cy:.1f}) -- "
      f"({xsh:.1f},{cy+hd:.1f}) -- ({xsh:.1f},{cy+sh:.1f}) -- ({x1:.1f},{cy+sh:.1f});")
    w(f"\\draw[line width={LW}pt,draw={stroke}] ({x1:.1f},{cy+sh:.1f}) -- ({x1:.1f},{y1:.1f}) -- "
      f"({x0:.1f},{y1:.1f});")
    n = len(text)
    pitch = min((y1 - y0 - 26) / n, 46)
    y_first = y0 + ((y1 - y0) - (n - 1) * pitch) / 2
    for i, ch in enumerate(text):
        node((x0 + x1) / 2, y_first + pitch * i, ch, 8.6, stroke)


def cylinder(cx, y0, y1, rx, ry, text, stroke):
    k = 0.5523 * ry
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx-rx:.1f},{y0:.1f}) -- ({cx-rx:.1f},{y1:.1f}) "
      f".. controls ({cx-rx:.1f},{y1+k:.1f}) and ({cx+rx:.1f},{y1+k:.1f}) .. ({cx+rx:.1f},{y1:.1f}) "
      f"-- ({cx+rx:.1f},{y0:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx:.1f},{y0:.1f}) ellipse ({rx:.1f} and {ry:.1f});")
    node(cx, (y0 + y1) / 2 + 6, text, 8.3, stroke)


def card3d(x0, x1, ytop, ybot, dx, dy, title, body, stroke, side):
    w(f"\\fill[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) -- ({x0+dx:.1f},{ytop-dy:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1:.1f},{ytop:.1f}) -- cycle;")
    w(f"\\fill[fill={side},draw={stroke},line width={LW}pt] "
      f"({x1:.1f},{ytop:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- ({x1+dx:.1f},{ybot-dy:.1f}) -- "
      f"({x1:.1f},{ybot:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) rectangle ({x1:.1f},{ybot:.1f});")
    node((x0 + x1) / 2 + dx / 2, ytop - dy / 2, title, 8.8, stroke, True)
    n = len(body)
    for i, line in enumerate(body):
        y = (ytop + ybot) / 2 + 4 + (i - (n - 1) / 2) * 26
        node((x0 + x1) / 2, y, line, 7.6, "black")


def pill(x0, y0, x1, y1, text, fill, stroke):
    w(f"\\draw[fill={fill},draw={stroke},line width={LW}pt,"
      f"rounded corners={(y1-y0)/2/72:.4f}cm] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    node((x0 + x1) / 2, (y0 + y1) / 2, text, 8.8, stroke, True)


def vtext(cx, y0, y1, text, color, fs=8.3):
    n = len(text)
    pitch = min((y1 - y0 - 20) / n, 44)
    yf = y0 + ((y1 - y0) - (n - 1) * pitch) / 2
    for i, ch in enumerate(text):
        node(cx, yf + pitch * i, ch, fs, color)


def line(x0, y0, x1, y1, stroke):
    w(f"\\draw[line width={LW}pt,draw={stroke}] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")


def dbl_arrow(cy, x0, x1, stroke):
    hl, h, s = 20, 24, 8
    assert x1 - x0 >= 2 * hl + 20, f"双向箭头太短 {x1-x0}"
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0+hl:.1f},{cy-s:.1f}) -- ({x1-hl:.1f},{cy-s:.1f}) -- ({x1-hl:.1f},{cy-h:.1f}) -- "
      f"({x1:.1f},{cy:.1f}) -- ({x1-hl:.1f},{cy+h:.1f}) -- ({x1-hl:.1f},{cy+s:.1f}) -- "
      f"({x0+hl:.1f},{cy+s:.1f}) -- ({x0+hl:.1f},{cy+h:.1f}) -- ({x0:.1f},{cy:.1f}) -- "
      f"({x0+hl:.1f},{cy-h:.1f}) -- cycle;")


# ---------------- 内容 ----------------
CYL = ["雨量遥测库", "管网拓扑库", "历史内涝库", "预案知识库"]
CARD_T = "多源数据融合与样本构建"
CARD_B = ["时钟对齐 · 缺测修复 · 汇水单元编码", "特征构建 · 样本分层 · 训练验证切分"]
MODULES = [("模型输入", "边界与初始场"), ("参数标定", "糙率 · 坡度 · 管径")]
BRANCH = ["一维管网水力", "二维地表漫流", "耦合求解调度", "残差智能订正"]
CHILD = ["短信与 App 推送", "泵站联合调度", "交通诱导联动", "抢险资源调度"]
OUTCOME = "支撑「监测—推演—预警—处置」闭环的城市内涝实时防控"

# ---------------- 几何（栅格单位，1 单位 = 1/72cm）----------------
CX0, CX1 = 40, 960
LB0, LB1 = 54, 86
B0, B1 = 172, 946
MID = (B0 + B1) / 2                      # 559

C1 = (40, 404)
C2 = (482, 764)
C3 = (842, 1086)
C4 = (1164, 1232)

PAD_MAX = 42     # 容器到内容的最大允许留白（单位=1/72cm），超了就是"空一大块"


def fit(name, c_top, c_bot, b_top, b_bot):
    """容器必须贴着内容包：上下留白都不许超过 PAD_MAX。"""
    assert b_top - c_top <= PAD_MAX, f"{name} 顶部留白 {b_top-c_top} > {PAD_MAX}"
    assert b_bot - c_bot <= PAD_MAX, f"{name} 底部留白 {b_bot-c_bot} > {PAD_MAX}"


def draw(ts):
    t1, t2, t3 = ts
    L1, H1, T1, S1 = t1["line"], t1["hdr"], t1["hdrT"], t1["side"]
    L2, H2, T2, S2 = t2["line"], t2["hdr"], t2["hdrT"], t2["side"]
    L3, H3, T3, S3 = t3["line"], t3["hdr"], t3["hdrT"], t3["side"]

    # ===== 1. 数据治理 =====
    dashed(CX0, C1[0], CX1, C1[1], L1)
    label_box(LB0, C1[0] + 14, LB1, C1[1] - 14, "数据治理", L1)
    cxs = [257, 457, 657, 857]
    for cx, name in zip(cxs, CYL):
        cylinder(cx, 68, 166, 89, 9, name, L1)
    line(cxs[0], 196, cxs[-1], 196, L1)
    for cx in cxs:
        line(cx, 175, cx, 196, L1)
    line(578, 196, 578, 222, L1)
    card3d(257, 857, 264, 374, 42, 42, CARD_T, CARD_B, L1, S1)
    fit("数据治理", 59, 374, C1[0], C1[1])

    # ===== 2. 模型推演 =====
    dashed(CX0, C2[0], CX1, C2[1], L2)
    label_box(LB0, C2[0] + 14, LB1, C2[1] - 14, "模型推演", L2)
    mod_cy = []
    for i, (m, note) in enumerate(MODULES):
        y0 = 528 + i * 132
        rect(180, y0, 330, y0 + 90, 12, "white", L2)
        two(255, y0 + 45, m, note, 8.3, 6.4, L2, 1.2)
        mod_cy.append(y0 + 45)
    w(f"\\draw[line width={LW}pt,draw={L2},-{{Latex[length=1.5mm,width=1.0mm]}}] "
      f"(255,{mod_cy[0]+45:.1f}) -- (255,{mod_cy[1]-45:.1f});")
    br_cy = []
    for i, b in enumerate(BRANCH):
        y0 = 512 + i * 66
        rect(390, y0, 650, y0 + 56, 10, "white", L2)
        node(520, y0 + 28, b, 8.3, L2)
        br_cy.append(y0 + 28)
    for cy_m, idx in [(mod_cy[0], (0, 1)), (mod_cy[1], (2, 3))]:
        line(330, cy_m, 358, cy_m, L2)
        line(358, br_cy[idx[0]], 358, br_cy[idx[1]], L2)
        for i in idx:
            line(358, br_cy[i], 390, br_cy[i], L2)
    for y in br_cy:
        line(650, y, 676, y, L2)
    line(676, br_cy[0], 676, br_cy[-1], L2)
    line(676, 639, 700, 639, L2)
    rect(700, 512, 824, 766, 12, "white", L2)
    two(762, 639, "内涝预报", "核心模型", 8.8, 7.0, L2, 1.4)
    dbl_arrow(639, 824, 884, L2)
    rect(884, 512, 946, 766, 12, "white", L2)
    vtext(915, 572, 722, "积水深度预警", L2, 8.3)
    fit("模型推演", 512, 766, C2[0], C2[1])

    varrow(MID, 404, 404 + 78, L2)
    varrow(MID, 764, 764 + 78, L3)

    # ===== 3. 预警联动 =====
    dashed(CX0, C3[0], CX1, C3[1], L3)
    label_box(LB0, C3[0] + 14, LB1, C3[1] - 14, "预警联动", L3)
    pill(300, 842, 700, 892, "风险研判与分级预警", H3, L3)
    rect(300, 906, 700, 976, 10, "white", L3)
    node(500, 941, "内涝风险实时研判", 8.6, L3, True)
    kids = [208, 388, 568, 748]
    line(500, 976, 500, 1006, L3)
    line(kids[0] + 80, 1006, kids[-1] + 80, 1006, L3)
    for k, txt in zip(kids, CHILD):
        line(k + 80, 1006, k + 80, 1044, L3)
        rect(k, 1044, k + 160, 1076, 10, "white", L3)
        node(k + 80, 1060, txt, 8.0, L3)
    fit("预警联动", 842, 1076, C3[0], C3[1])
    varrow(MID, 1086, 1086 + 78, L3)

    # ===== 4. 结论条 =====
    rect(CX0, C4[0], CX1, C4[1], 8, t2["bar"], t2["line"], 0.8)
    node((CX0 + CX1) / 2, (C4[0] + C4[1]) / 2, OUTCOME, 9.2, t2["barT"], True)


# ---------------- 两版 ----------------
w(r"\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]")
draw([{"line": "monoLine", "hdr": "monoHead", "hdrT": "black", "side": "monoSide",
       "bar": "monoHead", "barT": "black"}] * 3)
w(r"\end{tikzpicture}")
MONO = OUT[:]
OUT.clear()

w(r"\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]")
draw([{"line": "tealDeep", "hdr": "tealLight", "hdrT": "tealDeep", "side": "tealSide",
       "bar": "tealDeep", "barT": "white"},
      {"line": "navyDeep", "hdr": "navyLight", "hdrT": "navyDeep", "side": "navySide",
       "bar": "navyDeep", "barT": "white"},
      {"line": "warmDeep", "hdr": "warmLight", "hdrT": "warmDeep", "side": "warmSide",
       "bar": "warmDeep", "barT": "white"}])
w(r"\end{tikzpicture}")
COLOR = OUT[:]

HEAD = r"""% !TEX program = xelatex
% 城市内涝实时预警系统 —— 多图元组合（单色 / 彩色两版）
\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.5cm]{geometry}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\definecolor{monoLine}{HTML}{4D4D4D}
\definecolor{monoHead}{HTML}{D9D9D9}
\definecolor{monoSide}{HTML}{CBCBCB}
\definecolor{navyDeep}{HTML}{2A4370}
\definecolor{navyLight}{HTML}{D6E0EE}
\definecolor{navySide}{HTML}{B9CBE2}
\definecolor{tealDeep}{HTML}{2C736E}
\definecolor{tealLight}{HTML}{D3E7E4}
\definecolor{tealSide}{HTML}{B7D8D5}
\definecolor{warmDeep}{HTML}{B0702F}
\definecolor{warmLight}{HTML}{F4E6D4}
\definecolor{warmSide}{HTML}{E3C7A4}
\setlength{\parindent}{0pt}
\pagestyle{empty}
\begin{document}

\begin{center}
{\large\bfseries 城市内涝实时预警系统技术路线}\\[1pt]
{\footnotesize 同一份几何，两种配色}
\end{center}

\vspace{0pt}
{\footnotesize\textbf{(a) 单色版}　黑白印刷稿用。}

\vspace{0pt}
\begin{center}
"""
MID = r"""
\end{center}

\newpage

\vspace{2pt}
{\footnotesize\textbf{(b) 彩色版}　同一套几何，仅替换配色：容器描边、圆柱、立体卡片、胶囊与结论条统一取主色系深浅两档。}

\vspace{0pt}
\begin{center}
"""
TAIL = r"""
\end{center}

\vspace{0pt}
{\footnotesize
\textbf{图元}　数据库圆柱 ×4；立体折角卡片（顶面放标题、右侧面填灰）；胶囊标题；
分层虚线容器 + 左侧竖排标签 + 内嵌右向块箭头；层间空心块箭头；双向箭头；1→4 树形支架；结论条。
}

\end{document}
"""

open("fig.tex", "w", encoding="utf-8").write(HEAD + "\n".join(MONO) + MID + "\n".join(COLOR) + TAIL)
print("written fig.tex")
