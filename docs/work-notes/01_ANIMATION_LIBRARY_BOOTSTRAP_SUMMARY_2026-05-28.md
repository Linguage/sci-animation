---
title: "动力学动画库雏形搭建总结"
date: "2026-05-28"
created: "2026-05-28 21:10:34 +0800"
category: "worknotes"
tags: ["manim", "动力学动画", "结构动力学", "项目脚手架", "文档系统"]
---

# 动力学动画库雏形搭建总结

日期：2026-05-28

本轮工作从一个空的 `sci-animation` 项目开始，目标是探索如何用 Manim 制作类似 3Blue1Brown 风格的科学与工程动画，并逐步把项目整理成可持续开发的动力学动画库雏形。当前已经完成三个可渲染示例：曲柄摇杆机构、单自由度弹簧振子、三层剪切楼地震响应，同时补齐了依赖说明、文档系统、理论报告和 GitHub 可读的动画预览。

## 1. 背景与目标

项目最初的需求是制作机械机构动画演示，例如曲柄摇杆机构。后续需求扩展到动力学类动画：先做单自由度弹簧振子，再做三层楼在地震激励下的响应分析。

这个方向的核心问题不是单个动画如何写出来，而是如何把“力学模型”和“动画表达”分开，使后续能持续加入更多基于动力学理论的示例。当前项目因此采用了一个初步分层：

- `src/mechanisms/` 放力学、几何、数值求解逻辑。
- `scenes/` 放 Manim 场景、视觉表达和动画节奏。
- `docs/` 放项目治理文档、理论报告和工作记录。
- `media/` 放最终 mp4 与 GitHub 可预览 GIF。

这还不是最终的动画库架构，但已经形成了一个可运行、可记录、可继续扩展的最小基础。

## 2. 已完成的三个动画示例

第一个示例是曲柄摇杆机构。实现中将四杆机构抽象为机架、曲柄、连杆和摇杆，使用圆-圆相交求解活动铰点位置。动画展示曲柄输入、连杆运动、摇杆输出角和连杆端点轨迹。这个示例主要说明几何约束如何决定机构运动。

第二个示例是单自由度弹簧振子。实现中加入 `OscillatorConfig`，用解析解描述无阻尼自由振动：

```text
x(t) = A cos(omega_n t + phi)
x_ddot(t) = -omega_n^2 x(t)
```

动画左侧展示弹簧和质量块，右侧同步绘制位移和加速度时程曲线。这个示例建立了“自由度响应”和“时程曲线”之间的视觉联系。

第三个示例是三层剪切楼地震响应。实现中加入质量矩阵、刚度矩阵、Rayleigh 阻尼、合成地震输入和 Newmark 平均加速度法。动画左侧展示三层楼侧向响应，右侧展示三层相对位移时程和地面加速度输入。这个示例把单自由度响应扩展到了多自由度结构动力学。

## 3. 依赖与渲染链路

项目使用 Manim Community，并依赖 TeX 渲染公式和数字对象。过程中确认了以下依赖边界：

- 小型 TeX 包如 `standalone`、`preview` 可以用 `tlmgr --usermode` 安装。
- `dvisvgm` 是 Manim 渲染 TeX 所需的二进制工具，但不能用 `tlmgr --usermode` 安装。
- 为避免 Homebrew 拉取完整 TeX Live，本机只从 TeX Live 官方归档提取了 `dvisvgm` 二进制，并放入项目虚拟环境。

这些依赖被记录在 `DEPENDENCIES.md` 中，并在 `AGENTS.md` 中写入约束：不要未经确认安装完整 TeX 发行版、大型 Homebrew 依赖链或重量级二进制工具。

## 4. 文档系统与理论报告

项目已初始化 Git，并按文档系统骨架建立了：

- `docs/specs/BLUEPRINT.md`
- `docs/specs/ARCHITECTURE.md`
- `docs/specs/ROADMAP.md`
- `docs/jobs/`
- `docs/legacy/`
- `docs/reports/`
- `docs/work-notes/`
- `docs/theory/`
- `c.md`

另外生成了 `docs/reports/simulation-theory-overview.md`，集中介绍三个模拟的理论依据、建模假设和当前实现边界。由于 GitHub Markdown 对仓库内 mp4 的内嵌播放不可靠，报告中改用 GIF 预览，并保留 mp4 高清链接。对应的 GIF 存放在 `media/previews/`。

README 也已经补充了文档与报告入口，使新读者可以从根目录进入操作清单、依赖清单、项目蓝图、架构说明、路线图和理论报告。

## 5. 验证情况

已验证的内容包括：

- Python 语法检查：对新增场景和求解模块运行过 `python3 -m py_compile`。
- 曲柄摇杆几何求解：对一圈输入角进行过求解检查。
- 单自由度振子：验证了 `x(0)` 和 `a(0)` 的基本关系。
- 三层剪切楼：验证了响应矩阵维度和三阶频率输出。
- Manim 渲染：三个场景均已用低质量参数渲染成功，并生成 mp4。
- GIF 预览：三个 mp4 已转换为轻量 GIF，并确认报告中的相对链接可达。

当前最终动画包括：

- `media/videos/crank_rocker/480p15/CrankRockerScene.mp4`
- `media/videos/spring_oscillator/480p15/SpringOscillatorScene.mp4`
- `media/videos/three_story_earthquake/480p15/ThreeStoryEarthquakeScene.mp4`

当前 GitHub 预览图包括：

- `media/previews/crank_rocker.gif`
- `media/previews/spring_oscillator.gif`
- `media/previews/three_story_earthquake.gif`

## 6. 当前状态与未完成事项

当前项目已经具备动画库雏形，但基础架构仍偏“示例驱动”。也就是说，每个新场景已经能复用一部分求解模块，但动画组件、绘图面板、时程曲线、坐标映射、视觉样式等还没有沉淀成稳定公共层。

后续需要重点处理的问题包括：

- 将通用 Manim 元件抽象出来，例如时程曲线面板、动态图例、实时数值面板、结构楼层绘制器、弹簧/质量块组件。
- 将动力学模型进一步分层，例如模型配置、求解器、响应结果、可视化适配器分开。
- 为更多力学对象建立统一接口，例如 `state_at(t)`、`response_at(t)`、`sample_response()`。
- 增加更系统的测试，尤其是矩阵组装、积分算法、边界条件和能量/频率校验。
- 形成一个“新增动画”的开发模板，降低复杂模拟进入动画表达层的门槛。

总体上，本轮完成的是从零到可运行、可预览、可解释的第一阶段。下一阶段的重点不应只是继续增加示例，而是把已经重复出现的结构抽象为库能力。

