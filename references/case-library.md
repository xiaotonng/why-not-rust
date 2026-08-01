# Case library — cited precedents for the Rust-migration question

Match the target by **archetype** (same 14 archetypes as the weight table in `dimensions.md`) plus **driver tags**; pull 3–5 cases with deliberately mixed outcomes, then run §5 as the misconception audit.
Verification legend: **[V]** first-party verified (source fetched or benchmark reproducible), **[V(s)]** first-party source located, figures via search excerpts / background-cited URL, **[C]** vendor or speaker claim, unvetted.
Nuance flags inline: (vendor-claim), (vendor-curated), (N=1), (baseline-age), (self-reported). Every number keeps its URL; quote nothing that lacks one.

## Tag taxonomy

- **Driver tags** (why the org moved): `cpu-tight-loop` | `gc-tail-latency` | `memory-footprint` | `startup-time` | `memory-safety-from-c` | `single-binary` | `cross-platform-core` | `concurrency-correctness` | `ecosystem-pull` | `contributor-experience` | `cost-efficiency` | `hype-or-brand`
- **Debunk tags** (what a case disproves — §5 audits all of them): `amdahl-blindness` | `attribution-error` | `benchmark-theater` | `gc-phobia` | `safety-conflation` | `boundary-tax` | `hybrid-blindness` | `rewrite-freeze-risk` | `resume-driven`

## 1 · Genuine migrations (the preconditions were real)

### Discord · Read States service — Go → Rust (2020)
- scope: ONE hot-path service (read/unread tracking); the client stayed Electron, Python/Elixir stayed elsewhere | archetype: infra-hotpath | drivers: gc-tail-latency
- facts: [V] Go forced a GC pass every ~2 min that scanned a giant LRU (tens of millions of Read States) → latency/CPU spikes; Rust version "had no latency spikes" and after tokio 0.2 tuning they "beat Go on every single performance metric"; cache then raised to 8M entries; exact ms values exist only in graph images. (baseline-age) [V] footnote: benchmarked on **Go 1.9.2** (2017), only 1.8–1.10 tried; Go 1.12 GC + 1.14 preemption never tested. https://discord.com/blog/why-discord-is-switching-from-go-to-rust
- true driver: no-GC removed the periodic whole-cache scan — genuinely language-attributable on a pathological workload (huge long-lived working set, low garbage, strict tail SLO). Part of the gain is a hand-tailored BTreeMap LRU, i.e. data-structure work.
- proves: D3 +2 requires exactly this shape — measured GC-caused tail violations with tuning exhausted; also D1/D2 (the hot path was ~the whole service).
- skeptic: does not indict modern Go; a rerun on current Go + GOMEMLIMIT is the missing counterfactual (D12); no absolute numbers in text.

### Discord · message storage — Cassandra/JVM → Rust data services + ScyllaDB (2023)
- scope: storage tier | archetype: infra-hotpath | drivers: gc-tail-latency, concurrency-correctness
- facts: [V(s)] read p99 40–125ms → 15ms; insert p99 5–70ms → 5ms; 177 → 72 nodes; custom Rust migrator moved 3.2M messages/s. https://discord.com/blog/how-discord-stores-trillions-of-messages
- true driver: three at once — DB engine swap (Java → C++ ScyllaDB, shard-per-core), request-coalescing architecture, Rust in the middle tier; first-party framing credits ScyllaDB + coalescing at least as much as Rust.
- proves: D12 in production form: the p99 collapse is mostly the database — calibrates attribution for any "we added Rust and p99 fell" story.
- skeptic: attribution-error canonical; never quote the p99 delta as a language result.

### AWS · Aurora DSQL adjudicator — Kotlin/JVM → Rust (2024–25)
- scope: one component first, then the whole data + control plane | archetype: infra-hotpath | drivers: gc-tail-latency, cpu-tight-loop
- facts: [V(s)] years of tuning took Kotlin from 2,000 → 3,000 TPS; two engineers with zero Rust/C/C++ experience produced a Rust version at ~30,000 TPS — "10x faster than our carefully tuned Kotlin implementation – despite no attempt to make it faster." https://www.allthingsdistributed.com/2025/05/just-make-it-scale-an-aurora-dsql-story.html
- true driver: plausibly allocation patterns + serialization + JIT warmup + GC combined; no public benchmark harness; HN/Lobsters asked where the 10x came from.
- proves: D3/D1 can genuinely stack on a hot coordinator; also grades evidence tiers — first-party with no artifact is E1, not E2.
- skeptic: (N=1), unreproducible; "no attempt to make it faster" also means the tuned-JVM *redesign* counterfactual was never run.

### Cloudflare · Pingora + FL2 — C/Lua (NGINX + OpenResty) → Rust (2022; FL2 2025)
- scope: fleet-scale edge proxy, >1T req/day | archetype: infra-hotpath | drivers: memory-safety-from-c, concurrency-correctness, cost-efficiency
- facts: [V] Pingora: ~70% less CPU, ~67% less memory at the same traffic; median TTFB −5ms, p95 −80ms; one customer's connection reuse 87.1% → 99.92%. https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/ · [V(s)] FL2 (2025): median −10ms, +25% on CDN perf tests, CPU + memory cut by more than half. https://blog.cloudflare.com/20-percent-internet-upgrade/
- true driver: first-party verbatim — **"This is not because we run code faster. Even our old service could handle requests in the sub-millisecond range. The savings come from our new architecture which can share connections across all threads."** Rust earns partial credit vs Lua (no GC/copies) plus the C-replacement safety case.
- proves: D4 +2 shape (fleet $/GB math with numbers); D12: the headline is architecture — demand the same-architecture counterfactual before crediting the language.
- skeptic: retellings as "Rust made it 3x cheaper" contradict Cloudflare's own words; Workers still runs on C++/V8 (workerd) — polyglot, not doctrine.

### npm · authorization service — Node.js → Rust (2019)
- scope: one CPU-bound service | archetype: backend-crud | drivers: cpu-tight-loop, single-binary, contributor-experience
- facts: [V] whitepaper: "npm's first Rust program hasn't caused any alerts in its year and a half in production"; "My biggest compliment to Rust is that it's boring."; rewrite cost: ~1 hour in Node, 2 days in Go, ~1 week in Rust (learning included); zero throughput/latency numbers published. https://www.rust-lang.org/static/pdfs/Rust-npm-Whitepaper.pdf
- true driver: operability testimonial, not a perf story; Go was rejected over 2019-era dependency management — (baseline-age) obsolete since Go modules.
- proves: D11 calibration: 1h/2d/1w is the honest people-cost ratio for a small service; "boring in prod" is the post-ramp upside; stated downside = maintaining a second monitoring/logging stack.
- skeptic: proves ops-quiet, not fast.

### Figma · multiplayer sync server — TypeScript/Node → Rust child process (2018)
- scope: doc-sync engine only; Node KEPT the network layer, one Rust process per document over stdio | archetype: infra-hotpath | drivers: cpu-tight-loop, gc-tail-latency, memory-footprint
- facts: [V] worst-case serialization >10x faster; server-side multiplayer perf better by "an order of magnitude"; low Rust memory made process-per-document viable (table values image-only). Also [V] 2018 pain: two Rust compression crates had "subtle correctness issues that would have resulted in data loss" → fell back to a proven C library. https://www.figma.com/blog/rust-in-production-at-figma/
- true driver: single-threaded GC'd runtime × arbitrary-size documents; equally a scheduling/architecture fix (isolation per document) that low footprint enabled.
- proves: D10: the winning form was a hybrid at a process seam, not a stack migration; D4 when footprint × instance count is the multiplier.
- skeptic: (baseline-age) 2018 ecosystem caveats are dated; the "Rust rewrite" kept Node in front.

