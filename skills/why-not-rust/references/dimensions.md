# Evidence framework and decision protocol

Read this file fully before assessing a repository. It is the method, not a menu.

## What the method returns

Return four separate things. Never collapse them into one pseudo-precise score.

1. **Authorization** — `APPROVE`, `REJECT`, or `DEFER–MEASURE`.
2. **Scope** — `STAY`, `EXTRACT`, `PARTIAL`, or `MIGRATE`.
3. **Confidence** — `HIGH`, `MEDIUM`, or `LOW`, based on the decisive claims.
4. **Robustness** — `STABLE`, `CONDITIONAL`, or `INDETERMINATE`, based on whether
   plausible assumptions change the recommended scope.

The scope words mean:

| Scope | Meaning |
|---|---|
| `STAY` | Keep the assessed target in its current language. This may still include adopting an existing Rust-powered tool or library. |
| `EXTRACT` | Move one coarse, measurable kernel behind an existing API/process boundary. |
| `PARTIAL` | Replace one independently operated component, service, or subsystem. |
| `MIGRATE` | Replace the main implementation of the assessed target. It never means “rewrite every package in the repository.” |

`DEFER–MEASURE + STAY` means “do not authorize a migration yet; collect the named
evidence.” It does **not** mean “Rust cannot help.” This distinction keeps missing
evidence symmetric.

## Why there is no Rust Case Index

The 12 lenses below mix benefit, risk, feasibility, and option shape. Their states
are ordinal and are not commensurable: a clean FFI seam is not “twice” a team plan,
and neither can compensate for the absence of a real performance or safety need.
Do not multiply ordinal scores by arbitrary weights or derive verdicts from numeric
bands. The report may count evidence coverage, but it must not present that count as
a probability, ROI, or statistically validated predictor.

Use the lenses to build an evidence ledger, then compare explicit options through
the four non-compensatory proof gates.

## Evidence ledger

Create one record per applicable lens and decisive option claim. A record is always
about named options; repository facts do not become pro-Rust merely because native
execution might help. Each record must contain:

- `option_ids`: the explicit option or options to which the claim applies;
- `state`: `SUPPORTS`, `DISFAVORS`, `NEUTRAL`, `UNKNOWN`, or `N/A`;
- `strength`: `STRONG`, `MODERATE`, `WEAK`, or `UNKNOWN`;
- the exact claim the evidence supports;
- a repository `file:line`, artifact name, benchmark command/result, or linked
  source;
- baseline and workload regime;
- caveats and the assumption range that could change the decision.

State semantics are binding:

- `N/A` means the criterion does not bear on the stated objective.
- `UNKNOWN` means it matters but evidence is missing. Never silently convert it to
  neutral or to support for either side.
- `NEUTRAL` means evidence shows no material difference among the named options.
- `SUPPORTS` means the claim materially strengthens the named option(s) against the
  shared requirement and comparison set. It does not imply they are selected.
- `DISFAVORS` requires evidence that the named option(s) are worse or fail the shared
  requirement on that lens; the mere absence of a benefit is neutral, not negative.

The same lens may therefore have more than one record. For example, an owned CPU hot
path can support Rust, Go, C++, or WASM candidates at D1; only G2 and D12 can establish
whether Rust has a specific advantage over those alternatives.

### Evidence strength

Grade each decisive claim, not the repository as a whole.

- **STRONG** — direct measurement on the target, using a representative and current
  workload, with a checkable artifact or production trace and a comparable baseline.
- **MODERATE** — a reproducible repository benchmark, a first-party measurement with
  a disclosed method, or direct structural evidence whose causal link is strong;
  workload or baseline caveats remain.
- **WEAK** — code-shape inference, an unverified first-party/vendor claim, a close
  precedent, an old baseline, or a prompt assertion.
- **UNKNOWN** — no evidence for a decision-relevant claim.

For every `STRONG` or `MODERATE` label, check five facets and disclose failures:
directness, reproducibility, representativeness, freshness, and independence.
“First-party” is provenance, not independent verification. A benchmark can be
checkable and still be unrepresentative.

