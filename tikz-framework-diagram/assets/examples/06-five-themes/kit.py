#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公共图元库：按 tikz-framework-diagram 的令牌表实现。

坐标单位 = 1/72cm（1 单位 ≈ 1 格）。所有颜色取 01-style.md 的灰阶令牌。
"""
LW = 0.7
MONO_LINE, MONO_HEAD, MONO_SIDE = "monoLine", "monoHead", "monoSide"

_out = []


def begin():
    _out.clear()
    _out.append(r"\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]")


def end():
    _out.append(r"\end{tikzpicture}")
    return "\n".join(_out)


def w(s):
    _out.append(s)


# ---------------------------------------------------------------- 文本
def node(cx, cy, t, fs=8.3, color="black", bold=False):
    b = r"\bfseries " if bold else ""
    w(f"\\node[align=center,inner sep=0pt,outer sep=0pt,"
      f"font=\\fontsize{{{fs}}}{{{fs*1.4:.2f}}}\\selectfont,text={color}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{t}}};")


def two(cx, cy, t1, t2, fs1=8.3, fs2=6.5, color="black", gap=1.0):
    body = ("{\\fontsize{%.2f}{%.2f}\\selectfont\\bfseries %s}\\\\[%.2fpt]"
            "{\\fontsize{%.2f}{%.2f}\\selectfont %s}") % (
        fs1, fs1 * 1.15, t1, gap, fs2, fs2 * 1.2, t2)
    w("\\node[align=center,inner sep=0pt,outer sep=0pt,text=%s] at (%.1f,%.1f) {%s};"
      % (color, cx, cy, body))


def multiline(cx, cy, lines, fs=8.3, pitch=26, color="black"):
    n = len(lines)
    for i, t in enumerate(lines):
        node(cx, cy + (i - (n - 1) / 2) * pitch, t, fs, color)


def vtext(cx, y0, y1, text, color=MONO_LINE, fs=8.3, pitch_max=46):
    n = len(text)
    pitch = min((y1 - y0 - 20) / n, pitch_max)
    yf = y0 + ((y1 - y0) - (n - 1) * pitch) / 2
    for i, ch in enumerate(text):
        node(cx, yf + pitch * i, ch, fs, color)


# ---------------------------------------------------------------- 形状
def rect(x0, y0, x1, y1, r=0, fill="white", stroke=MONO_LINE, lw=LW):
    st = f"draw={stroke},line width={lw}pt,fill={fill}"
    if r:
        st += f",rounded corners={r/72:.4f}cm"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def dashed(x0, y0, x1, y1, stroke=MONO_LINE):
    w(f"\\draw[dashed,dash pattern=on 2.0pt off 1.6pt,line width=0.7pt,draw={stroke}] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")


def label(x0, y0, x1, y1, text, stroke=MONO_LINE):
    """左侧竖排标签 + 内嵌右向块箭头（箭尾与框共边）。"""
    cy = (y0 + y1) / 2
    sh, hd = 12, 23
    xsh, xhd = x1 + 14, x1 + 46
    w(f"\\draw[line width={LW}pt,draw={stroke}] ({x0:.1f},{y1:.1f}) -- ({x0:.1f},{y0:.1f}) -- "
      f"({x1:.1f},{y0:.1f}) -- ({x1:.1f},{cy-sh:.1f});")
    w(f"\\draw[line width={LW}pt,fill=white,draw={stroke}] ({x1:.1f},{cy-sh:.1f}) -- "
      f"({xsh:.1f},{cy-sh:.1f}) -- ({xsh:.1f},{cy-hd:.1f}) -- ({xhd:.1f},{cy:.1f}) -- "
      f"({xsh:.1f},{cy+hd:.1f}) -- ({xsh:.1f},{cy+sh:.1f}) -- ({x1:.1f},{cy+sh:.1f});")
    w(f"\\draw[line width={LW}pt,draw={stroke}] ({x1:.1f},{cy+sh:.1f}) -- ({x1:.1f},{y1:.1f}) -- "
      f"({x0:.1f},{y1:.1f});")
    vtext((x0 + x1) / 2, y0, y1, text, stroke, 8.6)


def cylinder(cx, y0, y1, rx, ry, text, stroke=MONO_LINE):
    k = 0.5523 * ry
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx-rx:.1f},{y0:.1f}) -- ({cx-rx:.1f},{y1:.1f}) "
      f".. controls ({cx-rx:.1f},{y1+k:.1f}) and ({cx+rx:.1f},{y1+k:.1f}) .. ({cx+rx:.1f},{y1:.1f}) "
      f"-- ({cx+rx:.1f},{y0:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx:.1f},{y0:.1f}) ellipse ({rx:.1f} and {ry:.1f});")
    node(cx, (y0 + y1) / 2 + 6, text, 8.0, stroke)


def card3d(x0, x1, ytop, ybot, dx, dy, title, body, stroke=MONO_LINE, side=MONO_SIDE, tfs=8.6):
    w(f"\\fill[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) -- ({x0+dx:.1f},{ytop-dy:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1:.1f},{ytop:.1f}) -- cycle;")
    w(f"\\fill[fill={side},draw={stroke},line width={LW}pt] "
      f"({x1:.1f},{ytop:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- ({x1+dx:.1f},{ybot-dy:.1f}) -- "
      f"({x1:.1f},{ybot:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0:.1f},{ytop:.1f}) rectangle ({x1:.1f},{ybot:.1f});")
    node((x0 + x1) / 2 + dx / 2, ytop - dy / 2, title, tfs, stroke, True)
    n = len(body)
    for i, line in enumerate(body):
        y = (ytop + ybot) / 2 + 4 + (i - (n - 1) / 2) * 26
        node((x0 + x1) / 2, y, line, 7.5, "black")


def pill(x0, y0, x1, y1, text, fill=MONO_HEAD, stroke=MONO_LINE, fs=8.8):
    w(f"\\draw[fill={fill},draw={stroke},line width={LW}pt,"
      f"rounded corners={(y1-y0)/2/72:.4f}cm] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    node((x0 + x1) / 2, (y0 + y1) / 2, text, fs, stroke, True)


# ---------------------------------------------------------------- 连线
def line(x0, y0, x1, y1, stroke=MONO_LINE, lw=LW, dash=False):
    st = f"line width={lw}pt,draw={stroke}"
    if dash:
        st += ",dashed,dash pattern=on 1.8pt off 1.6pt"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")


def varrow(cx, y0, y1, stroke=MONO_LINE, sw=34, hw=76, hh=18):
    assert y1 - y0 >= hh + 8, f"箭头太矮 {y1-y0} < {hh}+8"
    yh = y1 - hh
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{yh:.1f}) -- "
      f"({cx+hw/2:.1f},{yh:.1f}) -- ({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")


def hvarrow(y, x0, x1, stroke=MONO_LINE, sw=34, hw=76, hh=18):
    assert x1 - x0 >= hh + 8, f"箭头太短 {x1-x0}"
    xh = x1 - hh
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0:.1f},{y-sw/2:.1f}) -- ({xh:.1f},{y-sw/2:.1f}) -- ({xh:.1f},{y-hw/2:.1f}) -- "
      f"({x1:.1f},{y:.1f}) -- ({xh:.1f},{y+hw/2:.1f}) -- ({xh:.1f},{y+sw/2:.1f}) -- "
      f"({x0:.1f},{y+sw/2:.1f}) -- cycle;")


def thin(cx, y0, y1, stroke=MONO_LINE):
    w(f"\\draw[line width={LW}pt,draw={stroke},-{{Latex[length=1.3mm,width=0.9mm]}}] "
      f"({cx:.1f},{y0:.1f}) -- ({cx:.1f},{y1:.1f});")


def vdbl(cx, y0, y1, stroke=MONO_LINE):
    """竖直双向箭头：引擎与复核之间这种上下关系用它。"""
    w(f"\\draw[line width={LW}pt,draw={stroke},"
      f"{{Latex[length=1.3mm,width=0.9mm]}}-{{Latex[length=1.3mm,width=0.9mm]}}] "
      f"({cx:.1f},{y0:.1f}) -- ({cx:.1f},{y1:.1f});")


def dbl(y, x0, x1, stroke=MONO_LINE):
    h, s = 21, 7
    w(f"\\draw[fill=white,draw={stroke},line width={LW}pt] "
      f"({x0+11:.1f},{y-s:.1f}) -- ({x1-11:.1f},{y-s:.1f}) -- ({x1-11:.1f},{y-h:.1f}) -- "
      f"({x1:.1f},{y:.1f}) -- ({x1-11:.1f},{y+h:.1f}) -- ({x1-11:.1f},{y+s:.1f}) -- "
      f"({x0+11:.1f},{y+s:.1f}) -- ({x0+11:.1f},{y+h:.1f}) -- ({x0:.1f},{y:.1f}) -- "
      f"({x0+11:.1f},{y-h:.1f}) -- cycle;")


# ---------------------------------------------------------------- 版面检查
PAD_MAX = 42


def fit(name, c_top, c_bot, b_top, b_bot, pad_max=PAD_MAX):
    """容器必须贴着内容包：上下留白都在 0~pad_max 之间，超了直接报错。"""
    top, bot = c_top - b_top, b_bot - c_bot
    assert 0 <= top <= pad_max, f"{name}: 顶部留白 {top} 不在 0~{pad_max}"
    assert 0 <= bot <= pad_max, f"{name}: 底部留白 {bot} 不在 0~{pad_max}"
