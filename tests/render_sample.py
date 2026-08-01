#!/usr/bin/env python3
"""Render the committed synthetic golden report from the distributable template."""

from __future__ import annotations

import re
import sys
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "why-not-rust"
sys.path.insert(0, str(SKILL / "scripts"))

from decision_math import amdahl, with_target  # noqa: E402
from report_safety import html_text, json_for_html, safe_href  # noqa: E402


TARGET = "Reduce the synthetic 2 GB export from 3.8 s to ≤2.4 s."
CHANGE_TRIGGER = (
    "Conditional: re-open the decision if measured boundary cost exceeds 7%, "
    "parity is below 100%, or the funded second owner disappears."
)


def block(html: str, name: str, replacement: str) -> str:
    pattern = rf"<!-- BEGIN REPEAT {re.escape(name)}\b.*?-->.*?<!-- END REPEAT {re.escape(name)} -->"
    rendered, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"repeat block {name!r} not found exactly once")
    return rendered


def gate(gate_id: str, state: str, name: str, evidence: str) -> str:
    return (
        f'<div class="gate"><span class="id mono">{html_text(gate_id)}</span>'
        f'<span class="state {html_text(state.lower())}">{html_text(state)}</span><div><div class="name">{html_text(name)}</div>'
        f'<div class="ev">{html_text(evidence)}</div></div></div>'
    )


def tile(label: str, value: str, unit: str, note: str) -> str:
    return (
        f'<div class="tile"><div class="label">{html_text(label)}</div><div class="value mono">{html_text(value)}'
        f'<span class="unit">{html_text(unit)}</span></div><div class="note">{html_text(note)}</div></div>'
    )


def option(row_class: str, name: str, disposition: str, scope: str, benefit: str, cost: str,
           time: str, compat: str, evidence_class: str, evidence: str) -> str:
    return (
        f'<tr class="{html_text(row_class)}"><td><span class="option-name">{html_text(name)}</span>'
        f'<div class="source">{html_text(disposition)}</div></td><td><span class="scope-tag">{html_text(scope)}</span></td>'
        f'<td>{html_text(benefit)}</td><td>{html_text(cost)}</td><td>{html_text(time)}</td><td>{html_text(compat)}</td>'
        f'<td><span class="ev-tag {html_text(evidence_class)}">{html_text(evidence)}</span></td></tr>'
    )


LENSES = [
    ("D1", "Requirement & ownership", "SUPPORTS · native options", "neutral", "STRONG", "strong",
     "Synthetic CPU profile assigns 62% of export wall-clock to the owned parser/diff kernel.", "synthetic/export.cpuprofile · representative 2 GB fixture", "SUPPORTS", ["wasm-adopt", "rust-extract", "go-sidecar"]),
    ("D2", "End-to-end reach", "SUPPORTS · rust-extract", "rust", "MODERATE", "moderate",
     "A 5× kernel with 3% boundary cost predicts 1.87× product speed; the target is 1.59×.", "decision_math.py · f=.62, S=5, b=.03", "SUPPORTS", ["rust-extract"]),
    ("D3", "Tail & runtime", "NEUTRAL · all", "neutral", "STRONG", "strong",
     "No GC-correlated p99 violation appears in the synthetic trace; GC is not part of the case.", "synthetic/export-trace.json", "NEUTRAL", ["ts-opt", "wasm-adopt", "rust-extract", "go-sidecar"]),
    ("D4", "Fleet footprint", "N/A", "neutral", "MODERATE", "moderate",
     "Single desktop instances create no fleet-density objective for this decision.", "synthetic deployment inventory", "N/A", []),
    ("D5", "Startup shape", "N/A", "neutral", "STRONG", "strong",
     "The long-lived application starts export after warm initialization; startup is outside the objective.", "synthetic lifecycle trace", "N/A", []),
    ("D6", "Safety & correctness", "N/A", "neutral", "STRONG", "strong",
     "TypeScript app code has no native/FFI surface; this proposal makes no safety claim.", "synthetic package manifests", "N/A", []),
    ("D7", "Concurrency & invariants", "NEUTRAL · native options", "neutral", "MODERATE", "moderate",
     "Chunk parallelism is available in Go, workers, and Rust; it is not Rust-specific in this design.", "synthetic worker PoC", "NEUTRAL", ["wasm-adopt", "rust-extract", "go-sidecar"]),
    ("D8", "Distribution", "SUPPORTS · ts-opt", "current", "MODERATE", "moderate",
     "The current signed Electron packaging chain already meets distribution requirements.", "synthetic build config", "SUPPORTS", ["ts-opt"]),
    ("D9", "Ecosystem & alternatives", "NEUTRAL · native options", "neutral", "MODERATE", "moderate",
     "Rust, Go, and the existing WASM parser are all technically viable candidates.", "synthetic dependency spike", "NEUTRAL", ["wasm-adopt", "rust-extract", "go-sidecar"]),
    ("D10", "Boundary & compatibility", "SUPPORTS · rust-extract", "rust", "MODERATE", "moderate",
     "One immutable batch enters and one result batch returns; measured boundary estimate is 3%.", "synthetic boundary bench", "SUPPORTS", ["rust-extract"]),
    ("D11", "Delivery economics", "DISFAVORS · rust-extract", "rust", "WEAK", "weak",
     "One Rust maintainer creates bus-factor risk; the bounded extraction plan prices a second owner.", "synthetic staffing plan", "DISFAVORS", ["rust-extract"]),
    ("D12", "Counterfactual", "DISFAVORS · non-Rust options", "current", "MODERATE", "moderate",
     "Funded TypeScript, WASM, and Go trials stay below the 1.59× target on the same fixture.", "synthetic counterfactual benchmarks", "DISFAVORS", ["ts-opt", "wasm-adopt", "go-sidecar"]),
]


