---
name: tikz-flowchart-replica
description: This skill should be used when the user asks to reproduce, replicate, clone or redraw a raster flowchart / architecture diagram / research-framework figure as a TikZ vector graphic — e.g. "用tikz复刻这个流程图", "把这张图做成矢量图", "照这个图重画一版", "redraw this diagram in LaTeX", "replicate this flowchart as vector". Targets Chinese academic / journal / technical diagrams such as research frameworks, technical roadmaps and system architectures, where box geometry, tree connectors, dashed group containers, 3D card shapes and vertical Chinese text must match the source image closely.
agent_created: true
---

# TikZ 流程图复刻

把位图流程图重绘为可编辑的 TikZ 矢量图，要求几何、连线、文字排版都与原图对齐。

## 四条铁律

1. **先量后画**。所有坐标来自像素测量，不靠目测。目测一定错在行高、间距和连线端点上。
2. **坐标即像素**。用 `x=0.0138889cm, y=-0.0138889cm`（1 单位 = 1px = 1/72cm），代码里直接写原图坐标，省掉全部换算。
3. **用脚本生成 TikZ，不手写**。几十个节点手写必错且改动成本极高。写 Python 生成器，数据表与渲染函数分离。
4. **必须叠色比对，直到线条重合**。渲染→叠色→找差异→改生成器→再比对，至少 3 轮。

## 工作流

### 第 0 步：分清"图"和"页面"
截图里的底色、页面留白、扫描阴影**不属于图**，一律不画。穿过图内部结构的虚线框、分组框属于图，要画。判据：该元素是否参与图的结构表达。

### 第 1 步：量取几何
读 `references/01-measure.md`，配合 `scripts/measure.py`：
- 水平/竖直线段清单 → 容器、行列、框边界
- 覆盖率扫描 → 每一排方框的左右边界
- 墨迹包围盒 → 文字尺寸与字号
- ASCII 结构图 → 快速看懂树形/支架/箭头

产出一份像素坐标表，作为后续唯一依据。

### 第 2 步：定工程配置
读 `references/02-tex-setup.md`：文档骨架、中文字体、颜色、**像素→pt 的字号/行距换算**（最容易错的一步）。

### 第 3 步：拆解图元
读 `references/03-shapes.md`：矩形、圆角、胶囊、圆柱、立体卡片、空心块箭头、树形支架、虚线容器、双向箭头的画法与参数。
中文竖排、多行文本、字距控制见 `references/04-text.md`。

### 第 4 步：写生成器
复制 `scripts/scaffold.py` 为工作脚本，把坐标表填进去逐块输出。
`assets/examples/` 下有三份已验证的完整成品，需要看代码风格与参数取法时再读。

### 第 5 步：编译出图
`xelatex` 编译。目标文件名被预览面板占用时无法覆盖，改用 `-jobname` 输出新名再改名。

### 第 6 步：叠色比对迭代
读 `references/05-verify.md`，跑 `scripts/overlay.py`。
**红=我的、蓝=原图、黑=重合**（别搞反，否则会把"我漏画"看成"我多画"）。逐轮消掉红蓝分离，直到只剩字体渲染的亚像素差。

- 整图至少完整比对 2 轮
- 局部（箭头、支架端点、竖排文字）放大到 1:1 再看
- 用户说"不对"时先叠色定位，不要靠猜

### 第 7 步：交付
`.tex` + `.pdf` + 预览图。说明仍存在的偏差，以及原图本身的错漏（错别字、错误换行）。

## 出问题先查

`references/06-pitfalls.md` 收录 15 条真实踩坑。遇到"文字溢出框外 / 箭头只剩头 / 框被斜线穿过 / 元素整体偏移"一类症状，先翻它。
