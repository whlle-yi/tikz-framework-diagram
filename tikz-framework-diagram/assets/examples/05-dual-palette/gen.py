#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""示例 05：城市内涝实时预警系统 —— 泳道式技术路线，单色 + 彩色两版。

结构：顶部问题横幅 → 四条泳道（感知 / 数据 / 模型 / 服务），每条 6 个环节
      → 底部汇合到成果横幅。同一份几何出两版配色，放在一个 LaTeX 文件里。
    python gen.py && xelatex fig.tex
"""
OUT = []
def w(s): OUT.append(s)
LW = 0.7

# ---------------- 图元 ----------------
def node(cx, cy, text, fs=8.3, color="black", bold=False):
    b = r"\bfseries " if bold else ""
    w(f"\\node[align=center,inner sep=0pt,outer sep=0pt,"
      f"font=\\fontsize{{{fs}}}{{{fs * 1.4:.2f}}}\\selectfont,text={color}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{text}}};")



def two(cx, cy, t1, t2, fs1=8.3, fs2=6.6, color="black", gap=1.0):
    """框内两行：主标题 + 小字说明，交给 LaTeX 自己排行距。"""
    body = ("{\\fontsize{%.2f}{%.2f}\\selectfont\\bfseries %s}\\\\[%.2fpt]"
            "{\\fontsize{%.2f}{%.2f}\\selectfont %s}") % (
        fs1, fs1 * 1.15, t1, gap, fs2, fs2 * 1.2, t2)
    w("\\node[align=center,inner sep=0pt,outer sep=0pt,text=%s] at (%.1f,%.1f) {%s};" % (color, cx, cy, body))


def stage(x0, y0, x1, y1, title, note, deep, tcol=None):
    """一个环节：圆角框 + 主标题 + 小字说明。"""
    w(f"\\draw[draw={deep},line width={LW}pt,fill=white,rounded corners=7/72cm] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    two(cx, cy, title, note, 8.3, 6.6, tcol or deep)


def arrow_down(cx, y0, y1, stroke, size=1.3):
    w(f"\\draw[line width={LW}pt,draw={stroke},-{{Latex[length={size}mm,width=0.9mm]}}] "
      f"({cx:.1f},{y0:.1f}) -- ({cx:.1f},{y1:.1f});")


def arrow_right(y, x0, x1, stroke):
    w(f"\\draw[line width={LW}pt,draw={stroke},-{{Latex[length=1.4mm,width=1.0mm]}}] "
      f"({x0:.1f},{y:.1f}) -- ({x1:.1f},{y:.1f});")


def line(x0, y0, x1, y1, stroke, lw=LW):
    w(f"\\draw[line width={lw}pt,draw={stroke}] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")


def banner(x0, y0, x1, y1, text, fill, color, fs=9.0):
    w(f"\\draw[draw={color},line width=0.8pt,fill={fill},rounded corners=9/72cm] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
    node((x0 + x1) / 2, (y0 + y1) / 2, text, fs, color, True)


# ---------------- 内容 ----------------
PROBLEM = "城市内涝：降雨看不准、积水算不出、预警发不快、处置不联动"
OUTCOME = "支撑「监测—推演—预警—处置」闭环的城市内涝实时防控"

LANES = [
    ("感知层", "多源观测", [
        ("雨量站网", "分钟级 · 全网 32 站"),
        ("水位流量计", "关键节点 18 处"),
        ("视频积水识别", "路桥隧道 24 路"),
        ("雷达降雨外推", "6 分钟滚动"),
        ("管网工况信号", "泵站 12 座"),
        ("工单与舆情", "辅助核验"),
    ]),
    ("数据层", "清洗与建库", [
        ("时钟对齐", "统一到 1 分钟"),
        ("缺测异常修复", "规则 + 插值"),
        ("汇水单元编码", "划分为 46 个单元"),
        ("内涝样本库", "近 5 年 137 场"),
        ("特征构建", "雨强·坡度·管径"),
        ("训练验证切分", "时空分层抽样"),
    ]),
    ("模型层", "推演与预报", [
        ("管网水动力模型", "一维 Saint-Venant"),
        ("地表漫流耦合", "二维浅水方程"),
        ("深度学习订正", "LSTM 残差修正"),
        ("积水深度预报", "1h / 3h 滚动"),
        ("不确定性区间", "分位数回归"),
        ("阈值标定", "四级预警线"),
    ]),
    ("服务层", "预警与联动", [
        ("分级预警发布", "短信 · App · 大屏"),
        ("泵站联合调度", "规则 + 优化"),
        ("交通诱导联动", "可变情报板"),
        ("抢险资源调度", "队伍与设备"),
        ("处置效果回流", "工单闭环"),
        ("预案自学习", "季度迭代"),
    ]),
]

# ---------------- 几何（栅格单位，1 单位 = 1/72cm）----------------
X0 = 40
LANE_W, GAP = 240, 40
HEAD_Y0, HEAD_Y1 = 84, 140
NODE_W, NODE_H, NODE_GAP = 190, 56, 16
FIRST_Y = 156
LANES_BOT = FIRST_Y + 6 * NODE_H + 5 * NODE_GAP + 18
MERGE_Y = LANES_BOT + 26
BAR_Y0, BAR_Y1 = MERGE_Y + 22, MERGE_Y + 54
TOP_Y0, TOP_Y1 = 16, 62


def lane_x(i):
    return X0 + i * (LANE_W + GAP)


def node_y(j):
    return FIRST_Y + j * (NODE_H + NODE_GAP)


def draw(colors, mono):
    """colors = [(deep, light)] * 4"""
    banner(X0, TOP_Y0, lane_x(3) + LANE_W, TOP_Y1, PROBLEM, "monoHead", "black", 8.8)

    for i, (name, sub, items) in enumerate(LANES):
        deep, light = colors[i]
        tcol = "black" if deep in ("monoLine", "grayDeep") else deep
        lx, rx = lane_x(i), lane_x(i) + LANE_W
        w(f"\\draw[dashed,dash pattern=on 2.0pt off 1.6pt,line width=0.7pt,draw={deep}] "
          f"({lx:.1f},{HEAD_Y0:.1f}) rectangle ({rx:.1f},{LANES_BOT:.1f});")
        w(f"\\draw[draw={deep},line width=0.8pt,fill={light}] "
          f"({lx:.1f},{HEAD_Y0:.1f}) rectangle ({rx:.1f},{HEAD_Y1:.1f});")
        two((lx + rx) / 2, (HEAD_Y0 + HEAD_Y1) / 2, name, sub, 9.4, 7.0, tcol, 2.0)
        cx = (lx + rx) / 2
        for j, (title, note) in enumerate(items):
            ny = node_y(j)
            stage(cx - NODE_W / 2, ny, cx + NODE_W / 2, ny + NODE_H, title, note, deep, tcol)
            if j < 5:
                arrow_down(cx, ny + NODE_H, ny + NODE_H + NODE_GAP, deep)
        if i < 3:
            arrow_right(HEAD_Y0 + 18, rx + 6, rx + GAP - 6, deep)

    # 汇合线 + 成果横幅
    centers = [lane_x(i) + LANE_W / 2 for i in range(4)]
    last_bottom = node_y(5) + NODE_H
    for i, cx in enumerate(centers):
        line(cx, last_bottom, cx, MERGE_Y, colors[i][0])
    line(centers[0], MERGE_Y, centers[3], MERGE_Y, colors[1][0])
    mid = (centers[0] + centers[3]) / 2
    arrow_down(mid, MERGE_Y, BAR_Y0, colors[1][0], 1.6)
    banner(X0, BAR_Y0, lane_x(3) + LANE_W, BAR_Y1, OUTCOME,
           "monoHead" if mono else colors[1][0],
           "black" if mono else "white", 9.0)


# ---------------- 两版 ----------------
w(r"\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]")
draw([("monoLine", "monoHead")] * 4, True)
w(r"\end{tikzpicture}")
MONO = OUT[:]
OUT.clear()

w(r"\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]")
draw([("tealDeep", "tealLight"), ("navyDeep", "navyLight"),
      ("warmDeep", "warmLight"), ("grayDeep", "grayLight")], False)
w(r"\end{tikzpicture}")
COLOR = OUT[:]

HEAD = r"""% !TEX program = xelatex
% 城市内涝实时预警系统 —— 泳道式技术路线（单色 / 彩色两版）
\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.6cm]{geometry}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\definecolor{monoLine}{HTML}{4D4D4D}
\definecolor{monoHead}{HTML}{D9D9D9}
\definecolor{navyDeep}{HTML}{2A4370}
\definecolor{navyLight}{HTML}{D6E0EE}
\definecolor{tealDeep}{HTML}{2C736E}
\definecolor{tealLight}{HTML}{D3E7E4}
\definecolor{warmDeep}{HTML}{B0702F}
\definecolor{warmLight}{HTML}{F4E6D4}
\definecolor{grayDeep}{HTML}{8A8A8A}
\definecolor{grayLight}{HTML}{EFEFEF}
\setlength{\parindent}{0pt}
\pagestyle{empty}
\begin{document}

