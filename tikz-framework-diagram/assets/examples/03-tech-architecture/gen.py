# -*- coding: utf-8 -*-
"""图3 流程图生成器：坐标用原图像素，1px = 1/72cm = 0.3937pt"""

PX2PT = 72/2.54/72     # = 0.3937 (1 unit = 1/72cm, 1pt=1/72in)
def pt(px): return px*PX2PT

out = []
def w(s): out.append(s)
LW = 0.7

def node(cx,cy,wcm,hcm,text,fs=8.2,lead=None,style="",bold=False,align=True):
    if lead is None: lead = fs*1.42
    b = r"\bfseries " if bold else ""
    al = "align=center," if align else ""
    w(f"\\node[{al}inner sep=0pt,outer sep=0pt,font=\\fontsize{{{fs}}}{{{lead:.2f}}}\\selectfont,{style}] "
      f"at ({cx:.1f},{cy:.1f}) {{{b}{text}}};")


def mlines(cx,cy,lines,fs=8.2,pitch=30.0):
    n=len(lines)
    for i,t in enumerate(lines):
        y=cy+(i-(n-1)/2.0)*pitch
        w(f"\\node[inner sep=0pt,outer sep=0pt,font=\\fontsize{{{fs}}}{{{pt(pitch):.2f}}}\\selectfont] at ({cx:.1f},{y:.1f}) {{{t}}};")

def chars_at(cx,yfirst,pitch,text,fs=8.2):
    for i,ch in enumerate(text):
        y=yfirst+pitch*i
        w(f"\\node[inner sep=0pt,outer sep=0pt,font=\\fontsize{{{fs}}}{{10}}\\selectfont] at ({cx:.1f},{y:.1f}) {{{ch}}};")

def chars(cx,y0,y1,text,fs=8.2):
    n=len(text); pitch=(y1-y0-26)/n
    for i,ch in enumerate(text):
        y=y0+13+pitch*(i+0.5)
        w(f"\\node[inner sep=0pt,outer sep=0pt,font=\\fontsize{{{fs}}}{{10}}\\selectfont] at ({cx:.1f},{y:.1f}) {{{ch}}};")

def box(x0,y0,x1,y1,text="",fs=8.2,r=0,lw=LW,lead=None):
    st=f"draw=black,line width={lw}pt,fill=white"
    if r: st+=f",rounded corners={r/72:.4f}cm"
    if text:
        w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")
        if isinstance(text,list): mlines((x0+x1)/2,(y0+y1)/2,text,fs,30)
        else: node((x0+x1)/2,(y0+y1)/2,x1-x0,y1-y0,text,fs,lead)
    else:
        w(f"\\draw[{st}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")

def line(x0,y0,x1,y1):
    w(f"\\draw[line width={LW}pt] ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y1:.1f});")

def dashed(x0,y0,x1,y1):
    w(f"\\draw[dashed,dash pattern=on 1.9pt off 1.5pt,line width=0.7pt] "
      f"({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});")

def varrow(cx,y0,y1,sw,hw,hh):
    yh=y1-hh
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({cx-sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{y0:.1f}) -- ({cx+sw/2:.1f},{yh:.1f}) -- "
      f"({cx+hw/2:.1f},{yh:.1f}) -- ({cx:.1f},{y1:.1f}) -- ({cx-hw/2:.1f},{yh:.1f}) -- "
      f"({cx-sw/2:.1f},{yh:.1f}) -- cycle;")

def label_box(x0,y0,x1,y1,text,p0,pc):
    cy=(y0+y1)/2
    w(f"\\draw[line width={LW}pt] ({x0:.1f},{y1:.1f}) -- ({x0:.1f},{y0:.1f}) -- ({x1:.1f},{y0:.1f}) -- ({x1:.1f},{cy-12:.1f});")
    w(f"\\draw[line width={LW}pt,fill=white] ({x1:.1f},{cy-12:.1f}) -- ({x1+11:.1f},{cy-12:.1f}) -- "
      f"({x1+11:.1f},{cy-21:.1f}) -- (252,{cy:.1f}) -- ({x1+11:.1f},{cy+21:.1f}) -- "
      f"({x1+11:.1f},{cy+12:.1f}) -- ({x1:.1f},{cy+12:.1f});")
    w(f"\\draw[line width={LW}pt] ({x1:.1f},{cy+12:.1f}) -- ({x1:.1f},{y1:.1f}) -- ({x0:.1f},{y1:.1f});")
    chars_at((x0+x1)/2,p0,pc,text)

