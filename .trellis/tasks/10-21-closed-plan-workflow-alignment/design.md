# 设计：Marketplace 规划工作流收敛

## 职责边界

Marketplace workflow 负责把用户请求交给唯一规划入口、说明何时调用 Trellis 原生接口、保持批准时序清晰。规划入口模型负责对封口后的变化按已批准方案进行 minor/major 语义判断，Marketplace workflow 不复制这些判据。Trellis CLI 是阶段、结构校验、摘要、seal、approval、start 和 replan 的唯一状态权威；workflow 不持久化状态、不复制转移逻辑、不直接改 `task.json`。

## 调用合同

- 用 `trellis-idea-to-closed-plan` 处理需要任务规划的请求，并根据原生 task stage 继续当前断点。
- `pennix-decision-grill` 只处理待用户决定的实质选择；用户答复写入任务决策材料后，由规划入口调用原生 `plan advance`。
- 方案必须完整且顺序可执行，明确仓库、分支、依赖、验证、风险、回退与唯一停止点，再进入独立方案审查。
- 向用户展示完整材料后计算/读取原生 `plan digest`。只有同一份材料经用户明确批准，才按新 CLI 合同 seal、approve 并 start；CLI 拒绝摘要时回到修改与审查，不复用旧批准。
- direct、analysis-only、已有任务继续、replan 与行政 archive 按原生合同区分；workflow 不创造跳过审批的快捷路径。

## 封口后变化处理

四份 workflow 对新需求、现场变化和实施发现使用同一分流：先由 `trellis-idea-to-closed-plan` 模型判断新请求是否属于当前 task；独立交付目标进入独立 task，不改变无关活动 task；有界核验仍无法确定关联性时保持当前 task 不变并向用户澄清；已归档或完成的 task 保持终态、后续事项另建 task。planned task 以当前已批准 revision 为基线；direct task 以已接受的单一变化、owner、验证和回退合同为基线。对属于当前 task 的变化，再比较适用承诺。只有所有目标/范围/验收、决定、owner、设计、依赖、验证、风险/回滚和停止点承诺均不变，且可在基线内执行时才是 minor；因此即使需求很小，只要改变当前 task 已批准范围或验收，仍是 major；若是独立交付则新建 task。direct task 还必须保持 direct 资格。只在 `execution.md` 记录 baseline revision/分类、触发事实/证据、判断理由、受影响步骤或 direct 合同、实施差异和验证，保持当前状态并继续。

任何承诺变化、关键假设失效、需要重开重要用户选择、direct 资格失效，或有界取证后仍不能证明是 minor 时均为 major。先停止依赖该变化的工作，由规划入口决定最早受影响 stage（direct 资格失效回 `intake`）并调用 Trellis 原生 replan；只对 `in_progress` task 与 `planning/plan_closed` 使用该回退入口；replan 会使旧 seal/approval 失效。重新完整审查、向用户展示并取得明确批准前不得继续相关实施。Workflow 只提醒并路由，不自行选择阶段或补写生命周期记录。

## 受影响来源

四个源模板保留各自的任务类型和协作策略，只统一规划入口和状态接口。Codex Subnode workflow 继续限定其 Channel 协作流程；TDD workflow 继续约束测试节奏；channel-driven workflow 继续约束子任务与检查；native workflow 保持单会话默认。`index.json` 只更新四个修改后文件的 `sha256`。

## 方案审查

Marketplace owner task 只负责 `main` 分支上四份实际 workflow 源及其索引摘要，不承担状态写入或 minor/major 语义分类。实施步骤先核对源摘要，再改四份 workflow、更新对应摘要并运行完整 Python 测试；根组合验收和最终 gitlink 固定仍由协调 task 执行。请求关联不明时不修改现有 task，已批准范围变化不因请求较小而绕过 major 路径，终态 follow-up 创建新 task。owner task 的 branch 元数据已由原生 Trellis 命令设为 `main`，与实际 checkout 一致；代码测试留待当前方案批准后执行。

## 验收边界

Marketplace 单元测试验证索引 digest 和 workflow 内容合同。本任务不运行 Trellis 源码检查；根协调 task 在删除 Trellis 嵌套 Marketplace 后运行跨仓组合门禁并核对物化工作流 provenance。
