# 对齐 Marketplace 规划工作流与闭合方案状态机

## 目标

在 `main` 更新四份实际可选的 Marketplace workflow 源及 `index.json`，使其准确调用 Trellis 唯一规划入口和原生阶段命令，并保留明确的整份方案审查与用户批准边界。

## 需求

- 更新 `workflows/native/workflow.md`、`workflows/tdd/workflow.md`、`workflows/channel-driven-subagent-dispatch/workflow.md` 和 `workflows/codex-subnode-channel/workflow.md`。
- 四份 workflow 使用统一入口 `trellis-idea-to-closed-plan`，按 Trellis CLI 当前 stage 路由；不创建第二套规划状态机或独立规划 Skill。
- 明确完整方案形成、审查、向用户展示、按当前摘要封口、明确批准、原生 `start` 的先后约束；任何展示后材料变更都必须重新规划并使旧审批失效。
- 在方案 `plan_closed` 后，明确由 `trellis-idea-to-closed-plan` 中的模型按已批准方案判断新需求、现场变化和实施发现的影响：minor 必须不改变任何已批准承诺，只记录到未封口 `execution.md` 并保持当前 status/stage；major 或在有界取证后仍不能确认 minor 的情况，停止相关实施，通过 Trellis 原生 replan 回到最早受影响阶段，失效旧 seal/approval，并在重新完整审查和用户明确批准后继续。Marketplace workflow 不另行复制大小判据或选择回退阶段。
- 规划入口先判断新请求是否属于当前 task；独立交付目标进入独立 task，不改变无关活动 task；有界核验仍无法判断关联性时保持当前 task 不变并向用户澄清；改变当前 task 的批准结果、范围或验收时，即使需求很小也走 major replan 路径。
- 对从 `direct_ready` 启动的已建 task，以已接受的单一变化、owner、验证和回退合同为基线；minor 还必须符合全部 direct 资格，超出时由规划入口调用 replan 回 `intake` 重新分类。已归档或完成 task 的后续事项创建新 task，不把终态重新打开。
- 决策提问继续交由 `pennix-decision-grill`；workflow 不自行推断用户已批准，也不直接写 `task.json`。
- 只在被修改的工作流源和 `index.json` digest 范围内变更；不修改 Trellis CLI、项目安装资产或根集成门禁。

## 验收标准

- [ ] 四份 workflow 对规划入口、阶段读取、命令时序和用户批准边界的表述一致，并与 Trellis CLI 合同一致。
- [ ] Marketplace workflow 不重复完整状态转移表，不写入状态，不把 `seal`、材料齐全或沉默当作用户批准。
- [ ] 四份 workflow 明确 planned 与 direct 的基线、minor 留在当前状态并记 execution.md 后继续、major/有界取证后仍不确定时由唯一规划入口模型分流并调用原生 replan/重新分类/重审/批准；关系不明时不改当前 task 并先澄清；改变已批准范围或验收的小需求仍属 major；归档/完成任务的后续工作创建新 task；Marketplace 不自行实现语义分类或阶段判断。
- [ ] `index.json` 中四份 workflow 的摘要与源码逐字节匹配。
- [ ] `python3 -B -m unittest discover -s tests -q` 通过；定向 Codex Subnode workflow 测试覆盖整份方案审阅和显式批准约束。
- [ ] 活动 workflow 源中不再把 `trellis-brainstorm` 用作规划入口。

## 范围边界

本任务只维护 Marketplace `main` 的四份 workflow 源和索引。Trellis CLI/模板与去重由 Trellis owner task 维护；根侧组合检查、生成资产和 gitlink 由根协调 task 维护。不得在 Trellis 仓库中复制 Marketplace workflow 源。

<!-- trellis-decisions:v1 -->
```json
{
  "schema_version": 1,
  "decisions": [
    {
      "id": "workflow-change-triage-owner",
      "status": "decided",
      "question": "Marketplace workflow 是否自行判断封口后变化大小？",
      "evidence": ["prd.md#需求", "design.md#封口后变化处理", "Trellis owner task decision post-closure-impact-owner"],
      "answer_or_reason": "不自行分类。所有 workflow 将变化交给唯一规划入口的模型；Marketplace 只说明调用和批准时序，Trellis CLI 只校验显式状态转移。",
      "impact": "保持跨工作流语义单一，避免各模板给出不同的 minor/major 边界。",
      "reopen_when": "Trellis 规划入口的调用合同发生变化，或 Marketplace 来源无法准确表达其原生 replan 边界。"
    },
    {
      "id": "marketplace-minor-major-routing",
      "status": "decided",
      "question": "四类 workflow 如何表达封口后的 minor 与 major 变化？",
      "evidence": ["prd.md#需求", "design.md#封口后变化处理", "Trellis owner task design.md#Post-closure change triage"],
      "answer_or_reason": "独立交付进入独立 task；关联不明且有界核验不能澄清时保持原 task 不变并询问用户；终态 task 不重开。当前 task 中 minor 保持全部承诺，在 execution.md 记录后留在现有生命周期状态继续；改变已批准范围或验收的需求即使很小仍属 major，停止相关实施并由规划入口调用原生 replan 到最早受影响阶段，重新完整审查并取得用户明确批准。",
      "impact": "工作流可继续小幅执行修正，同时避免重大变化继承旧批准。",
      "reopen_when": "Trellis CLI 或规划入口改变 execution ledger 字段、replan 可用来源状态或批准顺序。"
    }
  ]
}
```
