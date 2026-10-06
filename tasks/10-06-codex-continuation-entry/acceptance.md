# Acceptance

2026-10-06: four published workflow variants now reference pennix-decision-grill; the selected codex-subnode-channel workflow reuses current/compacted checkpoints and prohibits replaying consumed input while retaining native ownership checks. Native workflow mirror matches the Trellis source. No task/runtime/deployment changes.

Validation: git diff --check; Trellis's 23 workflow integration tests plus workflow-resolver/phase-state suites passed in the 2,209-passing CLI suite. New selected-workflow provenance will use this published functional commit through native consumer commands. Existing continuous user authorization covers commit/push and landing.
