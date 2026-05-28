# sci-animation 架构文档 (Architecture)

> 实现框架文档：功能实现框架与技术细节说明。
> 最近更新: 2026-05-28

---

## 1. 系统总览

项目使用 Manim Community 生成机械、振动和结构动力学动画。核心思路是：

- `src/sci_animation/` 负责响应数据结构、教学模型、求解器、replay 读取和可复用 Manim 组件。
- `src/mechanisms/` 保留为兼容层，继续支持旧的 `from mechanisms import ...` 导入方式。
- `scenes/` 负责 Manim 视觉表达、动画节奏和标注。
- `media/videos/` 存放最终 mp4；`media/previews/` 存放 GitHub 报告中直接展示的 GIF。
- `docs/reports/` 负责沉淀理论依据、建模假设、可复用结论和动画说明。

长期目标是演进为“动画叙事优先”的工程科学动画库。数值计算代码不是专业仿真软件替代品，而是教学模型、结果再现和动画数据准备的一部分。

## 2. 模块结构

- `src/sci_animation/schemas/`：统一响应与几何状态数据结构。
- `src/sci_animation/models/`：四杆机构、单自由度振子、剪切楼等教学模型。
- `src/sci_animation/solvers/`：Newmark 等小型透明求解器。
- `src/sci_animation/replay/`：外部仿真或实验结果读取与标准化。
- `src/sci_animation/viz/`：时程图、实时读数、弹簧/墙/剪切楼等可复用 Manim 组件。
- `src/mechanisms/`：兼容导出层。
- `scenes/crank_rocker.py`：曲柄摇杆机构动画场景。
- `scenes/spring_oscillator.py`：弹簧振子动画与位移/加速度时程。
- `scenes/three_story_earthquake.py`：三层剪切楼地震响应动画。
- `scenes/replay_time_response.py`：CSV replay 数据读取与时程响应动画。
- `scenes/_helpers.py`：场景共享的渲染工具链检查。
- `manim.cfg`：Manim 默认渲染配置。
- `DEPENDENCIES.md`：跨设备依赖清单。

## 3. 目标分层

后续架构应显式区分三类代码。

### 3.1 Teaching Model

教学模型用于解释核心理论，允许在项目内直接求解。它们应保持小、透明、可读，例如：

- 单自由度振子。
- 多自由度剪切楼。
- 简支梁影响线或模态。
- 四杆机构运动学。

这类模型的目标是“足够准确地讲清楚理论”，不是覆盖完整工程设计场景。

### 3.2 Replay Adapter

仿真再现层用于读取外部仿真或实验结果，并转换为统一动画数据结构。外部来源可以是：

- CSV / JSON / HDF5。
- MATLAB / Python 脚本导出的结果。
- OpenSees、Abaqus、ANSYS、SAP2000 等专业软件结果。
- 实验采集数据。

本项目不应为了动画而重写这些专业软件的求解能力。对于复杂项目，应优先导入结果、标准化数据、重放和讲解。

### 3.3 Visualization Components

可视化组件是项目最值得长期沉淀的核心资产，包括：

- 时程曲线面板。
- 动态追踪点和图例。
- 实时数值面板。
- 变形形状绘制。
- 弹簧、质量块、支座、楼层、梁、荷载等基础视觉元件。
- GIF 预览与 mp4 结果链接约定。

## 4. 数据流

### 4.1 教学模型动画

```text
model config
  -> solver / analytic response
  -> response object
  -> Manim scene adapter
  -> mp4 + gif preview + report
```

### 4.2 外部仿真再现动画

```text
external simulation / experiment
  -> exported data
  -> replay adapter
  -> standard response schema
  -> reusable visualization components
  -> Manim scene
```

这个流程要求场景代码尽量依赖标准化后的响应对象，而不是直接依赖某个一次性的仿真脚本。

## 5. 关键技术决策

- 力学/几何求解与动画场景分离，便于后续复用到其它示例。
- 对简单教学模型保留项目内求解；对复杂工程仿真优先做结果导入和再现。
- 后续应建立统一响应数据结构，例如 `TimeResponse`、`GeometryState`、`FieldFrame`、`ModeShape`。
- TeX 被视为正式渲染依赖，保留 `MathTex` 与 Manim 数字对象。
- 缺少小型 TeX 包时可用 `tlmgr --usermode` 补齐；大型二进制或完整发行版安装必须先确认。
- 当前 `dvisvgm` 采用项目虚拟环境内的最小二进制补齐方式，避免全局安装额外包。
- GitHub 报告中优先使用 `media/previews/*.gif` 作为可直接查看的动画预览，同时保留 mp4 链接。

## 6. 目录映射

```text
.
├── DEPENDENCIES.md
├── README.md
├── c.md
├── docs/
│   ├── jobs/
│   ├── legacy/
│   ├── reports/
│   ├── specs/
│   ├── theory/
│   └── work-notes/
├── scenes/
│   ├── _helpers.py
│   ├── crank_rocker.py
│   ├── replay_time_response.py
│   ├── spring_oscillator.py
│   └── three_story_earthquake.py
└── src/
    ├── sci_animation/
    │   ├── models/
    │   ├── replay/
    │   ├── schemas/
    │   ├── solvers/
    │   └── viz/
    └── mechanisms/
        ├── __init__.py
        ├── four_bar.py
        ├── oscillator.py
        └── shear_building.py
```

## 7. 建议的下一阶段包结构

当前 `src/mechanisms/` 已经承载了机构、振动和结构动力学，名称会逐渐变窄。后续可以演进为：

```text
src/sci_animation/
├── schemas/          # TimeResponse, GeometryState, FieldFrame, ModeShape
├── models/           # 教学模型
├── solvers/          # 小型透明求解器，如 Newmark、RK4、模态叠加
├── replay/           # 外部仿真结果读取与标准化
├── viz/              # 可复用 Manim 组件
└── scenes/           # 可选：场景基类或模板
```

短期不必一次性迁移，但新增复杂动画时应尽量朝这个边界靠拢。
