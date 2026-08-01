# The 12 dimensions, the weight table, and the verdict engine

This file is the scoring core of `why-not-rust`. Read it fully before scoring.
Nothing here is advisory styling — the caps and floors at the bottom are hard rules
that override the numeric index.

## How scoring works

- Each dimension gets a **score `s ∈ {−2,−1,0,+1,+2}`** — positive means *Rust migration
  buys something real here*, negative means *this dimension argues for staying*.
- Each dimension gets a **weight `w ∈ {0,1,2,3}`** from the archetype table below,
  then adjusted by explicit user constraints (log every adjustment).
- **Rust Case Index** `= 100 × Σ(sᵢ·wᵢ) ÷ (2 × Σwᵢ)`, range −100…+100.
- Verdict bands (before caps/floors):
  - `≥ +40` → **MIGRATE** (full migration justified)
  - `+15 … +40` → **PARTIAL** (rewrite one component/service)
  - `−10 … +15` → **EXTRACT** if a clean seam exists (D10 ≥ +1) **and at least
    one gain dimension among D1–D9 scored ≥ +1 on evidence** (a clean seam with
    nothing behind it is an option, not a verdict), else **STAY**
  - `< −10` → **STAY** (still note a kernel opportunity if D10 ≥ +1 and some
    dimension scored +2 on measured evidence)
- Scores must cite evidence (`file:line`, a profile, a config) or be marked
  `estimated`. Never average away a hard rule with arithmetic.

The four verdicts form a ladder of *smallest sufficient step*:
**STAY** (optimize in place) → **EXTRACT** (hot kernel via wasm/napi/PyO3/sidecar)
→ **PARTIAL** (one component/service) → **MIGRATE** (the stack). Always recommend
the smallest step that meets the user's stated goal.

## The dimensions

### D1 · Bottleneck locus — where does wall-clock actually go?
The master dimension. Language changes only help time spent in *code you own,
executing language-bound work*. Time in DOM/layout, the database, the network,
disk, or a subprocess is invisible to a rewrite.
- **−2** dominated by DOM/DB/network/IO/another process (browser layout pipeline,
  SQL waits, API fan-out)
- **0** mixed, or unknown (unknown also triggers the evidence cap, C1)
- **+2** measured majority of time in owned CPU-bound code: parsing, diffing,
  encoding, tokenizing, simulation, tight loops over large arrays
Signals: CPU profiles; framework type (CRUD server vs codec); grep for hot-loop
nouns; DB client density vs compute-library density.

### D2 · Amdahl ceiling — how much of end-to-end time is the candidate hot path?
A 20× kernel speedup on 10% of runtime is a 1.1× product. Compute the ceiling
before admiring the multiplier.
- **−2** hot candidate < 10% of the end-to-end path users feel
- **0** 20–40%, or plausible but unmeasured (mark estimated)
- **+2** ≥ 60% of a path users care about, measured
Signals: profile percentages; if absent, back-of-envelope from operation counts —
and say so. Structural inference is allowed for tool-shaped repos: when the tool
IS the hot path (a formatter, compiler, codec CLI — no DB, no DOM, no network in
the loop), +2 may rest on structural certainty plus in-repo compilation evidence
(e.g. "AOT-compiling the core doubled throughput" implies owned-CPU dominance);
label the residual share `estimated`. C1 still applies — structural certainty is
not a profile artifact.

### D3 · Latency profile — GC pauses and tail SLOs
The Discord case (Go GC spikes vs a hard tail SLO) is real but narrow. Modern GCs
(Go sub-ms STW, V8 concurrent, JVM generational ZGC) already deliver sub-millisecond
pauses; GC-phobia without a measured pause problem scores negative, not zero.
- **−2** no tail SLO; GC never shows in traces (or nobody ever looked because
  nothing hurt)
- **0** occasional GC visibility, tunable headroom left (ballast/soft-limit/heap
  sizing not yet tried)
- **+2** hard p99.9+ SLO, measured GC-caused violations, tuning exhausted
Signals: SLO docs, latency dashboards, GC flags in deploy configs, incident notes.

### D4 · Memory footprint & density economics
Footprint is money only when multiplied: per-instance × fleet, per-tab, embedded
RAM ceilings, serverless cold-start memory. A single desktop instance rarely
justifies anything (and an Electron baseline is the shell's cost, not your code's).
- **−2** single-instance app; RSS is a non-issue or dominated by the shell/runtime
  baseline you're keeping anyway
