# Local formal handoff contract

Owner: Marketplace main. Coordinator: root task `10-04-cognee-memory-base-removal`.
User approved the complete retirement on 2026-10-04. This repository has no
initialized Trellis task runtime; this owner record does not initialize one.

Scope: update the custom Codex workflow's formal handoff paragraph to the
local JSON/prompt, source seal, and native task ownership contract. Preserve
RecoveryBrief boundaries, workflow phases, dispatch policy, and historical
records. No replacement service is introduced.

Acceptance: source workflow no longer requires a remote proof; Trellis template
regressions and consumer workflow verification validate the released contract.
Source publication and consumer verification are tracked by the coordinator.

Consumer preview rejected the first commit because its index digest had not
been refreshed. Correct the exact index entry, run the existing four planning
and integrity tests, and require native preview/apply/verify at the corrected
immutable commit before accepting consumer delivery.

The corrected source is published at `01aeef87a504bfaf6f9242887bf1e9a60294035f`.
The custom-workflow candidate digest is `4599e2743270da553a25d65509e7a16043b1254e59cb3167afb043315c8ff013`;
native preview/apply/verify passed for both custom consumers, and all seven
project roots passed `trellis workflow --verify` after their native update.