def lens_html(item: tuple[str, ...]) -> str:
    lens_id, name, state, state_class, strength, strength_class, claim, source, _, _ = item
    return (
        f'<div class="lens"><div class="name">{html_text(lens_id)} · {html_text(name)}</div>'
        f'<div><span class="dir-tag {html_text(state_class)}">{html_text(state)}</span></div>'
        f'<div><span class="ev-tag {html_text(strength_class)}">{html_text(strength)}</span></div>'
        f'<div class="claim">{html_text(claim)}<div class="source mono">{html_text(source)}</div></div></div>'
    )


def card(css_class: str, title: str, body: str, ref: str) -> str:
    return f'<div class="card {html_text(css_class)}"><h3>{html_text(title)}</h3><p>{html_text(body)}</p><span class="ref mono">{html_text(ref)}</span></div>'


def precedent(name: str, outcome: str, body: str, match: str, mismatch: str, url: str, source: str) -> str:
    return (
        f'<article class="precedent"><div class="top"><h3>{html_text(name)}</h3><span class="outcome">{html_text(outcome)}</span></div>'
        f'<p>{html_text(body)}</p><div class="match">match: {html_text(match)} · mismatch: {html_text(mismatch)}</div>'
        f'<a class="ref mono" href="{safe_href(url)}">{html_text(source)}</a></article>'
    )


def step(title: str, body: str, cost: str) -> str:
    return f'<div class="step"><span class="number"></span><div><h3>{html_text(title)}</h3><p>{html_text(body)}</p></div><span class="cost">{html_text(cost)}</span></div>'


def check(state: str, name: str, body: str) -> str:
    css_class = "pass" if state == "PASS" else "unknown" if state in {"HIT", "UNKNOWN"} else "fail"
    return f'<div class="check"><span class="state {html_text(css_class)}">{html_text(state)}</span><div><b>{html_text(name)}</b> — {html_text(body)}</div></div>'