- **0** footprint matters but current stack has untried headroom
- **+2** fleet-scale $/GB math or hard RAM ceiling, with numbers (the
  Cloudflare/npm shape)

### D5 · Startup time & invocation shape
Cold start matters for per-keystroke/per-save CLIs (the ruff/uv shape: JIT warmup
and interpreter boot dominate small runs) and scale-to-zero serverless. It's
irrelevant for daemons and long-lived apps.
- **−2** long-running process; starts once a day
- **0** started often; startup annoying but not the workflow bottleneck
- **+2** invoked constantly in inner dev loops / per-request cold starts, and
  runtime boot is a measured share of each run

### D6 · Memory-safety delta
Rust's safety argument is **vs C/C++**, not vs GC languages. TS/JS/Go/Java/Python
are already memory-safe: migrating them to Rust buys ≈0 safety. The ~70%-of-CVEs
figure (MSRC, Chrome) and the Android trajectory apply only to memory-unsafe code.
- **−2** source is memory-safe and has no meaningful native/FFI surface (claiming
  "safety" here is the classic conflation — flag it)
- **0** memory-safe source but a real native-dep/FFI surface (score the surface,
  not the app; the case for replacing a risky native dep goes in the findings and
  path as prose — it never lifts this score above 0)
- **+2** C/C++ core parsing untrusted input / privileged context (also triggers
  floor C4)
For security-parser targets, the highest-value D6 artifact is an **advisory
taxonomy**: dissect the project's own CVE/advisory history (NEWS, security
advisories) into {eliminated-by-construction in Rust / downgraded to safe crash /
language-independent} and score from the first bucket's share, not from the raw
count.

### D7 · Concurrency & parallelism upside
Score the *unclaimed* parallelism the current stack can't reach: single-threaded
runtime with an embarrassingly-parallel workload, GIL-bound Python compute,
worker-pool experiments eaten by serialization tax. If the workload is sequential
or already saturates cores, there's nothing to buy.
- **−2** inherently sequential, or already parallel and IO-bound anyway
- **0** parallelizable in current stack (workers/threads) but untried
- **+2** measured serialization-tax or GIL wall blocking data-parallel speedup
  Rust/rayon/shared-memory would unlock

### D8 · Distribution & deployment constraints
Real Rust wins: single static binary where the runtime can't go, wasm targets,
no-runtime embedding (plugins, edge, sandboxes). But check the stay-stack answers
first: Node SEA / Bun compile / Go already do single binaries; Electron/Tauri is a
shell choice, not an app-language choice.
- **−2** current distribution already meets requirements; a rewrite would break a
  working packaging chain
- **0** distribution friction exists; stay-stack options untried
- **+2** hard requirement current stack cannot meet (no-runtime embed, wasm-only
  host, air-gapped static binary)

