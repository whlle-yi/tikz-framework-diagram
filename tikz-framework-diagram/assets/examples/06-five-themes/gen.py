#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""五个不同主题的版式测试：验证 tikz-framework-diagram 的骨架能否套住异构内容。

箭头通道按 01-style.md 预留：区块之间 78、标签栏到内容区 86。
    python gen.py && xelatex fig.tex
"""
import kit as K
from kit import (node, two, multiline, vtext, rect, dashed, label, cylinder,
                 card3d, pill, line, varrow, hvarrow, thin, dbl, fit, begin, end,
                 MONO_LINE, MONO_HEAD, w, vdbl, ARROW_GAP, CONTENT_X0)

CX0, CX1 = 30, 1010
LB0, LB1 = 42, 86
MID = (CX0 + CX1) / 2            # 520
GAP = ARROW_GAP                  # 区块间箭头通道 78


# ================================================================ T1 校园碳核算
def t1():
    begin()
    # 数据采集 30..330
    dashed(CX0, 30, CX1, 330)
    label(LB0, 44, LB1, 316, "数据采集")
    xs = [200, 390, 580, 770]
    for x, name in zip(xs, ["用电计量库", "燃气台账库", "交通出行库", "废弃物台账"]):
        cylinder(x + 90, 56, 146, 89, 9, name)
    line(xs[0] + 90, 170, xs[-1] + 90, 170)
    for x in xs:
        line(x + 90, 155, x + 90, 170)
    card3d(300, 860, 212, 300, 42, 42, "校园碳排放在线核算",
           ["范围一 直接排放 · 范围二 购入电力 · 范围三 价值链", "活动数据 × 排放因子 · 逐月滚动更新"])
    fit("数据采集", 47, 300, 30, 330)

    # 碳排核算 408..628（与上层间隔 78）
    dashed(CX0, 408, CX1, 628)
    label(LB0, 422, LB1, 614, "碳排核算")
    for x0, x1, t, s in [(170, 420, "范围一", "锅炉 · 公务车 · 逸散"),
                         (435, 685, "范围二", "外购电力 · 外购热力"),
                         (700, 950, "范围三", "通勤 · 采购 · 废弃物")]:
        rect(x0, 432, x1, 502, 10)
        two((x0 + x1) / 2, 467, t, s, 8.6, 6.4)
    rect(340, 532, 780, 592, 8)
    node(560, 562, "碳排放总量 · 强度 · 结构占比", 8.6, MONO_LINE, True)
    for cx in (295, 560, 825):
        line(cx, 502, cx, 522)
    line(295, 522, 825, 522)
    line(560, 522, 560, 532)
    fit("碳排核算", 432, 592, 408, 628)

    # 减排路径 706..894
    dashed(CX0, 706, CX1, 894)
    label(LB0, 720, LB1, 880, "减排路径")
    meas = ["照明与空调改造", "屋顶光伏建设", "绿色出行激励",
            "采购低碳电力", "食堂与废弃物减量", "碳汇与绿证抵消"]
    for i, m in enumerate(meas):
        col, row = i % 3, i // 3
        x0 = CONTENT_X0 + col * 265
        y0 = 734 + row * 75
        rect(x0, y0, x0 + 250, y0 + 55, 10)
        node(x0 + 125, y0 + 27, m, 8.3, MONO_LINE)
    fit("减排路径", 734, 864, 706, 894)

    # 三条区块箭头，整条落在 78 的通道里
    varrow(MID, 330, 330 + GAP)
    varrow(MID, 628, 628 + GAP)
    varrow(MID, 894, 894 + GAP)

    rect(CX0, 972, CX1, 1040, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 1006, "支撑校园碳排放年度核算、达峰路径推演与减排绩效考核", 9.2, "black", True)
    return end()


# ================================================================ T2 中药材追溯
def t2():
    begin()
    heads = [(130, 330, "追溯环节"), (350, 730, "关键控制点"), (750, 920, "检测与判定")]
    for x0, x1, t in heads:
        rect(x0, 30, x1, 80, 6, MONO_HEAD, MONO_LINE, 0.8)
        node((x0 + x1) / 2, 55, t, 8.8, MONO_LINE, True)

    rows = [("种植", "产地环境 · 种源鉴定", "土壤重金属检测"),
            ("采收", "采收期 · 初加工方式", "水分与灰分测定"),
            ("加工", "炮制工艺 · 辅料控制", "浸出物与含量测定"),
            ("仓储", "温湿度 · 虫霉防控", "黄曲霉毒素检测"),
            ("流通", "批次赋码 · 冷链衔接", "农药残留快检")]
    for i, (a, b, c) in enumerate(rows):
        y0 = 100 + i * 106               # 框高 68 + 细箭头 38
        rect(130, y0, 330, y0 + 68, 8)
        node(230, y0 + 34, a, 8.6, MONO_LINE, True)
        rect(350, y0, 730, y0 + 68, 8)
        node(540, y0 + 34, b, 8.3, MONO_LINE)
        rect(750, y0, 920, y0 + 68, 8)
        node(835, y0 + 34, c, 7.8, MONO_LINE)
        line(330, y0 + 34, 350, y0 + 34)
        line(730, y0 + 34, 750, y0 + 34)
        if i < 4:
            thin(230, y0 + 68, y0 + 106)

    rect(130, 640, 920, 700, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(525, 670, "一物一码 · 来源可查 · 去向可追 · 责任可究", 9.0, "black", True)
    for cx in (230, 540, 835):
        line(cx, 592, cx, 612)
    line(230, 612, 835, 612)
    line(525, 612, 525, 640)
    return end()


# ================================================================ T3 认知筛查
def t3():
    begin()
    dashed(CX0, 30, CX1, 590)
    label(LB0, 44, LB1, 576, "筛查流程")

    # 左：三类输入
    for i, (t, s) in enumerate([("量表测评", "MoCA · MMSE · 画钟"),
                                ("影像与语音", "海马体积 · 语速停顿"),
                                ("行为与生活", "步态 · 睡眠 · 用药")]):
        y0 = 70 + i * 140
        rect(200, y0, 450, y0 + 100, 10)
        two(325, y0 + 50, t, s, 8.6, 6.4)
        line(450, y0 + 50, 495, y0 + 50)

    # 中：融合引擎
    rect(495, 60, 765, 460, 14)
    node(630, 100, "多模态融合筛查模型", 9.4, MONO_LINE, True)
    for i, t in enumerate(["特征标准化与缺失补全", "时序 + 影像双通道编码",
                           "风险分层与可解释输出", "跨中心外部验证"]):
        rect(515, 140 + i * 74, 745, 140 + i * 74 + 54, 8)
        node(630, 167 + i * 74, t, 8.0, MONO_LINE)

    # 右：分级输出
    for i, (t, s) in enumerate([("低风险", "年度随访"), ("中风险", "专项复查"),
                                ("高风险", "转诊记忆门诊"), ("疑似", "影像与检验")]):
        y0 = 60 + i * 100
        rect(815, y0, 985, y0 + 80, 10)
        two(900, y0 + 40, t, s, 8.4, 6.4)
        line(765, y0 + 40, 815, y0 + 40)

    # 医生复核（双向）
    rect(495, 500, 765, 560, 10)
    node(630, 530, "医师复核与随访登记", 8.6, MONO_LINE, True)
    vdbl(630, 462, 498)
    fit("筛查流程", 60, 560, 30, 590)

    varrow(MID, 590, 590 + GAP)
    rect(CX0, 668, CX1, 736, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 702, "形成「社区初筛—医院复核—分级干预」的认知障碍早筛闭环", 9.0, "black", True)
    return end()


# ================================================================ T4 乡村物流
def t4():
    begin()
    dashed(CX0, 30, CX1, 700)
    label(LB0, 44, LB1, 686, "网络优化")

    rect(420, 55, 680, 115, 10, MONO_HEAD, MONO_LINE, 0.8)
    node(550, 85, "县域物流网络优化", 9.0, MONO_LINE, True)

    hubs = ["县级分拨中心", "乡镇中转站", "村级服务站", "末端配送"]
    centers = [280, 470, 660, 850]
    line(550, 115, 550, 150)
    line(centers[0], 150, centers[-1], 150)
    for cx, h in zip(centers, hubs):
        line(cx, 150, cx, 172)
        rect(cx - 90, 172, cx + 90, 232, 10)
        node(cx, 202, h, 8.4, MONO_LINE, True)

    subs = [["选址与容量", "线路排班", "共同配送"],
            ["库存与周转", "冷链接入", "代收代发"],
            ["订单聚合", "车货匹配", "时效监控"],
            ["路径规划", "成本核算", "签收溯源"]]
    for cx, group in zip(centers, subs):
        for j, s in enumerate(group):
            y0 = 262 + j * 92           # 框高 58 + 细箭头 34
            rect(cx - 80, y0, cx + 80, y0 + 58, 8)
            node(cx, y0 + 29, s, 7.8, MONO_LINE)
            if j == 0:
                line(cx, 232, cx, 262)
            else:
                thin(cx, y0 - 34, y0)
    fit("网络优化", 55, 690, 30, 700)

    rect(200, 630, 930, 690, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(565, 660, "时效提升 · 成本下降 · 覆盖率扩展 · 冷链损耗降低", 9.0, "black", True)
    for cx in centers:
        line(cx, 504, cx, 610)
    line(centers[0], 610, centers[-1], 610)
    line(550, 610, 550, 630)
    return end()


# ================================================================ T5 电池梯次利用
def t5():
    begin()
    dashed(CX0, 30, CX1, 360)
    label(LB0, 44, LB1, 346, "闭环流程")

    segs = [("生产制造", ["电芯一致性", "电池护照"]),
            ("整车使用", ["工况与快充", "健康度衰减"]),
            ("回收拆解", ["残值评估", "安全放电"]),
            ("梯次利用", ["储能配组", "模块重构"]),
            ("再生冶练", ["湿法提锂", "材料回用"])]
    xs = [170, 340, 510, 680, 850]
    W = 100                              # 组间通道 70，容得下横向块箭头
    for i, ((name, subs), x0) in enumerate(zip(segs, xs)):
        rect(x0, 60, x0 + W, 120, 10, MONO_HEAD, MONO_LINE, 0.8)
        node(x0 + W / 2, 90, name, 8.6, MONO_LINE, True)
        for j, s in enumerate(subs):
            y0 = 140 + j * 78
            rect(x0, y0, x0 + W, y0 + 62, 8)
            node(x0 + W / 2, y0 + 31, s, 7.8, MONO_LINE)
            line(x0 + W / 2, 120 if j == 0 else y0 - 16, x0 + W / 2, y0)
        if i < 4:
            hvarrow(90, x0 + W, xs[i + 1])

    # 闭环回流
    yb = 330
    xr, xl = xs[-1] + W / 2, xs[0] + W / 2
    w(f"\\draw[dashed,dash pattern=on 1.8pt off 1.6pt,line width={K.LW}pt,draw={MONO_LINE},"
      f"-{{Latex[length=1.5mm,width=1.0mm]}}] ({xr},{280}) -- ({xr},{yb}) -- ({xl},{yb}) -- ({xl},282);")
    node(560, 310, "退役电池逆向回收与再生材料回流", 7.8, MONO_LINE)
    fit("闭环流程", 60, 330, 30, 360)

    varrow(MID, 360, 360 + GAP)
    rect(CX0, 438, CX1, 506, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 472, "满足溯源、安全与碳足迹核算要求，形成「生产—使用—回收—再生」闭环", 8.8, "black", True)
    return end()


PAGES = [("校园碳排放核算与减排路径", t1),
         ("中药材全链条质量追溯体系", t2),
         ("老年认知障碍早期筛查流程", t3),
         ("乡村电商物流网络优化框架", t4),
         ("退役动力电池梯次利用闭环", t5)]

# 每页按内容紧裁：preview 的 tightpage 让五张图各自成页，不留大片空白
HEAD = r"""% !TEX program = xelatex
\documentclass[10pt]{article}
\usepackage[paperwidth=16cm,paperheight=24cm,margin=1cm]{geometry}
\usepackage[active,tightpage]{preview}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\definecolor{monoLine}{HTML}{4D4D4D}
\definecolor{monoHead}{HTML}{D9D9D9}
\definecolor{monoSide}{HTML}{CBCBCB}
\setlength{\parindent}{0pt}
\newenvironment{myfig}{\begin{minipage}{14cm}\centering}{\end{minipage}}
\PreviewEnvironment{myfig}
\pagestyle{empty}
\begin{document}
"""
TAIL = "\n\\end{document}\n"

parts = [HEAD]
for title, fn in PAGES:
    body = fn()
    parts.append("\\begin{myfig}\n{\\large\\bfseries %s}\\par\\vspace{4pt}\n" % title)
    parts.append(body + "\n\\end{myfig}\n")
parts.append(TAIL)

open("fig.tex", "w", encoding="utf-8").write("".join(parts))
print("written fig.tex with %d tightly-cropped pages" % len(PAGES))