Decision confidence describes evidence quality only:

- **HIGH** when every decisive proof-gate claim is strong and current;
- **MEDIUM** when decisive claims are at least moderate, with disclosed limitations;
- **LOW** when any decisive claim is weak/unknown or the repository scan is partial.

Robustness describes sensitivity separately:

- **STABLE** when plausible assumptions do not change the selected option or scope;
- **CONDITIONAL** when a named, bounded trigger changes the decision;
- **INDETERMINATE** when unknown ranges are too wide to know which option wins.

`MEDIUM + CONDITIONAL` is valid: the evidence can be adequate while a known boundary
threshold still controls the decision.

## The 12 evidence lenses

The archetype only routes attention and probes. It never assigns numeric weights.
Use `N/A` freely; do not manufacture a finding merely to fill all rows.

### D1 · Requirement and bottleneck ownership

Name the unmet requirement before naming a language: p99 target, monthly compute
budget, memory ceiling, startup budget, vulnerability class, sandbox constraint, or
delivery invariant. For performance, locate the user-felt wall-clock and determine
whether it lives in code the team owns.

- Supports every retained option that can touch a measured, owned CPU bottleneck;
  D1 alone never makes this a Rust-specific finding.
- Disfavors a proposal when it cannot touch the dominant DOM, DB, network, disk,
  GPU-driver, or subprocess time.
- Unknown when the only evidence is “feels slow.”

Required evidence: target/SLO plus profile, trace, cost report, incident, or hard
external requirement. A safety or deployment objective does not require a CPU
profile, but it still requires direct evidence of the unsafe surface or constraint.

### D2 · Reachable end-to-end impact (Amdahl and boundary cost)

For performance proposals, quantify the fraction `f` of baseline end-to-end time in
the candidate kernel, the kernel speedup `S`, and added boundary cost `b` as a
fraction of baseline time:

`end_to_end_speedup = 1 / ((1 - f) + f / S + b)`

The infinite-kernel ceiling is `1 / ((1 - f) + b)`. If `f = 0.31` and `b = 0`, no
kernel can make the product faster than `1 / 0.69 ≈ 1.45×`. An acceptance threshold
above that ceiling is invalid.

Use `scripts/decision_math.py amdahl` for the calculation. Report input ranges, not
point estimates, when `f`, `S`, or `b` is uncertain.

### D3 · Tail latency and runtime behavior

Look for a runtime mechanism in the actual tail: GC, allocator contention, JIT
warmup, scheduler stalls, or stop-the-world work. Modern collectors **can** achieve
sub-millisecond pauses under suitable workloads and configuration; only the target's
trace decides whether that matters here.

- Supports the Rust option when a hard p99.9+ SLO is violated by a measured runtime
  mechanism and realistic tuning/runtime upgrades are exhausted.
- Neutral when the mechanism is absent or has no material effect.
- Disfavors the Rust option when it introduces a worse scheduler/runtime tradeoff for
  this workload.

### D4 · Footprint and fleet economics

Translate memory/CPU into a constraint or money: per-instance delta × instance count
× utilization × price. Separate a shell/runtime baseline that remains (Chromium,
system webview, database) from code that the migration can remove.

- Supports the Rust option when measured steady-state savings clear an explicit
  break-even at fleet, per-tab, embedded, or serverless scale.
- Neutral when footprint is immaterial.
- Disfavors the Rust option when added binaries, duplicated runtimes, or operational
  stacks cost more than they save.

### D5 · Startup and invocation shape

Startup is valuable for per-keystroke/per-save CLIs, scale-to-zero functions, plugins,
and short-lived workers. It is usually immaterial for long-lived daemons and desktop
apps started once.

Require a decomposition of runtime boot, initialization, I/O, and useful work. Do not
transfer a warm-cache multiplier to a cold/network-bound workload.

### D6 · Safety and correctness delta

Separate memory safety from broader correctness.

- A C/C++ or other manually managed core parsing untrusted input, running privileged,
  or exposed across a trust boundary is a strong Rust safety case.
