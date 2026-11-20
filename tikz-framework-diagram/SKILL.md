---
name: tikz-framework-diagram
description: This skill should be used when the user asks to draw, design or produce a Chinese academic-style framework figure with TikZ / LaTeX — e.g. "画一个技术路线图", "做一张研究框架图", "帮我画系统架构图", "画个方法流程图（论文用）", "draw a research framework diagram in TikZ", "make an architecture diagram for my paper". Encodes a fixed visual language for journal figures — white boxes on a strict grid, gray tier headers, dashed group containers, vertical Chinese labels, outline block arrows and orthogonal tree connectors — so output looks like a professionally typeset figure rather than a default TikZ sketch.
agent_created: true
---

# 中文学术框架图 / 技术路线图（TikZ）

按一套固定的视觉语言，从"这张图要表达什么"直接产出论文可用的 TikZ 插图：
给定内容与逻辑关系，画出符合这套风格的图。

## 何时使用

- 要画：研究框架图、技术路线图、系统架构图、方法流程图、指标体系图
- 要求输出 LaTeX / TikZ 矢量、黑白灰阶、可印刷
- 中文标注（或中英混排）

不适用：自由曲线 / 手绘风格、需要阴影渐变的效果图、数据可视化（那该用 pgfplots）。

## 三条原则

1. **结构先于装饰**。先定层级（几层 / 每层几个 / 怎么连），再算坐标。结构没想清楚就开始摆框，必然反复调位置。
2. **网格一致**。同类元素同高、同间距；全图字号只有 3 级；容器的内边距只有一个值。
3. **留白均匀**。拥挤是这类图最常见的失败原因——宁可缩字号、拆图，也不要让框贴边。

## 工作流

### 1. 定版式
读 [references/02-layouts.md](references/02-layouts.md)，从五种骨架里选一个：
单列纵向流程 / 三列框架（步骤-内容-方法）/ 分层架构（层+左标签）/ 树形分解 / 矩阵对照。
选完先写一份"层级清单"：几行、每行几个、谁连谁。

### 2. 套风格令牌
先定单色还是彩色：

- **单色（默认）** —— 读 [references/01-style.md](references/01-style.md)，取字号、灰阶、线宽、圆角、间距、箭头尺寸。
  黑白印刷稿一律用这套。
- **彩色** —— 读 [references/09-color.md](references/09-color.md)，几何与字号仍用 01，只把灰阶换成"三色系 + 中性灰"的深浅两档。

两套令牌都提炼自已发表的期刊插图，直接用，不要重新发明。

### 3. 选图元
读 [references/03-shapes.md](references/03-shapes.md)：矩形、圆角、胶囊、圆柱、立体卡片、块箭头、树形支架、虚线容器、共边标签框。
文字排版（多行、竖排、字距）见 [references/04-text.md](references/04-text.md)。

### 4. 写生成器
复制 [scripts/scaffold.py](scripts/scaffold.py) 为 `gen.py`，把层级清单填成数据表，逐块输出。
不要手写 `.tex`——几十个节点手写必错，且改一次要改十处。

### 5. 编译
读 [references/05-tex-setup.md](references/05-tex-setup.md)：`xelatex` + `xeCJK` + 中文字体。
**字号与坐标是两套单位**（1 单位 = 1/72cm，1pt = 1/72in），换算是这一步最容易错的地方。

### 6. 自检 → 交付
过一遍 [references/06-checklist.md](references/06-checklist.md)：对齐、字号层级、留白、箭头、文字溢出、线型。
交付 `.tex` + `.pdf` + 预览图；说明版面尺寸与如何插入正文。

## 参考成品

`assets/examples/` 下有五张按本风格完成的图，可直接编译，也是参数取法的样例：

| 目录 | 版式 | 亮点 |
|---|---|---|
| `01-top-level-plan` | 单列纵向 + 左侧三段大箭头 | 最小可用样例 |
| `02-research-framework` | 三列框架（步骤 / 内容 / 方法） | 5 个虚线单元、树形支架、竖排标签 |
| `03-tech-architecture` | 分层架构 | 圆柱、立体卡片、胶囊标题、双向箭头 |
| `04-color-scheme` | 分层架构（彩色版） | 三色系色板、浅填充 + 深描边、细箭头 |
| `05-dual-palette` | 四层容器（多图元） | 圆柱 + 立体卡片 + 胶囊 + 块箭头 + 树形支架；单色与彩色两版合并在一个 LaTeX 文件 |

改版式前先看这几张，改完对照着看有没有跑偏。1–3 是单色，4 是彩色。

## 出问题先查

[references/08-pitfalls.md](references/08-pitfalls.md)：15 条按"症状 → 原因 → 修法"排的踩坑。
"文字溢出框外 / 箭头只剩个头 / 框被斜线穿过 / 整块看着歪"这几类，那里都有现成答案。
