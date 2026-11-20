#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""五个不同主题的版式测试：验证 tikz-framework-diagram 的骨架能否套住异构内容。

    python gen.py && xelatex fig.tex
"""
import kit as K
from kit import (node, two, multiline, vtext, rect, dashed, label, cylinder,
                 card3d, pill, line, varrow, hvarrow, thin, dbl, fit, begin, end,
                 MONO_LINE, MONO_HEAD, w, vdbl)

CX0, CX1 = 30, 970
LB0, LB1 = 44, 102
MID = 500


# ================================================================ T1 校园碳核算
def t1():
    begin()
    # 数据采集
    dashed(CX0, 30, CX1, 330)
    label(LB0, 44, LB1, 316, "数据采集")
    xs = [160, 350, 540, 730]
    for x, name in zip(xs, ["用电计量库", "燃气台账库", "交通出行库", "废弃物台账"]):
        cylinder(x + 90, 56, 146, 89, 9, name)
    line(xs[0] + 90, 170, xs[-1] + 90, 170)
    for x in xs:
        line(x + 90, 155, x + 90, 170)
    card3d(260, 820, 212, 300, 42, 42, "校园碳排放在线核算",
           ["范围一 直接排放 · 范围二 购入电力 · 范围三 价值链", "活动数据 × 排放因子 · 逐月滚动更新"])
    fit("数据采集", 47, 300, 30, 330)

    # 碳排核算
    dashed(CX0, 370, CX1, 590)
    label(LB0, 384, LB1, 576, "碳排核算")
    for x0, x1, t, s in [(130, 380, "范围一", "锅炉 · 公务车 · 逸散"),
                         (395, 645, "范围二", "外购电力 · 外购热力"),
                         (660, 910, "范围三", "通勤 · 采购 · 废弃物")]:
        rect(x0, 400, x1, 470, 10)
        two((x0 + x1) / 2, 435, t, s, 8.6, 6.4)
    rect(300, 500, 740, 560, 8)
    node(520, 530, "碳排放总量 · 强度 · 结构占比", 8.6, MONO_LINE, True)
    for cx in (255, 520, 785):
        line(cx, 470, cx, 490)
    line(255, 490, 785, 490)
    line(520, 490, 520, 500)
    fit("碳排核算", 400, 560, 370, 590)

    # 减排路径
    dashed(CX0, 630, CX1, 830)
    label(LB0, 644, LB1, 816, "减排路径")
    meas = ["照明与空调改造", "屋顶光伏建设", "绿色出行激励",
            "采购低碳电力", "食堂与废弃物减量", "碳汇与绿证抵消"]
    for i, m in enumerate(meas):
        col, row = i % 3, i // 3
        x0 = 130 + col * 265
        y0 = 670 + row * 75
        rect(x0, y0, x0 + 250, y0 + 55, 10)
        node(x0 + 125, y0 + 27, m, 8.3, MONO_LINE)
    fit("减排路径", 670, 800, 630, 830)

    varrow(MID, 334, 366)
    varrow(MID, 594, 626)
    varrow(MID, 834, 866)

    rect(CX0, 870, CX1, 938, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 904, "支撑校园碳排放年度核算、达峰路径推演与减排绩效考核", 9.2, "black", True)
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
        y0 = 100 + i * 82
        rect(130, y0, 330, y0 + 68, 8)
        node(230, y0 + 34, a, 8.6, MONO_LINE, True)
        rect(350, y0, 730, y0 + 68, 8)
        node(540, y0 + 34, b, 8.3, MONO_LINE)
        rect(750, y0, 920, y0 + 68, 8)
        node(835, y0 + 34, c, 7.8, MONO_LINE)
        line(330, y0 + 34, 350, y0 + 34)
        line(730, y0 + 34, 750, y0 + 34)
        if i < 4:
            thin(230, y0 + 68, y0 + 82)

    rect(130, 540, 920, 600, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(525, 570, "一物一码 · 来源可查 · 去向可追 · 责任可究", 9.0, "black", True)
    for cx in (230, 540, 835):
        line(cx, 508, cx, 524)
    line(230, 524, 835, 524)
    line(525, 524, 525, 540)
    return end()


# ================================================================ T3 认知筛查
def t3():
    begin()
    dashed(CX0, 30, CX1, 585)
    label(LB0, 44, LB1, 571, "筛查流程")

    # 左：三类输入
    for i, (t, s) in enumerate([("量表测评", "MoCA · MMSE · 画钟"),
                                ("影像与语音", "海马体积 · 语速停顿"),
                                ("行为与生活", "步态 · 睡眠 · 用药")]):
        y0 = 70 + i * 140
        rect(130, y0, 380, y0 + 100, 10)
        two(255, y0 + 50, t, s, 8.6, 6.4)
        line(380, y0 + 50, 430, y0 + 50)

    # 中：融合引擎
    rect(430, 60, 700, 460, 14)
    node(565, 100, "多模态融合筛查模型", 9.4, MONO_LINE, True)
    for i, t in enumerate(["特征标准化与缺失补全", "时序 + 影像双通道编码",
                           "风险分层与可解释输出", "跨中心外部验证"]):
        rect(450, 140 + i * 74, 680, 140 + i * 74 + 54, 8)
        node(565, 167 + i * 74, t, 8.0, MONO_LINE)

    # 右：分级输出
    for i, (t, s) in enumerate([("低风险", "年度随访"), ("中风险", "专项复查"),
                                ("高风险", "转诊记忆门诊"), ("疑似", "影像与检验" )]):
        y0 = 60 + i * 100
        rect(750, y0, 920, y0 + 80, 10)
        two(835, y0 + 40, t, s, 8.4, 6.4)
        line(700, y0 + 40, 750, y0 + 40)

    # 医生复核（双向）
    rect(430, 495, 700, 555, 10)
    node(565, 525, "医师复核与随访登记", 8.6, MONO_LINE, True)
    vdbl(565, 462, 493)
    fit("筛查流程", 60, 555, 30, 585)

    varrow(MID, 589, 621)
    rect(CX0, 625, CX1, 693, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 659, "形成「社区初筛—医院复核—分级干预」的认知障碍早筛闭环", 9.0, "black", True)
    return end()


# ================================================================ T4 乡村物流
def t4():
    begin()
    dashed(CX0, 30, CX1, 700)
    label(LB0, 44, LB1, 686, "网络优化")

    rect(380, 55, 640, 115, 10, MONO_HEAD, MONO_LINE, 0.8)
    node(510, 85, "县域物流网络优化", 9.0, MONO_LINE, True)

    hubs = ["县级分拨中心", "乡镇中转站", "村级服务站", "末端配送"]
    centers = [230, 420, 610, 800]
    line(510, 115, 510, 150)
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
            y0 = 262 + j * 74
            rect(cx - 80, y0, cx + 80, y0 + 58, 8)
            node(cx, y0 + 29, s, 7.8, MONO_LINE)
            if j == 0:
                line(cx, 232, cx, 262)
            else:
                thin(cx, y0 - 16, y0)
    fit("网络优化", 55, 690, 30, 700)

    rect(130, 630, 890, 690, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(510, 660, "时效提升 · 成本下降 · 覆盖率扩展 · 冷链损耗降低", 9.0, "black", True)
    for cx in centers:
        line(cx, 486, cx, 610)
    line(centers[0], 610, centers[-1], 610)
    line(510, 610, 510, 630)
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
    xs = [160, 327, 494, 661, 828]
    W = 130
    for i, ((name, subs), x0) in enumerate(zip(segs, xs)):
        rect(x0, 60, x0 + W, 120, 10, MONO_HEAD, MONO_LINE, 0.8)
        node(x0 + W / 2, 90, name, 8.6, MONO_LINE, True)
        for j, s in enumerate(subs):
            y0 = 140 + j * 78
            rect(x0, y0, x0 + W, y0 + 62, 8)
            node(x0 + W / 2, y0 + 31, s, 7.8, MONO_LINE)
            line(x0 + W / 2, 120 if j == 0 else y0 - 16, x0 + W / 2, y0)
        if i < 4:
            hvarrow(90, x0 + W, xs[i + 1], sw=20, hw=36, hh=18)

    # 闭环回流
    yb = 330
    xr, xl = xs[-1] + W / 2, xs[0] + W / 2
    w(f"\\draw[dashed,dash pattern=on 1.8pt off 1.6pt,line width={K.LW}pt,draw={MONO_LINE},"
      f"-{{Latex[length=1.4mm,width=1.0mm]}}] ({xr},{280}) -- ({xr},{yb}) -- ({xl},{yb}) -- ({xl},282);")
    node(540, 310, "退役电池逆向回收与再生材料回流", 7.8, MONO_LINE)
    fit("闭环流程", 60, 330, 30, 360)

    varrow(MID, 364, 396, sw=30, hw=64, hh=14)
    rect(CX0, 400, CX1, 468, 8, MONO_HEAD, MONO_LINE, 0.8)
    node(MID, 434, "满足溯源、安全与碳足迹核算要求，形成「生产—使用—回收—再生」闭环", 8.8, "black", True)
    return end()


PAGES = [("校园碳排放核算与减排路径", t1),
         ("中药材全链条质量追溯体系", t2),
         ("老年认知障碍早期筛查流程", t3),
         ("乡村电商物流网络优化框架", t4),
         ("退役动力电池梯次利用闭环", t5)]

HEAD = r"""% !TEX program = xelatex
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
\setlength{\parindent}{0pt}
\pagestyle{empty}
\begin{document}
"""
TAIL = "\n\\end{document}\n"

parts = [HEAD]
for i, (title, fn) in enumerate(PAGES):
    body = fn()
    if i:
        parts.append("\n\\newpage\n")
    parts.append("\\begin{center}{\\large\\bfseries %s}\\end{center}\n\\vspace{2pt}\n" % title)
    parts.append("\\begin{center}\n" + body + "\n\\end{center}\n")
parts.append(TAIL)

open("fig.tex", "w", encoding="utf-8").write("".join(parts))
print("written fig.tex with %d pages" % len(PAGES))