- A memory-safe application with no native/FFI surface receives little additional
  **memory-safety** benefit. Rust may still improve race freedom, resource handling,
  sandbox integration, or invariant encoding, but those claims need their own incident
  or design evidence.
- A risky native dependency is assessed at that dependency's scope, not used to
  justify migrating the whole application.

For security targets, classify the project's advisory history into:
`eliminated-by-construction`, `downgraded-to-safe-failure`, and
`language-independent`. Raw CVE counts are not a causal argument.

### D7 · Concurrency, parallelism, and invariants

Distinguish throughput parallelism from concurrency correctness.

- Performance claim: show data-parallel work blocked by the GIL, serialization,
  shared-memory limits, or runtime scheduling, and compare current-language workers.
- Correctness claim: show real races, nondeterministic state, ownership bugs, or a
  design whose invariants Rust can encode materially better.

Existing parallelism, inherently sequential work, or I/O concurrency is neutral
unless the Rust option is demonstrably better or worse.

### D8 · Distribution, embedding, and runtime constraints

Test the hard constraint: static/no-runtime deployment, wasm-only host, kernel or OS
sandbox primitives, air-gapped distribution, plugin ABI, cross-compilation, or
embedded target. Compare current-stack answers (Node SEA, Bun compile, GraalVM,
WasmGC, Go) before declaring the constraint Rust-specific.

### D9 · Ecosystem and alternative availability

Inventory the target ecosystem and the current one: production-ready crates,
vendor SDKs, observability, GUI/accessibility/IME support, build tooling, and
maintenance signals. Also search for an existing Rust-powered tool/library that can
be adopted without a rewrite, and for non-Rust native alternatives.

“The best engine is a Rust crate” may favor adoption or extraction; it does not by
itself favor a full migration.

### D10 · Boundary, seam, and compatibility

This lens chooses adoption shape; it does not create benefit.

- A coarse batch-in/batch-out pure kernel or stable process/service contract supports
  `EXTRACT`/`PARTIAL`.
- Per-item FFI, JSON round-trips, shared mutable state, ORM callbacks, and DOM/event
  loop entanglement create boundary tax.
- Record data-copy cost, call frequency, ABI/platform matrix, error semantics,
  observability, and behavioral-compatibility surface.

Never recommend an extraction without including `b` in D2 and a parity test.

### D11 · Delivery economics and team readiness

Price the transition once instead of smuggling its cost into every benefit lens.
Record affected LOC/interfaces, dual-run duration, one-time engineering cost,
ongoing second-stack cost, feature-freeze exposure, hiring/ramp, bus factor,
CI/build impact, ownership, and rollback plan.

Use ranges with provenance. A generic industry rewrite multiplier is weak evidence;
the repository's change rate, compatibility surface, and staffing plan are stronger.

### D12 · Current-stack and non-Rust counterfactual

Compare like with like. Every rewrite includes redesign work, so price:

- the same algorithm/data-model/architecture change in the current language;
- a runtime/compiler/collector upgrade;
- caching, batching, query/index changes, workers, or isolation;
- adopting an existing library/service;
- a non-Rust native option such as Go, C++, Zig, or WasmGC where appropriate.

Do not compare “new Rust architecture” with “old unoptimized implementation.” Do not
compare Rust with a hypothetical perfect current stack that nobody will fund either.

## Explicit option comparison

Always evaluate at least four options:

1. stay + the strongest funded in-stack change;
2. adopt an existing library/tool/service, when one exists;
3. the smallest plausible Rust extraction/component;
4. the proposed Rust scope.

Add the strongest non-Rust native option when the benefit is native execution rather
than a Rust-specific safety/ecosystem property. Record why any option is excluded.

For every retained option, report:

| Field | Requirement |
|---|---|
| Target | Same measurable objective/SLO for every option |
| Benefit | End-to-end interval; separate language, redesign, and boundary effects |
| One-time cost | Engineering, parity, migration, tooling, and dual-run range |
| Recurring cost | Infra, build/CI, on-call, hiring, second-stack maintenance |
| Time-to-value | First measurable value, not final rewrite completion |
| Compatibility | API/data/behavior/platform risk and validation plan |
| Reversibility | Rollback/kill switch and sunk-cost boundary |
| Evidence | Claim-level strength and citations |