### AWS · Firecracker — QEMU/C role displaced by greenfield Rust VMM (2018→)
- scope: microVM monitor under Lambda/Fargate | archetype: infra-hotpath | drivers: memory-safety-from-c, startup-time, memory-footprint
- facts: [V(s)] spec-defined targets: <125ms to guest userspace, <5MiB overhead per microVM, 150 microVMs/s/host; trillions of Lambda invokes/month. https://github.com/firecracker-microvm/firecracker/blob/main/SPECIFICATION.md
- true driver: the minimal device model + KVM gives the speed; Rust buys the safety case at a hostile multi-tenant trust boundary.
- proves: D6 +2 territory (privileged context) and D5/D4 as spec'd requirements rather than vibes.
- skeptic: a minimal C VMM could boot as fast; greenfield — no migration delta exists.

### AWS · S3 ShardStore — prior C storage node → Rust (2021)
- scope: one storage-node type, >40K LOC | archetype: infra-hotpath | drivers: memory-safety-from-c, concurrency-correctness
- facts: [V(s)] SOSP'21: lightweight formal methods (executable reference models, property tests, Loom, Crux) caught 16 issues pre-production; ~9 months of formal-methods effort; non-experts wrote 18% of model code. https://www.cs.utexas.edu/~bornholt/papers/shardstore-sosp21.pdf
- true driver: a correctness-tooling culture that Rust's type system supports; not a perf story at all.
- proves: D6/concurrency-correctness as first-order motives — and that "correctness" claims came with a verification budget, not just a language.
- skeptic: without the formal-methods investment the rewrite alone would not have caught those 16 issues.

### Microsoft · OpenHCL paravisor + the Russinovich rule — C/C++ displaced (2022–24)
- scope: Azure virtualization layer; company-adjacent policy statement | archetype: infra-hotpath | drivers: memory-safety-from-c
- facts: [V(s)] OpenHCL (Rust paravisor) runs on >1.5M Azure VMs/month. https://techcommunity.microsoft.com/blog/windowsosplatform/openhcl-the-new-open-source-paravisor/4273172 · [V(s)] Russinovich 2022: "halt starting any new projects in C/C++ and use Rust for those scenarios where a non-GC language is required." https://www.theregister.com/2022/09/20/rust_microsoft_c/
- true driver: security at the trust boundary; the rule's own hierarchy is GC language first, Rust only where GC is disqualified.
- proves: D6 framing plus the decision rule this skill inherits: Rust is the C/C++ replacement, not the everything replacement.
- skeptic: personal opinion, not official policy; the same company chose Go for the TypeScript compiler (§4).

### GitHub · code search (Blackbird) — Elasticsearch/Java → purpose-built Rust (2023)
- scope: search engine over ~45M repos / 115TB corpus | archetype: infra-hotpath | drivers: cpu-tight-loop, memory-footprint
- facts: [V(s)] 115TB → 25TB index (content dedupe + delta indexing); ingest ~120K docs/s; ~640 qps; shard p99 ~100ms; "about twice as fast" end-to-end with far better features. https://github.blog/engineering/architecture-optimization/the-technology-behind-githubs-new-code-search/
- true driver: domain-specific index design carries the headline; Rust supplied predictable perf and safe parallelism.
- proves: D9 when no off-the-shelf engine fits the domain; D12 discipline — purpose-built vs general-purpose is not "Rust beats Java".
- skeptic: attribution-error if quoted as a language result.

### InfluxDB · 3.0 / IOx — Go → Rust full core rewrite (2020–23)
- scope: whole database engine, rebuilt on Arrow/DataFusion/Parquet | archetype: data-pipeline | drivers: ecosystem-pull, hype-or-brand (partial)
- facts: [C] (vendor-claim) "100x faster queries on high cardinality, 10x ingest, 10x cheaper storage" — no neutral benchmark; compares a new columnar engine to their own aging TSM engine. https://www.influxdata.com/blog/influxdays-recap-paul-dix-journey-influxdb/
- true driver: the defensible part is ecosystem-pull — the columnar stack they wanted (Arrow/DataFusion) IS Rust; InfluxData became a top DataFusion contributor.
- proves: D9 +2 shape: best-in-class engine for the domain already lives in Rust crates you would otherwise reimplement.
- skeptic: benchmark-theater flag on all three multipliers; a storage-format + query-engine change, not a language result.

### Deno — Go prototype → Rust (2018)
- scope: JS runtime | archetype: cli-longtask | drivers: gc-tail-latency (runtime composition), single-binary
- facts: [V(s)] rewritten for v0.1 chiefly to avoid stacking Go's GC beside V8's GC — "double runtime… garbage collection pressure" (Dahl). https://en.wikipedia.org/wiki/Deno_(software)
- true driver: an embedding constraint — two competing collectors in one process — not Go's general fitness.
- proves: D9/D8 for VM-embedding projects only.
- skeptic: routinely misquoted as "Go was too slow for Deno"; that was never the claim.

### Astral · ruff — flake8/Black/isort/pylint (Python) → Rust (2022–)
- scope: Python linter + formatter | archetype: cli-quick | drivers: cpu-tight-loop, startup-time
- facts: [C] 10–100x claimed; [V(s)] adopters exceed it: Dagster ~1000x vs 4-core-parallel pylint (2.5min → 0.4s); Bokeh co-creator ~150–200x vs flake8; lints CPython in <500ms. https://github.com/astral-sh/ruff
- true driver: Marsh's own decomposition [V(s)]: read + parse every file exactly ONCE for all rules (vs N tools × N parses), native execution, no-GIL file parallelism, caching, no interpreter cold start. https://notes.crmarsh.com/python-tooling-could-be-much-much-faster
- proves: D5 +2 shape (per-save invocation, interpreter boot a measured share) and D7 (GIL wall); D12 note: nobody built the equally-integrated pure-Python control.
- skeptic: honest comparison is "one integrated native tool vs a federation of Python plugins each re-parsing" — architecture does a large share.

### Astral · uv — pip/pip-tools (Python) → Rust (2024)
- scope: package manager | archetype: cli-quick | drivers: startup-time, cpu-tight-loop
- facts: [V] published suite, cold cache **8–10x** (independently reproduced) vs warm cache **80–115x**; venv creation 80x vs `python -m venv`. https://astral.sh/blog/uv
- true driver: the warm multiplier is cache/installer design (global wheel cache, hardlink/CoW ≈ zero copy work); the cold 8–10x is the language + parallelism + no-interpreter share; network-bound installs converge toward parity.
- proves: how to quote regime-split numbers (D2/D12): give warm AND cold; "100x" alone is the regime where the tool does ~no work.
- skeptic: benchmark-theater if only the warm number is quoted.

