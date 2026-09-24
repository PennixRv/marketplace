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
