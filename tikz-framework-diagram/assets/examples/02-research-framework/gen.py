# -*- coding: utf-8 -*-
"""研究框架图生成器：三列框架，坐标用栅格单位（1 单位 = 1/72cm）"""

BOX_FILL   = "cbox"   # 内容白框
COL_FILL   = "ccol"   # 左右两列
HDR_FILL   = "chdr"   # 区块标题
TOP_FILL   = "ctop"   # 顶部三个框
LINE       = "cline"   # 线条颜色

out = []
def w(s): out.append(s)

def box(x0,y0,x1,y1,text,fill=BOX_FILL,bold=False,fs=6.7,lw=0.55,align='center'):
    style = f"fill={fill}"
    b = r"\bfseries " if bold else ""
    w(f"\\node[box,{style},line width={lw}pt,minimum width={(x1-x0)/72:.4f}cm,"
      f"minimum height={(y1-y0)/72:.4f}cm,font=\\fontsize{{{fs}}}{{{fs*1.28:.2f}}}\\selectfont] at ({(x0+x1)/2:.1f},{(y0+y1)/2:.1f})"
      f" {{{b}{text}}};")

def line(x0,y0,x1,y1,lw=0.55,arrow=None):
    if arrow:
        st = f"draw={LINE},line width={lw}pt,-{{Latex[length=1.2mm,width=0.95mm]}}"
    else:
        st = f"draw={LINE},line width={lw}pt"
    w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")

def rect(x0,y0,x1,y1,style):
    w(f"\\draw[{style}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")

def hollow_down(cx,y0,y1,sw=26,hh=12,hw=55):
    """空心向下箭头：sw 轴宽，hw 头宽，hh 头长"""
    yh = y1-hh
    w(f"\\draw[fill=white,draw={LINE},line width=0.7pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{yh:.1f}) -- "
      f"({cx+hw/2:.1f},{yh:.1f}) -- ({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")

# ============ 头部 ============
# 不画页面底色：白底由 PDF 自带

# 顶部三个框
box(143,52,281,97,"研究步骤",TOP_FILL,True,7.0)
box(302,52,920,97,"XXXXXX对XXXXXX恢复性效应的影响研究",TOP_FILL,True,7.0)
box(941,52,1080,97,"研究方法",TOP_FILL,True,7.0)
line(143,97,1080,97,0.8)

