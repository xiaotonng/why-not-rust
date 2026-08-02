#!/usr/bin/env python3
"""Render the public case-study reports from the distributable skill template.

Each case lives in `examples/cases/<slug>.py` and exposes a `CASE` dict. Every
visible string, link, and JSON value goes through the skill's own
`scripts/report_safety.py`, and every performance number goes through
`scripts/decision_math.py`, so the published examples obey the same contract the
skill imposes on a real run.

Bilingual text
--------------
Any visible string may be written either as a plain `str` (used in both
languages) or as an `(english, chinese)` pair. A pair renders as two sibling
spans and the report's language button switches between them. The machine-
readable assessment record always stores the English side.

Usage:
    python3 examples/build_cases.py            # render every case
    python3 examples/build_cases.py curl redis # render selected slugs
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "why-not-rust"
CASES_DIR = Path(__file__).resolve().parent / "cases"
sys.path.insert(0, str(SKILL / "scripts"))

from decision_math import amdahl, break_even_months, with_target  # noqa: E402
from report_safety import html_text, json_for_html, safe_href  # noqa: E402

VERDICT_CLASS = {"STAY": "v-stay", "EXTRACT": "v-extract", "PARTIAL": "v-partial", "MIGRATE": "v-migrate"}
AUTH_CLASS = {"APPROVE": "a-approve", "REJECT": "a-reject", "DEFER–MEASURE": "a-defer"}
CHECK_CLASS = {"PASS": "pass", "HIT": "unknown", "UNKNOWN": "unknown", "FAIL": "fail"}
GATE_CLASS = {"PASS": "pass", "FAIL": "fail", "UNKNOWN": "unknown"}


# --------------------------------------------------------------- bilingual text

def t(value: object) -> str:
    """Escape a visible string. An (en, zh) pair renders both languages."""
    if isinstance(value, (tuple, list)):
        english, chinese = value
        return (
            f'<span data-l="en">{html_text(str(english))}</span>'
            f'<span data-l="zh">{html_text(str(chinese))}</span>'
        )
    return html_text(str(value))


def en(value: object) -> str:
    """The English side of a value, for the machine-readable record."""
    if isinstance(value, (tuple, list)):
        return str(value[0])
    return str(value)


# Verdict words, evidence states, dates and identifiers stay identical in both
# languages, so they are written plain and escaped directly.
LABELS = {
    "L_LANG": "EN / 中文",
    "L_THEME": ("light / dark", "浅色 / 深色"),
    "L_KICKER": ("Rust adoption decision", "Rust 采用决策"),
    "L_AUTH": ("Authorization", "授权"),
    "L_SCOPE": ("Scope", "范围"),
    "L_CONFIDENCE": ("Confidence", "置信度"),
    "L_ROBUSTNESS": ("Robustness", "稳健性"),
    "L_GATES": ("Four proof gates", "四道证据门"),
    "L_OPTIONS": ("The options", "备选方案"),
    "L_LENSES": ("Evidence ledger", "证据账本"),
    "L_EVIDENCE": ("What decided it", "决定性证据"),
    "L_BUYS": ("What Rust buys here, and what it doesn't", "Rust 在这里买得到什么，买不到什么"),
    "BUYS_YES_LABEL": ("Buys", "买得到"),
    "BUYS_NO_LABEL": ("Doesn't buy", "买不到"),
    "L_PRECEDENTS": ("Who has done this before", "同型先例"),
    "L_PATH": ("What to do next", "可逆路径"),
    "L_CHALLENGES": ("Arguing both sides", "对称反证"),
    "CHALLENGE_MIGRATION_LABEL": ("Against migrating", "反驳「迁移」"),
    "CHALLENGE_STAY_LABEL": ("Against staying", "反驳「不动」"),
    "L_METHOD": ("How this was produced", "方法与记录"),
    "GAP_LABEL": ("What we don't know", "证据缺口"),
    "GAP_EFFECT_LABEL": ("What it would change", "会改变什么"),
    "H_OPTION": ("Option", "方案"),
    "H_SCOPE": ("Scope", "范围"),
    "H_BENEFIT": ("Benefit", "收益"),
    "H_COST": ("Cost", "成本"),
    "H_TIME": ("Time to value", "见效时间"),
    "H_COMPAT": ("Compatibility / rollback", "兼容 / 回滚"),
    "H_EVIDENCE": ("Evidence", "证据"),
    "L_MATCH": ("matches", "匹配"),
    "L_MISMATCH": ("differs", "不匹配"),
    "N_OPTIONS": "01",
    "N_LENSES": "02",
    "N_EVIDENCE": "03",
    "N_BUYS": "04",
    "N_PRECEDENTS": "05",
    "N_PATH": "06",
    "N_CHALLENGES": "07",
    "N_METHOD": "08",
}

# Tokens that land inside an attribute or must stay a bare word: never wrapped.
PLAIN_TOKENS = {
    "LANG", "LANG_DEFAULT", "PROJECT_NAME", "DATE", "VERDICT_CLASS", "AUTH_CLASS",
    "SCOPE_WORD", "AUTH_WORD", "CONFIDENCE", "ROBUSTNESS", "ASSESSMENT_JSON",
    "N_OPTIONS", "N_LENSES", "N_EVIDENCE", "N_BUYS", "N_PRECEDENTS", "N_PATH",
    "N_CHALLENGES", "N_METHOD", "L_LANG",
}


# --------------------------------------------------------------------- fragments

def block(html: str, name: str, replacement: str) -> str:
    pattern = rf"<!-- BEGIN REPEAT {re.escape(name)}\b.*?-->.*?<!-- END REPEAT {re.escape(name)} -->"
    rendered, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"repeat block {name!r} not found exactly once")
    return rendered


def gate_html(gate: dict) -> str:
    css = GATE_CLASS[gate["state"]]
    return (
        '<div class="gate">'
        f'<span class="id mono">{html_text(gate["id"])}</span><div>'
        f'<div class="head"><span class="name">{t(gate["short"])}</span>'
        f'<span class="state {css}">{html_text(gate["state"])}</span></div>'
        f'<div class="ev">{t(gate["hero_evidence"])}</div></div></div>'
    )


def tile_html(tile: tuple) -> str:
    label, value, unit, note = tile
    return (
        f'<div class="tile"><div class="label">{t(label)}</div>'
        f'<div class="value mono">{html_text(str(value))}<span class="unit">{t(unit)}</span></div>'
        f'<div class="note">{t(note)}</div></div>'
    )


def option_html(opt: dict) -> str:
    disposition = opt["disposition"]
    row = "selected" if disposition == "selected" else "excluded" if disposition == "exclude" else ""
    return (
        f'<tr class="{html_text(row)}">'
        f'<td><span class="option-name">{t(opt["name"])}</span>'
        f'<span class="source">{t(opt["note"])}</span></td>'
        f'<td><span class="scope-tag">{html_text(opt["scope_tag"])}</span></td>'
        f'<td>{t(opt["benefit_interval"])}</td>'
        f'<td>{t(opt["cost_cell"])}</td>'
        f'<td>{t(opt["time_to_value"])}</td>'
        f'<td>{t(opt["compat_cell"])}</td>'
        f'<td><span class="ev-tag {html_text(opt["evidence_strength"].lower())}">'
        f'{html_text(opt["evidence_strength"])}</span></td></tr>'
    )


def lens_html(lens: dict) -> str:
    return (
        '<div class="lens"><div>'
        f'<div class="name">{html_text(lens["id"])} · {t(lens["name"])}</div>'
        f'<div class="tags"><span class="dir-tag {html_text(lens["css"])}">{html_text(lens["label"])}</span>'
        f'<span class="ev-tag {html_text(lens["strength"].lower())}">{html_text(lens["strength"])}</span></div>'
        f'</div><div><div class="claim">{t(lens["claim"])}</div>'
        f'<div class="source mono">{html_text(str(lens["source"]))}</div></div></div>'
    )


def finding_html(item: tuple) -> str:
    css, title, body, ref = item
    return (
        f'<div class="card {html_text(css)}"><h3>{t(title)}</h3>'
        f'<p>{t(body)}</p><span class="ref mono">{html_text(str(ref))}</span></div>'
    )


def precedent_html(p: dict) -> str:
    return (
        f'<article class="precedent"><div class="top"><h3>{html_text(p["name"])}</h3>'
        f'<span class="outcome">{html_text(p["outcome"])}</span></div><p>{t(p["body"])}</p>'
        f'<div class="match">{t(LABELS["L_MATCH"])}: {t(p["match"])} · '
        f'{t(LABELS["L_MISMATCH"])}: {t(p["mismatch"])}</div>'
        f'<a class="ref mono" href="{safe_href(p["url"])}">{html_text(p["source_label"])}</a></article>'
    )


def step_html(s: dict) -> str:
    # `body` is an authored sentence. Older cases without one fall back to the
    # labelled concatenation of the structured fields.
    body = s.get("body") or (
        f'Owner: {en(s["owner"])}. Artifact: {en(s["artifact"])}. '
        f'Acceptance: {en(s["acceptance"])}. Stop: {en(s["stop"])}. Rollback: {en(s["rollback"])}.'
    )
    return (
        '<div class="step"><span class="number mono"></span>'
        f'<div><h3>{t(s["title"])}</h3><p>{t(body)}</p></div>'
        f'<span class="cost">{t(s["cost_range"])}</span></div>'
    )


def check_html(c: dict) -> str:
    css = CHECK_CLASS[c["state"]]
    return (
        f'<div class="check"><span class="state {html_text(css)}">{html_text(c["state"])}</span>'
        f'<b>{t(c["name"])}</b> — {t(c["claim"])}</div>'
    )


# --------------------------------------------------------------------- math

def resolve_math(case: dict) -> dict:
    """Run every declared calculation through the skill's own calculator."""
    out: dict[str, object] = {"amdahl": None, "break_even": None}
    spec = case.get("amdahl")
    if spec:
        result = with_target(
            amdahl(spec["share"], spec["kernel_speedup"], spec.get("boundary", 0.0)),
            spec.get("target"),
        )
        payload = asdict(result)
        for key, value in payload.items():
            if isinstance(value, float) and value == float("inf"):
                payload[key] = "unbounded"
        payload["inputs_note"] = en(spec["note"])
        out["amdahl"] = payload
    spec = case.get("break_even")
    if spec:
        months = break_even_months(spec["one_time"], spec["monthly_savings"], spec.get("monthly_recurring", 0.0))
        out["break_even"] = {
            "one_time_cost": spec["one_time"],
            "monthly_savings": spec["monthly_savings"],
            "monthly_recurring_cost": spec.get("monthly_recurring", 0.0),
            "break_even_months": months if months != float("inf") else "never",
            "unit": en(spec["unit"]),
        }
    return out