## The four proof gates

The gates are non-compensatory. A strong team cannot replace a missing reason, and a
clean seam cannot replace a benefit.

### G1 · Requirement

**PASS** when a measurable gap or hard safety/distribution/correctness constraint is
real and material. **FAIL** when the target already meets the requirement. **UNKNOWN**
when the requirement or baseline is not measured.

### G2 · Rust-specific causal advantage

**PASS** when evidence connects Rust (or a Rust ecosystem asset) to a material part
of the benefit after separating redesign, algorithm, database, cache, and baseline
changes. **FAIL** when the gain is wholly language-independent or in an untouched
layer. **UNKNOWN** when attribution cannot yet be separated.

### G3 · Economics and smallest sufficient option

**PASS** when the option's benefit/risk-reduction interval clears its one-time and
recurring cost, and no cheaper option meets the same target. **FAIL** when an in-stack,
adoption, or smaller extraction option meets the target sooner/cheaper. **UNKNOWN**
when cost, benefit, or Amdahl inputs are missing.

### G4 · Delivery and reversibility

**PASS** when compatibility, team ownership, dual-run, observability, acceptance,
and rollback are credible for the scope. **FAIL** when a critical compatibility or
ownership constraint makes the scope unshippable. **UNKNOWN** when the plan is absent.

## Decision table

| Gate result | Authorization | Scope rule |
|---|---|---|
| Any decisive gate `UNKNOWN` | `DEFER–MEASURE` | `STAY` now; name the exact artifact/experiment that can reopen the decision |
| G1 or G2 `FAIL` | `REJECT` | `STAY`; explain that the requirement or causal case failed |
| G3 `FAIL` because adoption/in-stack work wins | `REJECT` | `STAY`; recommend that option |
| G4 `FAIL` | `REJECT` | `STAY`, or reduce to a smaller option whose delivery gate passes; never authorize an unshippable scope |
| G1–G4 pass; low-risk coarse kernel is smallest | `APPROVE` | `EXTRACT`; require an end-to-end acceptance and rollback threshold |
| G1–G4 pass for one independent component | `APPROVE` | `PARTIAL` |
| All gates pass for the assessed target; no smaller option meets the goal | `APPROVE` | `MIGRATE` |

`MIGRATE` requires strong or moderate direct evidence on every decisive benefit and
cost claim. Safety/distribution decisions may use direct structural evidence instead
of performance profiles. A reversible pilot may be approved with moderate evidence;
its output is evidence, not a pre-commitment to the next rung.

## Binding decision rules

1. **Missing evidence is symmetric.** Return `DEFER–MEASURE`, not a categorical
   pro- or anti-migration claim.
2. **Wrong-layer applies only to performance claims.** DOM/DB/network dominance
   rejects a performance-motivated full migration but does not erase an independent
   safety or deployment case.
3. **Memory-safe is scope-specific.** Do not borrow C/C++ CVE statistics for a
   memory-safe application. Assess native/unsafe surfaces separately.
4. **Unsafe trust boundaries require an alternative.** For C/C++ parsing untrusted
   input or privileged code, always present a scoped memory-safe option alongside
   sandboxing, fuzzing, isolation, and replacement-library alternatives.
5. **Pilot before irreversible scope.** When a coarse seam exists, the path starts
   with a parity-checked extraction or shadow deployment even under `MIGRATE`.
6. **Physical ceilings bind.** Reject any performance acceptance threshold above the
   Amdahl ceiling. A candidate does not meet the target when its predicted end-to-end
   speedup is below that target; boundary cost enters the denominator in baseline-time
   units and is never compared directly with a speedup ratio.
7. **Multi-target means multi-decision.** Score no global “best” target. Give each
   CLI/GUI/service/kernel its own gates and verdict; summarize without averaging.