### D9 · Domain ecosystem fit
Does Rust's ecosystem *pull* (Arrow/DataFusion/Polars for columnar data, tokio for
network infra, embedded HALs) or *drag* (GUI toolkits still young vs the DOM;
vendor SDKs missing; your domain's gravity in npm/PyPI)?
- **−2** domain gravity is in the current ecosystem; Rust equivalents immature
  (classic: desktop GUI, vendor SDK breadth)
- **0** parity
- **+2** the best-in-class engine for this domain is already a Rust crate you'd
  otherwise reimplement (ecosystem-pull, the InfluxDB shape)
Note the inversion: sometimes the ecosystem-pull answer is *use the Rust-powered
library from your current language* (Polars from Python) — that's D12's territory;
score it there as a strong counterfactual.

### D10 · Seam quality — is there an incremental path?
The single best predictor of a *successful* adoption. A pure-function kernel with
struct-in/struct-out (diff, parse, validate, encode) extracts cleanly via
wasm/napi-rs/PyO3/sidecar; a kernel tangled with the event loop, ORM, or DOM does
not. Stylo (extracted, shipped) vs whole-Servo (never replaced Gecko) is the
canonical pair.
- **−2** no seam: logic diffused through framework callbacks and shared mutable
  state; boundary would be chatty (per-item calls, the serialization tax eats the
  win)
- **0** seam exists but boundary cost unmeasured
- **+2** clean coarse-grained boundary; data crosses rarely and in bulk; bindings
  story proven in this ecosystem
Score seam × payload: a clean boundary with **no hot kernel behind it** caps at
+1, and the note must name the absence — an empty seam is an option, not an
argument.
Boundary math to include when scoring +: kernel_speedup_effective =
1 ÷ (boundary_cost_share + kernel_share/kernel_speedup).

### D11 · Team & organizational readiness
Rust's learning curve and compile-time tax are consistently the top complaints in
Rust's own annual survey; Google reports teams reach Go-comparable velocity after
ramp — but ramp is months, and a bus-factor-of-one Rust codebase is a liability.
- **−2** zero Rust capability, no hiring plan, delivery pressure high
- **0** a couple of enthusiasts; org tolerant of ramp
- **+2** experienced Rust engineers on staff; CI/tooling already speaks Rust
This dimension gates MIGRATE (cap C5) but should rarely block a one-kernel EXTRACT
— a bounded kernel is how teams learn.

### D12 · Counterfactual strength — what would staying achieve?
The attribution-error killer. Any rewrite ships a redesign, and the redesign is
usually where the win lives. Before crediting Rust: newer runtime (Node LTS bump,
YJIT, JDK 21), a better algorithm, caching, batching, worker threads, an existing
fast library (better-sqlite3, Polars, sharp), architecture fixes (virtualization,
batching DOM writes).
- **−2** obvious stay-stack moves untried — the counterfactual is strong, so it
  argues AGAINST migration (score negative)
- **0** some optimization done; inventory incomplete
- **+2** counterfactual exhausted: algorithmic best-known in current language,
  profiled, and still short of the requirement by a language-sized gap
Note the direction: this dimension is *reverse-framed*. A strong untried
counterfactual pushes the index down. Worked example: a repo that already ships
AOT-compiled wheels, caching, and multiprocess parallelism has *spent* its
counterfactual → score +1/+2 (pushes the index UP — staying has little left to
offer); a repo with an obvious untried algorithm swap scores −2 (pushes it DOWN).

### Source-language calibration (read before scoring native→native)

The anchors above are written from a GC-runtime source's perspective. When the
source is already a native, non-GC language (C/C++/Zig), recalibrate: D1/D3/D5
performance upside anchors near **0 absent measured wins** — Bun's Zig→Rust port
moved performance 2–5%; fish shipped C++→Rust at self-declared parity; uutils
shipped with regressions against 40-year-tuned GNU C. The live dimensions become
D6 (untrusted-input exposure — use the advisory taxonomy), concurrency
*correctness* (fish's actual motive), D11 contributor economics, and D12 in the
form "what would sandboxing/fuzzing/isolation buy without a rewrite?". Rule:
for an AOT-native source, cap D1 at 0 unless a measured, language-attributed
delta exists (otherwise D1 double-counts what D12 already scores).

**Migration already in flight?** When the repo contains a live migration
experiment (an `engine-rs` beside the shipping engine), don't invent a fifth
verdict and don't score the experiment as a separate target: score the shipping
target normally, and express the experiment's disposition as a **quantified
promotion gate** rider — the measurable bars (same-dataset quality ≥ incumbent,
latency ≤ incumbent, etc.) it must clear to be promoted, and what archiving it
gracefully looks like if it stalls (the curl-hyper precedent).

## Meta-attributes (not scored, but binding)

**Evidence tier** — grade the whole assessment:
- `E2 measured`: profiles/benchmarks exist as **checkable artifacts** (a
  .cpuprofile, a bench script + numbers, CI perf output)
- `E1 repo-signal`: indirect evidence (perf commits, worker experiments, caching
  layers, TODO(perf) density). **A first-party documented claim without a
  checkable artifact — "compiling doubled performance" in the docs, a
  measurement in an engineering note with methodology but no re-runnable
  script — is E1, not E2.** C1 hinges on this exact call; when in doubt, E1.
  Well-documented first-party notes may justify individual dimension scores, but
  confidence caps at Medium and the path must include landing a re-runnable
  benchmark in-repo.
- `E0 hearsay`: "feels slow", hype, no artifacts
Confidence: High = E2 on decisive dimensions; Medium = E1; Low = E0 or partial
scan. Confidence appears in the hero, always.

**Motivation audit** — check the ask itself against the misconception list in
`case-library.md` §Traps (safety-conflation, amdahl-blindness, attribution-error,
gc-phobia, benchmark-theater, hybrid-blindness, rewrite-freeze denial,
resume-driven). Report hits honestly, including when the *user's own prompt*
presupposes the answer.

## Archetype weight table

Pick the archetype(s); a monorepo gets one assessment per distinct target (a CLI
and a GUI in one repo are two rows, one report with per-target verdicts). Weights
are defaults — adjust only with explicit reasons, and log adjustments in the
report's methodology box.

| Archetype | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 |
|---|--|--|--|--|--|--|--|--|--|--|--|--|
| web-frontend (browser SPA) | 3 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 3 |
| electron-desktop | 3 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 3 | 2 | 3 |
| native-desktop-gui | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 2 |
| mobile-app | 3 | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 3 | 2 | 2 | 2 |
| cli-quick (per-keystroke/save) | 3 | 3 | 1 | 1 | 3 | 1 | 2 | 2 | 2 | 2 | 2 | 3 |
| cli-longtask (minutes per run) | 3 | 3 | 1 | 2 | 1 | 1 | 3 | 2 | 2 | 2 | 2 | 3 |
| compiler-buildtool | 3 | 3 | 1 | 2 | 2 | 1 | 3 | 2 | 2 | 2 | 2 | 3 |
| backend-crud (IO/DB-bound API) | 3 | 3 | 2 | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 3 |
| infra-hotpath (proxy/broker/engine at fleet scale) | 3 | 2 | 3 | 3 | 1 | 2 | 3 | 2 | 2 | 2 | 2 | 2 |
| data-pipeline (columnar/stream) | 3 | 3 | 1 | 2 | 1 | 1 | 3 | 1 | 3 | 3 | 2 | 3 |
| lib-with-bindings (scripting-lang hot core) | 3 | 3 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 3 | 2 | 2 |
| embedded-realtime | 2 | 2 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 1 | 2 | 1 |
| game | 3 | 2 | 3 | 2 | 1 | 1 | 3 | 2 | 3 | 2 | 2 | 2 |
| security-parser (C/C++ on untrusted input) | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 2 | 2 | 3 | 2 | 2 |

Rationale anchors: cli-quick weights D5 high (the ruff/uv shape); infra-hotpath
weights D3/D4 high (the Discord/Cloudflare shape); security-parser weights D6
high (the sudo-rs/Android shape); electron-desktop weights D10/D12 high because
its wins come from kernels and architecture, almost never from app-code language.

## Caps and floors (hard rules — they override the index)

- **C1 · Evidence cap.** No E2 evidence behind the performance-motivated scores →
  verdict caps at **EXTRACT**, and recommendation #1 must be *measure* (name the
  exact profile to capture). Does not apply when the driver is safety (D6) or
  distribution (D8) with hard external requirements. Rider display rule: the
  "(measure first)" qualifier appears on the verdict chip only when the capped
  verdict is EXTRACT or above — a STAY verdict doesn't need it (it reads as
  indecision); there, C1 lives in the methodology box and as path step 1. In a
  multi-target report the rider attaches to the affected target's own chip,
  never to the global verdict.
