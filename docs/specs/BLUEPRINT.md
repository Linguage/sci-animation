# sci-animation 项目蓝图 (Blueprint)

> 战略性文档：宏观规划与理念阐述。
> 最近更新: 2026-05-28

---

## 1. 项目定位

用 Manim 制作机械机构与科学概念的可复现动画演示，当前以曲柄摇杆机构为起点，逐步沉淀机构几何求解、动画表达和渲染工具链。

## 2. 核心挑战与技术路线

- 将机构几何求解与 Manim 场景表达分层，避免动画代码和数学模型耦合。
- 保持依赖可迁移，尤其是 Manim、TeX、`dvisvgm`、ffmpeg 等渲染链路。
- 先用小而完整的机构示例验证工作流，再扩展滑块曲柄、齿轮、凸轮等机制。

## 3. 验收标准

- 能在新设备上按 `DEPENDENCIES.md` 建立环境。
- 能渲染 `CrankRockerScene` 并生成 mp4。
- 新机构应至少包含几何求解入口、Manim 场景和最小验证命令。

## 4. 战略治理原则

1. **价值优先**：默认先交付业务价值，再按需做结构优化。
2. **证据驱动**：关键结论应有测试或可复现工况支撑。
3. **文档分层**：战略（Blueprint）、架构（Architecture）、路线（Roadmap）各司其职。
4. **一问一主文档**：同一个高频问题只保留一个主文档负责回答，避免并行维护多个真相源。
5. **Day 1 可归档**：明显会形成任务线、专题线或实验线的工作，从第一天开始保留入口、输出、摘要、验证和冻结条件。

## 5. 文档系统边界

| 文档 | 职责 |
|------|------|
| `docs/specs/BLUEPRINT.md` | 战略层：宏观规划、理念、技术路线与验收标准 |
| `docs/specs/ARCHITECTURE.md` | 架构层：功能实现框架与关键技术细节 |
| `docs/specs/ROADMAP.md` | 执行层：阶段路线与 todo-list |
| `docs/jobs/` | 在制专题文档 |
| `docs/legacy/` | 已完成任务归档 |
| `docs/reports/` | **经验沉淀**：阶段分析、专项复盘、可复用结论与决策证据 |
| `docs/work-notes/` | **经历记录**：按时间推进的研发工作记录与 session 索引 |

`reports/` 与 `work-notes/` 的硬性边界：

- 只描述"当时做了什么"→ `work-notes/`
- 已经提炼为可复用结论、原则或专题决策证据 → `reports/`
- 在 work-notes 中发现某份记录被反复回看且实际承担了经验文档的职责，应主动迁入 reports，并保留迁移说明。

默认主文档分工：

- "怎么运行/结果去哪"优先看 `c.md` 或对应子项目 `c.md`
- "当前结构边界与目录语义"优先看 `docs/specs/ARCHITECTURE.md`
- "当前做什么/下一步做什么"优先看 `docs/specs/ROADMAP.md` 与 active `docs/jobs/`
- "历史材料如何回捞"优先看 `docs/legacy/`
- "经验沉淀与复盘结论"优先看 `docs/reports/INDEX.md`
- "研发过程的时间线记录"优先看 `docs/work-notes/INDEX.md`