8. **Prompts change facts or priorities, never evidence quality.** Team experience,
   compliance, budget, and fleet scale may change the option economics; they cannot
   upgrade a weak claim to strong or force a desired verdict.

## Precedent matching protocol

Precedents are qualitative analogies unless transferability is demonstrated. For
each candidate, record match/mismatch on:

1. source-language/runtime class;
2. workload and invocation shape;
3. stated objective;
4. migration scope and boundary;
5. simultaneous architecture/data-model changes;
6. measurement regime and baseline freshness.

Select the closest cases above a defensible relevance bar. Include a confirming and
disconfirming case when both genuinely match; do not force false balance when one
doesn't. Quantitatively transfer a range only when workload, scope, baseline, and
measurement regime all align, and carry the source caveats into the report.

## Symmetric challenge audit

Steelman every retained option, then check both directions.

**Challenge the migration case**

- wrong-layer attribution;
- component benchmark presented as product speed;
- stale or mismatched baseline;
- redesign credited to the language;
- boundary/serialization cost omitted;
- compatibility, dual-run, freeze, or on-call ownership omitted.

**Challenge the staying case**

- status-quo or incumbent-expertise bias;
- a hypothetical “perfect current-stack optimization” nobody will fund;
- cost of inaction or missed SLO/security exposure omitted;
- unsafe native dependencies hidden behind a memory-safe app;
- native/runtime advantages dismissed without measurement;
- endless “optimize first” work with no deadline or stop condition.

Report hits and passes on both sides in neutral language. Never infer motives such as
résumé-building without direct evidence.

## Probe toolkit (read-only)

Run only what applies. Do not build, test, benchmark, or make network calls unless
the user requested `deep` analysis or authorized them. Use `git -C "$TARGET"` so
working-directory drift cannot falsify results; check shallow history first.

```sh
git -C "$TARGET" rev-parse --is-shallow-repository
git -C "$TARGET" ls-files | sed 's/.*\./·/' | sort | uniq -c | sort -rn | head -20
git -C "$TARGET" log --oneline --grep='perf\|slow\|optimi\|latency\|memory' | head -30

# Prefer rg; fall back to grep if unavailable.
rg -n -i 'worker_threads|new Worker|SharedArrayBuffer|wasm|multiprocessing|rayon' "$TARGET"
rg -n -i '\b(parse|tokeni|diff|encode|decode|compress|serializ|hash)' "$TARGET"
rg -n -i 'node-gyp|binding\.gyp|maturin|cffi|ctypes|cgo|unsafe\s*\{' "$TARGET"
rg -n -i 'electron|tauri|experimental-sea|bun build --compile|serverless' "$TARGET"
find "$TARGET" \( -name '*.cpuprofile' -o -name 'flamegraph*' -o -name '*.speedscope.json' \) -print | head
```

Read the README/architecture docs, dependency manifests, perf artifacts, incident
notes, and any migration RFC. For a large repository, disclose the sampled paths and
anything not inspected.

## Adapting to the user's prompt

| User input | Effect |
|---|---|
| `quick` | Run the five-question gate below; omit the 12-lens ledger and any numeric summary |
| `deep` / permission to run code | May run existing benchmarks/profilers; preserve the target except for the report |
| `focus on X` / `只看 X` | Assess X as the target; whole-repo facts are context only |
| team, compliance, budget, fleet constraints | Insert as option facts and G3/G4 inputs; cite as user-supplied |
| requested conclusion | Steelman it, then run the same gates; do not conclusion-shop |
| language/path | Obey; default report language is the conversation language |

## Five-question quick gate

1. What measurable requirement is currently missed?
2. Where does that gap live, and is it in code the team owns?
3. What Rust-specific mechanism changes it after the same-redesign counterfactual?
4. What is the smallest option that meets the target, with Amdahl/boundary math?
5. Who owns compatibility, dual-run, acceptance, and rollback?

Return gate states, `authorization + scope`, confidence, the decisive unknowns, and
the next measurement. Quick mode never fabricates an index from five answers.
