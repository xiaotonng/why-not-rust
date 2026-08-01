import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "why-not-rust"


class PackageLayoutTests(unittest.TestCase):
    def test_standard_skill_package_is_complete(self) -> None:
        required = [
            "SKILL.md",
            "LICENSE",
            "agents/openai.yaml",
            "assets/assessment-template.json",
            "assets/report-template.html",
            "references/case-library.md",
            "references/dimensions.md",
            "references/report-style.md",
            "scripts/decision_math.py",
            "scripts/report_safety.py",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_ROOT / relative).is_file())

    def test_frontmatter_uses_only_supported_top_level_fields(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---\n", 2)[1]
        keys = re.findall(r"^([a-z][a-z0-9_-]*):", frontmatter, flags=re.MULTILINE)
        self.assertEqual(keys, ["name", "description"])
        self.assertRegex(frontmatter, r"(?m)^name: why-not-rust$")
        self.assertEqual(SKILL_ROOT.name, "why-not-rust")

    def test_assessment_template_is_valid_json(self) -> None:
        assessment = json.loads(
            (SKILL_ROOT / "assets" / "assessment-template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(assessment["method"], "why-not-rust/2.0")
        self.assertEqual([gate["id"] for gate in assessment["gates"]], ["G1", "G2", "G3", "G4"])


class DocumentationIntegrityTests(unittest.TestCase):
    def test_case_library_contains_52_cases(self) -> None:
        library = (SKILL_ROOT / "references" / "case-library.md").read_text(encoding="utf-8")
        headings = re.findall(r"^### (?!Challenge )", library, flags=re.MULTILINE)
        self.assertEqual(len(headings), 52)
        sections = re.split(r"^## [1-5] · .*?$", library, flags=re.MULTILINE)[1:5]
        self.assertEqual([len(re.findall(r"^### ", section, flags=re.MULTILINE)) for section in sections], [24, 7, 12, 9])

    def test_readme_relative_links_and_images_exist(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        markdown_targets = re.findall(r"!?(?:\[[^]]*\])\(([^)]+)\)", readme)
        html_images = re.findall(r'<img\s+[^>]*src="([^"]+)"', readme)
        relative_targets = [
            target.split("#", 1)[0]
            for target in [*markdown_targets, *html_images]
            if target and not re.match(r"^[a-z]+://", target)
        ]
        for target in relative_targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).exists())

    def test_removed_index_cannot_reappear_as_an_output(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("rust case index", skill.lower())
        self.assertIn("evidence ledger—not additive points", readme.lower())


if __name__ == "__main__":
    unittest.main()
