# 05 工程配置

## 1. 文档骨架

```latex
% !TEX program = xelatex
\documentclass[tikz,border=6pt]{standalone}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\setmainfont{Microsoft YaHei}[BoldFont={Microsoft YaHei Bold}]
\xeCJKsetup{CJKecglue={}}          % 去掉"汉字+数字"之间的自动空隙
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,positioning}
\definecolor{cfold}{HTML}{CBCBCB}  % HTML 颜色必须先 definecolor
\begin{document}
\begin{tikzpicture}[x=0.0138889cm,y=-0.0138889cm]
  \input{body}
\end{tikzpicture}
\end{document}
```

- 用 `standalone` 而不是 article：版面自动收缩到图形包围盒，插进正文时尺寸可控。
- 字体名在 Windows 上是 `Microsoft YaHei`；黑体用 `SimHei`，宋体用 `SimSun`。
- **必须显式给 BoldFont**，否则 `\bfseries` 会报 Undefined control sequence。

## 2. 单位：整个方法的地基

```latex
x=0.0138889cm, y=-0.0138889cm
```

定义 **1 个栅格单位 = 1/72 cm**，`y` 取负（向下为正）。于是代码里写 `(313,204)`
就是"右 313 单位、下 204 单位"，一整张 A4 宽的图大约 1500 单位见方，粒度足够细，
又不必写小数。

- 好处：所有尺寸都能用整数思考（框宽 114、行高 45、圆角 10），改版时加减乘除不烧脑。
- **不要写成 `0.0352778cm`**——那是 1/72 英寸，会让整幅图放大 2.54 倍。

## 3. 字号与行距：栅格单位 → pt

绘图坐标和字体尺寸是两套单位，必须换算：

```
1 单位 = 1/72 cm ，1 pt = 1/72 inch = 2.54/72 cm
=> 1 单位 = 1/2.54 pt = 0.3937 pt
=> 字号(pt) = 字宽(单位) × 0.3937
```

**字号 = 汉字字宽**（1 em），所以按"字宽"查表最直接：

| 字宽 | 字号 | 典型用途 |
|---|---|---|
| 17 | 6.7 pt | 极密图正文 |
| 21 | 8.3 pt | 常规正文框 |
| 24–25 | 9.5 pt | 主流程框 |
| 28–30 | 11–12 pt | 大标题条 |

行距同理：想让行间留 30 单位 → `\fontsize{8.3}{11.8}`（30×0.3937≈11.8）。
**把栅格单位直接填进第二个参数是最常见的错误**，行距会放大 2.54 倍、文字全部飞出框外。

## 4. 线宽与线型

| 元素 | 线宽 | 说明 |
|---|---|---|
| 普通框线 | 0.55–0.7 pt | 约 1.5–2 单位 |
| 标题条 / 外框 | 0.8 pt | 拉开层次 |
| 虚线容器 | 0.7 pt | `dash pattern=on 1.7pt off 1.3pt` |
| 点线内框 | 1 pt + `line cap=round` | `dash pattern=on 0.6pt off 1.6pt` |

虚线密度按 4 单位实 / 3 单位空取 → `on 1.6pt off 1.2pt`（4×0.3937≈1.6）。
密度不对会产生"描边感"，一眼看出是软件拼的。

## 5. 颜色

- 纯黑白最安全，学术图基本只用灰阶。
- 只用令牌表那 5 档：`#FFFFFF` `#F2F2F2` `#D9D9D9` `#BFBFBF` `#CBCBCB`。
- `\definecolor{name}{HTML}{RRGGBB}` 之后用 `fill=name`。**`#` 不能直接出现在代码里**（是宏参数符）。
- 线条色不要用纯黑，`#4D4D4D` 更接近印刷灰线；文字用纯黑。

## 6. 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error fig.tex
```

- 必须 `xelatex`（fontspec + xeCJK）。
- 目标 PDF 被预览器占用时会报 `Error 1 (driver return code)`：改用 `-jobname=tmp` 输出到新文件，再覆盖。
- 每次改生成器后重新 `python gen.py && xelatex ...`，不要手改 `.tex`（会被下次生成覆盖）。
