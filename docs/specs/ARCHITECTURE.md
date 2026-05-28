# sci-animation 架构文档 (Architecture)

> 实现框架文档：功能实现框架与技术细节说明。
> 最近更新: 2026-05-28

---

## 1. 系统总览

项目使用 Manim Community 生成机械机构科普动画。核心思路是：

- `src/mechanisms/` 负责机构几何、状态求解和可复用模型。
- `scenes/` 负责 Manim 视觉表达、动画节奏和标注。
- `media/` 由 Manim 生成，不作为源码维护。

## 2. 模块结构

- `src/mechanisms/four_bar.py`：四杆机构配置、状态数据结构和圆交点求解。
- `scenes/crank_rocker.py`：曲柄摇杆机构动画场景。
- `manim.cfg`：Manim 默认渲染配置。
- `DEPENDENCIES.md`：跨设备依赖清单。

## 3. 数据流

1. `FourBarConfig` 定义杆长和装配支路。
2. `ValueTracker` 驱动输入曲柄角。
3. `solve_four_bar()` 根据输入角计算 A/B/C/D 关节坐标与输出角。
4. Manim 的 `always_redraw()` 将状态实时映射为连杆、关节、轨迹和标注。
5. Manim 输出 mp4 到 `media/videos/`。

## 4. 关键技术决策

- 几何求解与动画场景分离，便于后续复用到其它机构。
- TeX 被视为正式渲染依赖，保留 `MathTex` 与 Manim 数字对象。
- 缺少小型 TeX 包时可用 `tlmgr --usermode` 补齐；大型二进制或完整发行版安装必须先确认。
- 当前 `dvisvgm` 采用项目虚拟环境内的最小二进制补齐方式，避免全局安装额外包。

## 5. 目录映射

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
│   └── crank_rocker.py
└── src/
    └── mechanisms/
        └── four_bar.py
```