def build_assessment() -> dict[str, object]:
    math_result = with_target(amdahl(0.62, 5.0, 0.03), 1.59)
    lens_records = [
        {
            "id": item[0], "name": item[1], "option_ids": item[9], "state": item[8], "strength": item[4],
            "claim": item[6], "source": item[7], "baseline_regime": "synthetic 2 GB export fixture",
            "caveat": "Illustrative synthetic data; do not transfer to a real repository.", "change_trigger": ""
        }
        for item in LENSES
    ]
    return {
        "method": "why-not-rust/2.0",
        "generated_at": "2026-08-01",
        "repository": {"path": "synthetic://acme-desk", "commit": "illustrative", "scope": "export kernel", "sampling": "synthetic golden fixture"},
        "analysis": {
            "mode": "synthetic-golden",
            "user_supplied_facts": [],
            "evidence_gaps": ["production boundary cost", "second Rust owner continuity", "production workload mix"],
        },
        "objective": {"driver": "performance", "requirement": "reduce 2 GB export from 3.8 s to <=2.4 s", "baseline": "3.8 s", "target": "1.59x or better"},
        "decision": {
            "authorization": "APPROVE", "scope": "EXTRACT", "selected_option_id": "rust-extract", "confidence": "MEDIUM", "robustness": "CONDITIONAL",
            "because": "The owned kernel dominates the path and a coarse extraction clears the target without replacing the application.",
            "change_trigger": CHANGE_TRIGGER,
        },
        "gates": [
            {"id": "G1", "option_id": "rust-extract", "name": "requirement", "state": "PASS", "evidence": "3.8 s baseline misses 2.4 s target"},
            {"id": "G2", "option_id": "rust-extract", "name": "rust-specific causality", "state": "PASS", "evidence": "62% owned CPU kernel; 5x bounded kernel result"},
            {"id": "G3", "option_id": "rust-extract", "name": "economics and smallest option", "state": "PASS", "evidence": "funded TypeScript, WASM, and Go trials miss the target"},
            {"id": "G4", "option_id": "rust-extract", "name": "delivery and reversibility", "state": "PASS", "evidence": "coarse boundary, feature flag, parity corpus, rollback"},
        ],
        "options": [
            {"id": "ts-opt", "name": "TypeScript optimize", "implementation": "current", "scope": "stay", "target": TARGET, "benefit_interval": "1.25–1.40x", "one_time_cost": "2–4 engineer-days", "recurring_cost": "low", "time_to_value": "days", "compatibility": "native", "reversibility": "git revert", "evidence_strength": "MODERATE", "disposition": "retain", "reason": "Does not meet 1.59x target alone"},
            {"id": "wasm-adopt", "name": "Existing WASM parser", "implementation": "external", "scope": "adopt", "target": TARGET, "benefit_interval": "1.38–1.52x", "one_time_cost": "1–2 weeks", "recurring_cost": "dependency", "time_to_value": "1 week", "compatibility": "format adapter", "reversibility": "adapter flag", "evidence_strength": "MODERATE", "disposition": "retain", "reason": "Same-fixture trial misses the target"},
            {"id": "rust-extract", "name": "Rust kernel extraction", "implementation": "rust", "scope": "extract", "target": TARGET, "benefit_interval": "1.70–1.90x", "one_time_cost": "2–3 weeks", "recurring_cost": "second owner", "time_to_value": "1 week pilot", "compatibility": "batch boundary", "reversibility": "feature flag", "evidence_strength": "MODERATE", "disposition": "selected", "reason": "Recommended smallest sufficient option"},
            {"id": "go-sidecar", "name": "Go sidecar", "implementation": "non-rust-native", "scope": "extract", "target": TARGET, "benefit_interval": "1.44–1.55x", "one_time_cost": "2–3 weeks", "recurring_cost": "second stack", "time_to_value": "1 week pilot", "compatibility": "process boundary", "reversibility": "feature flag", "evidence_strength": "MODERATE", "disposition": "retain", "reason": "Same-fixture trial misses the target"},
            {"id": "rust-full", "name": "Full Rust/Tauri app", "implementation": "rust", "scope": "full", "target": TARGET, "benefit_interval": "no extra export gain", "one_time_cost": "9–14 months", "recurring_cost": "full dual stack", "time_to_value": "months", "compatibility": "whole UI", "reversibility": "poor", "evidence_strength": "WEAK", "disposition": "exclude", "reason": "Fails smallest-sufficient-option gate"},
        ],
        "lenses": lens_records,
        "math": {"amdahl": asdict(math_result), "break_even": None},
        "precedents": [
            {"name": "pydantic-core", "outcome": "EXTRACT", "match": "scripting API + hot pure kernel", "mismatch": "different data model and workload", "workload_regime": "validation core under a Python API", "source_class": "first-party vendor benchmark", "url": "https://pydantic.dev/articles/pydantic-v2"},
            {"name": "Prisma Rust-free", "outcome": "REVERSED", "match": "JS host + boundary cost", "mismatch": "database ORM calls are chattier", "workload_regime": "internal 25k-row findMany benchmark", "source_class": "first-party internal benchmark", "url": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm"},
            {"name": "TypeScript native port", "outcome": "NON-RUST", "match": "native-tool alternative", "mismatch": "whole compiler port, not one kernel", "workload_regime": "compiler and language-service preview benchmarks", "source_class": "first-party preview benchmark", "url": "https://devblogs.microsoft.com/typescript/typescript-native-port/"},
        ],
        "path": [
            {"step": 1, "title": "Freeze the decision fixture", "owner": "performance lead", "cost_range": "1 day", "artifact": "versioned 2 GB corpus, warm/cold protocol, and variance report", "acceptance": "three baseline runs within ±3%", "deadline_or_stop": "stop if the baseline no longer misses 2.4 s", "rollback": "discard the fixture commit; production is untouched"},
            {"step": 2, "title": "Confirm equal-boundary pilots", "owner": "two platform engineers", "cost_range": "1 week", "artifact": "Rust and Go candidates using the same batch API and copies", "acceptance": "≥1.59× end-to-end, 100% parity, and ≤7% boundary cost", "deadline_or_stop": "stop after one week if neither candidate clears every threshold", "rollback": "delete pilot branches and keep the TypeScript path"},
            {"step": 3, "title": "Shadow the selected kernel", "owner": "export team", "cost_range": "1 week", "artifact": "shadow diff log behind a disabled-by-default flag", "acceptance": "100% fixture parity and no p95 regression", "deadline_or_stop": "stop on the first unexplained mismatch", "rollback": "disable the flag and route all work to TypeScript"},
            {"step": 4, "title": "Roll out with a kill switch", "owner": "on-call maintainer", "cost_range": "1 release", "artifact": "5%→25%→100% rollout dashboard", "acceptance": "error budget stays green for one release", "deadline_or_stop": "remove the old path only after the observation window", "rollback": "activate the kill switch and restore the TypeScript route"},
        ],
        "assumptions": ["5x kernel result and 3% boundary cost are synthetic", "one additional Rust owner is funded"],
        "challenge_audit": {
            "migration_case": [
                {"id": "M1", "name": "End-to-end reach", "state": "PASS", "claim": "Amdahl share and boundary are included.", "evidence": "decision_math.py"},
                {"id": "M2", "name": "Attribution", "state": "PASS", "claim": "Rust, Go, and WASM use the same fixture and bounded interfaces.", "evidence": "synthetic counterfactual benchmarks"},
                {"id": "M3", "name": "Boundary uncertainty", "state": "HIT", "claim": "The 3% estimate is not yet a production measurement.", "evidence": "synthetic/boundary-bench.json"},
                {"id": "M4", "name": "Scope control", "state": "PASS", "claim": "The full application migration is explicitly excluded.", "evidence": "option comparison"},
                {"id": "M5", "name": "Ownership", "state": "PASS", "claim": "The plan funds a second maintainer and rollback owner.", "evidence": "synthetic staffing plan"},
            ],
            "staying_case": [
                {"id": "S1", "name": "Funded counterfactual", "state": "PASS", "claim": "TypeScript, WASM, and Go alternatives have owners and same-fixture results.", "evidence": "synthetic counterfactual benchmarks"},
                {"id": "S2", "name": "Target shortfall", "state": "HIT", "claim": "The measured 1.25–1.40× TypeScript range does not meet 1.59×.", "evidence": "synthetic/ts-baseline.json"},
                {"id": "S3", "name": "Cost of inaction", "state": "PASS", "claim": "The report names the missed 2.4 s workflow target.", "evidence": "synthetic requirement"},
                {"id": "S4", "name": "Unsafe-surface check", "state": "PASS", "claim": "No hidden native dependency was found in the synthetic manifests.", "evidence": "synthetic package manifests"},
                {"id": "S5", "name": "Stop condition", "state": "PASS", "claim": "Optimization ends when the fixture meets the target or the funded range is exhausted.", "evidence": "reversible path"},
            ],
        },
    }


def render() -> str:
    html = (SKILL / "assets" / "report-template.html").read_text(encoding="utf-8")
    html = re.sub(r"<!--\n  Fill this template.*?-->", "", html, count=1, flags=re.DOTALL)

    html = block(html, "gate", "\n".join([
        gate("G1", "PASS", "Requirement", "3.8 s baseline misses the 2.4 s export target."),
        gate("G2", "PASS", "Causality", "62% owned CPU kernel; bounded 5× kernel result."),
        gate("G3", "PASS", "Economics", "Funded TypeScript, WASM, and Go trials miss the target."),
        gate("G4", "PASS", "Delivery", "Batch boundary, parity corpus, flag, and rollback owner."),
    ]))
    html = block(html, "tile", "\n".join([
        tile("Baseline → target", "3.8 → 2.4", "s", "synthetic 2 GB export fixture"),
        tile("Owned hot path", "62", "%", "synthetic CPU profile"),
        tile("Predicted product gain", "1.87", "×", "f=.62 · S=5 · b=.03"),
        tile("Physical ceiling", "2.44", "×", "infinite kernel · same boundary"),
        tile("Pilot", "2–3", "weeks", "range from synthetic work breakdown"),
    ]))
    html = block(html, "option", "\n".join([
        option("", "TypeScript optimize", "retain · useful but insufficient", "STAY", "1.25–1.40×", "2–4 days; low recurring", "days", "native · git revert", "moderate", "MODERATE"),
        option("", "Existing WASM parser", "retain · measured below target", "ADOPT", "1.38–1.52×", "1–2 weeks; dependency", "1 week", "adapter flag · format adapter", "moderate", "MODERATE"),
        option("selected", "Rust kernel extraction", "recommended smallest sufficient option", "EXTRACT", "1.70–1.90×", "2–3 weeks; second owner", "1 week pilot", "batch API · feature flag", "moderate", "MODERATE"),
        option("", "Go sidecar", "retain · measured below target · Go", "EXTRACT", "1.44–1.55×", "2–3 weeks; second stack", "1 week pilot", "process API · feature flag", "moderate", "MODERATE"),
        option("excluded", "Full Rust/Tauri app", "exclude · no incremental export benefit", "MIGRATE", "no extra export gain", "9–14 months; full dual stack", "months", "whole UI · poor rollback", "weak", "WEAK"),
    ]))
    html = block(html, "lens", "\n".join(lens_html(item) for item in LENSES))
    html = block(html, "finding", "\n".join([
        card("rust", "The kernel is large enough to matter", "The synthetic profile assigns 62% of export time to owned parse/diff work; the 2.44× physical ceiling is above the 1.59× target.", "synthetic/export.cpuprofile"),
        card("current", "In-stack work is real but insufficient", "Buffer reuse and caching produce 1.25–1.40× on the same fixture. Fund them, but do not pretend they meet the target alone.", "synthetic/ts-baseline.json"),
        card("unknown", "Boundary cost controls the decision", "The 3% value is a bounded synthetic bench. At more than 7%, the lower benefit estimate no longer clears the target.", "synthetic/boundary-bench.json"),
        card("current", "The UI is outside the requirement", "DOM rendering and Electron startup do not participate in export time; replacing the shell would add cost without passing a new gate.", "synthetic/trace.json"),
    ]))
    html = block(html, "buy", "".join([
        "<li><b>Parser throughput</b> — native batch processing can close the measured export gap.</li>",
        "<li><b>Kernel-local invariants</b> — ownership can simplify the extracted buffer lifecycle.</li>",
        "<li><b>Reversible native option</b> — the unchanged TypeScript API keeps rollback cheap.</li>",
    ]))
    html = block(html, "nobuy", "".join([
        "<li><b>Faster DOM or database work</b> — neither appears in the measured export kernel.</li>",
        "<li><b>Application memory safety</b> — the TypeScript app has no unsafe native surface.</li>",
        "<li><b>A reason to replace Electron</b> — shell migration adds no export benefit.</li>",
    ]))
    html = block(html, "precedent", "\n".join([
        precedent("pydantic-core", "EXTRACT", "A Rust validation core kept the Python API and captured native value at a coarse seam.", "scripting API + hot pure kernel", "different data model and workload", "https://pydantic.dev/articles/pydantic-v2", "first-party · vendor benchmark"),
        precedent("Prisma Rust-free", "REVERSED", "Moving execution out of a chatty Rust boundary improved Prisma's own large-query benchmark.", "JS host + boundary cost", "database ORM calls are chattier", "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm", "first-party · internal benchmark"),
        precedent("TypeScript native port", "NON-RUST", "Go supplied native execution and shared-memory parallelism while preserving cyclic graph semantics.", "native-tool alternative", "whole compiler port, not one kernel", "https://devblogs.microsoft.com/typescript/typescript-native-port/", "first-party · preview benchmark"),
    ]))
    html = block(html, "step", "\n".join([
        step("Freeze the decision fixture", "Owner: performance lead. Artifact: versioned 2 GB corpus, warm/cold protocol, and variance report. Acceptance: three baseline runs within ±3%. Deadline/stop: stop if the baseline no longer misses 2.4 s. Rollback: discard the fixture commit; production is untouched.", "1 day"),
        step("Confirm equal-boundary pilots", "Owner: two platform engineers. Artifact: Rust and Go candidates using the same batch API and copies. Acceptance: ≥1.59× end-to-end, 100% parity, and ≤7% boundary cost. Deadline/stop: stop after one week if neither clears every threshold. Rollback: delete pilot branches and keep the TypeScript path.", "1 week"),
        step("Shadow the selected kernel", "Owner: export team. Artifact: shadow diff log behind a disabled-by-default flag. Acceptance: 100% fixture parity and no p95 regression. Deadline/stop: stop on the first unexplained mismatch. Rollback: disable the flag and route all work to TypeScript.", "1 week"),
        step("Roll out with a kill switch", "Owner: on-call maintainer. Artifact: 5%→25%→100% rollout dashboard. Acceptance: the error budget stays green for one release. Deadline/stop: remove the old path only after that window. Rollback: activate the kill switch and restore the TypeScript route.", "1 release"),
    ]))
    html = block(html, "migration check", "\n".join([
        check("PASS", "End-to-end reach", "Amdahl share and boundary are included."),
        check("PASS", "Attribution", "Rust, Go, and WASM use the same fixture and bounded interfaces."),
        check("HIT", "Boundary uncertainty", "3% is not yet a production measurement."),
        check("PASS", "Scope control", "The full application migration is explicitly excluded."),
        check("PASS", "Ownership", "The plan funds a second maintainer and rollback owner."),
    ]))
    html = block(html, "staying check", "\n".join([
        check("PASS", "Funded counterfactual", "TypeScript, WASM, and Go alternatives have owners and same-fixture results."),
        check("HIT", "Target shortfall", "The measured 1.25–1.40× range does not meet 1.59×."),
        check("PASS", "Cost of inaction", "The report names the missed 2.4 s workflow target."),
        check("PASS", "Unsafe-surface check", "No hidden native dependency was found in the synthetic manifests."),
        check("PASS", "Stop condition", "Optimization ends when the same fixture meets the target or its range is exhausted."),
    ]))
    html = block(html, "gap", "".join([
        "<tr><td>Production boundary cost</td><td>Above 7%, change authorization to DEFER–MEASURE and keep the TypeScript path.</td></tr>",
        "<tr><td>Second Rust owner</td><td>If unfunded, G4 becomes UNKNOWN; pilot may run, production extraction is not authorized.</td></tr>",
        "<tr><td>Production workload mix</td><td>If the owned kernel falls below the measured decision range, rerun D2 and G3 before rollout.</td></tr>",
    ]))

    values = {
        "LANG": "en", "PROJECT_NAME": "acme-desk", "PROJECT_DESC": "ILLUSTRATIVE SYNTHETIC EXAMPLE · no real repository was analyzed",
        "DATE": "2026-08-01", "VERDICT_CLASS": "v-extract", "AUTH_CLASS": "a-approve",
        "L_THEME": "light / dark", "L_KICKER": "RUST ADOPTION DECISION", "SCOPE_WORD": "EXTRACT",
        "N_OPTIONS": "01", "N_LENSES": "02", "N_EVIDENCE": "03", "N_BUYS": "04",
        "N_PRECEDENTS": "05", "N_PATH": "06", "N_CHALLENGES": "07", "N_METHOD": "08",
        "SCOPE_SUB": "isolate one measured export kernel", "L_AUTH": "Authorization", "AUTH_WORD": "APPROVE",
        "DECISION_WHY": "The synthetic profile puts 62% of export time in an owned parser/diff kernel, and a coarse extraction clears the 1.59× target without replacing the TypeScript application.",
        "CHANGE_TRIGGER": CHANGE_TRIGGER,
        "L_SCOPE": "Scope", "SCOPE": "export kernel only", "L_CONFIDENCE": "Confidence", "CONFIDENCE": "MEDIUM",
        "L_ROBUSTNESS": "Robustness", "ROBUSTNESS": "CONDITIONAL", "TARGET_ARCHETYPE": "Electron desktop · CPU export path",
        "L_GATES": "Four proof gates", "L_OPTIONS": "Option comparison", "OPTIONS_SUB": "Same target: reduce the synthetic 2 GB export from 3.8 s to ≤2.4 s.",
        "L_LENSES": "Twelve-lens evidence ledger", "LENSES_SUB": "States are option-scoped evidence, not additive scores.", "NA_LENSES_NOTE": "N/A lenses: D4 fleet footprint, D5 startup, and D6 safety do not bear on this synthetic performance objective.",
        "L_EVIDENCE": "Decisive evidence", "L_BUYS": "What Rust buys / doesn't buy here", "BUYS_YES_LABEL": "What it buys", "BUYS_NO_LABEL": "What it doesn't buy",
        "L_PRECEDENTS": "Matched precedents", "L_PATH": "Reversible path", "L_CHALLENGES": "Symmetric challenge audit",
        "CHALLENGE_MIGRATION_LABEL": "Challenge the migration case", "CHALLENGE_STAY_LABEL": "Challenge the staying case",
        "L_METHOD": "Method and decision record", "METHOD_TITLE": "Synthetic golden fixture · why-not-rust method 2.0",
        "METHOD_BODY": "This report is intentionally fictional and exists to regression-test the template. Repository commit: illustrative; scope: export kernel; sampling: synthetic golden fixture; mode: static synthetic analysis; user-supplied facts: none. Objective: reduce the 2 GB export from 3.8 s to ≤2.4 s. The method compares explicit options through four non-compensatory gates; it is not a statistical predictor. Amdahl inputs: f=.62, S=5, b=.03 → 1.87×; infinite-kernel ceiling 2.44×. No project code or network was run.",
        "GAP_LABEL": "Evidence gap", "GAP_EFFECT_LABEL": "Decision effect",
        "H_OPTION": "Option", "H_SCOPE": "Scope", "H_BENEFIT": "Benefit / risk reduction", "H_COST": "Cost",
        "H_TIME": "Time to value", "H_COMPAT": "Compatibility / rollback", "H_EVIDENCE": "Evidence",
        "L_MATCH": "match", "L_MISMATCH": "mismatch",
        "FOOTER_DISCLOSURE": "illustrative synthetic fixture · static analysis + synthetic artifacts",
        "ASSESSMENT_JSON": json_for_html(build_assessment()),
    }
    for key, value in values.items():
        replacement = value if key == "ASSESSMENT_JSON" else html_text(value)
        html = html.replace("{{" + key + "}}", replacement)
    leftovers = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
    if leftovers:
        raise RuntimeError(f"unfilled tokens: {leftovers}")
    return html


def render_quick() -> str:
    """Return a compact fixture to regression-test quick-mode section order."""
    html = render()
    for number in ("02", "03", "04", "05"):
        pattern = rf'<section>\s*<h2 class="section-title"><span class="no">{number}</span>.*?</section>'
        html, count = re.subn(pattern, "", html, count=1, flags=re.DOTALL)
        if count != 1:
            raise RuntimeError(f"quick-mode section {number} not found")
    for old, new in (("06", "02"), ("07", "03"), ("08", "04")):
        html = html.replace(f'<span class="no">{old}</span>', f'<span class="no">{new}</span>', 1)
    return html


def main() -> None:
    output = ROOT / "examples" / "sample-report.html"
    output.write_text(render(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
