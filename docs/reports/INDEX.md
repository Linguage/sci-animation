# reports 索引

本目录存放**沉淀出来的经验内容**：阶段分析、专项复盘、跨任务教训、可复用决策证据。与 `work-notes/` 的核心区别：

- `work-notes/` 是**经历**：按时间推进的研发记录，描述发生了什么。
- `reports/` 是**经验**：从经历中提炼后仍服务当前决策、实现理解或专题结论的内容。

只有仍然服务当前判断的问题，才应放在"当前优先阅读"区域。

## 当前优先阅读

- [`simulation-theory-overview.md`](simulation-theory-overview.md)：当前三个模拟动画的理论依据、建模假设与动画表达说明。
- [`monte-carlo-method.md`](monte-carlo-method.md)：蒙特卡罗估计 pi 的概率依据、收敛特征与动画表达说明。
- [`galton-board.md`](galton-board.md)：高尔顿板、二项分布和正态近似的动画表达说明。
- `DEPENDENCIES.md`：当前 Manim + TeX 渲染链路的最小依赖说明。
- `docs/specs/ARCHITECTURE.md`：机构求解与动画场景的分层边界。

## 专题经验沉淀

- [`simulation-theory-overview.md`](simulation-theory-overview.md)：曲柄摇杆、弹簧振子、三层剪切楼地震响应的理论综述。
- [`monte-carlo-method.md`](monte-carlo-method.md)：随机采样、面积比例和大数定律的可视化说明。
- [`galton-board.md`](galton-board.md)：随机左右分岔如何形成钟形分布的可视化说明。

## 使用建议

1. 新增报告时在此索引中添加条目。
2. 标注「当前优先阅读」帮助新读者快速定位。
3. 想追踪当前做什么，不看 reports，转去 `../specs/ROADMAP.md` 与 `../jobs/README.md`。
4. 内容如果只是"当时做了什么"，归 `../work-notes/`；如果已经提炼为可复用结论或可迁移原则，归本目录。