- **C2 · Wrong-layer cap.** D1 ≤ −1 (time lives in DOM/DB/network) → verdict caps
  at **PARTIAL**, and any PARTIAL must target only the owned-CPU component. You
  cannot rewrite your way out of the browser layout pipeline or a slow query.
- **C3 · Safety zero.** All source languages memory-safe → D6 ≤ 0 no matter what
  the prompt claims. Replacing a risky native dep is a scoped argument worth at
  most +1 with the scope named.
- **C4 · Safety floor.** Memory-unsafe core parsing untrusted input in a
  security-relevant context → the report must present a scoped migration option
  (at least PARTIAL consideration) even if the index is negative — with honest
  cost, and alternatives (sandboxing, fuzzing, wasm isolation) beside it.
- **C5 · Team gate.** D11 = −2 → MIGRATE demotes to PARTIAL; state what readiness
  change would re-open it.
- **C6 · Hybrid first.** Even a MIGRATE verdict starts its recommended path with
  an extraction pilot when D10 ≥ +1 — de-risk before committing the fleet.

## Probe toolkit (read-only; each probe names the dimensions it feeds)

Run what applies; skip what doesn't; never run the project's own build/tests or
any network call without the user asking. Sample large repos and disclose sampling.

Run every `git` probe as `git -C "$TARGET"` (the shell's cwd drifts across tool
calls; relative-path xargs failures look like empty results). And check history
depth FIRST — on a shallow clone every `git log` probe silently returns nothing:

