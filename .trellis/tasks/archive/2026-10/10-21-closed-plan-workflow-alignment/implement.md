# 实施计划

## 前置条件

- 根协调 task 正在修订 revision 2；本计划与 Trellis owner 合同通过完整审查、重新封口和用户明确批准前，不修改 Marketplace workflow 源。
- 目标分支为 Marketplace `main`；唯一源 checkout 为根 `pennix-marketplace`。
- 先读取 Trellis owner task 已定稿的状态字段和命令接口，再修改 workflow 文案，不自行猜测 CLI 参数。

## 有序步骤

1. 检查四份 workflow 与索引当前 digest，列出所有活动规划入口和现有批准表述。
2. 更新 native、TDD、channel-driven-subagent-dispatch、codex-subnode-channel 四份 workflow；保留各自用途，只统一规划入口、stage 查询/推进、完整方案审查和批准时序，并说明请求关联不明时不变更当前 task、先向用户澄清；变化交由规划入口模型判断：minor 写入 execution.md 后保持当前状态继续；即使需求很小，只要改变已批准范围或验收即属 major；major/有界取证后仍不确定时停止相关实施、调用原生 replan、必要时从 direct 回 intake 重新分类，并要求重新审查和批准。
3. 核对新请求属于当前 task 还是独立 task、direct、analysis-only、minor continuation、major replan、归档/完成后的新 task 和继续已有 task 等分流没有隐含旁路；确认独立需求不改变无关 task、终态 task 不重开、workflow 不复制模型判据或自行选阶段；检索活动 workflow 中旧 `trellis-brainstorm` 规划入口。
4. 更新 `index.json` 中受影响源文件的 `sha256`，不修改无关条目。
5. 运行完整 Python unittest，重点核验 `tests/test_codex_subnode_channel_workflow.py` 对完整方案审阅、显式批准、独立任务隔离、终态 follow-up、关联不明时无变更并澄清、小需求修改已批准范围仍走 major、minor 台账继续、major replan/reapproval 的约束及所有索引摘要；保存回执。

## 停止点

停止于四份 workflow 与索引符合 Trellis 原生命令和模型负责变化分流合同、Marketplace 完整测试通过、工作树仅含已审查的 Marketplace 任务文件和 workflow/index 变更。根组合验收和最终 gitlink 固定由根协调 task 执行；本任务不推送或发布。

<!-- trellis-implementation-plan:v1 -->
```json
{
  "schema_version": 1,
  "steps": [
    {"id":"source-baseline","depends_on":[],"target":{"repository":"pennix-marketplace","branch":"main","component_or_path":"four target workflow files and index.json"},"action":"Record current source hashes and existing planning, approval, direct, analysis, replan, and archive wording","deliverables":"Marketplace workflow and index baseline","verification":"Exactly the four in-scope workflows and their current digests are identified","risks":"Accidentally altering unrelated workflow sources","rollback":"No source write occurs in this step"},
    {"id":"workflow-contract","depends_on":["source-baseline"],"target":{"repository":"pennix-marketplace","branch":"main","component_or_path":"workflows/native/workflow.md, workflows/tdd/workflow.md, workflows/channel-driven-subagent-dispatch/workflow.md, workflows/codex-subnode-channel/workflow.md"},"action":"Update the four workflows to route through the sole planning entry and express independent-task isolation, terminal follow-ups, ambiguity clarification without mutation, small scope-changing requests as major, model-owned minor/major triage, execution.md continuation, native replan, full re-review, and explicit user approval without duplicating state rules","deliverables":"Four consistent but purpose-specific Marketplace workflow sources","verification":"Tests reject approval shortcuts, duplicated classification ownership, unrelated-task mutation, terminal reopen, ambiguity mutation, minor state movement, small scope changes treated as minor, and major continuation without reapproval","risks":"Workflow text conflicts with the Trellis native contract","rollback":"Do not update source until the Trellis command contract is approved"},
    {"id":"index-and-test","depends_on":["workflow-contract"],"target":{"repository":"pennix-marketplace","branch":"main","component_or_path":"index.json and Marketplace Python tests"},"action":"Recompute only the four affected workflow hashes and run the full Marketplace unit suite","deliverables":"Updated index digests and test receipts","verification":"All four hashes match byte-for-byte and python3 -B -m unittest discover -s tests -q passes","risks":"Stale or unrelated index updates","rollback":"Restore only the affected index entries from the task baseline if validation fails"}
  ],
  "stop_point": {
    "condition":"The four Marketplace workflows express the approved Trellis entry, task isolation/terminal behavior, ambiguity clarification, small-scope-change major classification, minor/major, replan, review, and approval contract; index digests match and the complete Marketplace unit suite passes",
    "observable_evidence":"Four-source diff, exact index digest verification, passing tests/test_codex_subnode_channel_workflow.py for independent-task routing, terminal follow-up, ambiguous task relationship, small scope changes, and minor/major routing, plus full unittest receipt",
    "remaining_work":"Root cross-repository integration, Trellis source acceptance, and root gitlink pinning remain with the coordinator task"
  }
}
```
