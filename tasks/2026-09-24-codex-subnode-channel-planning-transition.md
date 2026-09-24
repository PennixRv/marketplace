# Codex subnode channel planning transition

Target: `workflows/codex-subnode-channel/workflow.md` on
`pennix/v0.7-beta`. Root coordination task:
`.trellis/tasks/09-24-trellis-workflow-planning-transition-regression` in
`codex-workflow-optimization`.

## Contract

- Eligible `analysis_only` tasks finish and archive from `planning` without
  `task.py start`.
- Change-bearing tasks remain in `planning` until required artifacts, Planning
  Seal, and implementation approval are present; then the main session runs the
  native `task.py start` before implementation.
- Phase 1.4 agrees with both state blocks. Preserve the generic rules already
  published at baseline `75842e6cd56237e48d8899bec7036397cb7967ee`.

## Acceptance

- Run `python3 tests/test_codex_subnode_channel_workflow.py` and `git diff
  --check`; review the full workflow diff against the root consumer.
- Push the beta commit and verify the exact remote ref. The consumer refresh
  pins this immutable commit and validates against installed Trellis
  `0.7.0-beta.10`; Marketplace has no npm version to release.
- Roll back with a normal revert to the baseline above if publication must be
  undone; never reset the shared branch.
