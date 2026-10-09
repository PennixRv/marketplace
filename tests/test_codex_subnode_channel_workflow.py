#!/usr/bin/env python3
"""Guard the published planning transition contract."""

import hashlib
import json
from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / "workflows/codex-subnode-channel/workflow.md"
).read_text(encoding="utf-8")


class PlanningTransitionTests(unittest.TestCase):
    def test_marketplace_index_matches_workflow_bytes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        index = json.loads((root / "index.json").read_text(encoding="utf-8"))
        template = next(
            item for item in index["templates"]
            if item["id"] == "codex-subnode-channel"
        )
        self.assertEqual(
            hashlib.sha256((root / template["path"]).read_bytes()).hexdigest(),
            template["sha256"],
        )

    def test_planning_blocks_and_activation_agree(self) -> None:
        for state in ("planning", "planning-inline"):
            with self.subTest(state=state):
                body = WORKFLOW.split(f"[workflow-state:{state}]\n", 1)[1].split(
                    f"[/workflow-state:{state}]", 1
                )[0]
                self.assertIn('delivery_mode = "analysis_only"', body)
                self.assertIn("regardless of complexity or cross-owner scope", body)
                self.assertIn("archive without running `task.py start`", body)
                self.assertIn("freeze the dispatch plan in task artifacts", body)
                self.assertIn("explicit user approval", body)
                self.assertIn("only the listed evidence work", body)
                self.assertIn("change-bearing task", body)
                self.assertIn("Planning Seal is closed", body)
                self.assertIn("user approves implementation", body)
                self.assertIn("native `python3 ./.trellis/scripts/task.py start", body)
                self.assertNotIn("Stay in planning. Create or refine", body)

    def test_in_progress_amendment_boundary_is_explicit(self) -> None:
        normalized_workflow = " ".join(WORKFLOW.split())
        for phrase in (
            "An explicitly user-requested addition to an `in_progress` task",
            "same actual owner and",
            "deployment/release path",
            "authorizes only that exact addition",
            "If any condition is false or",
            "record `decision-needed`",
            "native `task.py replan`",
        ):
            self.assertIn(phrase, normalized_workflow)

        for state in ("in_progress", "in_progress-inline"):
            body = WORKFLOW.split(f"[workflow-state:{state}]\n", 1)[1].split(
                f"[/workflow-state:{state}]", 1
            )[0]
            self.assertIn("bounded, explicitly user-requested amendment", body)
            self.assertIn("amendment condition is false or unclear", body)

    def test_progressive_decision_entry_and_execution_escalation(self) -> None:
        # Prompt contract only; does not claim live model behavior.
        for phrase in ("one material choice is sufficient", "dependency-ready", "then impact/priority", "missing evidence, not a closed plan", "blocking question tool", "immediately explain its impact"):
            self.assertIn(phrase, WORKFLOW)

    def test_subnode_profile_contract_is_preserved(self) -> None:
        for profile in (
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
            "gpt-6.1-sol",
            "gpt-5.6-luna",
            "single-dispatch override",
            "symlinked",
            "never silently fall back",
            "--reasoning-effort-reason",
            "profile configuration relative path and SHA-256 digest",
            "durable `spawned` event",
        ):
            self.assertIn(phrase, WORKFLOW)

        self.assertNotIn("| `code_path` |", WORKFLOW)
        self.assertIn("`code_path` is not a shipped preset", WORKFLOW)
        self.assertIn("| `docs_source` | `xhigh` |", WORKFLOW)
        self.assertIn("`max` is outside the current Trellis effort contract", WORKFLOW)

    def test_fifo_queue_contract_is_explicit(self) -> None:
        for phrase in (
            "queue init",
            "queue validate",
            "queue.json",
            "dispatch-claim.json",
            "native `channel spawn`/`send`",
            "native Channel waiter after a durable barrier",
            "complete report without validator concerns",
            "source/protected-target recheck",
            "healthy live predecessors do not block a refill",
            "multi-target-dispatch.md",
            "`accepted` disposition",
            "An abandoned queue cannot claim further work",
            "partition every queued ID",
            "claim-mismatched ranges",
            "high-frequency polling",
            "resident scheduler",
        ):
            self.assertIn(phrase, WORKFLOW)

        fifo = WORKFLOW.split("### Persistent FIFO Dispatch Queue", 1)[1].split("## Plan Approval", 1)[0]
        self.assertNotIn("all earlier items are accepted", fifo)

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
