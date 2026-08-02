"""Regression tests for the published case-study reports in examples/.

These guard the artifacts the README links to: every case module must still
render byte-identically to its committed HTML, obey the report-style contract,
and keep its Amdahl figures reproducible from the skill's own calculator.
"""

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
sys.path.insert(0, str(ROOT / "skills" / "why-not-rust" / "scripts"))

from build_cases import CASES_DIR, en, load_case, render, resolve_math  # noqa: E402
from decision_math import amdahl, with_target  # noqa: E402

# Desktop applications: the batch about teams who believed a rewrite was the answer.
DESKTOP_SLUGS = {
    "bitwarden-desktop", "fish-shell", "ghostty", "keepassxc", "lapce",
    "remacs", "signal-desktop", "spacedrive", "xi-editor", "zed",
}
# Systems and developer tooling: the original batch.
SYSTEMS_SLUGS = {
    "bun", "coreutils", "curl", "esbuild", "ffmpeg",
    "flake8", "openssl", "prisma-engines", "redis", "sqlite",
}
EXPECTED_SLUGS = DESKTOP_SLUGS | SYSTEMS_SLUGS
SCOPE_WORDS = {"STAY", "EXTRACT", "PARTIAL", "MIGRATE"}
AUTHORIZATIONS = {"APPROVE", "REJECT", "DEFER–MEASURE"}
RUST_IMPL = {"rust"}
CURRENT_IMPL = {"current", "external", "non-rust-native"}


def case_modules() -> list[Path]:
    return sorted(p for p in CASES_DIR.glob("*.py") if not p.name.startswith("_"))


class CaseReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = {}
        for path in case_modules():
            case = load_case(path)
            cls.cases[case["slug"]] = case

    def test_expected_case_set_is_present(self) -> None:
        # Guards against silently dropping a published case. While a new batch is
        # being authored this fails until every module has landed, which is the
        # intended signal: add the module, do not shorten the list.
        self.assertEqual(set(self.cases), EXPECTED_SLUGS)

    def test_committed_html_is_golden_output(self) -> None:
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                committed = ROOT / "examples" / f"{slug}-why-not-rust.html"
                self.assertTrue(committed.exists(), f"{committed.name} is not committed")
                self.assertEqual(committed.read_text(encoding="utf-8"), render(case))

    def test_no_template_tokens_and_one_inert_script(self) -> None:
        for slug in self.cases:
            with self.subTest(slug=slug):
                html = (ROOT / "examples" / f"{slug}-why-not-rust.html").read_text(encoding="utf-8")
                self.assertNotIn("{{", html)
                # The only <script> is the inert assessment record; the theme
                # toggle is an inline handler in the template, not a script tag.
                self.assertEqual(html.count("<script"), 1)
                self.assertIn('type="application/json"', html)

    def test_embedded_assessment_matches_the_visible_decision(self) -> None:
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                html = (ROOT / "examples" / f"{slug}-why-not-rust.html").read_text(encoding="utf-8")
                match = re.search(
                    r'<script type="application/json" id="why-not-rust-assessment">\s*(.*?)\s*</script>',
                    html,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(match, "embedded assessment record is missing")
                record = json.loads(match.group(1))
                self.assertEqual(record["method"], "why-not-rust/2.0")
                self.assertIn(record["decision"]["scope"], SCOPE_WORDS)
                self.assertIn(record["decision"]["authorization"], AUTHORIZATIONS)
                self.assertEqual(record["decision"]["scope"], case["scope_word"])
                self.assertEqual(record["decision"]["authorization"], case["auth"])
                self.assertEqual(len(record["gates"]), 4)
                selected = record["decision"]["selected_option_id"]
                self.assertEqual({g["option_id"] for g in record["gates"]}, {selected})
                picked = [o["id"] for o in record["options"] if o["disposition"] == "selected"]
                self.assertEqual(picked, [selected])
                self.assertTrue(record["repository"]["commit"])

    def test_all_twelve_lenses_are_covered(self) -> None:
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                ids = [lens["id"] for lens in case["lenses"]]
                self.assertEqual(
                    sorted(set(ids), key=lambda x: int(x[1:])),
                    [f"D{i}" for i in range(1, 13)],
                )

    def test_a_repeated_lens_argues_both_ways(self) -> None:
        """One lens may carry two entries, but only to show opposing evidence.

        remacs splits D6 into the collector (DISFAVORS) and the clean seams
        (SUPPORTS). That is the method working. Two entries under one id with
        the same state is a copy-paste, so the states must differ.
        """
        for slug, case in self.cases.items():
            by_id: dict[str, list[str]] = {}
            for lens in case["lenses"]:
                by_id.setdefault(lens["id"], []).append(lens["state"])
            for lens_id, states in by_id.items():
                if len(states) > 1:
                    with self.subTest(slug=slug, lens=lens_id):
                        self.assertEqual(
                            len(states), len(set(states)),
                            f"{slug}: {lens_id} repeats a state — a split lens must "
                            "argue different directions",
                        )

    def test_every_case_pins_a_full_commit_sha(self) -> None:
        """A short hash is ambiguous, and the record exists to be reproducible."""
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                commit = case["repository"]["commit"]
                self.assertRegex(
                    commit, r"^[0-9a-f]{40}$",
                    f"{slug}: pin the full 40-character SHA, not {commit!r}",
                )

    def test_lens_colour_class_matches_the_option_family(self) -> None:
        """CSS classes name the option family, never the direction of the evidence."""
        for slug, case in self.cases.items():
            impl = {o["id"]: o["implementation"] for o in case["options"]}
            for lens in case["lenses"]:
                with self.subTest(slug=slug, lens=lens["id"]):
                    state, css = lens["state"], lens["css"]
                    families = {impl[i] for i in lens["option_ids"]}
                    if state == "UNKNOWN":
                        self.assertEqual(css, "unknown")
                    elif state in {"NEUTRAL", "N/A"}:
                        self.assertEqual(css, "neutral")
                    elif families and families <= RUST_IMPL:
                        self.assertEqual(css, "rust")
                    elif families and families <= CURRENT_IMPL:
                        self.assertEqual(css, "current")

    def test_amdahl_figures_reproduce_from_the_calculator(self) -> None:
        for slug, case in self.cases.items():
            spec = case.get("amdahl")
            if spec is None:
                continue
            with self.subTest(slug=slug):
                expected = with_target(
                    amdahl(spec["share"], spec["kernel_speedup"], spec.get("boundary", 0.0)),
                    spec.get("target"),
                )
                produced = resolve_math(case)["amdahl"]
                self.assertEqual(produced["end_to_end_speedup"], expected.end_to_end_speedup)
                self.assertEqual(produced["target_speedup"], expected.target_speedup)
                self.assertEqual(
                    produced["target_met_by_candidate"], expected.target_met_by_candidate
                )

    def test_no_impossible_acceptance_threshold_is_presented_as_reachable(self) -> None:
        for slug, case in self.cases.items():
            spec = case.get("amdahl")
            if spec is None or spec.get("target") is None:
                continue
            with self.subTest(slug=slug):
                produced = resolve_math(case)["amdahl"]
                if produced["target_met_by_candidate"] is False:
                    # The report must say so rather than quietly implying the target is met.
                    self.assertTrue(
                        any(
                            lens["state"] in {"DISFAVORS", "UNKNOWN"}
                            for lens in case["lenses"]
                            if lens["id"] == "D2"
                        ),
                        "D2 must record a missed or unknown target when the math says MISSES",
                    )

    def test_every_case_discloses_gaps_and_assumptions(self) -> None:
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                self.assertGreaterEqual(len(case["gaps"]), 3)
                self.assertGreaterEqual(len(case["assumptions"]), 2)
                self.assertEqual(len(case["migration_checks"]), 5)
                self.assertEqual(len(case["staying_checks"]), 5)
                # These three may ship as (english, chinese) pairs; the record keeps English.
                disclosure = en(case["method_title"]) + en(case["method_body"]) + en(case["footer"])
                self.assertIn("commit", disclosure)

    def test_every_case_ships_both_languages(self) -> None:
        """A published case must be readable in English and in Chinese."""
        for slug in self.cases:
            with self.subTest(slug=slug):
                html = (ROOT / "examples" / f"{slug}-why-not-rust.html").read_text(encoding="utf-8")
                english = html.count('data-l="en"')
                chinese = html.count('data-l="zh"')
                self.assertEqual(english, chinese, "every English span needs a Chinese sibling")
                # The shared label set alone is ~37 pairs; a real translation is far more.
                self.assertGreater(chinese, 120, f"{slug} looks only partly translated")
                self.assertIn('data-lang="en"', html, "the language switch needs a starting value")

    def test_machine_record_stays_english(self) -> None:
        """The embedded assessment is a data record, not a bilingual document."""
        cjk = re.compile(r"[\u4e00-\u9fff]")
        for slug in self.cases:
            with self.subTest(slug=slug):
                html = (ROOT / "examples" / f"{slug}-why-not-rust.html").read_text(encoding="utf-8")
                record = re.search(
                    r'<script type="application/json" id="why-not-rust-assessment">\s*(.*?)\s*</script>',
                    html, flags=re.DOTALL,
                ).group(1)
                self.assertIsNone(cjk.search(record), "the assessment record must stay English")

    def test_path_steps_read_as_prose(self) -> None:
        """Steps carry an authored passage, not a dump of labelled fields."""
        for slug, case in self.cases.items():
            for i, step in enumerate(case["path"]):
                with self.subTest(slug=slug, step=i + 1):
                    self.assertIn("body", step, "each step needs an authored body")
                    body = en(step["body"])
                    for label in ("Owner:", "Artifact:", "Acceptance:", "Rollback:"):
                        self.assertNotIn(label, body, "the labelled field dump is not prose")
                    for field in ("owner", "artifact", "acceptance", "stop", "rollback"):
                        self.assertTrue(step[field], f"{field} still feeds the machine record")

    def test_verdict_obeys_the_decision_table(self) -> None:
        """Gates are non-compensatory, so authorization cannot contradict them.

        The table in references/dimensions.md pairs APPROVE only with EXTRACT,
        PARTIAL or MIGRATE, and every row yielding STAY with REJECT or
        DEFER-MEASURE. The invariant underneath: you cannot approve a scope with
        a gate that failed, and you cannot reject one where every gate passed.
        """
        for slug, case in self.cases.items():
            with self.subTest(slug=slug):
                states = {g["id"]: g["state"] for g in case["gates"]}
                all_pass = set(states.values()) == {"PASS"}
                # Every gate in the record is bound to the selected option, so a
                # non-STAY scope is a recommendation to adopt Rust at that scope
                # and the option must have cleared all four gates. Recording a
                # FAIL against the option you are recommending is incoherent,
                # including under the "reduce to a smaller option" row, which
                # requires that smaller option's delivery gate to pass.
                self.assertEqual(
                    case["scope_word"] == "STAY", case["auth"] != "APPROVE",
                    f'{slug}: {case["scope_word"]}/{case["auth"]} — a non-STAY scope '
                    "is an adoption recommendation and must be APPROVE",
                )
                if case["auth"] == "APPROVE":
                    self.assertTrue(all_pass, f"{slug}: APPROVE needs all four gates to pass")
                    self.assertNotEqual(
                        case["scope_word"], "STAY",
                        f"{slug}: APPROVE never pairs with STAY — grade the gates "
                        "against the Rust proposal, not the status quo",
                    )
                else:
                    self.assertFalse(
                        all_pass,
                        f'{slug}: {case["auth"]} requires a gate that did not pass',
                    )
                if case["auth"] == "DEFER–MEASURE":
                    self.assertIn(
                        "UNKNOWN", states.values(),
                        f"{slug}: DEFER-MEASURE means a decisive gate is UNKNOWN",
                    )

    def test_verdict_spread_proves_the_method_is_not_one_sided(self) -> None:
        authorizations = {c["auth"] for c in self.cases.values()}
        scopes = {c["scope_word"] for c in self.cases.values()}
        self.assertEqual(scopes, SCOPE_WORDS, "the published set must cover every scope word")
        self.assertEqual(
            authorizations, AUTHORIZATIONS, "the published set must cover every authorization"
        )


if __name__ == "__main__":
    unittest.main()
