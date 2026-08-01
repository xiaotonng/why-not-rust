---
name: why-not-rust
version: 0.1.0
description: >-
  Evidence-based analysis of whether the current project should migrate to Rust —
  and, almost always more useful, whether it should NOT. Produces a verdict
  (STAY / EXTRACT / PARTIAL / MIGRATE) with a 12-dimension scorecard, matched
  industry precedents, and a self-contained styled HTML report. Use when the user
  asks any variant of: "should we rewrite/migrate this to Rust", "would Rust make
  this faster", "评估一下迁移 Rust", "要不要用 Rust 重写", "why not rust", or asks
  to sanity-check a Rust-rewrite proposal. Also fits: evaluating a specific module
  for extraction into Rust (wasm/napi/PyO3), or reviewing someone else's
  Rust-migration RFC.
---

# why-not-rust

The industry ships loud "we rewrote it in Rust and it's 25× faster" stories.
Some are real (ruff, Pingora, pydantic-core). Many credit the language for wins
that came from a redesign, better algorithms, parallelism, or cold-start physics —
and most interactive-app "slowness" lives in layers (DOM, DB, network) a language
swap cannot touch. This skill answers the migration question with evidence, in
either direction. The name is the question *and* the default posture: the burden
of proof is on the migration.

**Principles** (they resolve every judgment call):
1. **Burden of proof on migration.** No measurement → no MIGRATE verdict.
2. **Smallest sufficient step.** STAY → EXTRACT (kernel) → PARTIAL (component) →
   MIGRATE. Recommend the first rung that meets the stated goal.
3. **Attribution honesty.** A rewrite always ships a redesign; compare against
   "redesign in the current language", not against the legacy code.
4. **Wrong-layer realism.** DOM/DB/network time is invisible to a rewrite.
5. **Safety is a C/C++ argument.** Memory-safe languages get ≈0 safety from Rust.
6. **Honest both ways.** When the evidence says migrate (Discord-shaped tail
   SLOs, ruff-shaped CLIs, C-parsing-untrusted-input), say MIGRATE plainly.

## Files

| File | Load when |
|---|---|
| `references/dimensions.md` | ALWAYS before scoring — 12 dimensions, weight table, caps/floors, probes, prompt-adaptation table, quick gate |
| `references/case-library.md` | When matching precedents & writing the traps section — 40+ cited industry cases with true-driver tags |
| `references/report-style.md` | Before rendering — the visual contract |
| `assets/report-template.html` | The report skeleton — copy and fill; never restyle |

## Workflow

### 0 · Parse the ask
Extract from the user's prompt: scope (whole repo? one module?), constraints
(team, compliance, budget, deadlines), depth (`quick` | default | `deep`), output
language (default: the conversation's language) and path (default:
`<repo-root>/why-not-rust-report.html` — an untracked file; say so in the TL;DR.
If the checkout must stay pristine — CI bot, read-only clone — write next to the
repo instead: `<repo-parent>/<name>-why-not-rust.html`). Apply the adaptation
table in
`dimensions.md`. If the prompt presupposes a conclusion, note it — the engine
still runs honestly.

### 1 · Inventory the project (read-only)
Run the probe toolkit (`dimensions.md` §Probes): languages & LOC, deployment
shape, native/FFI surface, hot-path nouns, parallelism attempts, perf evidence
(profiles, benches, perf-tagged commits), IO/DB dependency shape. Read the
README/architecture docs and any perf-related issues or docs you find. Do NOT
build, test, or run the project unless the user said `deep`/allowed it. Do NOT
modify anything except writing the final report file.

### 2 · Classify archetype(s)
Pick archetype rows from the weight table. A monorepo with distinct targets (CLI +
GUI + server) gets one scored column per target and per-target verdicts in one
report. Name the archetype in the report hero.

### 3 · Score the 12 dimensions
For each dimension: score −2…+2 with a one-line evidence citation (`file:line`,
profile name, config) or an explicit `estimated`. Grade the evidence tier
(E0/E1/E2). Compute the index. Apply every cap/floor that triggers (C1–C6) —
they override arithmetic.

### 4 · Verdict + confidence
One of STAY / EXTRACT / PARTIAL / MIGRATE (+ per-target variants), one-sentence
"because", confidence High/Medium/Low from the evidence tier. If C1 triggered,
the verdict line carries the "measure first" rider and recommendation #1 is the
exact profile to capture.

### 5 · Match precedents
From `case-library.md`, pick 3–5 cases sharing the archetype/driver tags —
deliberately mixed outcomes (a stayed-and-won, a hybrid, a genuine migration, and
where apt a failed/abandoned one). One line each: what they did, what it proves
for THIS project. Run the traps checklist; report hits and passes.

### 6 · Recommended path
3–5 ordered steps following smallest-sufficient-step, each with rough effort and
an explicit acceptance threshold where measurable (e.g. "wasm PoC wins only if
end-to-end ≥4× including boundary cost"). Full-migration steps appear only under
a MIGRATE verdict or as the explicitly-labeled trigger condition of the last step.

### 7 · Render the report
Copy `assets/report-template.html`, delete its instructional header comment, fill
every `{{TOKEN}}` (`SKILL_VERSION` = the `version` in this file's frontmatter),
duplicate the marked repeatable blocks, delete unused optional blocks, translate
labels to the report
language. Follow `report-style.md` exactly — same palette, same section order; the
uniform look across projects and users is a feature. Verify: every bar width =
|score×weight| ÷ 6 × 50 (% of the full track — recompute one row by hand); numbers
in the HTML match the scores; no `{{` left. Then give the chat TL;DR: verdict +
index + confidence + 3 decisive
bullets + report path. If an artifact-delivery tool exists in this environment,
also deliver the file.

`quick` mode: run probes shallowly, answer the 5-question gate, render the short
report variant (hero + tiles + gate answers + path), still apply caps C1–C3.

## Guardrails

- Target repo is **read-only**; the only write is the report file (and only at
  its default/agreed path).
- Never fabricate numbers. Estimates are labeled `estimated`; absent evidence is
  "unknown", which is itself a finding (it caps the verdict via C1).
- Every repo claim carries `file:line` or a filename. Every industry number in
  the report must exist in `case-library.md` with its URL — no from-memory stats.
- Large repo? Sample (top dirs by LOC + entry points) and disclose the sampling
  in the methodology box.
- WebSearch, if available, may enrich precedents — but the report must stand on
  the bundled case library alone (offline-safe).
- The report never shames the current stack or cheerleads Rust; it prices a
  decision.
