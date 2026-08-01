#!/usr/bin/env python3
"""Small deterministic calculators for why-not-rust decision reports."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AmdahlResult:
    kernel_share: float
    kernel_speedup: float
    boundary_cost_share: float
    end_to_end_speedup: float
    infinite_kernel_ceiling: float
    target_speedup: float | None
    target_physically_possible: bool | None
    target_met_by_candidate: bool | None


def amdahl(kernel_share: float, kernel_speedup: float, boundary_cost_share: float = 0.0) -> AmdahlResult:
    """Return end-to-end speedup with added boundary cost in baseline-time units."""
    if not math.isfinite(kernel_share) or not 0.0 <= kernel_share <= 1.0:
        raise ValueError("kernel_share must be between 0 and 1")
    if math.isnan(kernel_speedup) or kernel_speedup <= 0.0:
        raise ValueError("kernel_speedup must be greater than 0 (positive infinity is allowed)")
    if not math.isfinite(boundary_cost_share) or boundary_cost_share < 0.0:
        raise ValueError("boundary_cost_share must be non-negative")

    denominator = (1.0 - kernel_share) + kernel_share / kernel_speedup + boundary_cost_share
    end_to_end = math.inf if denominator == 0.0 else 1.0 / denominator
    ceiling_denominator = (1.0 - kernel_share) + boundary_cost_share
    ceiling = math.inf if ceiling_denominator == 0.0 else 1.0 / ceiling_denominator
    return AmdahlResult(
        kernel_share=kernel_share,
        kernel_speedup=kernel_speedup,
        boundary_cost_share=boundary_cost_share,
        end_to_end_speedup=end_to_end,
        infinite_kernel_ceiling=ceiling,
        target_speedup=None,
        target_physically_possible=None,
        target_met_by_candidate=None,
    )


def with_target(result: AmdahlResult, target_speedup: float | None) -> AmdahlResult:
    if target_speedup is None:
        return result
    if not math.isfinite(target_speedup) or target_speedup <= 0.0:
        raise ValueError("target_speedup must be a finite value greater than 0")
    return AmdahlResult(
        **{
            **asdict(result),
            "target_speedup": target_speedup,
            "target_physically_possible": target_speedup <= result.infinite_kernel_ceiling,
            "target_met_by_candidate": target_speedup <= result.end_to_end_speedup,
        }
    )


def break_even_months(one_time_cost: float, monthly_savings: float, monthly_recurring_cost: float = 0.0) -> float:
    values = (one_time_cost, monthly_savings, monthly_recurring_cost)
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("costs and savings must be non-negative")
    net_monthly_savings = monthly_savings - monthly_recurring_cost
    if net_monthly_savings <= 0.0:
        return math.inf
    return one_time_cost / net_monthly_savings


def finite_or_label(value: float) -> float | str:
    return value if math.isfinite(value) else "unbounded"


def json_safe(payload: dict[str, object]) -> dict[str, object]:
    """Replace permitted positive infinities so output remains strict JSON."""
    return {
        key: finite_or_label(value) if isinstance(value, float) else value
        for key, value in payload.items()
    }


def run_amdahl(args: argparse.Namespace) -> int:
    result = with_target(amdahl(args.share, args.kernel_speedup, args.boundary), args.target)
    payload = json_safe(asdict(result))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    else:
        print(f"end-to-end speedup: {finite_or_label(result.end_to_end_speedup)}x")
        print(f"infinite-kernel ceiling: {finite_or_label(result.infinite_kernel_ceiling)}x")
        if result.target_speedup is not None:
            physical = "possible" if result.target_physically_possible else "IMPOSSIBLE"
            candidate = "MEETS" if result.target_met_by_candidate else "MISSES"
            print(f"target {result.target_speedup}x: physically {physical}; candidate {candidate}")
    return 2 if result.target_met_by_candidate is False else 0


def run_breakeven(args: argparse.Namespace) -> int:
    months = break_even_months(args.one_time_cost, args.monthly_savings, args.monthly_recurring_cost)
    payload = {
        "one_time_cost": args.one_time_cost,
        "monthly_savings": args.monthly_savings,
        "monthly_recurring_cost": args.monthly_recurring_cost,
        "net_monthly_savings": args.monthly_savings - args.monthly_recurring_cost,
        "break_even_months": finite_or_label(months),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    elif math.isfinite(months):
        print(f"break-even: {months:.2f} months")
    else:
        print("break-even: never (recurring cost is greater than or equal to savings)")
    return 0 if math.isfinite(months) else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    amdahl_parser = subparsers.add_parser("amdahl", help="compute Amdahl speedup and physical ceiling")
    amdahl_parser.add_argument("--share", type=float, required=True, help="baseline fraction in the candidate kernel, 0..1")
    amdahl_parser.add_argument("--kernel-speedup", type=float, required=True, help="candidate kernel speedup, >0; accepts inf")
    amdahl_parser.add_argument("--boundary", type=float, default=0.0, help="added boundary cost as baseline-time fraction")
    amdahl_parser.add_argument("--target", type=float, help="optional end-to-end acceptance threshold")
    amdahl_parser.add_argument("--json", action="store_true")
    amdahl_parser.set_defaults(handler=run_amdahl)

    break_even_parser = subparsers.add_parser("breakeven", help="compute simple migration payback period")
    break_even_parser.add_argument("--one-time-cost", type=float, required=True)
    break_even_parser.add_argument("--monthly-savings", type=float, required=True)
    break_even_parser.add_argument("--monthly-recurring-cost", type=float, default=0.0)
    break_even_parser.add_argument("--json", action="store_true")
    break_even_parser.set_defaults(handler=run_breakeven)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
