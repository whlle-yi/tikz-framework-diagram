# 03 图元库

所有坐标都用同一套栅格单位（1 单位 = 1/72 cm，详见 `05-tex-setup.md`）。函数可直接抄进生成器。

## 1. 矩形框

```python
def box(x0,y0,x1,y1,text="",fs=8.3,r=0):
    st=f"draw=black,line width=0.7pt,fill=white"
    if r: st+=f",rounded corners={r/72:.4f}cm"     # r 用像素给，内部转 cm
    # 宽度必须用 minimum width，不能用 text width，否则框会随文字收缩
```

**关键**：`minimum width/height` + `inner sep=0` 才能得到精确尺寸；
`text width` 会让框跟着文字变，位置就全乱了。

## 2. 圆角与胶囊

- 圆角矩形：`rounded corners=10/72cm`（10px 半径）
- 胶囊（两端全圆）：`rounded corners = 高度/2`
  例：`h=59px` → `rounded corners=29.5/72cm`

## 3. 虚线 / 点线容器

```latex
\draw[dashed,dash pattern=on 1.7pt off 1.3pt,line width=0.7pt] (x0,y0) rectangle (x1,y1);
\draw[dotted,line cap=round,dash pattern=on 0.6pt off 1.6pt] (x0,y0) rectangle (x1,y1);
```

**嵌套**：大方框里套小方框时，若两者边距只有 6~12 单位，看起来就是一条线。
照原样画即可，重合部分会自然加粗，视觉上是一致的。

## 4. 空心块箭头

块箭头是这类图最常用的连接件，比例靠代码卡死，不要凭手感给数。

```python
def check_arrow(L, sw, hw, hh, name="块箭头"):
    """L 总长 / sw 轴宽 / hw 头宽 / hh 头长，单位都是栅格。"""
    assert hh >= 0.5 * hw,  f"{name}: 头长 {hh} < 头宽 {hw}/2，会画成一根针"
    assert hw >= 1.8 * sw,  f"{name}: 头宽 {hw} 相对轴宽 {sw} 不够"
    shaft = L - hh
    assert shaft >= 0.9 * hh, f"{name}: 箭轴 {shaft} < 0.9×头长 {hh}，头尾都太短"

def varrow(cx, y0, y1, sw=26, hw=62, hh=36):        # 向下
    check_arrow(y1-y0, sw, hw, hh)
    yh = y1 - hh
    # (cx±sw/2, y0) → (cx±sw/2, yh) → (cx±hw/2, yh) → (cx, y1) 闭合
```

- 默认 `sw=26 / hw=62 / hh=36`，区块间距取 **76–84**（箭轴 40–48）
- `hh / hw ≈ 0.58`、`hw / sw ≈ 2.4`，头和尾都有明显长度，远端一看就是箭头
- **先留通道，再放箭头**：两个虚线容器之间的距离先按 78 定下来，箭头整条放进去，
  两端各贴住相邻元素；通道不够就把版式拉开，不要压缩箭头尺寸
- 四方向只是坐标镜像，写一个参数化函数 + 方向枚举，不要到处复制

细实心箭头同理：`Latex[length=1.5mm,width=1.0mm]`，箭身 ≥ 30 单位，
行距按 30–38 取值，同样用 `assert y1-y0 >= 30` 卡住。

## 5. 树形支架

结构：一条横干（trunk）+ 若干短分支（stub）。用途：一个父节点分出 N 个子节点，或 N 个合并到 1 个。

```
父 ──┬── 子1
     ├── 子2
     └── 子3
```
```python
# 横干：x 固定，y 从首个子节点中心到最后一个
line(X, cy_first, X, cy_last)
# 每个子节点：从横干拉一条 stub 到子节点边
for cy in centers: line(X, cy, x_child_edge, cy)
# 父节点接横干：接在横干中点（不是父节点中心，除非刚好重合）
line(x_parent, y_mid, X, y_mid)
```

**端点必须对齐**：横干的两端要正好落在首/末子节点的中心线上。差 10px 就会有一根竖线悬空——
这是实际交付里被用户指出过的错误，比对时专门看每个支架的端点。

**分流式**：父→横干→子，再 子→横干2→孙（两层）。横干2 的跨距按孙节点的首末中心取。

## 6. 圆柱（数据库）

```python
def cylinder(cx,y0,y1,rx,ry,text):
    k=0.5523*ry
    # 体：左边线下行 → 贝塞尔下弧 → 右边线上行 → 闭合
    # 顶部再叠一个整椭圆
```