### VoidZero & friends · JS toolchain — Babel/ESLint/Prettier/Rollup (JS) → Rust (2022–25)
- scope: swc, oxc/oxlint, Biome, rolldown-vite | archetype: compiler-buildtool | drivers: cpu-tight-loop, startup-time, ecosystem-pull
- facts: swc [C] "20x/70x" vs [V] ~2–5x in full pipelines (discord.js measured 2x; Next.js claims "up to 5x"). https://swc.rs/ · oxlint [C] 50–100x; [V(s)] (vendor-curated) Airbnb 126k files in 7s where ESLint timed out; ~62x independent; RAM 92MB vs 1.4GB. https://voidzero.dev/posts/whats-new-dec-2025 · Biome [V] won Prettier's $22.5k bounty (>95% JS/TS test compat, Nov 2023); [C] ~25x. https://prettier.io/blog/2023/11/27/20k-bounty-was-claimed.html · rolldown-vite [V(s)] (self-reported, vendor showcase repo) GitLab 2.5min → 22s (7x; 43x vs webpack), ~100x lower peak memory; Excalidraw 16x. https://voidzero.dev/posts/announcing-rolldown-vite
- true driver: cold-start elimination + parallelism the JS runtime forbade + single-pass/single-engine architecture (rolldown removes double bundling); one-phase microbenchmarks inflate to 20–100x, end-to-end lands 2–7x.
- proves: D5/D7 for per-save dev tools; carries the (vendor-curated) flag — headline numbers are self-selected success stories.
- skeptic: ESLint's value is plugins + type-aware rules — the part oxlint covered last; JS plugins pull Rust tools back toward JS speed.

### Vercel · Turbopack — webpack (JS) → Rust (2022–25)
- scope: bundler/dev server by webpack's author | archetype: compiler-buildtool | drivers: cpu-tight-loop, hype-or-brand
- facts: [C → retracted] "700x vs webpack / 10x vs Vite" at launch; [V] Evan You showed the bench ran Turbopack+SWC vs Vite+**Babel** and rounded 15ms → "0.01s"; with SWC on Vite the gap mostly closed. https://github.com/yyx990803/vite-vs-next-turbo-hmr/discussions/8 · [V(s)] where it landed: default in Next 16 with official "2–5x faster production builds"; independent migrations 2.6–4x.
- true driver: incremental-computation architecture + Rust + parallelism; the 700x was warm-incremental HMR on synthetic 20k-module trees vs cold webpack.
- proves: benchmark-theater in its marketing form — and that the real product still won 2–5x; both facts travel together.
- skeptic: quote the walkback with the launch number, never the launch number alone.

### fish shell 4.0 — C++ → Rust (2023–25)
- scope: whole shell: 57k lines C++ → 75k Rust, ~2 years, 200+ authors | archetype: cli-longtask | drivers: concurrency-correctness, contributor-experience, memory-safety-from-c
- facts: [V] first-party perf admission: "usually slightly better in terms of time taken, memory use has a slightly higher floor but a lower ceiling" — parity, stated plainly; "the killer feature of Rust, from fish-shell's perspective, is Send and Sync"; only 17 people had ≥10 commits to the C++ code in 11 years; the "handwaving, half a year" estimate became ~2 years. https://fishshell.com/blog/rustport/
- true driver: thread-safety for future concurrent execution + contributor funnel + tooling; explicitly not performance.
- proves: honest C++→Rust expectation: perf parity (D1 ≈ 0), value in D6/contributor concerns; also a schedule-realism datum.
- skeptic: a success that would score STAY on a perf-motivated scorecard; cite against "Rust will make it faster".

### Trifecta · sudo-rs — C → Rust (2023–25)
- scope: privilege tool; Ubuntu 25.10 default | archetype: cli-quick (security boundary) | drivers: memory-safety-from-c
- facts: [V] shipped as default with zero performance framing anywhere first-party; "less is more" attack-surface reduction; original sudo maintainer Todd Miller advising. https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/
- true driver: setuid C parsing attacker-influenced input — the exact C4-floor shape.
- proves: D6 +2 with floor F1/C4: security-relevant C on untrusted input justifies migration with no perf argument at all.
- skeptic: proves nothing about performance or about migrating memory-safe code.

### uutils coreutils — GNU C → Rust (Ubuntu 25.10 default, 2025)
- scope: coreutils userland (~500/600 GNU tests passing at announcement) | archetype: cli-quick | drivers: memory-safety-from-c, cross-platform-core
- facts: [V] shipped default WITH regressions: `cksum` up to **17x slower** than GNU on large files (later patched); `base64` slower, then fixed faster; md5sum behavior differences broke Makeself self-extracting installers. https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf
- true driver: Canonical's motive is resilience/safety ahead of the LTS, not speed; 40 years of GNU tuning is a real baseline.
- proves: C→Rust is not automatically faster (D1 caution); behavioral compatibility is the hidden cost of any port (D12).
- skeptic: not a failure — the safety rationale stands; quote the 17x only against "Rust is faster than C" claims.