# --------------------------------------------------------------------- assessment

def build_assessment(case: dict, math_record: dict) -> dict:
    return {
        "method": "why-not-rust/2.0",
        "generated_at": case["date"],
        "repository": case["repository"],
        "analysis": {
            "mode": case.get(
                "analysis_mode",
                "public-repository static analysis; no build, benchmark, or network run against the target",
            ),
            "user_supplied_facts": [en(f) for f in case.get("user_supplied_facts", [])],
            "evidence_gaps": [en(g[0]) for g in case["gaps"]],
        },
        "objective": {k: en(v) for k, v in case["objective"].items()},
        "decision": {
            "authorization": case["auth"],
            "scope": case["scope_word"],
            "selected_option_id": case["selected"],
            "confidence": case["confidence"],
            "robustness": case["robustness"],
            "because": en(case["why"]),
            "change_trigger": en(case["trigger"]),
        },
        "gates": [
            {
                "id": g["id"],
                "option_id": case["selected"],
                "name": en(g["name"]),
                "state": g["state"],
                "evidence": en(g["evidence"]),
            }
            for g in case["gates"]
        ],
        "options": [
            {
                "id": o["id"],
                "name": en(o["name"]),
                "implementation": o["implementation"],
                "scope": o["scope"],
                "target": en(case["objective"]["requirement"]),
                "benefit_interval": en(o["benefit_interval"]),
                "one_time_cost": en(o["one_time_cost"]),
                "recurring_cost": en(o["recurring_cost"]),
                "time_to_value": en(o["time_to_value"]),
                "compatibility": en(o["compatibility"]),
                "reversibility": en(o["reversibility"]),
                "evidence_strength": o["evidence_strength"],
                "disposition": o["disposition"],
                "reason": en(o["reason"]),
            }
            for o in case["options"]
        ],
        "lenses": [
            {
                "id": l["id"],
                "name": en(l["name"]),
                "option_ids": l["option_ids"],
                "state": l["state"],
                "strength": l["strength"],
                "claim": en(l["claim"]),
                "source": en(l["source"]),
                "baseline_regime": en(l["regime"]),
                "caveat": en(l["caveat"]),
                "change_trigger": en(l.get("change_trigger", "")),
            }
            for l in case["lenses"]
        ],
        "math": math_record,
        "precedents": [
            {
                "name": p["name"],
                "outcome": p["outcome"],
                "match": en(p["match"]),
                "mismatch": en(p["mismatch"]),
                "workload_regime": en(p["regime"]),
                "source_class": p["source_label"],
                "url": p["url"],
            }
            for p in case["precedents"]
        ],
        "path": [
            {
                "step": i + 1,
                "title": en(s["title"]),
                "owner": en(s["owner"]),
                "cost_range": en(s["cost_range"]),
                "artifact": en(s["artifact"]),
                "acceptance": en(s["acceptance"]),
                "deadline_or_stop": en(s["stop"]),
                "rollback": en(s["rollback"]),
            }
            for i, s in enumerate(case["path"])
        ],
        "assumptions": [en(a) for a in case["assumptions"]],
        "challenge_audit": {
            "migration_case": [
                {"id": f"M{i + 1}", "name": en(c["name"]), "state": c["state"],
                 "claim": en(c["claim"]), "evidence": en(c["evidence"])}
                for i, c in enumerate(case["migration_checks"])
            ],
            "staying_case": [
                {"id": f"S{i + 1}", "name": en(c["name"]), "state": c["state"],
                 "claim": en(c["claim"]), "evidence": en(c["evidence"])}
                for i, c in enumerate(case["staying_checks"])
            ],
        },
    }


