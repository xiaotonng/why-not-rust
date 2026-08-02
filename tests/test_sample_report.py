import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from render_sample import render, render_quick  # noqa: E402


class SampleReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = render()
        cls.committed = (ROOT / "examples" / "sample-report.html").read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/json" id="why-not-rust-assessment">\s*(.*?)\s*</script>',
            cls.rendered,
            flags=re.DOTALL,
        )
        if match is None:
            raise AssertionError("embedded assessment record is missing")
        cls.assessment = json.loads(match.group(1))

    def test_committed_report_is_golden_output(self) -> None:
        self.assertEqual(self.committed, self.rendered)

    def test_no_template_tokens_remain(self) -> None:
        self.assertNotIn("{{", self.rendered)

    def test_embedded_assessment_is_valid_and_complete(self) -> None:
        assessment = self.assessment
        self.assertEqual(assessment["method"], "why-not-rust/2.0")
        self.assertEqual(len(assessment["gates"]), 4)
        self.assertEqual([lens["id"] for lens in assessment["lenses"]], [f"D{i}" for i in range(1, 13)])
        self.assertTrue(assessment["math"]["amdahl"]["target_physically_possible"])
        self.assertTrue(assessment["math"]["amdahl"]["target_met_by_candidate"])

    def test_selected_option_and_gates_are_machine_checkable(self) -> None:
        assessment = self.assessment
        selected_id = assessment["decision"]["selected_option_id"]
        selected = [option for option in assessment["options"] if option["disposition"] == "selected"]
        self.assertEqual([option["id"] for option in selected], [selected_id])
        self.assertTrue(all(gate["option_id"] == selected_id for gate in assessment["gates"]))
        self.assertTrue(all(option["target"] for option in assessment["options"]))
        row = re.search(r'<tr class="selected">.*?</tr>', self.rendered, flags=re.DOTALL)
        self.assertIsNotNone(row, "the selected option must be highlighted in the table")
        self.assertIn(selected[0]["name"], row.group(0))

    def test_machine_record_preserves_method_precedents_path_and_challenges(self) -> None:
        assessment = self.assessment
        self.assertEqual(assessment["analysis"]["mode"], "synthetic-golden")
        self.assertEqual(assessment["analysis"]["user_supplied_facts"], [])
        precedent_fields = {"name", "outcome", "match", "mismatch", "workload_regime", "source_class", "url"}
        self.assertTrue(all(precedent_fields <= precedent.keys() for precedent in assessment["precedents"]))
        path_fields = {"step", "title", "owner", "cost_range", "artifact", "acceptance", "deadline_or_stop", "rollback"}
        self.assertTrue(all(path_fields <= item.keys() and all(item[field] for field in path_fields) for item in assessment["path"]))
        for side in ("migration_case", "staying_case"):
            self.assertTrue(all(item["state"] in {"HIT", "PASS", "UNKNOWN"} for item in assessment["challenge_audit"][side]))

    def test_time_target_and_boundary_threshold_are_conservative(self) -> None:
        target_speedup = self.assessment["math"]["amdahl"]["target_speedup"]
        self.assertGreaterEqual(target_speedup, 3.8 / 2.4)
        lower_candidate_speedup_at_three_percent = 1.70
        maximum_boundary = 1 / target_speedup - (1 / lower_candidate_speedup_at_three_percent - 0.03)
        self.assertGreaterEqual(maximum_boundary, 0.07)
        self.assertIn("≤7% boundary cost", self.rendered)

    def test_visible_trigger_matches_machine_record(self) -> None:
        self.assertIn(self.assessment["decision"]["change_trigger"], self.rendered)

    def test_quick_mode_has_contiguous_sections(self) -> None:
        quick = render_quick()
        numbers = re.findall(r'<span class="no">(\d\d)</span>', quick)
        self.assertEqual(numbers, ["01", "02", "03", "04"])
        self.assertNotIn("Evidence ledger", quick)
        self.assertNotIn("Who has done this before", quick)

    def test_report_is_visibly_synthetic(self) -> None:
        self.assertGreaterEqual(self.rendered.lower().count("synthetic"), 10)


if __name__ == "__main__":
    unittest.main()