def cylinder(cx,y0,y1,rx,ry,text):
    k=0.5523*ry
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] "
      f"({cx-rx:.1f},{y0:.1f}) -- ({cx-rx:.1f},{y1:.1f}) "
      f".. controls ({cx-rx:.1f},{y1+k:.1f}) and ({cx+rx:.1f},{y1+k:.1f}) .. ({cx+rx:.1f},{y1:.1f}) "
      f"-- ({cx+rx:.1f},{y0:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] ({cx:.1f},{y0:.1f}) ellipse ({rx:.1f} and {ry:.1f});")
    node(cx,(y0+y1)/2+2,0,0,text,8.2)

def vbox(x0,y0,x1,y1,text):
    box(x0,y0,x1,y1,"")
    n=len(text); pitch=32.0 if n==5 else 25.6
    yfirst=y0+((y1-y0)-(n-1)*pitch)/2.0
    chars_at((x0+x1)/2,yfirst,pitch,text)

def box3d(x0,x1,ytop,ybot,dx,dy,title,body):
    w(f"\\fill[fill=white,draw=black,line width={LW}pt] ({x0:.1f},{ytop:.1f}) -- ({x0+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1+dx:.1f},{ytop-dy:.1f}) -- ({x1:.1f},{ytop:.1f}) -- cycle;")
    w(f"\\fill[fill=cfold,draw=black,line width={LW}pt] ({x1:.1f},{ytop:.1f}) -- ({x1+dx:.1f},{ytop-dy:.1f}) -- "
      f"({x1+dx:.1f},{ybot-dy:.1f}) -- ({x1:.1f},{ybot:.1f}) -- cycle;")
    w(f"\\draw[fill=white,draw=black,line width={LW}pt] ({x0:.1f},{ytop:.1f}) rectangle ({x1:.1f},{ybot:.1f});")
    node((x0+x1)/2+dx/2+5,ytop-dy/2,0,0,title,9.7,lead=12.0,style="",bold=True)
    mlines((x0+x1)/2,(ytop+ybot)/2+3,body,8.2,30)

# ================= 容器 =================
for (a,b) in [(38,366),(400,599),(634,895),(928,1206),(1240,1417)]:
    dashed(141,a,1076,b)

# ================= 左侧标签 =================
for (y0,y1,t,p0,pc) in [(52,357,"数据源头归集与预处理",88.5,25.7),(413,582,"数据集成型",446.5,20.2),
                  (647,880,"模型搭建与训练",686.5,30.8),(943,1189,"模型优化",1028.5,19.0),
                  (1251,1406,"成果落地",1290.5,25.3)]:
    label_box(156,y0,217,y1,t,p0,pc)

# ================= 区块1 =================
CX=[363.5,564,767.5,971.5]
for cx,t in zip(CX,["工况实测数据库","仿真样本数据库","文献标准数据库","故障案例数据库"]):
    cylinder(cx,61,128,90.5,9,t)
line(363.5,149,971.5,149)
for cx in CX: line(cx,137,cx,149)
line(476.5,149,476.5,169); line(879.5,149,879.5,169)
for (bx0,bx1,px0,px1,ttl,body) in [
    (284,647,360,593,"多源数据清洗处理",["缺失值填充、异常值剔除、","数据降噪、归一化归一处理"]),
    (695,1053,763,996,"数据特征标注划分",["样本标签标定、数据集分层、","训练 / 验证 / 测试集拆分"])]:
    box(bx0,190,bx1,350,"",r=20)
    box(px0,169,px1,228,ttl,8.6,r=29.5)
    mlines((bx0+bx1)/2,276,body,8.2,30)