**不要用 `arc`**：坐标系 y 翻转后，`arc(180:360)` 画出来是上弧不是下弧。
用两段三次贝塞尔 `.. controls (cx-rx,y1+k) and (cx+rx,y1+k) ..` 控制点朝 +y，不受翻转影响。

参考值：`ry ≈ 9`（很扁），`rx ≈ 90`，体高 ≈ 67。

## 7. 立体卡片（3D 文档框）

三块面：正面矩形 + 顶面平行四边形（放标题）+ 右侧面平行四边形（填灰）。

```
(x0,ytop) ─ (x0+dx,ytop-dy) ─ (x1+dx,ytop-dy) ─ (x1,ytop)     顶面
(x1,ytop) ─ (x1+dx,ytop-dy) ─ (x1+dx,ybot-dy) ─ (x1,ybot)     右侧面（灰）
(x0,ytop) ─ (x1,ybot) 矩形                                     正面
```
- 偏移量 `(dx,dy)`：正面顶边与顶面后边的 y 差即 `dy`，x 差即 `dx`（常见 40~45 单位）
- 标题放在**顶面中心** `((x0+x1)/2+dx/2, ytop-dy/2)`，粗体，字号略小于正文
- 顶面高度只有 `dy`（约 42 单位），标题字号必须压进去（约 8.4pt 粗体）
- 压盖顺序：先画顶面和侧面，再画正面（正面白底会盖住多余线）

## 8. 双向箭头 ⇔

两条三角形背靠背 + 中间短轴：

```python
def dbl(y, x0, x1, stroke):
    hl, h, s = 20, 24, 8          # 头长 / 头半高 / 轴半高
    assert x1 - x0 >= 2*hl + 20, "双向箭头太短"
    # 左尖 → 上轴 → 右上 → 右尖 → 右下 → 下轴 → 左下
    draw[fill=white] (x0+hl,y-s) -- (x1-hl,y-s) -- (x1-hl,y-h) -- (x1,y)
                     -- (x1-hl,y+h) -- (x1-hl,y+s) -- (x0+hl,y+s)
                     -- (x0+hl,y+h) -- (x0,y) -- (x0+hl,y-h) -- cycle
```
头长 20 对头高 48，两个方向都读得出箭头；总长 ≥ 60。

## 9. 竖排标签框（框与箭头共边）

常见版式：左侧灰色/白色竖排标题框，右边一个块箭头指向内容区，**箭尾与框的右边框重合，框线在箭尾处断开**。

必须分三段画。通道 = `content_x - x1`，先按 ≥ 86 定好，箭头尖端停在内容区左侧 ≥ 10 处：

```python
def label_box(x0, y0, x1, y1, text, content_x):
    cy = (y0 + y1) / 2
    sh, hd = 12, 25                # 轴半高 / 头半高
    xsh, xhd = x1 + 32, x1 + 74    # 轴长 32、头长 42
    assert xhd + 10 <= content_x, "标签箭头戳进了内容区"

    # 1) 左边 + 顶边 + 右上半段
    draw (x0,y1) -- (x0,y0) -- (x1,y0) -- (x1, cy-sh)
    # 2) 箭头（箭尾就是上面两条端点，天然共边）
    draw[fill=white] (x1,cy-sh) -- (xsh,cy-sh) -- (xsh,cy-hd) -- (xhd,cy)
                     -- (xsh,cy+hd) -- (xsh,cy+sh) -- (x1,cy+sh)
    # 3) 右下段 + 底边  ← 结束，不要 cycle
    draw (x1,cy+sh) -- (x1,y1) -- (x0,y1)
```

头长 42 对头高 50、轴长 32 对轴高 24，头尾比例与区块箭头一致。
竖排文字见 `04-text.md`；`sh < hd` 时轮廓才会在头部张开，取值不要颠倒。

**第 3 段不能加 `-- cycle`**。`cycle` 回到的是本段起点 `(x1,cy+sh)`，不是第一段的起点，
结果会从 `(x0,y1)` 斜拉一条线穿过框内文字。

## 10. 扇形发散（非正交树）

一个父节点向下发散到一排竖条，连线是**斜线**而不是横干+竖线：

```python
for (x0,x1) in children:
    line(cx_parent, y_parent_bottom, (x0+x1)/2, y_child_top)
```
从父节点底部同一点发散，或从父节点底边若干点发散，按版面需要选择。