# 外虚线框
# 三个并排的虚线单元：左(研究步骤列) / 中(研究内容列) / 右(研究方法列)
for (cx0,cx1) in [(142,281),(302,919),(941,1079)]:
    rect(cx0,120,cx1,1400,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")

# 顶部连线
line(281,75,302,75); line(920,75,941,75)
line(212,97,212,137,arrow=True)
line(1010,97,1010,235)

# ============ 左列 ============
LX0,LX1 = 165,259
L = [(137,383,"提出\\\\问题"),
     (440,677,"研究样\\\\点选择\\\\与实地\\\\测量"),
     (713,951,"问卷设\\\\计和主\\\\观数据\\\\收集"),
     (984,1171,"生理指\\\\标数据\\\\收集"),
     (1215,1387,"提出优\\\\化设计\\\\策略")]
for i,(y0,y1,t) in enumerate(L):
    box(LX0,y0,LX1,y1,t,COL_FILL,True,6.9)
for i in range(4):
    line(212,L[i][1],212,L[i+1][0],arrow=True)

# ============ 右列 ============
RX0,RX1 = 951,1069
R = [(235,283,"文献研究法"),(534,582,"实地调研法"),(807,855,"问卷调查法"),
     (1053,1101,"数据分析法"),(1278,1327,"归纳总结法")]
for (y0,y1,t) in R:
    box(RX0,y0,RX1,y1,t,COL_FILL,True,6.9)
for i in range(4):
    line(1010,R[i][1],1010,R[i+1][0])

# 中列 -> 右列 箭头
for (y0,y1,_) in R:
    line(909,(y0+y1)/2,951,(y0+y1)/2,arrow=True)

# ============ 区块容器 ============
MX0,MX1 = 313,909
rect(313,120,909,398,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")
rect(313,425,909,690,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")
rect(313,710,909,946,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")
rect(313,984,909,1180,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")
rect(313,1203,909,1401,f"dashed,dash pattern=on 1.7pt off 1.3pt,draw={LINE},line width=0.7pt")

# 区块间空心箭头
hollow_down(611,400,425)
hollow_down(611,691,712)
hollow_down(611,951,974)
hollow_down(611,1181,1203)

# ============ 区块 1 ============
box(314,126,908,172,"本项目研究的意义及在国内外的研究现状与存在的问题",HDR_FILL,True,6.7)
line(611,172,611,187)
line(370,187,852,187)
for cx in (370,491,611,732,852):
    line(cx,187,cx,204)
r1 = [(313,427,"研究背景"),(434,548,"研究意义"),(554,668,"相关概念"),
      (674,788,"国内外研究\\\\进展"),(795,909,"存在的问题")]
for (x0,x1,t) in r1: box(x0,204,x1,267,t)
for cx in (370,491,611,732,852):
    line(cx,267,cx,279)
line(371,279,853,279)
line(611,279,611,299)
line(385,299,838,299)
for cx in (384,535,685,837):
    line(cx,299,cx,312)
r2 = [(313,456,"城市扩张导致\\\\XXX问题严重"),(464,606,"XXXXXX问题\\\\影响多维感知"),
      (614,757,"XXX对城市绿\\\\地的健康需求"),(766,909,"XXX的恢复性\\\\效应仍需提升")]
for (x0,x1,t) in r2: box(x0,312,x1,389,t)

# ============ 区块 2 ============
box(314,440,908,485,"XXXXXX对街旁绿地声视热环境感知的影响",HDR_FILL,True,6.7)
line(611,485,611,500)
line(460,500,761,500)
for cx in (460,761): line(cx,500,cx,514)
box(314,514,607,554,"实地测量"); box(614,514,908,554,"行为观察")
for cx in (460,761): line(cx,554,cx,572)
line(363,572,559,572); line(686,572,839,572)
for cx in (363,461,559,686,839): line(cx,572,cx,590)
r2b = [(318,408,"噪声水\\\\平监测"),(416,506,"XXX参\\\\数测量"),
       (514,603,"视觉环\\\\境特征\\\\记录"),(616,754,"记录绿地使用\\\\行为"),
       (769,907,"记录\\\\XXXXXXXX分\\\\布")]
for (x0,x1,t) in r2b: box(x0,590,x1,677,t)

# ============ 区块 3 ============
box(314,722,908,766,"XXXXXXXXX对街旁绿地恢复性效应的影响分析",HDR_FILL,True,6.7)
box(318,782,370,935,"设\\\\计\\\\调\\\\查\\\\问\\\\卷")
line(370,858,383,858)
line(383,803,383,913)
for cy in (803,858,913): line(383,cy,395,cy)
box(395,782,647,827,"声、视、热环境感知评分")
box(395,837,647,881,"恢复性环境量表")
box(395,891,647,935,"人口统计学信息")
for cy in (803,858,913): line(647,cy,660,cy)
line(660,803,660,913)
line(660,858,674,858)
box(674,782,754,935,"实施问\\\\卷调查")
line(754,858,768,858)
line(768,815,768,901)
for cy in (815,901): line(768,cy,781,cy)
box(781,781,909,850,"现场发放与\\\\回收问卷")
box(781,867,909,936,"获取主观评\\\\价数据")

# ============ 区块 4 ============
box(314,984,908,1029,"XXXXXXXXXXXXXXXX数据采集与实测样本匹配",HDR_FILL,True,6.7)
rect(320,1040,792,1168,f"dotted,line cap=round,dash pattern=on 0.6pt off 1.6pt,draw={LINE},line width=1pt")
box(324,1050,790,1092,"同步生理监测")
line(557,1092,557,1107)
line(436,1107,681,1107)
for cx in (436,680): line(cx,1107,cx,1116)
box(324,1116,548,1160,"心率监测")
box(568,1116,792,1160,"肌电活动监测")
box(852,1040,908,1168,"数\\\\据\\\\整\\\\理")
line(792,1104,852,1104,arrow=True)

# ============ 区块 5 ============
box(313,1213,909,1257,"基于模型运算结果解析噪声 — 生理响应 — 恢复效应的内在作用机制",HDR_FILL,True,6.7)
box(313,1269,586,1313,"总结关键路径")
box(636,1269,909,1313,"提出设计策略")
for cx in (449,772): line(cx,1313,cx,1329)
line(449,1329,772,1329)
line(611,1329,611,1345,arrow=True)
box(313,1345,909,1389,"为城市街旁绿地的恢复性提升和交通噪声治理提供科学依据",HDR_FILL,True,6.9)

tex = r"""% !TEX program = xelatex
% 研究框架图 —— TikZ 矢量图
% 坐标系：x=1/72cm, y=-1/72cm，1 单位 = 1 栅格
% y 取负：向下为正
\documentclass[tikz,border=6pt]{standalone}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}
\setmainfont{Microsoft YaHei}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,positioning}
\xeCJKsetup{CJKecglue={}}
\definecolor{cbox}{HTML}{FFFFFF}
\definecolor{ccol}{HTML}{F2F2F2}
\definecolor{chdr}{HTML}{D9D9D9}
\definecolor{ctop}{HTML}{BFBFBF}
\definecolor{cline}{HTML}{4D4D4D}
\begin{document}
\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm,
  box/.style={draw=cline,inner sep=1pt,outer sep=0pt,align=center,
              execute at begin node={\setlength{\baselineskip}{9.2pt}}}]
""" + "\n".join(out) + r"""
\end{tikzpicture}
\end{document}
"""

open("fig.tex","w",encoding="utf-8").write(tex)
print("written", len(tex))