varrow(605,368,400,39,78,15)

# ================= 区块2 =================
for (x0,x1,t,b) in [(273,512,"结构化数据集构建",["整理规整原始数据，","划分训练 / 验证 /","测试集"]),
                    (530,769,"特征库矩阵封装",["把提取的各类特征封","装为矩阵格式，适配","模型输入计算"]),
                    (786,1024,"数据脱敏与格式适配",["去除涉密敏感信息、","统一文件格式"])]:
    box3d(x0,x1,456,582,42,42,t,b)
varrow(605,602,634,39,78,15)

# ================= 区块3 =================
box(273,652,393,749,["模型输入","模块"],8.2,r=10)
box(273,783,393,880,["参数配置","模块"],8.2,r=10)
line(333,749,333,783)
line(393,700,414,700); line(414,675,414,728)
line(414,674,435,674); line(414,727,435,727)
line(393,831,414,831); line(414,805,414,859)
line(414,805,435,805); line(414,857,435,857)
for (y0,y1,t) in [(652,697,"特征提取分支1"),(705,750,"特征提取分支2"),
                  (783,828,"超参初始化设定"),(835,880,"训练策略调控")]:
    box(435,y0,673,y1,t)
for cy in (674,727,805,857): line(673,cy,697,cy)
line(697,675,697,859); line(697,766,724,766)
box(724,675,872,858,["核心算法模","型训练"],8.2)
w(f"\\draw[fill=white,draw=black,line width={LW}pt] (883,760) -- (907,760) -- (907,744) -- (919,768) -- "
  f"(907,792) -- (907,776) -- (883,776) -- (883,792) -- (871,768) -- (883,744) -- cycle;")
box(918,675,1066,858,["模型权重文","件与推理接","口"],8.2)
varrow(605,897,928,39,78,15)

# ================= 区块4 =================
vbox(273,943,322,1107,"模型迭代优化")
for cy in (973,1025,1077): line(322,cy,339,cy)
line(339,973,339,1079)
for (y0,y1,t) in [(950,995,"精度优化"),(1003,1047,"收敛提速"),(1055,1100,"鲁棒性增强")]:
    box(357,y0,595,y1,t)
for cy in (973,1025,1077): line(595,cy,611,cy)
line(611,973,611,1079); line(611,1025,629,1025)
vbox(629,943,677,1107,"模型性能评估")
varrow(476,1106,1140,30,61,18)
box(273,1147,678,1189,"模型轻量化与算法固化")
box(784,943,996,995,"系统总体架构设计",8.2,r=10)
for (x0,x1,t) in [(714,762,"人机交互界面"),(772,820,"数据通讯模块"),
                  (831,879,"采集驱动模块"),(890,939,"预警判别模块"),
                  (950,999,"存储管理模块"),(1011,1059,"输出执行模块")]:
    vbox(x0,1025,x1,1190,t)
    line(890,995,(x0+x1)/2,1025)
varrow(605,1209,1240,39,78,15)

# ================= 区块5 =================
box(496,1251,844,1303,"系统集成联调与整体验证",8.2,r=10)
line(670,1303,670,1326)
line(357.5,1326,969.5,1326)
for cx in (357.5,562,768,969.5): line(cx,1326,cx,1349)
for (x0,x1,t) in [(267,448,"仿真试验验证"),(471,653,"实物样机测试"),
                  (677,859,"工程现场试运行"),(879,1060,"成果总结")]:
    box(x0,1349,x1,1406,t)

tex = r"""% !TEX program = xelatex
% 流程图 TikZ 矢量复刻（水印已去除）；坐标 = 原图像素，1px = 1/72cm
\documentclass[tikz,border=6pt]{standalone}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\usepackage{tikz}
\definecolor{cfold}{HTML}{CBCBCB}
\xeCJKsetup{CJKecglue={\hskip 0pt}}
\begin{document}
\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]
""" + "\n".join(out) + r"""
\end{tikzpicture}
\end{document}
"""
open("fig.tex","w",encoding="utf-8").write(tex)
print("ok")
