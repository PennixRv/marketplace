#!/usr/bin/env python3
"""Guard the published planning transition contract."""

from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / "workflows/codex-subnode-channel/workflow.md"
).read_text(encoding="utf-8")


class PlanningTransitionTests(unittest.TestCase):
    def test_planning_blocks_and_activation_agree(self) -> None:
        for state in ("planning", "planning-inline"):
            with self.subTest(state=state):
                body = WORKFLOW.split(f"[workflow-state:{state}]\n", 1)[1].split(
                    f"[/workflow-state:{state}]", 1
                )[0]
                self.assertIn('delivery_mode = "analysis_only"', body)
                self.assertIn("archive without running `task.py start`", body)
                self.assertIn("change-bearing task", body)
                self.assertIn("Planning Seal is closed", body)
                self.assertIn("user approves implementation", body)
                self.assertIn("native `python3 ./.trellis/scripts/task.py start", body)
                self.assertNotIn("Stay in planning. Create or refine", body)

    def test_subnode_profile_contract_is_explicit(self) -> None:
        for profile in (
            "code_path",
            "docs_source",
            "fault_diagnosis",
            "correctness_test",
            "security_permission",
            "architecture_compat",
            "requirements_assumption",
            "ux_accessibility",
            "evidence_synthesis",
        ):
            self.assertIn(f"`{profile}`", WORKFLOW)
        for phrase in (
            ".trellis/agents/subnode-profiles.json",
            "gpt-6-sol",
            "single-dispatch override",
            "symlinked",
            "never silently fall back",
            "--reasoning-effort-reason",
            "profile configuration relative path and SHA-256 digest",
            "durable `spawned` event",
        ):
            self.assertIn(phrase, WORKFLOW)

    def test_fifo_queue_contract_is_explicit(self) -> None:
        for phrase in (
            "queue init",
            "queue validate",
            "queue.json",
            "dispatch-claim.json",
            "native `channel spawn`/`send`",
            "native Channel waiter after a durable barrier",
            "complete report with no validator concerns",
            "matching source",
            "target recheck",
            "`accepted` disposition",
            "An abandoned queue cannot claim further work",
            "partition every queued ID",
            "claim-mismatched ranges",
            "high-frequency polling",
            "resident scheduler",
        ):
            self.assertIn(phrase, WORKFLOW)

        phase = " ".join(
            WORKFLOW.split("#### 1.4 Activate Task", 1)[1]
            .split("#### 1.5 Completion Criteria", 1)[0]
            .split()
        )
        for phrase in (
            "change-bearing tasks only",
            "Planning Seal",
            "user approves implementation",
            "task.py start <task-dir>",
            "analysis_only",
            "without start",
        ):
            self.assertIn(phrase, phase)


if __name__ == "__main__":
    unittest.main()