# --------------------------------------------------------------------- render

def validate(case: dict) -> None:
    slug = case["slug"]
    selected = [o for o in case["options"] if o["disposition"] == "selected"]
    if len(selected) != 1:
        raise RuntimeError(f'{slug}: exactly one option must be "selected", found {len(selected)}')
    if selected[0]["id"] != case["selected"]:
        raise RuntimeError(f"{slug}: selected option id mismatch")
    if [g["id"] for g in case["gates"]] != ["G1", "G2", "G3", "G4"]:
        raise RuntimeError(f"{slug}: gates must be exactly G1..G4")
    if not 4 <= len(case["tiles"]) <= 6:
        raise RuntimeError(f"{slug}: use 4-6 magnitude tiles")
    if len(case["options"]) < 4:
        raise RuntimeError(f"{slug}: retain at least four options")
    if not 3 <= len(case["precedents"]) <= 5:
        raise RuntimeError(f"{slug}: use 3-5 precedents")
    if not 3 <= len(case["path"]) <= 5:
        raise RuntimeError(f"{slug}: use 3-5 path steps")
    if case["scope_word"] not in VERDICT_CLASS or case["auth"] not in AUTH_CLASS:
        raise RuntimeError(f"{slug}: unknown scope/authorization word")
    known = {o["id"] for o in case["options"]}
    for lens in case["lenses"]:
        if lens["state"] not in {"SUPPORTS", "DISFAVORS", "NEUTRAL", "UNKNOWN", "N/A"}:
            raise RuntimeError(f'{slug}: bad lens state {lens["state"]!r}')
        if lens["state"] not in {"NEUTRAL", "N/A"} and not lens["option_ids"]:
            raise RuntimeError(f'{slug}: lens {lens["id"]} must name option_ids')
        unknown_ids = set(lens["option_ids"]) - known
        if unknown_ids:
            raise RuntimeError(f'{slug}: lens {lens["id"]} references unknown options {unknown_ids}')


def render(case: dict) -> str:
    validate(case)
    math_record = resolve_math(case)
    html = (SKILL / "assets" / "report-template.html").read_text(encoding="utf-8")
    html = re.sub(r"<!--\n  Fill this template.*?-->", "", html, count=1, flags=re.DOTALL)

    html = block(html, "gate", "\n".join(gate_html(g) for g in case["gates"]))
    html = block(html, "tile", "\n".join(tile_html(x) for x in case["tiles"]))
    html = block(html, "option", "\n".join(option_html(o) for o in case["options"]))
    html = block(html, "lens", "\n".join(lens_html(l) for l in case["lenses"]))
    html = block(html, "finding", "\n".join(finding_html(f) for f in case["findings"]))
    html = block(html, "buy", "".join(
        f"<li><b>{t(h)}</b> — {t(b)}</li>" for h, b in case["buys"]))
    html = block(html, "nobuy", "".join(
        f"<li><b>{t(h)}</b> — {t(b)}</li>" for h, b in case["nobuys"]))
    html = block(html, "precedent", "\n".join(precedent_html(p) for p in case["precedents"]))
    html = block(html, "step", "\n".join(step_html(s) for s in case["path"]))
    html = block(html, "migration check", "\n".join(check_html(c) for c in case["migration_checks"]))
    html = block(html, "staying check", "\n".join(check_html(c) for c in case["staying_checks"]))
    html = block(html, "gap", "".join(
        f"<tr><td>{t(w)}</td><td>{t(e)}</td></tr>" for w, e in case["gaps"]))

    values = dict(LABELS)
    values.update({
        "LANG": case.get("lang", "en"),
        "LANG_DEFAULT": case.get("lang_default", "en"),
        "PROJECT_NAME": case["project_name"],
        "PROJECT_DESC": case["project_desc"],
        "DATE": case["date"],
        "VERDICT_CLASS": VERDICT_CLASS[case["scope_word"]],
        "AUTH_CLASS": AUTH_CLASS[case["auth"]],
        "SCOPE_WORD": case["scope_word"],
        "SCOPE_SUB": case["scope_sub"],
        "AUTH_WORD": case["auth"],
        "DECISION_WHY": case["why"],
        "CHANGE_TRIGGER": case["trigger"],
        "SCOPE": case["scope_chip"],
        "CONFIDENCE": case["confidence"],
        "ROBUSTNESS": case["robustness"],
        "TARGET_ARCHETYPE": case["archetype"],
        "OPTIONS_SUB": case["options_sub"],
        "LENSES_SUB": case["lenses_sub"],
        "NA_LENSES_NOTE": case["na_note"],
        "METHOD_TITLE": case["method_title"],
        "METHOD_BODY": case["method_body"],
        "FOOTER_DISCLOSURE": case["footer"],
        "ASSESSMENT_JSON": json_for_html(build_assessment(case, math_record)),
    })
    for key, value in values.items():
        if key == "ASSESSMENT_JSON":
            replacement = value
        elif key in PLAIN_TOKENS:
            replacement = html_text(str(value))
        else:
            replacement = t(value)
        html = html.replace("{{" + key + "}}", replacement)

    leftovers = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
    if leftovers:
        raise RuntimeError(f'{case["slug"]}: unfilled tokens {leftovers}')
    return html


def load_case(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(f"case_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.CASE


def main() -> int:
    wanted = set(sys.argv[1:])
    paths = sorted(p for p in CASES_DIR.glob("*.py") if not p.name.startswith("_"))
    if wanted:
        paths = [p for p in paths if p.stem in wanted]
        if not paths:
            print(f"no case modules matched {sorted(wanted)}", file=sys.stderr)
            return 1
    failures = 0
    for path in paths:
        case = load_case(path)
        try:
            html = render(case)
        except RuntimeError as error:
            print(f"FAIL {path.stem}: {error}", file=sys.stderr)
            failures += 1
            continue
        out = CASES_DIR.parent / f'{case["slug"]}-why-not-rust.html'
        out.write_text(html, encoding="utf-8")
        bilingual = "bilingual" if '<span data-l="zh">' in html else "en only"
        print(f'{case["scope_word"]:8} {case["auth"]:14} {bilingual:9} {out.relative_to(ROOT)}')
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
