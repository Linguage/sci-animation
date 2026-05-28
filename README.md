# Mechanical Science Animations

这是一个用 Manim 制作机械机构、振动、结构动力学与数值方法科普动画的基础框架。当前包含曲柄摇杆机构、单自由度弹簧振子、三层剪切楼地震响应、CSV replay、蒙特卡罗估计 pi 和高尔顿板示例，结构上把模型/数据处理和 Manim 动画场景分开。

## 文档与报告

- [操作清单](c.md)：常用命令、结果路径、目录入口。
- [依赖清单](DEPENDENCIES.md)：跨设备配置 Manim、TeX、`dvisvgm` 等依赖。
- [项目蓝图](docs/specs/BLUEPRINT.md)：项目定位、技术路线和验收标准。
- [架构说明](docs/specs/ARCHITECTURE.md)：模块边界、数据流和目录映射。
- [路线图](docs/specs/ROADMAP.md)：当前阶段和后续 todo。
- [报告索引](docs/reports/INDEX.md)：经验沉淀与专题报告入口。
- [三个模拟动画的理论依据](docs/reports/simulation-theory-overview.md)：曲柄摇杆、弹簧振子、三层剪切楼的理论说明，并包含 GitHub 可直接查看的 GIF 预览。
- [蒙特卡罗方法动画说明](docs/reports/monte-carlo-method.md)：用面积比例和大数定律解释随机采样估计 pi 的动画表达。
- [高尔顿板动画说明](docs/reports/galton-board.md)：用随机左右分岔解释二项分布与正态近似。

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

## 渲染示例

```bash
manim -pqh scenes/crank_rocker.py CrankRockerScene
manim -pqh scenes/spring_oscillator.py SpringOscillatorScene
manim -pqh scenes/three_story_earthquake.py ThreeStoryEarthquakeScene
manim -pqh scenes/monte_carlo_pi.py MonteCarloPiScene
manim -pqh scenes/galton_board.py GaltonBoardScene
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
│   ├── crank_rocker.py
│   ├── galton_board.py
│   ├── monte_carlo_pi.py
│   ├── replay_time_response.py
│   ├── spring_oscillator.py
│   └── three_story_earthquake.py
├── src/
│   ├── mechanisms/              # 兼容导出层
│   └── sci_animation/
│       ├── models/
│       ├── replay/
│       ├── schemas/
│       ├── solvers/
│       └── viz/
├── docs/
│   ├── reports/
│   └── specs/
├── media/
│   ├── previews/                # GitHub 报告中使用的 GIF 预览
│   └── videos/                  # Manim 输出的最终 mp4
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