```sh
git -C "$TARGET" rev-parse --is-shallow-repository   # true → history probes lie;
                                                     # fall back to NEWS/CHANGELOG files
```

```sh
# Inventory & languages (all dimensions' context)
git ls-files | sed 's/.*\./·/' | sort | uniq -c | sort -rn | head -20
git ls-files '*.<main-ext>' -z | xargs -0 wc -l | tail -1          # LOC per language
# tokei/cloc if installed — prefer them, note which you used

# Archetype & deployment (D4, D5, D8)
ls Dockerfile* compose* serverless* fly.toml 2>/dev/null
grep -l '"electron"\|tauri' package.json */package.json 2>/dev/null
grep -rn 'pkg\|nexe\|--experimental-sea\|bun build --compile' package.json scripts/ 2>/dev/null

# Native/FFI surface (D6, D8, D10)
grep -rn 'node-gyp\|binding.gyp\|\.node"' package.json */package.json 2>/dev/null
grep -rn 'maturin\|cffi\|ctypes\|cgo' pyproject.toml go.mod 2>/dev/null
ls Cargo.toml */Cargo.toml 2>/dev/null                              # Rust already here?

# Hot-path nouns & parallelism attempts (D1, D2, D7, D10)
# NOTE: repeat --include per extension — a quoted brace glob ('*.{ts,py}') silently
# matches nothing on BSD grep; and `| head` masks grep's exit code, so treat an
# empty result as "not shown", not "absent" — re-run unfiltered before concluding.
grep -rniE 'worker_threads|new Worker|SharedArrayBuffer|wasm|multiprocessing|rayon' src/ --include='*.ts' --include='*.js' --include='*.py' --include='*.go' -l
grep -rniE '\b(parse|tokeni|diff|encode|decode|compress|serializ|hash)' src/ -l | head

# Perf evidence (D1, D2, D3, evidence tier) — find, not ** globs (globstar is
# shell-dependent; a silent non-match reads as "no evidence")
find . -name '*.cpuprofile' -o -name 'flamegraph*' -o -name '*.speedscope.json' 2>/dev/null | head
ls -d bench* benchmarks* perf* 2>/dev/null
git -C "$TARGET" log --oneline --grep='perf\|slow\|optimi\|latency\|memory' | head -30

# IO/DB shape (D1)
grep -oE '"(pg|mysql2?|redis|ioredis|prisma|mongoose|sqlalchemy|gorm)"' package.json */package.json pyproject.toml 2>/dev/null
```

## Adapting to the user's prompt

The invocation may carry constraints. Apply them mechanically and log them:

| User says (examples) | Effect |
|---|---|
| "只看 X / focus on X" | Scope = X; archetype from X; whole-repo facts become context only |
| "我们有 N 名 Rust 工程师 / team knows Rust" | D11 score/weight up; log |
| "必须满足内存安全合规 (CISA/内部红线)" | D6 weight → 3; C3 still applies to memory-safe sources — compliance is about the unsafe surface |
| "fleet 规模 / 每月云账单 $X" | D4 weight → 3; ask the math to appear in the report |
| "quick" | Run the 5-question gate only; short report |
| "deep / 可以跑代码" | May run existing benchmarks/profilers; still never mutate the repo |
| "帮我论证迁移是对的" | Run the engine honestly; if the verdict disagrees, say so explicitly — the skill's contract is evidence over conclusion-shopping |
| output language / path | Obey; default report language = conversation language |

## The 5-question quick gate (for `quick` mode)

1. Where does wall-clock go, per a profile? (No profile → the answer is "measure",
   not "migrate".)
2. Is that time in code you own, doing language-bound work — not DOM/DB/network?
3. What share of the end-to-end path is it (Amdahl ceiling)?
4. What's the smallest step that captures ~80% of the gap — algorithm, cache,
   parallelism, an existing fast library, a kernel extraction?
5. What breaks during an N-month rewrite freeze, and who maintains two stacks?

Quick mode still renders the report (short form) and still applies caps C1–C3.