\begin{center}
{\large\bfseries 城市内涝实时预警系统技术路线}\\[1pt]
{\footnotesize 同一份几何，两种配色：四条泳道，每道六个环节}
\end{center}

\vspace{1pt}
{\footnotesize\textbf{(a) 单色版}　黑白印刷稿用；层级由灰阶、字号与虚线分组表达。}

\vspace{1pt}
\begin{center}
"""
MID = r"""
\end{center}

\vspace{5pt}
{\footnotesize\textbf{(b) 彩色版}　同一套几何，仅替换配色：每条泳道一种色系，浅色作标题底、深色作描边与文字，道内连线跟随本道颜色。}

\vspace{1pt}
\begin{center}
"""
TAIL = r"""
\end{center}

\vspace{3pt}
{\footnotesize
\textbf{图例}　虚线框 = 泳道边界；竖向箭头 = 道内工序；横向箭头 = 泳道推进；底部横线 = 成果汇合。\\[2pt]
\textbf{两版仅有颜色差异}　几何、字号、间距、线宽完全一致：标题条 \texttt{\#D9D9D9} → 本泳道浅档；
框线 \texttt{\#4D4D4D} → 本泳道深档；成果条 \texttt{\#D9D9D9}+黑字 → 主色深档+白字。
}

\end{document}
"""

open("fig.tex", "w", encoding="utf-8").write(HEAD + "\n".join(MONO) + MID + "\n".join(COLOR) + TAIL)
print("written fig.tex")
