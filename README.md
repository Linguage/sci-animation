# Mechanical Science Animations

这是一个用 Manim 制作机械机构科普动画的基础框架。当前包含一个“曲柄摇杆机构”示例，结构上把机构几何求解和 Manim 动画场景分开。

## 安装

建议使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## 系统依赖

Manim 渲染 `MathTex`、`Tex` 和部分数字对象时需要完整的 TeX 渲染链。当前示例使用了 `MathTex` 和 `DecimalNumber`，因此至少需要：

- `latex`
- `dvisvgm`
- TeX 包：`standalone`、`preview`

小型 TeX 包可以用用户级 `tlmgr` 安装：

```bash
tlmgr --usermode install standalone preview
```

如果缺的是 `dvisvgm` 这类二进制工具，请先确认安装方式，避免包管理器拉取完整 TeX 发行版。Manim 还可能需要 Cairo、Pango、ffmpeg 等系统依赖。

## 渲染曲柄摇杆示例

```bash
manim -pqh scenes/crank_rocker.py CrankRockerScene
```

常用质量参数：

```bash
manim -pql scenes/crank_rocker.py CrankRockerScene
manim -pqm scenes/crank_rocker.py CrankRockerScene
manim -pqh scenes/crank_rocker.py CrankRockerScene
```

## 项目结构

```text
.
├── scenes/
│   └── crank_rocker.py          # Manim 动画场景
├── src/
│   └── mechanisms/
│       ├── __init__.py
│       └── four_bar.py          # 四杆机构几何求解
├── manim.cfg
└── pyproject.toml
```

## 调参入口

在 `scenes/crank_rocker.py` 里修改 `FourBarConfig`：

```python
config = FourBarConfig(
    ground=4.8,
    crank=1.25,
    coupler=3.8,
    rocker=3.0,
    assembly="open",
)
```

四个长度分别是：机架、曲柄、连杆、摇杆。`assembly` 可选 `"open"` 或 `"crossed"`，用于选择四杆机构的装配支路。

## 后续扩展建议

- 在 `src/mechanisms/` 里新增机构几何模型，例如 `slider_crank.py`、`cam.py`、`gear_train.py`。
- 在 `scenes/` 里只负责画图、动画节奏和标注。
- 对每个机构先实现 `point_at(angle)` 或 `state_at(t)`，再把状态喂给 Manim。
