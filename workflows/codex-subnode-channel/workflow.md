# Codex Subnode Channel Workflow

---

## Core Contract

1. **Plan before delivery** — define the task, acceptance criteria, and necessary evidence before changing code.
2. **The main session delivers by default** — it owns implementation, task facts, final verification, and Git.
3. **A `subnode` is explicit independent evidence** — use one only when the user expressly needs independently reviewable analysis, design, audit, review, counterargument, or verification. It is never the automatic implementation or checking path.
4. **Artifacts are durable** — the coordinator creates an immutable `brief.json`; the subnode appends its `worklog.md` and writes one pending-review `report.json` under the active task.
5. **Completion is not acceptance** — the coordinator validates the report, rechecks material sources and protected targets, then records `accepted`, `rejected`, or `deferred` with its reason.
6. **Channel is the lifecycle surface** — use its native create, spawn, send, and wait protocol. Wait for events rather than high-frequency polling; do not create a second waiter, use terminal JSON as the report, or add automatic retry/scheduling.

This workflow assumes Codex's default `codex.dispatch_mode: inline`. Do not
select `auto` or `sub-agent` for this workflow: those modes seed native-agent
context and belong to the Native Trellis Workflow instead.

## Trellis System

### Task And Spec Records

Keep requirements, research, plans, review conclusions, and acceptance evidence
in the current task. Read relevant package and layer guidance before editing:

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
python3 ./.trellis/scripts/task.py current --source
```

Create a task only after the user has approved task creation. A task may be
PRD-only when lightweight; complex work also needs `design.md` and
`implement.md` before it starts.

When research, audit, or review establishes task-relevant verified facts,
candidates, uncertainty, or a decision basis that should persist, use
`trellis-research-record` to write the conclusion with its evidence in the
active task. Do not create a record for routine navigation or transient output.

### Semantic RecoveryBrief

Trellis task artifacts remain the semantic record. Use the low-level
`ctx_recovery_brief` provider only after task start, after `trellis-check`
confirms a material recorded change, immediately before an explicit formal
handoff or user-requested pause/finish, or on an explicit inspect, repair, or
force-refresh request. Derive any CAS update from verified task evidence; do
not write one for ordinary edits, tests, diffs, compaction, resume, or a
subnode event/report. For an explicitly user-requested formal handoff, a valid
task-local Brief is evidence only; receipt validation and new-session task
restoration remain authoritative.

### Independent Evidence

For an explicit independent-evidence request, first load `trellis-channel` and
follow its `subnode-work` reference. It defines the brief schema, safe artifact
initialization, role prompt, native wait protocol, report validation, and
counterwork. The coordinator may create a bounded subnode while the task is
`planning` or `in_progress`.

The subnode may inspect the necessary current project, external sources, and
internet evidence. It may write only its assigned `worklog.md` and
`report.json`; it must not change protected targets, task facts, Git state, or
worker lifecycle. The final Channel message is a short status and report path,
not the report payload.

Use `workspace_note.py` only for a durable cross-task observation, decision,
open question, or blocker. It is separate from task and subnode evidence.

---

## Phase Index

```text
Phase 1: Plan    -> classify, create approved task, establish requirements and evidence needs
Phase 2: Execute -> main-session delivery; optional explicit subnode evidence
Phase 3: Finish  -> verify, retain conclusions, update specs, commit, and wrap up
```

### Request Triage

- Simple conversation or a small task: ask only whether to create a Trellis task.
- Complex work: create a task after approval, then complete planning before implementation.
- Task-creation approval is not implementation approval.
- Do not create a subnode merely because work is broad or inconvenient. State the independent question, reason, evidence method, scope, and stop condition first; use the main session when independent evidence adds no decision value.

### Planning Artifacts

- `prd.md` — requirements, constraints, and acceptance criteria.
- `design.md` — boundaries, data flow, contracts, and tradeoffs for complex work.
- `implement.md` — ordered execution, validation, and rollback plan for complex work.
- `research/` — attributable external or local findings.
- `subnodes/<work-id>/<subnode-id>/` — a coordinator brief, append-only node worklog, and pending-review report when independent evidence was expressly requested.

[workflow-state:no_task]
No active task. Classify the request and obtain task-creation approval before creating a task. Do not implement, spawn a subnode, or promote an unrecorded conclusion as task fact.
[/workflow-state:no_task]

[workflow-state:task_error]
The active task record cannot be read. Do not create or activate another task. Repair the current task record while preserving existing artifacts, or ask the user when its status cannot be determined safely.
[/workflow-state:task_error]

[workflow-state:planning]
Stay in planning. Create or refine the required planning artifacts and record research. The main session performs ordinary work directly. A subnode is allowed only for a user-requested independent-evidence question with a frozen brief and durable task artifact path; report status is never acceptance.
[/workflow-state:planning]

[workflow-state:planning-inline]
Stay in planning. Create or refine the required planning artifacts and record research. The main session performs ordinary work directly. A subnode is allowed only for a user-requested independent-evidence question with a frozen brief and durable task artifact path; report status is never acceptance.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Deliver and verify in the main session. Before code changes, load `trellis-before-dev`; after changes, use `trellis-check` and the task acceptance criteria. Invoke a Channel subnode only for explicit independent evidence, then validate its report and recheck sources before recording a disposition. The main session alone commits and finishes.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Deliver and verify in the main session. Before code changes, load `trellis-before-dev`; after changes, use `trellis-check` and the task acceptance criteria. Invoke a Channel subnode only for explicit independent evidence, then validate its report and recheck sources before recording a disposition. The main session alone commits and finishes.
[/workflow-state:in_progress-inline]

[workflow-state:completed]
The task is complete only after required verification, decision records, and Git work are complete. Use `trellis-finish-work` to wrap up; return to the appropriate phase if the working tree or acceptance evidence is incomplete.
[/workflow-state:completed]

---

## Phase 1: Plan

#### 1.0 Create Task `[required · once]`

After user approval, create the task and record its scope, actual modification
target, constraints, and acceptance criteria. Do not treat task creation as
permission to implement.

#### 1.1 Requirements And Design `[required · repeatable]`

Write `prd.md`; add `design.md` and `implement.md` when the task is complex.
Resolve only unknowns that can change scope, risk, modification path, or
acceptance. Keep alternatives as alternatives until the user selects one or
evidence justifies a decision.

#### 1.2 Research `[optional · repeatable]`

Perform ordinary local and external research in the main session and write
material findings to `research/`. When the user expressly needs independent
evidence, define one narrow `subnode` brief and use the installed
`trellis-channel` reference. Preserve both the report and the coordinator's
later decision; do not substitute a Channel message for either record.

#### 1.3 Prepare Execution `[required · once]`

Confirm the direct implementation and verification path. This workflow uses
inline Codex execution: do not curate native-agent JSONL or dispatch native
implementation/check workers. Plan any optional subnode as evidence work with
protected targets, an independence reason, evidence method, stop conditions,
and a deadline.

#### 1.4 Activate Task `[required · once]`

Review the planning artifacts, then start the task. A lightweight task needs a
complete PRD; a complex task also needs its design and implementation plan.

#### 1.5 Completion Criteria

Before Phase 2, ensure that the modification target, acceptance criteria,
validation commands, and known risks are explicit. For a planned subnode,
ensure the question is independent and bounded rather than a proxy for normal
implementation or review.

---

## Phase 2: Execute

#### 2.1 Implement `[required · repeatable]`

The main session loads `trellis-before-dev`, reads the reviewed task artifacts,
implements the approved scope, and records relevant findings. Do not expand the
change for hypothetical future needs.

When a user explicitly requests independent evidence, the coordinator creates
the artifact brief before spawning `subnode` through Trellis Channel. The node
does not implement business changes. After its native terminal event, validate
the report and independently recheck enough evidence to decide its disposition.

#### 2.2 Quality Check `[required · repeatable]`

The main session runs the task's relevant checks and `trellis-check`, then
addresses verified issues. An optional counter-subnode is appropriate only when
the evidence is consequential and a distinct lens can materially challenge the
primary report; it is never automatic.

#### 2.3 Rollback `[on demand]`

If verification or evidence disproves the selected approach, record the reason,
restore the smallest correct state, and return to the relevant planning or
implementation step. Do not hide a retracted conclusion by rewriting a
subnode worklog or report history.

---

## Phase 3: Finish

#### 3.2 Debug Retrospective `[on demand]`

For repeated failures, use `trellis-break-loop` to identify the root cause and
the missing prevention rule. Keep the retrospective proportional to the actual
failure mode.

#### 3.3 Update Spec `[required · once]`

Use `trellis-update-spec` only when the task established a reusable contract,
convention, or prevention rule. Keep task-specific evidence in the task rather
than inflating permanent specifications.

#### 3.4 Commit Changes `[required · once]`

After required checks pass, review the diff, retain task and decision records,
and create the scoped commit. The main session owns all Git operations.

#### 3.5 Wrap Up `[required · once]`

Use `trellis-finish-work` to report checks, remaining risks, and task state.
Do not claim complete until the evidence and verification appropriate to the
task are actually recorded.