### Bun · Zig → Rust port — the natural experiment (2026)
- scope: JS runtime; ~535k lines of Zig mechanically ported in ~11 days by ~64 parallel Claude agents (~$165k API cost) | archetype: cli-longtask | drivers: memory-safety-from-c (Zig's manual lifetimes), concurrency-correctness
- facts: [V] first-party: **performance changed only 2–5%** (Bun.serve +4.8%, `next build` +4.5%); binaries ~20% smaller; big leak fixes; 19 regressions (since fixed); motive was a persistent stream of use-after-free/double-free/leak bugs — "Compiler errors are a better feedback loop than a style guide." https://bun.com/blog/bun-in-rust · [C] production-readiness unproven; Zig's creator called it "unreviewed slop". https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743
- true driver: same architecture in a different systems language ≈ same speed — the cleanest published cap on the "language alone" effect; Bun's original speed was JSC-vs-V8 + syscall work per its own author.
- proves: the ceiling for D1 claims when the source is already native: expect single-digit %.
- skeptic: tests-pass ≠ production-ready; port quality contested.

### Zed · GPUI — greenfield Rust editor vs Electron incumbents (2024)
- scope: code editor + a custom GPU UI framework they had to build | archetype: native-desktop-gui | drivers: cpu-tight-loop, startup-time, memory-footprint
- facts: [C] 120fps UI, <10ms typing; [V(s)] third-party unaudited: ~58ms end-to-end vs VS Code ~97ms; insertion ~2ms vs ~12ms. https://zed.dev/blog/videogame
- true driver: game-engine-style GPU scene graph — no existing Rust GUI framework hit the bar, so they wrote GPUI; Sublime (C++) shows native editors predate Rust.
- proves: D9 −2 for Rust desktop GUI (the flagship app built its own framework — that cost is part of the price); the perf is architecture-first.
- skeptic: not a migration; numbers unaudited; GPUI is reusable but Zed-shaped.

### OpenAI · Codex CLI — TypeScript/Node → Rust (2025)
- scope: agent CLI (~95.7% Rust after the rewrite) | archetype: cli-longtask | drivers: single-binary, startup-time, memory-footprint
- facts: [V(s)] stated reasons: zero-dependency install (drop the Node ≥22 requirement), native OS sandboxing (landlock/seccomp/seatbelt), lower startup/memory without GC, language-agnostic wire protocol. https://www.infoq.com/news/2025/06/codex-cli-rust-native-rewrite
- true driver: distribution + sandbox primitives, not throughput; TS was the deliberate velocity choice for v1.
- proves: D8 +2 shape — requirements the runtime can't meet (no-runtime install, OS sandboxing).
- skeptic: Anthropic's competing Claude Code stayed TypeScript and ships as a Bun-compiled binary (https://bun.com/docs/bundler/executables) — the rewrite is not table stakes for the category (D8 stay-stack answers exist).

### Dropbox · Nucleus — Python → Rust (2020)
- scope: desktop sync engine; ~4-year rewrite, shipped Mar 2020 | archetype: cli-longtask (desktop daemon) | drivers: concurrency-correctness, cross-platform-core
- facts: [V] motives were data-model flaws, untestability, thread nondeterminism — "More than performance, its ergonomics and focus on correctness has helped us tame sync's complexity"; explicit redesign: new three-tree model, one deterministic control thread, simulation testing "millions of scenarios every day"; NO performance numbers published. https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine
- true driver: a redesign whose invariants got encoded in the type system; most gains trace to the new data model.
- proves: correctness-motivated MIGRATE exists (type-system value, D7-adjacent) — but it arrived with a full redesign budget and 4 years.
- skeptic: the counterfactual (same three-tree redesign in Python) was never priced; zero quantified perf evidence.

### Grab · Counter service — Go → Rust (2024)
- scope: one high-QPS counting service | archetype: infra-hotpath | drivers: cost-efficiency, memory-footprint
- facts: [V] ~70% infra savings (elsewhere "80%" — internal inconsistency flagged); at 1,000 QPS: 20 Go cores → 4.5 Rust cores (~4.4x); **"the P99 latency is similar (or perhaps even slightly worse) in the Rust service"**; first-party: "rewriting a Golang service in Rust solely for performance improvements is unlikely to yield significant benefits" — expect "~50% compute savings" as the honest rule; async Rust footgun admitted (shipped a sync Redis call by mistake). https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust
- true driver: steady-state Rust-vs-Go delta is cores/footprint, not latency; pays only at high traffic.
- proves: D4 scoring: cost-efficiency is the honest Go→Rust win (~2–5x cores at fleet scale); D3 stays ≈0 without a GC-spike pathology.
- skeptic: the best-documented refutation of "Rust will cut our p99" for Go services.

## 2 · Extractions & hybrids (the seam did the work)

### Mozilla · Stylo — C++ CSS engine → Rust component extracted from Servo (2015–17)
- scope: the CSS style system only, landed in Firefox 57 "Quantum" (Nov 14, 2017) | archetype: lib-with-bindings | drivers: cpu-tight-loop (parallel styling), memory-safety-from-c
- facts: [V] started by 2 engineers late 2015, first pixels April 2016; shipped in ~2 years; Holley: "Almost everything successful is incremental in one way or another… the desire to throw everything away and start from scratch tends to be an emotional one." https://bholley.net/blog/2017/stylo.html
- true driver: extraction at a seam where Rust had a real edge — parallel styling that prior C++ attempts had failed to land safely.
- proves: D10 is the success predictor: same org, same codebase — the extraction shipped, the whole-engine replacement (Servo, §4) died.
- skeptic: rode Servo's R&D as a donor project; not a cheap standalone path.

### Google · Android memory-safety program — new code in Rust/Kotlin, old C/C++ left in place (2019–25)
- scope: OS components; explicitly NOT a mass rewrite ("safety by attrition") | archetype: infra-hotpath (OS native layer) | drivers: memory-safety-from-c
- facts: [V] memory-safety share of Android vulns: 76% (2019) → 24% (2024) → **below 20%** (2025, first time); Rust ~0.2 vuln/MLOC vs ~1,000/MLOC C/C++ (**">1000x reduction"**); Rust changes: rollback rate ~4x lower than C++, ~25% less review time, ~20% fewer revisions; ~4% of Rust lines are `unsafe`. https://blog.google/security/rust-in-android-move-fast-fix-things/ · [V] decay finding: 5-year-old code has 3.4–7.4x lower vuln density than new code — their stated conclusion: write NEW code safe, interop over rewrite, let old code decay. https://www.theregister.com/2024/09/25/google_rust_safe_code_android/
- true driver: stop the tap of new unsafe code; vulnerabilities decay exponentially with code age.
- proves: the strongest safety numbers in existence are ANTI-mass-rewrite in method (D6 evidence, C6 hybrid-first doctrine).
- skeptic: a security outcome, not a perf story; C/C++-relative only — zero bearing on migrating memory-safe code (cap C3).

### pydantic · pydantic-core — Python → Rust core, Python API kept (2022–23)
- scope: validation inner loop via PyO3 | archetype: lib-with-bindings | drivers: cpu-tight-loop
- facts: [C] 4–50x vs v1, ~17x on a representative model; [V(s)] end-to-end FastAPI apps 2–3x (user-reported). https://pydantic.dev/articles/pydantic-v2
- true driver: hot kernel behind an unchanged API — the template for non-disruptive extraction.
- proves: D2 in numbers: 17x kernel → 2–3x app; quote both or neither.
- skeptic: amdahl-blindness if the 17x is pitched as the app-level gain.

### Hugging Face · tokenizers + OpenAI · tiktoken — Rust cores under Python APIs (2019–22)
- scope: tokenization libraries fronted by Python/Node bindings | archetype: lib-with-bindings | drivers: cpu-tight-loop, ecosystem-pull
- facts: [C] (vendor-claim) HF README: "less than 20 seconds to tokenize a GB of text"; no independent audit found. https://github.com/huggingface/tokenizers · [C] tiktoken README: "3–6x faster" than comparable tokenizers. https://github.com/openai/tiktoken
- true driver: hot loop in native code under a scripting API — achievable in C++/Cython too; the pattern, not the language brand, is the point.
- proves: D10 +2 shape: batch-in/batch-out kernels, data crossing rarely and in bulk.
- skeptic: both figures are vendor READMEs.

### Polars — pandas displaced by a Rust engine with Python bindings (2020–)
- scope: DataFrame engine used FROM Python | archetype: data-pipeline / lib-with-bindings | drivers: cpu-tight-loop, memory-footprint, ecosystem-pull
- facts: [V] third-party benches (JetBrains, codecentric): group-by 5–10x, CSV read ~5x with ~87% less memory; gap grows with data size. https://blog.jetbrains.com/pycharm/2024/07/polars-vs-pandas/
- true driver: columnar Arrow layout + multicore-by-default + lazy query optimizer; DuckDB (C++) achieves the same class of wins — the design differentiates, not the language.
- proves: D9's inversion: the ecosystem-pull answer can be "use the Rust-powered library from your current language" — a strong D12 counterfactual AGAINST rewriting.
- skeptic: pandas is comparable or faster on small data; `apply`-style code gains little.

### Amazon · Prime Video living-room UI — JS low-level systems → Rust+WASM, JS kept on top (2022–24)
- scope: client SDK across 8,000+ device types; business logic stayed React/JS | archetype: web-frontend | drivers: cross-platform-core, memory-footprint, cpu-tight-loop
- facts: [V(s)] 37K LOC Rust after ~1 year; WASM VM adds ≤7.5MB while saving 30MB of JS heap; steady-60fps goal; egui debug overlay integrated in hours. https://www.amazon.science/blog/how-prime-video-updates-its-app-for-more-than-8-000-device-types
- true driver: split-stack — native-speed rendering/animation core under a scripting UI; as much a WASM story as a Rust story.
- proves: D10 hybrid on RAM-constrained devices; the JS layer survives because the seam is coarse.
- skeptic: a TV-client SDK, not a template for general web apps.

### gitoxide — Rust git as a library, not a replacement (2020–)
- scope: Rust git implementation; Cargo uses gix for fetching; the CLI is "explicitly not to be understood as git replacement" | archetype: lib-with-bindings | drivers: memory-safety-from-c, ecosystem-pull
- facts: [V] first-party status: `gix blame` "typically still up to 30% slower" than git with commitgraph caches on; some parallel-friendly ops beat git. https://github.com/GitoxideLabs/gitoxide/discussions/1791
- true driver: library-first succeeds where op-for-op replacement of hyper-optimized C is a decade-scale project.
- proves: honest pacing for "rewrite git-shaped C" proposals (D1/D12 caution): 6 years in, parity is still open.
- skeptic: "Rust rewrite of git" remains aspirational by its own author's framing.

## 3 · Stayed and won (same goal, no migration)

### Microsoft · VS Code — stayed TypeScript/Electron; native only at seams (2016–)
- scope: editor; C++ text buffer attempt reverted; ripgrep adopted as search subprocess | archetype: electron-desktop | drivers: (control case for) cpu-tight-loop claims
- facts: [V(s)] 2018 native-buffer verdict: **"TL;DR: We tried. It didn't work out for us"** — converting strings between native representation and V8 "compromised any performance gained"; the fix was a better data structure in TypeScript (piece tree). https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation · [V(s)] ripgrep (Rust) powers text search since v1.11 (Mar 2017) — a subprocess at a clean seam. https://users.rust-lang.org/t/ripgrep-is-now-the-standard-text-search-provider-in-vs-code/10285 · [V(s)] perceived speed = extension-host process isolation + lazy activation + virtualized lists + V8 snapshots; 73.6% professional-editor share (SO survey 2024). https://survey.stackoverflow.co/2024/
- true driver: boundary tax beat in-language gains once (buffer); Rust won once as a whole process exchanging bulk results (search); architecture carried the product.
- proves: D10 in both directions inside one product: chatty per-op boundary = −2, process-seam bulk boundary = +2; cap C2's poster child.
- skeptic: does not prove native never helps — it proves the boundary decides.

### Notion · performance journey — caching architecture, language kept (2021; 2024)
- scope: Electron desktop + browser app | archetype: electron-desktop | drivers: (control case) — the fix was I/O placement
- facts: [V(s)] native SQLite caching → desktop page loads/navigation **50% faster** (2021); WASM SQLite (OPFS) in the browser → navigation **+20%** across all modern browsers, 28–33% in AU/CN/IN (2024); they race disk cache vs network because old Android devices read disk slower than network. https://www.notion.com/blog/how-we-sped-up-notion-in-the-browser-with-wasm-sqlite
- true driver: user-perceived speed was an I/O-and-caching problem; the fix was a database placement decision.
- proves: D1 −2 pattern: time lived in network/disk — invisible to any rewrite (cap C2).
- skeptic: says nothing about CPU-bound cores; it says most apps don't have one.

### Linear · sync engine — local-first design in TypeScript (2019–)
- scope: SaaS project tool | archetype: web-frontend | drivers: (control case)
- facts: [V(s)] all reads/writes hit a local object graph (MobX + IndexedDB) synced via websocket deltas off the Postgres replication log; most page loads <50ms; offline works. https://linear.app/now/scaling-the-linear-sync-engine
- true driver: eliminated network round-trips architecturally; the language never changed.
- proves: "feels native" is a D1/D12 architecture outcome; no language swap touches round-trips.
- skeptic: sync engines are hard — the cost went into design, not into a rewrite.

### Figma · fast-in-browser core — C++ → WASM, not Rust (2017)
- scope: editor core compiled to WASM; JS/TS UI around it | archetype: web-frontend | drivers: cpu-tight-loop (via C++)
- facts: [V(s)] "WebAssembly cut Figma's load time by 3x" (vs prior asm.js), regardless of document size; 2018 follow-up: large doc 29s → <8s. https://www.figma.com/blog/webassembly-cut-figmas-load-time-by-3x/
- true driver: compiled code where the profile demands it + scripting UI; the celebrated frontend case involves no Rust — the language brand is incidental.
- proves: attribution hygiene: "Rust-class" wins are really "compiled-kernel" wins; D10 hybrid again.
- skeptic: C++ WASM carries memory-unsafety into the sandbox; Rust would add safety there, not speed.

### Google · Sheets calc engine — JS → Java compiled to WasmGC (2023–24)
- scope: browser calculation engine | archetype: web-frontend | drivers: cpu-tight-loop
- facts: [V(s)] ~**2x** vs the prior JS engine via a WasmGC port of the Java code; WasmGC baseline in all engines since Safari 18.2 (Dec 2024). https://v8.dev/blog/wasm-gc-porting
- true driver: shared code + near-native execution WITH a GC — no borrow checker involved.
- proves: the stay-managed WASM path exists for GC-shaped codebases (D12/D8 alternative to Rust-wasm).
- skeptic: 2x, not 20x — browser compute gaps are modest when the JS was already JIT-hot.

### Shopify · YJIT — made Ruby faster instead of leaving Ruby (2021–23)
- scope: JIT built into CRuby, deployed fleet-wide | archetype: backend-crud | drivers: (control case for) gc-phobia, benchmark-theater
- facts: [V(s)] production (A/B vs JIT-off): 5–10% end-to-end on Ruby 3.2, **+15%** on 3.3; official benchmark suite: **61.2–67.4%** faster — i.e. bench numbers run 4–10x hotter than fleet numbers on the same product; adopted by Discourse fleet-wide. https://railsatscale.com/2023-09-18-ruby-3-3-s-yjit-runs-shopify-s-production-code-15-faster/ · https://speed.ruby-lang.org/
- true driver: runtime investment; the bench-vs-fleet gap is the quantified benchmark-theater coefficient.
- proves: D12: runtime upgrades give double-digit fleet wins with zero freeze risk; and the ÷4–10 discount to apply to any vendor bench.
- skeptic: 15% ≠ 10x — if the requirement is 10x, neither YJIT nor a language swap helps when D1 is IO-bound.

### Twitch · Go memory ballast → GOMEMLIMIT — GC tuned, no rewrite (2019 → 2022)
- scope: their busiest Go API service | archetype: backend-crud | drivers: (control case) gc-phobia
- facts: [V(s)] ~1GB never-touched ballast slice made the GC pacer run far less often; peak tail latency improved; pauses were already single-digit ms. https://blog.twitch.tv/en/2019/04/10/go-memory-ballast-how-i-learnt-to-stop-worrying-and-love-the-heap/ · [V(s)] Go 1.19 `GOMEMLIMIT` (2022) made the ballast hack obsolete; GC CPU capped ~50%. https://tip.golang.org/doc/go1.19
- true driver: a GC pacing knob — ten lines, then a runtime flag.
- proves: D3 discipline: "GC visible in traces" with untried knobs scores 0, not +2.
- skeptic: ballast fixed GC CPU churn — not a Discord-style resident-cache scan pathology; the two shapes differ.

### Netflix · Generational ZGC — JVM collector swap on JDK 21 (2024)
- scope: >half of critical streaming services | archetype: backend-crud | drivers: (control case) gc-phobia
- facts: [V(s)] default G1 → generational ZGC: consistently **sub-millisecond pauses** independent of heap size; removed GC as a source of gRPC tail-latency/timeout/retry storms — no language change. https://netflixtechblog.com/bending-pause-times-to-your-will-with-generational-zgc-256629c9386b
- true driver: runtime version + collector choice.
- proves: D3: "GC pause" in 2024+ is a configuration/runtime-version problem before it is a language problem.
- skeptic: memory-density economics survive sub-ms pauses (Hertz-Berger 3–5x heap, §6) — GC cost moved to RAM, it didn't vanish.

### GitHub · stayed Ruby on Rails (2023)
- scope: ~2M LOC monolith, 1000+ engineers, up to 20 deploys/day | archetype: backend-crud | drivers: (control case) rewrite-freeze-risk avoided
- facts: [V(s)] upgrades Rails weekly via automated PRs tracking Rails main; dual CI against Ruby HEAD; on Ruby 3.2 within a month of release — explicitly instead of replatforming. https://github.blog/engineering/architecture-optimization/building-github-with-ruby-and-rails/
- true driver: continuous upgrade beats starting over for a CRUD-shaped product.
- proves: D12/D11: a "legacy" monolith can ship 20x/day — the migration's opportunity cost is the argument.
- skeptic: the same org built Blackbird in Rust (§1) — stay-the-monolith and build-the-engine-in-Rust coexist.

### Stack Overflow · tiny .NET footprint (2016)
- scope: one of the top sites on Earth on 9 primary web servers | archetype: backend-crud | drivers: (control case) gc-phobia
- facts: [V(s)] (baseline-age 2016) 209,420,973 HTTP req/day on 9 web servers, C#/.NET + SQL Server; later moved to .NET Core in place. https://nickcraver.com/blog/2016/02/17/stack-overflow-the-architecture-2016-edition/
- true driver: perf culture + SQL/caching discipline; the GC language ceiling was never the constraint.
- proves: D1 for CRUD: the language is rarely the binding constraint at even extreme read scale.
- skeptic: dated snapshot, but the shape (IO-bound CRUD on a GC runtime) recurs everywhere.

### Prettier · pure-JavaScript CLI, 3x — same language, post-bounty (2023)
- scope: formatter CLI rework by a hired engineer, zero Rust | archetype: compiler-buildtool | drivers: (control case) attribution
- facts: [V] ~3x (e18e reproduced 29s → 9s) via profiling, caching and IPC fixes — announced days after Biome claimed the Rust bounty. https://prettier.io/blog/2023/11/30/cli-deep-dive · https://e18e.dev/blog/prettier-speed-up.html
- true driver: the baseline was unoptimized JS, not JS.
- proves: D12 −2 evidence: a chunk of any "Rust gap" is optimization never attempted in the current language.
- skeptic: 3x still ≪ Biome's claimed ~25x — both facts belong in the same sentence.

## 4 · Reversals, refusals, failures

### Prisma · deleted its Rust query engine — Rust → TypeScript (2025)
- scope: ORM core moved to TS; a small WASM query-plan compiler retained | archetype: lib-with-bindings | drivers: (reversal) boundary-tax
- facts: [V] their own numbers AFTER removing Rust: findMany 25k rows 185ms → 55ms (**3.4x faster**); complex joins 207 → 130ms; bundle ~14MB → 1.6MB (~90% smaller); reasons verbatim: "data must be serialized from JavaScript to Rust and then back to JavaScript"; per-OS/OpenSSL binaries; Rust+TS dual-skill shrank the contributor pool; edge runtimes can't carry the binary. GA v6.16.0 (Sept 2025), default in Prisma 7. https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm
- true driver: per-call serialization across a chatty JS↔Rust boundary swamped the native gains — the boundary, not the language, was the bottleneck.
- proves: D10 −2 in production: when callers live in another runtime and cross per-operation, DELETING Rust is the performance optimization.
- skeptic: does not indict coarse-boundary Rust kernels (pydantic, tokenizers); it prices the chatty ones.

### curl · dropped the hyper backend — C → Rust HTTP internals, abandoned at ~95% (2020 → Dec 2024)
- scope: one backend of curl; 4 years, ISRG-funded, nearly full test-suite parity | archetype: security-parser | drivers: memory-safety-from-c (failed on people, not tech)
- facts: [V] Stenberg: "There simply were no users asking for it and there were almost no developers interested or knowledgeable enough to work on it"; the C↔Rust glue needed rare dual expertise ("the overlap in the Venn diagram of the two universes is not big enough"); removed in curl 8.12.0 (Feb 2025). Date correction: the drop post is **Dec 21, 2024**, often misdated 2023. Meanwhile rustls (TLS) and quiche (QUIC/HTTP3) backends SURVIVED — "hooked in more cleanly and easier to maintain." https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/
- true driver: no user pull + unstaffable maintainer pool; library seams outlive deep integrations.
- proves: D11 kills technically-sound safety migrations at 95% complete; the surviving rustls/quiche seams are the D10 lesson inside the failure.
- skeptic: not evidence Rust can't do HTTP — evidence that migrations without contributors and demand die regardless of merit.

### Microsoft · TypeScript compiler → Go, Rust rejected (tsgo/Corsa, 2025)
- scope: tsc + language service, ported 1:1 for behavioral compatibility | archetype: compiler-buildtool | drivers: cpu-tight-loop (achieved), refusal of Rust
- facts: [V(s)] Microsoft's table: VS Code repo compile 77.8s → 7.5s (10.4x); editor project load 9.6s → 1.2s (8x); ~half the memory. https://devblogs.microsoft.com/typescript/typescript-native-port/ · Hejlsberg verbatim: "All of our data structures are heavily cyclic"; Go is "the lowest-level language we can get to" with native code + GC + cyclic structures; unraveling cycles for the borrow checker would make the job "insurmountably larger"; a **port, not a rewrite**, was mandatory. Cavanaugh: Rust = years + incompatible; Go = ~1 year + "extremely compatible semantics." https://thenewstack.io/microsoft-typescript-devs-explain-why-they-chose-go-over-rust-c/
- true driver: Hejlsberg's own split: ~3–3.5x native code + value types, the rest shared-memory parallelism — obtained WITH a GC; GC was a feature for cyclic ASTs.
- proves: gc-phobia debunk at maximum profile; D12 branch every scorecard must include: "what would a GC'd native language achieve?"
- skeptic: compilers are the best case for native ports; says little about IO-bound services.

### esbuild · chose Go over Rust (2020–)
- scope: bundler written from scratch by evanw | archetype: compiler-buildtool | drivers: startup-time, refusal of Rust
- facts: [V] repo-reproducible (`make bench-three`): esbuild 0.39s vs webpack5 41.21s (~106x); the FAQ's four factors, each "only a somewhat significant speedup," combined "multiple orders of magnitude": (1) native AOT — CLIs are "a worst-case performance situation for a JIT-compiled language"; (2) shared-memory parallelism (JS workers must serialize); (3) everything from scratch with consistent data structures; (4) memory efficiency — exactly three AST passes. https://esbuild.github.io/faq/
- true driver: every advertised Rust-rewrite advantage, achieved in a GC'd language.
- proves: the four-factor decomposition IS the scoring rubric for D1/D5/D7 on build tools.
- skeptic: single-author greenfield; the 106x is vs JS webpack, not vs another native tool.

### Mozilla · Servo as Gecko replacement — never shipped (2012–2020)
- scope: whole-browser-engine replacement moonshot | archetype: native-desktop-gui | drivers: memory-safety-from-c, hype-or-brand
- facts: [V] Holley: a full Gecko replacement "would probably require thousands of engineer-years" while Mozilla "could only afford a handful of heads"; Aug 2020: ~250 laid off including the whole Servo team; project moved to Linux Foundation; components (Stylo §2, WebRender) shipped instead. https://bholley.net/blog/2017/stylo.html · https://en.wikipedia.org/wiki/Servo_(software)
- true driver: scope economics, not language quality — the ocean-boil got cancelled, the extraction became the flagship.
- proves: rewrite-freeze-risk at maximum scale; with Stylo it forms the canonical D10 pair cited in `dimensions.md`.
- skeptic: Servo seeded the shipped components — the R&D wasn't wasted, the replacement goal was.

### Alacritty · "fastest terminal emulator in existence" vs the measurements (2017–)
- scope: claim audit of a greenfield Rust + OpenGL terminal | archetype: native-desktop-gui | drivers: hype-or-brand
- facts: [C] the README superlative; [V(s)] Dan Luu measured its latency mid-pack and called throughput dumps "as useless a benchmark as I can think of". https://danluu.com/term-latency/ · [V(s)] LWN: ancient xterm/mlterm beat every modern terminal on worst-case latency; a 2022 macOS light-sensor test put kitty (C/Python) lowest at 29.2ms. https://lwn.net/Articles/751763/
- true driver: "fastest" without a metric definition is branding; GPU throughput ≠ input latency.
- proves: the benchmark-theater tell in its purest form: superlative + no metric + no harness.
- skeptic: Alacritty is a fine terminal; only the claim fails audit.

### LogLog Games · leaving Rust gamedev after 3 years (2024)
- scope: 3+ years, >100k LOC (own engine, Bevy, Macroquad) abandoned for shipping games | archetype: game | drivers: (reversal) hype-or-brand
- facts: [V(s)] core claims: Rust fights rapid "is this fun?" iteration; problems "don't go away unless you're willing to constantly refactor and treat programming as puzzle-solving"; ecosystem rebuilds everything instead of reusing mature C/C++ stacks. Aras Pranckevičius: half the post is really about "hype cycles, tech zealotry, the search for silver bullets." https://loglog.games/blog/leaving-rust-gamedev/
- true driver: iteration-speed-dominated domain — borrow-checker rigor is a tax on the core loop, not a benefit.
- proves: D11/velocity realism for prototype-shaped work; the game archetype's D9 drag.
- skeptic: (N=1) indie account; engine-scale C++ teams weigh differently.

### Fixie (Matt Welsh) · Rust at a startup — first-party cautionary tale (2022)
- scope: velocity report from a CEO/ex-Google systems researcher | archetype: backend-crud | drivers: (cost datum) rewrite-freeze-risk, resume-driven
- facts: [V(s)] "Rust is awesome, for certain things. But think twice before picking it up for a startup that needs to move fast"; hiring hard; Rust "makes roughing out new features very hard." https://mdwdotla.medium.com/using-rust-at-a-startup-a-cautionary-tale-42ab823d9454
- true driver: learning curve + prototyping drag ahead of product-market fit.
- proves: D11 −2 realism; pairs with Rust's own survey numbers (§6).
- skeptic: one account; Google's ramp data (1/3 productive at 2 months, §6) is the counterweight.

### Tauri on Linux · the WebKitGTK reality (2023–26)
- scope: Rust-shell desktop apps on system webviews | archetype: electron-desktop | drivers: memory-footprint (marketed); (failure mode) benchmark-theater
- facts: [V(s)] official "Linux Graphics Issues" page (blank windows, NVIDIA DMABUF workarounds); maintainer: "we can't fully recommend Tauri for Linux right now," WebKitGTK "getting worse each release"; one app measured 40fps on WebKitGTK vs 240fps after converting to Electron. https://github.com/tauri-apps/tauri/discussions/8524 · https://github.com/tauri-apps/tauri/issues/14963
- true driver: bundle-size marketing hides a rendering engine you don't control; on Windows, WebView2 IS Chromium and RAM ≈ Electron (§6 row).
- proves: D8/D9 for Electron-replacement proposals: the webview is the product surface; "smaller installer" is not "better UX".
- skeptic: fine where WebKitGTK is acceptable or Linux is out of scope; macOS numbers (Hopp, §6) are real but (N=1).

## 5 · The eight traps (misconception audit checklist)

Run every proposal against all eight; report hits AND passes. Tags map 1:1 to the debunk taxonomy (T8 folds two process tags).

- **T1 · amdahl-blindness** — admiring a kernel multiplier without computing its share of end-to-end time. Canon: pydantic-core 17x kernel → 2–3x app (§2); Notion/Linear — time was in IO/round-trips (§3). The tell: the proposal quotes a component benchmark but no profile showing that component's share of user-felt latency.
- **T2 · attribution-error** — crediting the language for a redesign's win. Canon: Pingora's own "not because we run code faster… new architecture" (§1); Discord 2023 DB swap (§1); Blackbird index design (§1); Meta Buck2's "2x" from re-architecture [V(s)] https://engineering.fb.com/2022/07/27/developer-tools/programming-languages-endorsed-for-server-side-use-at-meta/ ; InfluxDB's columnar engine (§1). The tell: the before/after also changed architecture, data model, or database — and no same-language redesign was priced (D12).
- **T3 · benchmark-theater** — the number is real only in a regime users never see. Canon: Turbopack "700x" retracted (§1); uv 80–115x warm vs 8–10x cold (§1); YJIT 61–67% bench vs 5–15% fleet (§3); Discord's Go 1.9.2 baseline (§1); Alacritty (§4); Lightning CSS's ">100x" partly from "unsafe" transforms vs the slowest JS baseline [V] https://github.com/vercel/next.js/issues/38465 . The tell: superlative multiplier + no harness + baseline runtime version unstated or years old.
- **T4 · gc-phobia** — treating GC as disqualifying without a measured pause problem. Canon: Twitch ballast → GOMEMLIMIT (§3); Netflix generational ZGC <1ms (§3); Go <100µs STW since 1.8 (§6); tsgo took a GC language to 10x (§4); Stack Overflow (§3). The tell: "GC pauses" cited with no trace showing GC in the tail and no tuning attempted — D3 then scores ≤0, never +2.
- **T5 · safety-conflation** — claiming Rust's memory-safety dividend when the source is already memory-safe. Canon: matklad's "Not all programming is systems programming" [V] https://matklad.github.io/2020/09/20/why-not-rust.html ; ONCD/CISA count JS/TS/Go/Java/Python as memory-safe (§6); every 70%/Android number is C/C++-relative (§6); Bergstrom's 2x is vs C++ only — parity vs Go (§6). The tell: an RFC for a TS/Go/Python codebase quoting CVE statistics from C/C++ corpora (triggers cap C3).
- **T6 · boundary-tax** — putting the hot kernel behind a chatty FFI/serialization boundary and losing the win. Canon: Prisma 3.4x faster after deleting Rust (§4); VS Code C++ buffer "We tried. It didn't work out" (§3); ast-grep ~6% best-case vs serialization-dominated tree passing, N-API "never designed to be fast" (§6). The tell: per-item calls, JSON across the boundary, no boundary-cost term in the plan (the D10 math is absent).
- **T7 · hybrid-blindness** — framing the choice as rewrite-or-nothing when a seam extraction or an existing Rust-powered library meets the goal. Canon: Stylo vs whole-Servo (§2/§4); ripgrep inside VS Code (§3); rustls/quiche surviving where hyper died (§4); Polars-from-Python (§2); Figma's Rust child process behind Node (§1). The tell: the proposal has no EXTRACT rung between STAY and MIGRATE (violates smallest-sufficient-step / C6).
- **T8 · process traps** (rewrite-freeze-risk + resume-driven) — the rewrite freezes shipping while the old system rots, and/or the motive is brand/CV energy. Canon: Netscape ~3 years frozen, "single worst strategic mistake" [V] https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/ ; Servo cancelled (§4); rewrites run 1.5–2x over cost AND schedule (§6); Brooks' second-system effect https://en.wikipedia.org/wiki/Second-system_effect ; fish's "half a year" → 2 years (§1); the RIIR meme literature ("at best… unnecessary duplication of effort, at worst… buggy software") [V(s)] https://adventures.michaelfbryan.com/posts/how-not-to-riir/ ; Welsh (§4). The tell: no dual-run plan, no freeze budget, advocates who won't own the pager, excitement exceeding measurements.

## 6 · Numbers you can quote

| Fact | Number | Year | Ver | URL |
|---|---|---|---|---|
| Microsoft CVEs rooted in memory safety (C/C++) | ~70% of patched CVEs, stable ~12 yrs | 2019 | [V(s)] | https://msrc.microsoft.com/blog/2019/07/we-need-a-safer-systems-programming-language/ |
| Chromium high/critical bugs = memory unsafety | ~70% of 912 since 2015; half use-after-free | 2020 | [V] | https://www.chromium.org/Home/chromium-security/memory-safety/ |
| Android memory-safety vuln share | 76% (2019) → 24% (2024) → <20% (2025) | 2024–25 | [V] | https://blog.google/security/rust-in-android-move-fast-fix-things/ |
| Rust vs C/C++ vuln density on Android | ~0.2 vs ~1,000 vulns/MLOC — ">1000x" | 2025 | [V] | https://blog.google/security/rust-in-android-move-fast-fix-things/ |
| Vulnerability decay (anti-rewrite datum) | 5-yr-old code: 3.4–7.4x lower vuln density than new code | 2024 | [V] | https://www.theregister.com/2024/09/25/google_rust_safe_code_android/ |
| ONCD/CISA memory-safe language lists | JS/TS, Python, Java, C#, Go, Swift, Rust all count as memory-safe | 2022–24 | [V(s)] | https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf |
| Russinovich decision rule | GC language first; Rust "where a non-GC language is required"; halt new C/C++ | 2022 | [V(s)] | https://www.theregister.com/2022/09/20/rust_microsoft_c/ |
| App-level managed-runtime gap (LangBench) | Node/V8 apps avg 8.01x slower than C++; Java 1.43x; Go 1.30x | 2022 | [V(s)] | https://www.usenix.org/conference/atc22/presentation/lion |
| Hot monomorphic scalar JS loops vs native | ~1–2x (V8 prime bench 1.5x; best FP ≈ parity) | 2021 | [V(s)] | https://mmomtchev.medium.com/in-2021-is-there-still-a-huge-performance-difference-between-javascript-and-c-for-cpu-bound-8ff798d999d6 |
| WASM vs native ("Not So Fast", SPEC) | mean 1.55x slower (Chrome), 1.45x (Firefox) | 2019 | [V(s)] | https://www.usenix.org/conference/atc19/presentation/jangda |
| WasmGC in production (Google Sheets calc) | Java-on-WasmGC ≈ 2x vs prior JS engine | 2023–24 | [V(s)] | https://v8.dev/blog/wasm-gc-porting |
| Raw FFI floor | ~2–6 ns/call (bun:ffi vs ~4 ns C baseline); N-API deliberately slower | 2024 | [V(s)] | https://bun.com/blog/compile-and-run-c-in-js |
| Real-world napi boundary tax | ast-grep: ~6% FFI overhead sync parse; serialization dominates passing trees | 2023 | [V(s)] | https://medium.com/@hchan_nvim/benchmark-typescript-parsers-demystify-rust-tooling-performance-025ebfd391a3 |
| PyO3 per-call overhead | ~20–40 ns vs raw C-API; fix = batching + zero-copy | 2024 | [V(s)] | https://github.com/PyO3/pyo3/issues/3827 |
| Go GC pauses | typically <100 µs STW since 1.8 (often ~10 µs); GOMEMLIMIT since 1.19 | 2017/2022 | [V(s)] | https://tip.golang.org/doc/go1.19 |
| JVM Generational ZGC (JEP 439) | <1 ms pauses up to 16 TB heaps; Cassandra bench 4x throughput at 1/4 heap | 2023 | [V(s)] | https://openjdk.org/jeps/439 |
| GC space overhead (classic) | GC needs ~3–5x the memory of explicit management to match perf | 2005 | [V(s)] | https://people.cs.umass.edu/~emery/pubs/gcvsmalloc.pdf |
| Rust compile-time pain (own surveys) | 17% "serious problem" + 34% "could be significantly better"; ~45% of quitters cite compile times; 53% feel productive | 2024–25 | [V] | https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/ |
| Admired vs desired vs used | SO 2025: 72.4% admired, only 29.2% desired (2024: 83% admired, 12.6% used) | 2024–25 | [V(s)] | https://survey.stackoverflow.co/2025/technology/ |
| Rust job market | ~1% (TIOBE 0.94% #19; UK ads 0.30%) vs JS/TS ~30%, Python ~20% | 2025 | [V(s)] | https://www.devjobsscanner.com/blog/top-8-most-demanded-programming-languages/ |
| Google productivity (Bergstrom) | Rust ≈ Go productivity; >2x vs C++; ramp: 1/3 productive @2 mo, ~1/2 @4 mo | 2024 | [C] | https://www.theregister.com/2024/03/31/rust_google_c |
| Rewrite economics | 50+ rewrites: typically 1.5–2x over cost AND schedule; IT overruns power-law (mean 28–67%, max >500%) | 2022/2019 | [V(s)] | https://crosslaketech.com/how-long-does-a-complete-rewrite-of-a-software-application-take/ |
| Tauri vs Electron, measured | bundle 8.6 MiB vs 244 MiB; RAM ~172 vs ~409 MB after 6 windows (macOS, N=1, author uses Tauri); build 81s vs 16s | 2025 | [V] | https://www.gethopp.app/blog/tauri-vs-electron |
| Tauri RAM caveat on Windows | WebView2 IS Chromium — memory ≈ Electron once shared pages counted | 2023 | [V(s)] | https://github.com/tauri-apps/tauri/issues/5889 |
| Rust-native GUI maturity | 43 crates surveyed; overwhelming majority not production-ready (a11y, IME); viable-with-caveats: Dioxus/Slint/egui/iced | 2025 | [V(s)] | https://www.boringcactus.com/2025/04/13/2025-survey-of-rust-gui-libraries.html |
| Language-alone ceiling (natural experiment) | Bun Zig→Rust port: perf changed 2–5% | 2026 | [V] | https://bun.com/blog/bun-in-rust |
| Go→Rust steady-state cost win | Grab: 20 → 4.5 cores at 1K QPS; p99 "similar or perhaps even slightly worse" | 2024 | [V] | https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust |


