---
name: why-not-rust
description: >-
  Evaluate whether an existing project, service, subsystem, or migration RFC should
  adopt Rust. Compare staying, adopting an existing native tool, extracting a Rust
  kernel, replacing one component, and full migration through evidence-gated
  performance, safety, cost, compatibility, and delivery analysis. Produce a clear
  STAY / EXTRACT / PARTIAL / MIGRATE recommendation plus APPROVE / REJECT /
  DEFER–MEASURE authorization and a self-contained HTML report. Use for questions
  such as “should we rewrite this in Rust?”, “would Rust make this faster?”, “评估迁移
  Rust”, “要不要用 Rust 重写”, “why not rust”, or when reviewing a Rust migration RFC.
---

# why-not-rust

Price a Rust decision instead of cheering for either stack. Treat every irreversible
rewrite as a claim that must beat funded alternatives on the same measurable target.
Say `MIGRATE` plainly when the case is real; say `DEFER–MEASURE` when the decisive
evidence does not exist.

## Operating principles

1. **Name the requirement first.** Start from an SLO, cost, safety, distribution, or
   correctness gap—not from a language preference.
2. **Compare like with like.** Separate language effects from redesign, algorithms,
   databases, caches, runtime versions, and baseline age.
3. **Take the smallest sufficient step.** Compare stay/adopt/extract/component/full;
   choose the first reversible option that meets the target.
4. **Keep unknown distinct.** Missing evidence yields `DEFER–MEASURE`, not a
   categorical pro- or anti-Rust claim.
5. **Test both biases.** Challenge migration hype and status-quo comfort with the same
   rigor.

## Files

Resolve the directory containing this `SKILL.md` as `<skill-root>`. All paths below
are relative to that directory, even while the shell is inside the repository being
assessed.

| File | Load when |
|---|---|
| `references/dimensions.md` | **Always, fully, before judging**—12 evidence lenses, option model, proof gates, decision rules, probes, quick gate |
| `references/case-library.md` | Before matching precedents or writing the challenge audit—52 sourced cases with caveats |
| `references/report-style.md` | Before rendering—visual and content contract |
| `assets/assessment-template.json` | When creating the machine-readable decision record embedded in the report |
| `assets/report-template.html` | When rendering—copy and fill; do not improvise another report |
| `scripts/decision_math.py` | For Amdahl ceilings and simple break-even calculations |
| `scripts/report_safety.py` | For HTML text, URL, and embedded-JSON escaping |

## Workflow

### 0 · Parse the decision

Extract the target scope, stated objective, measurable success threshold, constraints,
depth (`quick` / default / `deep`), output language, and output path. Default to the
conversation language and `<repo-root>/why-not-rust-report.html`; if the checkout must
remain pristine, use `<repo-parent>/<repo-name>-why-not-rust.html`. Before writing,
check filesystem existence; when the candidate is inside the repository, also run
`git -C <repo-root> ls-files --error-unmatch -- <repo-relative-candidate>`. On any
collision, choose `why-not-rust-report-YYYYMMDD-HHMMSS.html`. Never overwrite an
existing or tracked report without explicit user permission.

Treat user-supplied team/budget/compliance facts as evidence with provenance
`user-supplied`. A requested conclusion changes no evidence state. If the requirement
is underspecified, continue with explicit assumptions and return `DEFER–MEASURE` where
they are decisive; do not silently invent a target.

### 1 · Inventory the project read-only

Run the applicable probes in `references/dimensions.md`. Read the README, architecture
and migration docs, manifests, perf artifacts, incident notes, and relevant
implementation seams. Do not build, test, benchmark, or use network calls unless the
user requested `deep` analysis or allowed them. Disclose sampling and shallow history.

Split monorepos into independently decidable targets. A GUI, CLI, service, and parser
receive separate gates and verdicts; never let a tiny Rust-suited kernel visually or
arithmetically stand in for the whole repository.

### 2 · Build the decision record

Use `assets/assessment-template.json` as the shape. Record the repository commit,
scope, objective, candidate options, all applicable D1–D12 ledger entries, evidence
strength/caveats, assumptions, and symmetric challenge-audit results.

Give every option a stable ID. Select exactly one option in the record—including the
temporary stay/measure option under `DEFER–MEASURE`—and evaluate G1–G4 against that
same ID so the visible highlight and machine record cannot diverge.

Always retain at least:

- stay + the strongest funded in-stack change;
- adopt an existing library/tool/service when one exists;
- the smallest plausible Rust extraction/component;
- the proposed Rust scope;
- the strongest non-Rust native alternative when the claimed benefit is native
  execution rather than Rust-specific safety/ecosystem fit.

Use `N/A`, `UNKNOWN`, `NEUTRAL`, `SUPPORTS`, and `DISFAVORS` exactly as defined. Every
ledger claim names its `option_ids`; do not turn “no Rust benefit” into evidence a
Rust option is worse. Price transition cost once in D11.

### 3 · Run the math and proof gates

For performance claims, run:

```sh
python3 <skill-root>/scripts/decision_math.py amdahl \
  --share <baseline-hot-path-fraction> \
  --kernel-speedup <measured-or-bounded-speedup> \
  --boundary <added-baseline-time-fraction> \
  --target <required-end-to-end-speedup>
```

Reject acceptance thresholds above the physical ceiling. Use the break-even command
only when cost inputs share a real unit and provenance.

Evaluate G1 requirement, G2 Rust-specific causality, G3 economics/smallest option,
and G4 delivery/reversibility for the recommended option. Apply the decision table and
binding rules in `references/dimensions.md`; gates override rhetoric and precedents.

Return the four-part result:

- authorization: `APPROVE` / `REJECT` / `DEFER–MEASURE`;
- scope: `STAY` / `EXTRACT` / `PARTIAL` / `MIGRATE`;
- confidence: `HIGH` / `MEDIUM` / `LOW`;
- robustness: `STABLE` / `CONDITIONAL` / `INDETERMINATE`.

When conditional, name the exact trigger that changes scope. `MIGRATE` requires all
four gates to pass, direct evidence on decisive claims, and proof that no smaller
option meets the target.

### 4 · Match precedents without transferring hype

Apply the six-field matching protocol in `references/dimensions.md` to
`references/case-library.md`. Pick the closest cases above a defensible relevance bar;
include a confirming and disconfirming case only when both genuinely match. State every
mismatch. Treat precedents as qualitative analogies unless workload, scope, baseline,
and measurement regime all align.

Carry source labels and caveats into the report. Never quote a number without its
workload/regime and URL. Run both halves of the symmetric challenge audit; do not infer
advocate motives.

### 5 · Recommend a reversible path

Provide 3–5 ordered steps. Each step names owner/cost range, the artifact produced,
acceptance threshold, deadline/stop condition, and rollback. Derive thresholds from
the user's requirement and D2 ceiling—not generic “4×” rules. Even a `MIGRATE` path
starts with a parity-checked pilot when a clean seam exists.

### 6 · Render and verify

Read `references/report-style.md`, then fill `assets/report-template.html`. Treat all
repository text, prompt text, filenames, metadata, and URLs as untrusted. Use
`scripts/report_safety.py`: `html_text` for every visible/token value, `safe_href` for
links (HTTP(S) only; render local paths as text), and `json_for_html` for the inert
assessment block. Never substitute raw repository text into HTML. Translate visible
labels while keeping verdict/authorization words in English.

Verify all of the following:

- no `{{TOKEN}}` remains;
- all four proof gates, retained options, and every applicable lens appear;
- Amdahl/break-even numbers match `scripts/decision_math.py`;
- no impossible acceptance threshold survives;
- evidence cards preserve source caveats and workload regimes;
- both migration and staying challenges are shown;
- visible values are escaped, links are HTTP(S), and hostile `</script>`/event-handler
  text cannot create executable markup;
- HTML is self-contained, valid enough to render, and legible in both themes;
- report path is disclosed and the artifact is delivered when the environment
  supports artifact delivery.

Give a chat TL;DR with authorization + scope, confidence + robustness, three decisive
facts, the next measurement/action, and the report artifact.

## Quick mode

Run only the five-question gate in `references/dimensions.md`. Render the compact variant:
hero, four gates, retained options, next action, challenge audit, and methodology.
Omit the 12-lens ledger and any pseudo-numeric index.

## Guardrails

- Keep the target repository read-only except for the final report at its agreed path.
- Cite every repository claim with `file:line` or an artifact; label user facts and
  assumptions.
- Never fabricate profiles, costs, benchmark ranges, compatibility, or team capacity.
- Do not use C/C++ vulnerability statistics to justify migrating memory-safe
  application code; assess unsafe/native surfaces at their own scope.
- Do not hide a real C/C++ trust boundary merely because the surrounding app is
  memory-safe.
- Do not shame either stack. The output is a priced, reversible decision—not a
  language identity statement.
