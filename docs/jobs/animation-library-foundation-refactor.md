# 动力学动画库基础层调整计划

- `状态`: done
- `最近更新`: 2026-05-29
- `lifecycle`: active patch
- `entrypoint`: `docs/jobs/animation-library-foundation-refactor.md`
- `outputs`: `src/sci_animation/`、`scenes/`、`docs/specs/ARCHITECTURE.md`、`docs/reports/`
- `summary`: 将当前示例驱动项目调整为可持续开发的动力学动画库基础框架。
- `smoke`: `python3 -m py_compile ...`，以及至少一个既有场景的 `manim -ql` 渲染。
- `freeze rule`: 完成统一响应结构、基础可视化组件、一个 replay 示例，并保持三个既有动画可渲染后归档。

## 1. 背景

当前项目已经完成三个可渲染示例：

- 曲柄摇杆机构。
- 单自由度弹簧振子。
- 三层剪切楼地震响应。

这些示例证明了 Manim 能用于工程科学动画，也初步验证了“模型计算”和“动画表达”分离的方向。但当前代码仍偏示例驱动：每个场景都有自己的时程曲线、动态图例、实时读数和模型数据适配逻辑。继续直接增加新动画，会让复杂度很快堆在 `scenes/` 中。

下一阶段的目标不是大规模重写，而是沉淀基础层，使项目能够长期支持更多基于动力学理论或外部仿真结果的动画。

## 2. 目标

本任务的目标是把项目调整为“教学模型 + 仿真结果再现 + 可复用可视化组件”的基础框架。

具体目标：

1. 建立统一响应数据结构，使动画层不用关心数据来自解析解、数值积分还是外部仿真文件。
2. 抽出可复用 Manim 组件，减少新增场景时的重复样板代码。
3. 将通用数值方法从具体模型中拆出，保留小型、透明、教学用途的求解器。
4. 建立 `replay/` 层，支持从外部仿真或实验结果中读取数据并生成动画。
5. 保持已有三个示例可运行，并用它们验证新基础层是否真的降低复杂度。

## 3. 非目标

本任务不做以下事情：

- 不把项目改造成通用结构动力学或有限元求解器。
- 不重写 OpenSees、Abaqus、ANSYS、SAP2000 等专业软件能力。
- 不一次性迁移所有目录并追求完美包结构。
- 不为了抽象而抽象；只有跨两个以上场景复用的能力才进入公共层。
- 不删除现有可运行示例，除非已有等价替代并完成渲染验证。

## 4. 建议目标结构

短期目标结构：

```text
src/sci_animation/
├── schemas/
│   ├── time_response.py
│   └── geometry.py
├── models/
│   ├── four_bar.py
│   ├── oscillator.py
│   └── shear_building.py
├── solvers/
│   └── newmark.py
├── replay/
│   └── csv_time_response.py
└── viz/
    ├── time_history.py
    ├── readout.py
    ├── mechanical.py
    └── structures.py
```

`src/mechanisms/` 可以先保留兼容导出，避免一次性破坏既有场景。

## 5. 阶段计划

### Step 1: 建立 schemas

- [x] 新增 `TimeResponse`，用于承载时程数据、单位、通道名和元数据。
- [x] 新增 `GeometryState` 或等价结构，用于承载可重放的节点/点位状态。
- [x] 为三个既有模型定义最小适配方式。
- [x] 补充基础单元测试或 smoke 验证。

验收标准：

- 弹簧振子和三层楼都能转换为 `TimeResponse`。
- 场景中不再直接依赖裸 `np.ndarray` 组织曲线数据。

### Step 2: 抽出可视化组件

- [x] 抽出 `TimeHistoryPlot`，支持多通道时程曲线、动态追踪点、颜色映射。
- [x] 抽出 `LiveValuePanel`，用于实时显示时间、位移、加速度等数值。
- [x] 抽出基础图例组件。
- [x] 抽出弹簧、质量块、剪切楼楼层等基础视觉组件，先保持小而可用。

验收标准：

- `spring_oscillator.py` 和 `three_story_earthquake.py` 共同使用同一个时程曲线组件。
- 至少两个场景共用 `LiveValuePanel` 或图例组件。

### Step 3: 拆出 solvers

- [x] 将 Newmark 平均加速度法从 `shear_building.py` 中拆到 `solvers/newmark.py`。
- [x] 保持 `shear_building.py` 只负责模型矩阵、阻尼、输入和响应组装。
- [x] 为 Newmark 添加最小验证，例如维度检查和简单单自由度对照。

验收标准：

- 三层剪切楼场景渲染结果仍可生成。
- Newmark 求解器不依赖具体结构模型。

### Step 4: 建立 replay 层

- [x] 设计 CSV 时程输入格式。
- [x] 新增 `replay/csv_time_response.py`，读取外部时程结果并转换为 `TimeResponse`。
- [x] 新增一个最小 replay 示例数据。
- [x] 新增一个 replay 场景或将既有场景改造成可读取 replay 数据。

验收标准：

- 可以从 CSV 读取三列以上响应数据。
- 可以用统一时程组件展示 replay 数据。

### Step 5: 场景迁移与文档更新

- [x] 迁移弹簧振子场景到新组件。
- [x] 迁移三层剪切楼场景到新组件。
- [x] 保留曲柄摇杆场景，必要时只做轻量适配。
- [x] 更新 `ARCHITECTURE.md` 的目录映射。
- [x] 更新 `c.md` 的运行命令。
- [x] 如新增示例，更新 `docs/reports/` 或补充新报告入口。

验收标准：

- 三个既有场景均能 `manim -ql` 渲染。
- README、c.md、ARCHITECTURE 与实际结构一致。

## 6. 验证计划

每个阶段至少运行：

```bash
python3 -m py_compile scenes/*.py src/**/*.py
```

关键阶段运行：

```bash
.venv/bin/manim -ql scenes/spring_oscillator.py SpringOscillatorScene
.venv/bin/manim -ql scenes/three_story_earthquake.py ThreeStoryEarthquakeScene
```

若涉及曲柄摇杆公共接口变化，也运行：

```bash
.venv/bin/manim -ql scenes/crank_rocker.py CrankRockerScene
```

GIF 预览更新不强制每次做；只有最终 mp4 有明显视觉变化时才重新生成 GIF。

## 7. 风险与处理

### 7.1 抽象过早

风险：为了未来复杂场景设计过大的抽象，反而让当前三个示例难以理解。

处理：只抽出已经在两个以上场景中重复出现的部分。所有公共组件都应有至少一个实际场景使用。

### 7.2 兼容破坏

风险：迁移包结构后，已有场景无法导入旧模块。

处理：保留 `src/mechanisms/` 兼容导出一段时间，先新增新结构，再逐步迁移。

### 7.3 求解器职责膨胀

风险：项目逐步变成工程求解器。

处理：`solvers/` 只保留小型、透明、教学用途算法；复杂仿真优先通过 `replay/` 导入外部结果。

### 7.4 媒体文件膨胀

风险：mp4、GIF、Manim 缓存导致仓库快速变大。

处理：继续只跟踪最终 mp4 与 `media/previews/*.gif`，忽略 `media/Tex/`、`media/texts/` 和 `partial_movie_files/`。

## 8. 当前下一步

建议从 Step 1 和 Step 2 开始，先做最小公共基础：

1. `TimeResponse`
2. `TimeHistoryPlot`
3. `LiveValuePanel`

这三个组件完成后，再迁移弹簧振子和三层剪切楼。它们会立刻验证公共层是否真正降低场景复杂度。
