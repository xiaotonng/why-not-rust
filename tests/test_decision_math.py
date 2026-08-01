import json
import math
import subprocess
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "why-not-rust" / "scripts"))

from decision_math import amdahl, break_even_months, with_target  # noqa: E402


class AmdahlTests(unittest.TestCase):
    def test_zero_kernel_share_cannot_speed_up_product(self) -> None:
        result = amdahl(0.0, 20.0)
        self.assertEqual(result.end_to_end_speedup, 1.0)
        self.assertEqual(result.infinite_kernel_ceiling, 1.0)

    def test_whole_product_kernel_tracks_kernel_speedup(self) -> None:
        result = amdahl(1.0, 10.0)
        self.assertAlmostEqual(result.end_to_end_speedup, 10.0)
        self.assertTrue(math.isinf(result.infinite_kernel_ceiling))

    def test_no_kernel_improvement_means_no_product_improvement(self) -> None:
        result = amdahl(0.6, 1.0)
        self.assertAlmostEqual(result.end_to_end_speedup, 1.0)

    def test_infinite_kernel_speed_respects_unaffected_share(self) -> None:
        result = amdahl(0.31, math.inf)
        self.assertAlmostEqual(result.end_to_end_speedup, 1.0 / 0.69)
        self.assertAlmostEqual(result.infinite_kernel_ceiling, 1.0 / 0.69)

    def test_boundary_cost_reduces_speedup_and_ceiling(self) -> None:
        result = amdahl(0.5, 10.0, 0.1)
        self.assertAlmostEqual(result.end_to_end_speedup, 1.0 / 0.65)
        self.assertAlmostEqual(result.infinite_kernel_ceiling, 1.0 / 0.6)

    def test_impossible_target_is_explicit(self) -> None:
        result = with_target(amdahl(0.31, 20.0), 4.0)
        self.assertFalse(result.target_physically_possible)
        self.assertFalse(result.target_met_by_candidate)

    def test_physically_possible_target_can_still_miss_candidate(self) -> None:
        result = with_target(amdahl(0.5, 1.1), 1.5)
        self.assertTrue(result.target_physically_possible)
        self.assertFalse(result.target_met_by_candidate)

    def test_invalid_inputs_are_rejected(self) -> None:
        for args in [
            (-0.1, 2.0, 0.0),
            (1.1, 2.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.5, math.nan, 0.0),
            (0.5, 2.0, -0.1),
            (0.5, 2.0, math.nan),
        ]:
            with self.assertRaises(ValueError):
                amdahl(*args)

    def test_cli_emits_strict_json_for_unbounded_values(self) -> None:
        script = Path(__file__).resolve().parents[1] / "skills" / "why-not-rust" / "scripts" / "decision_math.py"
        result = subprocess.run(
            [sys.executable, str(script), "amdahl", "--share", "1", "--kernel-speedup", "inf", "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["kernel_speedup"], "unbounded")
        self.assertEqual(payload["end_to_end_speedup"], "unbounded")

    def test_cli_rejects_nan_and_candidate_target_miss(self) -> None:
        script = Path(__file__).resolve().parents[1] / "skills" / "why-not-rust" / "scripts" / "decision_math.py"
        nan_result = subprocess.run(
            [sys.executable, str(script), "amdahl", "--share", ".5", "--kernel-speedup", "nan", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(nan_result.returncode, 0)
        miss_result = subprocess.run(
            [sys.executable, str(script), "amdahl", "--share", ".5", "--kernel-speedup", "1.1", "--target", "1.5"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(miss_result.returncode, 2)
        self.assertIn("candidate MISSES", miss_result.stdout)


class BreakEvenTests(unittest.TestCase):
    def test_break_even_uses_net_monthly_savings(self) -> None:
        self.assertEqual(break_even_months(120.0, 20.0, 5.0), 8.0)

    def test_no_positive_savings_never_breaks_even(self) -> None:
        self.assertTrue(math.isinf(break_even_months(100.0, 10.0, 10.0)))

    def test_non_finite_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            break_even_months(math.nan, 10.0, 0.0)


if __name__ == "__main__":
    unittest.main()
