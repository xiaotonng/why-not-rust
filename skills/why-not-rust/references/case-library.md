# Case library — cited precedents for the Rust-migration question

This library contains **60** adoption, extraction, refusal, reversal, and stay-stack
cases. Match them with the six-field protocol in `dimensions.md`; do not force one of
each outcome when it would create false balance.

Last audited: **2026-08-02**. The 2026-08-02 pass added eight desktop-application
cases — remacs, xi-editor, Lapce/Zed, Spacedrive, Ghostty, Signal Desktop, Bitwarden
desktop and KeePassXC — measured directly from public repositories at a pinned commit
rather than from vendor prose. Worked reports for all eight, and for twelve others,
are in the repository's `examples/` gallery.

Source-check legend: **[V]** the linked page directly supports the claim as last
checked; **[V(s)]** a supporting source was located but some figures were available
only through excerpts, images, or background citations; **[C]** a vendor/speaker
claim has not been independently checked. These markers grade source checking, not
independence or causal validity. Inline flags—(vendor-claim), (vendor-curated),
(N=1), (baseline-age), (self-reported)—carry provenance and transfer caveats. Every
number keeps its URL and workload regime; quote nothing that lacks them.

## Tag taxonomy

- **Case tags** (observable requirement, workload, or constraint): `cpu-tight-loop` | `gc-tail-latency` | `memory-footprint` | `startup-time` | `memory-safety-from-c` | `single-binary` | `cross-platform-core` | `concurrency-correctness` | `ecosystem-pull` | `contributor-experience` | `cost-efficiency` | `scope-economics` | `iteration-cost`
- **Claim-risk tags** (search aids, never motive labels): `amdahl-omission` | `attribution-error` | `benchmark-method-risk` | `benchmark-regime-risk` | `claim-metric-ambiguity` | `architecture-attribution-risk` | `gc-attribution-risk` | `safety-conflation` | `boundary-tax` | `hybrid-option-omission` | `rewrite-freeze-risk`. Apply them symmetrically through the prompts in §5.

## 1 · Rust adoptions and migrations with real preconditions

### Discord · Read States service — Go → Rust (2020)
- scope: ONE hot-path service (read/unread tracking); the client stayed Electron, Python/Elixir stayed elsewhere | archetype: infra-hotpath | factors: gc-tail-latency
- facts: [V] Go forced a GC pass every ~2 min that scanned a giant LRU (tens of millions of Read States) → latency/CPU spikes; Rust version "had no latency spikes" and after tokio 0.2 tuning they "beat Go on every single performance metric"; cache then raised to 8M entries; exact ms values exist only in graph images. (baseline-age) [V] footnote: benchmarked on **Go 1.9.2** (2017), only 1.8–1.10 tried; Go 1.12 GC + 1.14 preemption never tested. https://discord.com/blog/why-discord-is-switching-from-go-to-rust
- attribution note: no-GC removed the periodic whole-cache scan — genuinely language-attributable on a pathological workload (huge long-lived working set, low garbage, strict tail SLO). Part of the gain is a hand-tailored BTreeMap LRU, i.e. data-structure work.
- supports: D3 supports a Rust option only with this shape—measured GC-caused tail violations and exhausted counterfactuals; D1/D2 show the hot path dominated the service.
- transfer limit: does not indict modern Go; a rerun on current Go + GOMEMLIMIT is the missing counterfactual (D12); no absolute numbers in text.

### Discord · message storage — Cassandra/JVM → Rust data services + ScyllaDB (2023)
- scope: storage tier | archetype: infra-hotpath | factors: gc-tail-latency, concurrency-correctness
- facts: [V(s)] read p99 40–125ms → 15ms; insert p99 5–70ms → 5ms; 177 → 72 nodes; custom Rust migrator moved 3.2M messages/s. https://discord.com/blog/how-discord-stores-trillions-of-messages
- attribution note: three at once — DB engine swap (Java → C++ ScyllaDB, shard-per-core), request-coalescing architecture, Rust in the middle tier; first-party framing credits ScyllaDB + coalescing at least as much as Rust.
- supports: D12 in production form: the p99 collapse is mostly the database — calibrates attribution for any "we added Rust and p99 fell" story.
- transfer limit: attribution-error canonical; never quote the p99 delta as a language result.

### AWS · Aurora DSQL adjudicator — Kotlin/JVM → Rust (2024–25)
- scope: one component first, then the whole data + control plane | archetype: infra-hotpath | factors: gc-tail-latency, cpu-tight-loop
- facts: [V(s)] years of tuning took Kotlin from 2,000 → 3,000 TPS; two engineers with zero Rust/C/C++ experience produced a Rust version at ~30,000 TPS — "10x faster than our carefully tuned Kotlin implementation – despite no attempt to make it faster." https://www.allthingsdistributed.com/2025/05/just-make-it-scale-an-aurora-dsql-story.html
- attribution note: plausibly allocation patterns + serialization + JIT warmup + GC combined; no public benchmark harness; HN/Lobsters asked where the 10x came from.
- supports: D3/D1 can genuinely stack on a hot coordinator; it also shows why a first-party number with no checkable artifact remains `WEAK`, regardless of size.
- transfer limit: (N=1), unreproducible; "no attempt to make it faster" also means the tuned-JVM *redesign* counterfactual was never run.

### Cloudflare · Pingora + FL2 — C/Lua (NGINX + OpenResty) → Rust (2022; FL2 2025)
- scope: fleet-scale edge proxy, >1T req/day | archetype: infra-hotpath | factors: memory-safety-from-c, concurrency-correctness, cost-efficiency
- facts: [V] Pingora: ~70% less CPU, ~67% less memory at the same traffic; median TTFB −5ms, p95 −80ms; one customer's connection reuse 87.1% → 99.92%. https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/ · [V(s)] FL2 (2025): median −10ms, +25% on CDN perf tests, CPU + memory cut by more than half. https://blog.cloudflare.com/20-percent-internet-upgrade/
- attribution note: first-party verbatim — **"This is not because we run code faster. Even our old service could handle requests in the sub-millisecond range. The savings come from our new architecture which can share connections across all threads."** Rust earns partial credit vs Lua (no GC/copies) plus the C-replacement safety case.
- supports: D4 can support a Rust option when fleet math is explicit; D12 still requires the same-architecture counterfactual before crediting the language.
- transfer limit: retellings as "Rust made it 3x cheaper" contradict Cloudflare's own words; Workers still runs on C++/V8 (workerd) — polyglot, not doctrine.

### npm · authorization service — Node.js → Rust (2019)
- scope: one CPU-bound service | archetype: backend-crud | factors: cpu-tight-loop, single-binary, contributor-experience
- facts: [V] whitepaper: "npm's first Rust program hasn't caused any alerts in its year and a half in production"; "My biggest compliment to Rust is that it's boring."; rewrite cost: ~1 hour in Node, 2 days in Go, ~1 week in Rust (learning included); zero throughput/latency numbers published. https://www.rust-lang.org/static/pdfs/Rust-npm-Whitepaper.pdf
- attribution note: operability testimonial, not a perf story; Go was rejected over 2019-era dependency management — (baseline-age) obsolete since Go modules.
- supports: D11 calibration: 1h/2d/1w is the honest people-cost ratio for a small service; "boring in prod" is the post-ramp upside; stated downside = maintaining a second monitoring/logging stack.
- transfer limit: proves ops-quiet, not fast.

### Figma · multiplayer sync server — TypeScript/Node → Rust child process (2018)
- scope: doc-sync engine only; Node KEPT the network layer, one Rust process per document over stdio | archetype: infra-hotpath | factors: cpu-tight-loop, gc-tail-latency, memory-footprint
- facts: [V] worst-case serialization >10x faster; server-side multiplayer perf better by "an order of magnitude"; low Rust memory made process-per-document viable (table values image-only). Also [V] 2018 pain: two Rust compression crates had "subtle correctness issues that would have resulted in data loss" → fell back to a proven C library. https://www.figma.com/blog/rust-in-production-at-figma/
- attribution note: single-threaded GC'd runtime × arbitrary-size documents; equally a scheduling/architecture fix (isolation per document) that low footprint enabled.
- supports: D10: the winning form was a hybrid at a process seam, not a stack migration; D4 when footprint × instance count is the multiplier.
- transfer limit: (baseline-age) 2018 ecosystem caveats are dated; the "Rust rewrite" kept Node in front.

### AWS · Firecracker — QEMU/C role displaced by greenfield Rust VMM (2018→)
- scope: microVM monitor under Lambda/Fargate | archetype: infra-hotpath | factors: memory-safety-from-c, startup-time, memory-footprint
- facts: [V(s)] spec-defined targets: <125ms to guest userspace, <5MiB overhead per microVM, 150 microVMs/s/host; trillions of Lambda invokes/month. https://github.com/firecracker-microvm/firecracker/blob/main/SPECIFICATION.md
- attribution note: the minimal device model + KVM gives the speed; Rust buys the safety case at a hostile multi-tenant trust boundary.
- supports: D6 supports a Rust option at a privileged trust boundary; D5/D4 are specified requirements rather than vibes.
- transfer limit: a minimal C VMM could boot as fast; greenfield — no migration delta exists.

### AWS · S3 ShardStore — prior C storage node → Rust (2021)
- scope: one storage-node type, >40K LOC | archetype: infra-hotpath | factors: memory-safety-from-c, concurrency-correctness
- facts: [V(s)] SOSP'21: lightweight formal methods (executable reference models, property tests, Loom, Crux) caught 16 issues pre-production; ~9 months of formal-methods effort; non-experts wrote 18% of model code. https://www.cs.utexas.edu/~bornholt/papers/shardstore-sosp21.pdf
- attribution note: a correctness-tooling culture that Rust's type system supports; not a perf story at all.
- supports: D6/concurrency-correctness as first-order motives — and that "correctness" claims came with a verification budget, not just a language.
- transfer limit: without the formal-methods investment the rewrite alone would not have caught those 16 issues.

### Microsoft · OpenHCL paravisor + the Russinovich rule — C/C++ displaced (2022–24)
- scope: Azure virtualization layer; company-adjacent policy statement | archetype: infra-hotpath | factors: memory-safety-from-c
- facts: [V(s)] OpenHCL (Rust paravisor) runs on >1.5M Azure VMs/month. https://techcommunity.microsoft.com/blog/windowsosplatform/openhcl-the-new-open-source-paravisor/4273172 · [V(s)] Russinovich 2022: "halt starting any new projects in C/C++ and use Rust for those scenarios where a non-GC language is required." https://www.theregister.com/2022/09/20/rust_microsoft_c/
- attribution note: security at the trust boundary; the rule's own hierarchy is GC language first, Rust only where GC is disqualified.
- supports: D6 framing plus the decision rule this skill inherits: Rust is the C/C++ replacement, not the everything replacement.
- transfer limit: personal opinion, not official policy; the same company chose Go for the TypeScript compiler (§4).

### GitHub · code search (Blackbird) — Elasticsearch/Java → purpose-built Rust (2023)
- scope: search engine over ~45M repos / 115TB corpus | archetype: infra-hotpath | factors: cpu-tight-loop, memory-footprint
- facts: [V(s)] 115TB → 25TB index (content dedupe + delta indexing); ingest ~120K docs/s; ~640 qps; shard p99 ~100ms; "about twice as fast" end-to-end with far better features. https://github.blog/engineering/architecture-optimization/the-technology-behind-githubs-new-code-search/
- attribution note: domain-specific index design carries the headline; Rust supplied predictable perf and safe parallelism.
- supports: D9 when no off-the-shelf engine fits the domain; D12 discipline — purpose-built vs general-purpose is not "Rust beats Java".
- transfer limit: attribution-error if quoted as a language result.

### InfluxDB · 3.0 / IOx — Go → Rust full core rewrite (2020–23)
- scope: whole database engine, rebuilt on Arrow/DataFusion/Parquet | archetype: data-pipeline | factors: ecosystem-pull, architecture-attribution-risk
- facts: [C] (vendor-claim) "100x faster queries on high cardinality, 10x ingest, 10x cheaper storage" — no neutral benchmark; compares a new columnar engine to their own aging TSM engine. https://www.influxdata.com/blog/influxdays-recap-paul-dix-journey-influxdb/
- attribution note: the defensible part is ecosystem-pull — the columnar stack they wanted (Arrow/DataFusion) IS Rust; InfluxData became a top DataFusion contributor.
- supports: D9 can favor a Rust option when the domain engine already lives in Rust crates the team would otherwise reimplement.
- transfer limit: benchmark-method-risk flag on all three multipliers; a storage-format + query-engine change, not a language result.

### Deno — Go prototype → Rust (2018)
- scope: JS runtime | archetype: cli-longtask | factors: gc-tail-latency (runtime composition), single-binary
- facts: [V(s)] rewritten for v0.1 chiefly to avoid stacking Go's GC beside V8's GC — "double runtime… garbage collection pressure" (Dahl). https://en.wikipedia.org/wiki/Deno_(software)
- attribution note: an embedding constraint — two competing collectors in one process — not Go's general fitness.
- supports: D9/D8 for VM-embedding projects only.
- transfer limit: routinely misquoted as "Go was too slow for Deno"; that was never the claim.

### Astral · ruff — flake8/Black/isort/pylint (Python) → Rust (2022–)
- scope: Python linter + formatter | archetype: cli-quick | factors: cpu-tight-loop, startup-time
- facts: [C] 10–100x claimed; [V(s)] adopters exceed it: Dagster ~1000x vs 4-core-parallel pylint (2.5min → 0.4s); Bokeh co-creator ~150–200x vs flake8; lints CPython in <500ms. https://github.com/astral-sh/ruff
- attribution note: Marsh's own decomposition [V(s)]: read + parse every file exactly ONCE for all rules (vs N tools × N parses), native execution, no-GIL file parallelism, caching, no interpreter cold start. https://notes.crmarsh.com/python-tooling-could-be-much-much-faster
- supports: D5 favors native startup for per-save invocation and D7 captures the GIL wall; D12 notes that nobody built the equally integrated pure-Python control.
- transfer limit: honest comparison is "one integrated native tool vs a federation of Python plugins each re-parsing" — architecture does a large share.

### Astral · uv — pip/pip-tools (Python) → Rust (2024)
- scope: package manager | archetype: cli-quick | factors: startup-time, cpu-tight-loop
- facts: [C] Astral's published suite reports cold cache **8–10x** vs warm cache **80–115x**; venv creation 80x vs `python -m venv`. https://astral.sh/blog/uv
- attribution note: the warm multiplier is cache/installer design (global wheel cache, hardlink/CoW ≈ zero copy work); the cold 8–10x is the language + parallelism + no-interpreter share; network-bound installs converge toward parity.
- supports: how to quote regime-split numbers (D2/D12): give warm AND cold; "100x" alone is the regime where the tool does ~no work.
- transfer limit: benchmark-method-risk if only the warm number is quoted.

### VoidZero & friends · JS toolchain — Babel/ESLint/Prettier/Rollup (JS) → Rust (2022–25)
- scope: swc, oxc/oxlint, Biome, rolldown-vite | archetype: compiler-buildtool | factors: cpu-tight-loop, startup-time, ecosystem-pull
- facts: swc [C] "20x/70x" vs [V] ~2–5x in full pipelines (discord.js measured 2x; Next.js claims "up to 5x"). https://swc.rs/ · oxlint [C] 50–100x; [V(s)] (adopter-reported, vendor-curated) Airbnb 126k files in 7s where ESLint timed out; one curated result reported ~62x; RAM 92MB vs 1.4GB. https://voidzero.dev/posts/whats-new-dec-2025 · Biome [V] won Prettier's $22.5k bounty (>95% JS/TS test compat, Nov 2023); [C] ~25x. https://prettier.io/blog/2023/11/27/20k-bounty-was-claimed.html · rolldown-vite [V(s)] (self-reported, vendor showcase repo) GitLab 2.5min → 22s (7x; 43x vs webpack), ~100x lower peak memory; Excalidraw 16x. https://voidzero.dev/posts/announcing-rolldown-vite
- attribution note: cold-start elimination + parallelism the JS runtime forbade + single-pass/single-engine architecture (rolldown removes double bundling); one-phase microbenchmarks inflate to 20–100x, end-to-end lands 2–7x.
- supports: D5/D7 for per-save dev tools; carries the (vendor-curated) flag — headline numbers are self-selected success stories.
- transfer limit: ESLint's value is plugins + type-aware rules — the part oxlint covered last; JS plugins pull Rust tools back toward JS speed.

### Vercel · Turbopack — webpack (JS) → Rust (2022–25)
- scope: bundler/dev server by webpack's author | archetype: compiler-buildtool | factors: cpu-tight-loop, benchmark-regime-risk
- facts: [C → retracted] "700x vs webpack / 10x vs Vite" at launch; [V] Evan You showed the bench ran Turbopack+SWC vs Vite+**Babel** and rounded 15ms → "0.01s"; with SWC on Vite the gap mostly closed. https://github.com/yyx990803/vite-vs-next-turbo-hmr/discussions/8 · [V] where it landed: default in Next 16 with the first-party expectation "2–5x faster production builds" and "up to 10x" faster Fast Refresh. https://nextjs.org/blog/next-16
- attribution note: incremental-computation architecture + Rust + parallelism; the 700x was warm-incremental HMR on synthetic 20k-module trees vs cold webpack.
- supports: benchmark-method-risk in its marketing form — and that the real product still won 2–5x; both facts travel together.
- transfer limit: quote the walkback with the launch number, never the launch number alone.

### fish shell 4.0 — C++ → Rust (2023–25)
- scope: whole shell: 57k lines C++ → 75k Rust, ~2 years, 200+ authors | archetype: cli-longtask | factors: concurrency-correctness, contributor-experience, memory-safety-from-c
- facts: [V] first-party perf admission: "usually slightly better in terms of time taken, memory use has a slightly higher floor but a lower ceiling" — parity, stated plainly; "the killer feature of Rust, from fish-shell's perspective, is Send and Sync"; only 17 people had ≥10 commits to the C++ code in 11 years; the "handwaving, half a year" estimate became ~2 years. https://fishshell.com/blog/rustport/
- attribution note: thread-safety for future concurrent execution + contributor funnel + tooling; explicitly not performance.
- supports: honest C++→Rust expectation: perf parity (D1 ≈ 0), value in D6/contributor concerns; also a schedule-realism datum.
- transfer limit: a successful migration whose performance lens is near neutral; cite it against the claim that every Rust migration is a speed project.

### Trifecta · sudo-rs — C → Rust (2023–25)
- scope: privilege tool; Ubuntu 25.10 default | archetype: cli-quick (security boundary) | factors: memory-safety-from-c
- facts: [V] shipped as default with zero performance framing anywhere first-party; "less is more" attack-surface reduction; original sudo maintainer Todd Miller advising. https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/
- attribution note: setuid C parsing attacker-influenced input—the mandatory memory-safe-alternative shape.
- supports: D6 strongly favors a scoped memory-safe option; a performance argument is unnecessary.
- transfer limit: proves nothing about performance or about migrating memory-safe code.

### uutils coreutils — GNU C → Rust (Ubuntu 25.10 default, 2025)
- scope: coreutils userland (~500/600 GNU tests passing at announcement) | archetype: cli-quick | factors: memory-safety-from-c, cross-platform-core
- facts: [V] shipped default WITH regressions: `cksum` up to **17x slower** than GNU on large files (later patched); `base64` slower, then fixed faster; md5sum behavior differences broke Makeself self-extracting installers. https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf
- attribution note: Canonical's motive is resilience/safety ahead of the LTS, not speed; 40 years of GNU tuning is a real baseline.
- supports: C→Rust is not automatically faster (D1 caution); behavioral compatibility is the hidden cost of any port (D12).
- transfer limit: not a failure — the safety rationale stands; quote the 17x only against "Rust is faster than C" claims.

### Bun · Zig → Rust port — the natural experiment (2026)
- scope: JS runtime; ~535k lines of Zig mechanically ported in ~11 days by ~64 parallel Claude agents (~$165k API cost) | archetype: cli-longtask | factors: memory-safety-from-c (Zig's manual lifetimes), concurrency-correctness
- facts: [V] selected first-party benchmarks improved **2.2–4.8%** (Bun.serve +4.8%, `next build` +4.5%); binaries ~20% smaller; big leak fixes; 19 regressions (since fixed); motive was a persistent stream of use-after-free/double-free/leak bugs. https://bun.com/blog/bun-in-rust · [C] production-readiness was contested at publication. https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743
- attribution note: in this selected same-architecture native-to-native comparison, performance moved by single digits while safety, leaks, and maintainability drove the migration.
- supports: one useful D1/D12 natural experiment for native sources—not a universal language ceiling.
- transfer limit: tests-pass ≠ production-ready; port quality contested.

### Zed · GPUI — greenfield Rust editor vs Electron incumbents (2024)
- scope: code editor + a custom GPU UI framework they had to build | archetype: native-desktop-gui | factors: cpu-tight-loop, startup-time, memory-footprint
- facts: [C] 120fps UI, <10ms typing; [V(s)] third-party unaudited: ~58ms end-to-end vs VS Code ~97ms; insertion ~2ms vs ~12ms. https://zed.dev/blog/videogame
- attribution note: game-engine-style GPU scene graph — no existing Rust GUI framework hit the bar, so they wrote GPUI; Sublime (C++) shows native editors predate Rust.
- supports: D9 may favor the incumbent GUI ecosystem when the flagship Rust app had to build its own framework; that cost belongs in D11.
- transfer limit: not a migration; numbers unaudited; GPUI is reusable but Zed-shaped.

### OpenAI · Codex CLI — TypeScript/Node → Rust (2025)
- scope: agent CLI (~95.7% Rust after the rewrite) | archetype: cli-longtask | factors: single-binary, startup-time, memory-footprint
- facts: [V(s)] stated reasons: zero-dependency install (drop the Node ≥22 requirement), native OS sandboxing (landlock/seccomp/seatbelt), lower startup/memory without GC, language-agnostic wire protocol. https://www.infoq.com/news/2025/06/codex-cli-rust-native-rewrite
- attribution note: distribution + sandbox primitives, not throughput; TS was the deliberate velocity choice for v1.
- supports: D8 supports a Rust option when no-runtime installation and OS sandbox primitives are hard requirements the baseline cannot meet.
- transfer limit: Anthropic's competing Claude Code stayed TypeScript and ships as a Bun-compiled binary (https://bun.com/docs/bundler/executables) — the rewrite is not table stakes for the category (D8 stay-stack answers exist).

### Dropbox · Nucleus — Python → Rust (2020)
- scope: desktop sync engine; ~4-year rewrite, shipped Mar 2020 | archetype: cli-longtask (desktop daemon) | factors: concurrency-correctness, cross-platform-core
- facts: [V] motives were data-model flaws, untestability, thread nondeterminism — "More than performance, its ergonomics and focus on correctness has helped us tame sync's complexity"; explicit redesign: new three-tree model, one deterministic control thread, simulation testing "millions of scenarios every day"; NO performance numbers published. https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine
- attribution note: a redesign whose invariants got encoded in the type system; most gains trace to the new data model.
- supports: correctness-motivated MIGRATE exists (type-system value, D7-adjacent) — but it arrived with a full redesign budget and 4 years.
- transfer limit: the counterfactual (same three-tree redesign in Python) was never priced; zero quantified perf evidence.

### Grab · Counter service — Go → Rust (2025)
- scope: one high-QPS counting service | archetype: infra-hotpath | factors: cost-efficiency, memory-footprint
- facts: [V] ~70% infra savings (elsewhere "80%" — internal inconsistency flagged); at 1,000 QPS: 20 Go cores → 4.5 Rust cores (~4.4x); **"the P99 latency is similar (or perhaps even slightly worse) in the Rust service"**; first-party: "rewriting a Golang service in Rust solely for performance improvements is unlikely to yield significant benefits" — expect "~50% compute savings" as the honest rule; async Rust footgun admitted (shipped a sync Redis call by mistake). https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust
- attribution note: steady-state Rust-vs-Go delta is cores/footprint, not latency; pays only at high traffic.
- supports: D4 evidence can justify Rust on cost-efficiency (~2–5x cores at fleet scale); D3 stays neutral without a GC-spike pathology.
- transfer limit: the best-documented refutation of "Rust will cut our p99" for Go services.

## 2 · Extractions & hybrids (the seam did the work)

### Mozilla · Stylo — C++ CSS engine → Rust component extracted from Servo (2015–17)
- scope: the CSS style system only, landed in Firefox 57 "Quantum" (Nov 14, 2017) | archetype: lib-with-bindings | factors: cpu-tight-loop (parallel styling), memory-safety-from-c
- facts: [V] started by 2 engineers late 2015, first pixels April 2016; shipped in ~2 years; Holley: "Almost everything successful is incremental in one way or another… the desire to throw everything away and start from scratch tends to be an emotional one." https://bholley.net/blog/2017/stylo.html
- attribution note: extraction at a seam where Rust had a real edge — parallel styling that prior C++ attempts had failed to land safely.
- supports: D10 is the success predictor: same org, same codebase — the extraction shipped, the whole-engine replacement (Servo, §4) died.
- transfer limit: rode Servo's R&D as a donor project; not a cheap standalone path.

### Google · Android memory-safety program — new code in Rust/Kotlin, old C/C++ left in place (2019–25)
- scope: OS components; explicitly NOT a mass rewrite ("safety by attrition") | archetype: infra-hotpath (OS native layer) | factors: memory-safety-from-c
- facts: [V] memory-safety share of Android vulns: 76% (2019) → 24% (2024) → **below 20%** (2025, first time); Rust ~0.2 vuln/MLOC vs ~1,000/MLOC C/C++ (**">1000x reduction"**); Rust changes: rollback rate ~4x lower than C++, ~25% less review time, ~20% fewer revisions; ~4% of Rust lines are `unsafe`. https://blog.google/security/rust-in-android-move-fast-fix-things/ · [V] decay finding: 5-year-old code has 3.4–7.4x lower vuln density than new code — their stated conclusion: write NEW code safe, interop over rewrite, let old code decay. https://www.theregister.com/2024/09/25/google_rust_safe_code_android/
- attribution note: stop the tap of new unsafe code; vulnerabilities decay exponentially with code age.
- supports: the strongest safety numbers in the library support incremental safe new code and scoped replacement, not automatic mass rewrites.
- transfer limit: a security outcome, not a performance story; the memory-safety comparison is C/C++-relative and does not transfer to memory-safe application code.

### pydantic · pydantic-core — Python → Rust core, Python API kept (2022–23)
- scope: validation inner loop via PyO3 | archetype: lib-with-bindings | factors: cpu-tight-loop
- facts: [C] 4–50x vs v1, ~17x on a representative model; [V(s)] end-to-end FastAPI apps 2–3x (user-reported). https://pydantic.dev/articles/pydantic-v2
- attribution note: hot kernel behind an unchanged API — the template for non-disruptive extraction.
- supports: D2 in numbers: 17x kernel → 2–3x app; quote both or neither.
- transfer limit: amdahl-omission if the 17x is pitched as the app-level gain.

### Hugging Face · tokenizers + OpenAI · tiktoken — Rust cores under Python APIs (2019–22)
- scope: tokenization libraries fronted by Python/Node bindings | archetype: lib-with-bindings | factors: cpu-tight-loop, ecosystem-pull
- facts: [C] (vendor-claim) HF README: "less than 20 seconds to tokenize a GB of text"; no independent audit found. https://github.com/huggingface/tokenizers · [C] tiktoken README: "3–6x faster" than comparable tokenizers. https://github.com/openai/tiktoken
- attribution note: hot loop in native code under a scripting API — achievable in C++/Cython too; the pattern, not the language brand, is the point.
- supports: D10 supports extraction when the boundary is batch-in/batch-out and data crosses rarely in bulk.
- transfer limit: both figures are vendor READMEs.

### Polars — pandas displaced by a Rust engine with Python bindings (2020–)
- scope: DataFrame engine used FROM Python | archetype: data-pipeline / lib-with-bindings | factors: cpu-tight-loop, memory-footprint, ecosystem-pull
- facts: [V] third-party benches (JetBrains, codecentric): group-by 5–10x, CSV read ~5x with ~87% less memory; gap grows with data size. https://blog.jetbrains.com/pycharm/2024/07/polars-vs-pandas/
- attribution note: columnar Arrow layout + multicore-by-default + lazy query optimizer; DuckDB (C++) achieves the same class of wins — the design differentiates, not the language.
- supports: D9's inversion: the ecosystem-pull answer can be "use the Rust-powered library from your current language" — a strong D12 case for adoption without rewriting.
- transfer limit: pandas is comparable or faster on small data; `apply`-style code gains little.

### Amazon · Prime Video living-room UI — JS low-level systems → Rust+WASM, JS kept on top (2022–24)
- scope: client SDK across 8,000+ device types; business logic stayed React/JS | archetype: web-frontend | factors: cross-platform-core, memory-footprint, cpu-tight-loop
- facts: [V(s)] 37K LOC Rust after ~1 year; WASM VM adds ≤7.5MB while saving 30MB of JS heap; steady-60fps goal; egui debug overlay integrated in hours. https://www.amazon.science/blog/how-prime-video-updates-its-app-for-more-than-8-000-device-types
- attribution note: split-stack — native-speed rendering/animation core under a scripting UI; as much a WASM story as a Rust story.
- supports: D10 hybrid on RAM-constrained devices; the JS layer survives because the seam is coarse.
- transfer limit: a TV-client SDK, not a template for general web apps.

### gitoxide — Rust git as a library, not a replacement (2020–)
- scope: Rust git implementation; Cargo uses gix for fetching; the CLI is "explicitly not to be understood as git replacement" | archetype: lib-with-bindings | factors: memory-safety-from-c, ecosystem-pull
- facts: [V] first-party status: `gix blame` "typically still up to 30% slower" than git with commitgraph caches on; some parallel-friendly ops beat git. https://github.com/GitoxideLabs/gitoxide/discussions/1791
- attribution note: library-first succeeds where op-for-op replacement of hyper-optimized C is a decade-scale project.
- supports: honest pacing for "rewrite git-shaped C" proposals (D1/D12 caution): 6 years in, parity is still open.
- transfer limit: "Rust rewrite of git" remains aspirational by its own author's framing.

## 3 · Stayed and won (same goal, no migration)

### Ghostty · Zig core + native Swift macOS app, Rust declined (2023–)
- scope: terminal emulator; libghostty core in Zig, macOS UI in Swift/AppKit, GTK on Linux | archetype: native-desktop-gui | factors: memory-safety-from-c, cross-platform-core, attribution-error
- facts: [V] at `46edeee4`, 213,626 lines of Zig excluding inline test blocks across 755 files — and **32,377 lines of Swift across 160 files under `macos/Sources`** (67 import AppKit, 63 SwiftUI, four titlebar implementations). The Mac-native quality users praise comes from the layer that is neither Zig nor Rust. [V] Ghostty's own C++ is **995 lines** in `src/simd/*.cpp` reaching for portable SIMD via Google Highway, which is fetched at build time (`pkg/highway/build.zig.zon:9`), not vendored; the 52,566-line simdutf amalgamation is upstream. [V] **0 of 5 published advisories** are memory-safety defects: CWE-78, CWE-94, CWE-284, an fd leak, an escalation vector. [V] a safety-checked build already ships — the tip channel builds `ReleaseSafe`, codesigns and notarizes it, while `PACKAGING.md:111` says the safe build is *"currently too slow"* with no measurement behind it and 15 benchmark harnesses unused in the tree. https://github.com/ghostty-org/ghostty
- attribution note: Rust's ownership model does reach use-after-free where Zig's `ReleaseSafe` cannot, so the mechanism is real. The case fails on price: a 213,626-line rewrite cannot be the smallest sufficient step while an existing build flag goes unpriced.
- supports: D3 and D6 — separate "native, non-GC" from "Rust specifically", and check whether a configuration change reaches the goal before any rewrite.
- transfer limit: a judgement about this project's costs, not a general claim about Zig versus Rust.

### Signal Desktop · crypto extracted to Rust years ago, the shell stayed TypeScript (2020–)
- scope: Electron messenger; libsignal consumed as a prebuilt native module | archetype: electron-desktop | factors: memory-safety-from-c, safety-conflation
- facts: [V] at `34fa4531`, **555,145 lines of TypeScript and TSX across 2,764 files** and zero Rust in the application repository; Signal's own native code is **308 lines** — one `.c`, one `.cpp`, one `.mm`. [V] the Rust that matters is upstream: libsignal is 182,247 lines across 584 files, replacing `libsignal-protocol-c` (archived 2020-07-31) and shared by iOS, Android and Desktop; even it still links BoringSSL via `boring 5.0.2`. [V] Electron 43.0.0 (`package.json:245`) bundles Chromium, and Chromium's own security team attributes ~70% of 912 high/critical bugs since 2015 to memory safety — Signal's entire lever on that C++ is one version pin. [V] the shipped mitigation pattern is a Rust parser in front of the C++ decoder: `ts/util/handleVideoAttachment.preload.ts:34` runs every MP4 through libsignal's `mp4san` before Chromium sees it. https://github.com/signalapp/Signal-Desktop · https://www.chromium.org/Home/chromium-security/memory-safety/
- attribution note: the strongest imaginable memory-safety customer extracted the narrow, high-assurance kernel and left the large, fast-changing UI in a memory-safe managed language. Rewriting TypeScript into Rust would move no defect class.
- supports: D6 — locate the untrusted-input parsing before sizing a scope; the exposure here is bundled C++ nobody proposes to rewrite.
- transfer limit: applies to apps whose UI language is already memory-safe; says nothing about C or C++ desktop UIs.

### Bitwarden desktop · Rust at the OS seam only, Electron UI kept (2021–)
- scope: Electron/Angular password manager with a Rust native module | archetype: electron-desktop | factors: memory-safety-from-c, scope-economics
- facts: [V] at `f97b15bc`, **28,301 lines of Rust in 170 files, every one under `apps/desktop/desktop_native`**, exposed through exactly **38 functions** in a 491-line generated `napi/index.d.ts` and called from 15 files, all in the Electron main process; the desktop app's own TypeScript is 32,549 lines across 238 files (4.2% of the monorepo's 780,391). [V] **7,851 of those Rust lines never compile on macOS** — Windows WebAuthn, plugin authenticator, process isolation; there is no `macos.rs` in the `biometric` crate and `secure_memory` falls back to `mlock`. [V] the decrypted user key does reach the renderer (`renderer-biometrics.service.ts:87`), and vault crypto is already Rust→WASM returning a JavaScript string (`encrypt.service.implementation.ts:49`). https://github.com/bitwarden/clients
- attribution note: Rust was adopted precisely where Electron cannot reach — keychain, biometrics, secure enclave — and nowhere else. Because the plaintext already crosses into JavaScript, a Rust UI would relocate the heap holding secrets rather than empty it.
- supports: D6 and G3 — the smallest sufficient option here was taken years before anyone proposed a rewrite; use it as the constructive counterpart to 1Password 8.
- transfer limit: the narrow-FFI verdict depends on the 38-function surface; a chatty boundary would price differently.

### KeePassXC · C++/Qt kept; the safety case loses on scope (2016–)
- scope: native cross-platform password manager parsing attacker-supplied `.kdbx` files | archetype: native-desktop-gui | factors: memory-safety-from-c, scope-economics
- facts: [V] the mechanism is real — a hostile `.kdbx` reaches `Kdbx4Reader::readHeaderField` before the header HMAC is compared, and KDBX 3.1 has no header HMAC at all. [V] but KeePassXC frames only **2,003 lines** of that read path itself: XML goes to `QXmlStreamReader`, gzip to zlib, and every cipher, hash and KDF to Botan (`CMakeLists.txt:478`). The security-relevant core is **16,076 of 113,863 own-source lines (14.1%)** while `src/gui` alone is 50,344 (44.2%), and there are 12 `memcpy` occurrences in the whole tree. [V] **476 of 660** files include a Qt header, with 72 Qt Designer files holding 18,677 lines of `.ui` XML that has no Rust equivalent. [V] **0 of 6** NVD records for KeePassXC/KeePassX 2015–2026 are memory-safety defects. https://github.com/keepassxreboot/keepassxc
- attribution note: absence of found bugs is not absence of bugs, and the report keeps an idle AFL harness as the trigger that would reopen the decision. What decides it today is that a rewrite buys a new UI toolkit, not a safer parser.
- supports: D6 with D9 — when the untrusted bytes are handled by vetted external libraries, "rewrite for memory safety" targets code the project never wrote.
- transfer limit: reverses if fuzzing produces findings in the 2,003-line framing layer.
- counting caution: this repository's 45 `.ts` files are **Qt Linguist translation XML**, not TypeScript. Counted naively they are 73.3% of the line total and make a C++ project read as a TypeScript one. Always confirm what an extension actually contains.

### Microsoft · VS Code — stayed TypeScript/Electron; native only at seams (2016–)
- scope: editor; C++ text buffer attempt reverted; ripgrep adopted as search subprocess | archetype: electron-desktop | factors: (control case for) cpu-tight-loop claims
- facts: [V(s)] 2018 native-buffer verdict: **"TL;DR: We tried. It didn't work out for us"** — converting strings between native representation and V8 "compromised any performance gained"; the fix was a better data structure in TypeScript (piece tree). https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation · [V(s)] ripgrep (Rust) powers text search since v1.11 (Mar 2017) — a subprocess at a clean seam. https://users.rust-lang.org/t/ripgrep-is-now-the-standard-text-search-provider-in-vs-code/10285 · [V(s)] perceived speed = extension-host process isolation + lazy activation + virtualized lists + V8 snapshots; 73.6% professional-editor share (SO survey 2024). https://survey.stackoverflow.co/2024/
- attribution note: boundary tax beat in-language gains once (buffer); Rust won once as a whole process exchanging bulk results (search); architecture carried the product.
- supports: D10 in both directions inside one product: a chatty per-operation boundary failed while a coarse process boundary shipped.
- transfer limit: does not prove native never helps — it proves the boundary decides.

### Notion · performance journey — caching architecture, language kept (2021; 2024)
- scope: Electron desktop + browser app | archetype: electron-desktop | factors: (control case) — the fix was I/O placement
- facts: [V(s)] native SQLite caching → desktop page loads/navigation **50% faster** (2021); WASM SQLite (OPFS) in the browser → navigation **+20%** across all modern browsers, 28–33% in AU/CN/IN (2024); they race disk cache vs network because old Android devices read disk slower than network. https://www.notion.com/blog/how-we-sped-up-notion-in-the-browser-with-wasm-sqlite
- attribution note: user-perceived speed was an I/O-and-caching problem; the fix was a database placement decision.
- supports: D1 favors the current stack for this performance objective because time lived in network/disk, outside the proposed rewrite.
- transfer limit: says nothing about CPU-bound cores; it says most apps don't have one.

### Linear · sync engine — local-first design in TypeScript (2019–)
- scope: SaaS project tool | archetype: web-frontend | factors: (control case)
- facts: [V(s)] all reads/writes hit a local object graph (MobX + IndexedDB) synced via websocket deltas off the Postgres replication log; most page loads <50ms; offline works. https://linear.app/now/scaling-the-linear-sync-engine
- attribution note: eliminated network round-trips architecturally; the language never changed.
- supports: "feels native" is a D1/D12 architecture outcome; no language swap touches round-trips.
- transfer limit: sync engines are hard — the cost went into design, not into a rewrite.

### Figma · fast-in-browser core — C++ → WASM, not Rust (2017)
- scope: editor core compiled to WASM; JS/TS UI around it | archetype: web-frontend | factors: cpu-tight-loop (via C++)
- facts: [V(s)] "WebAssembly cut Figma's load time by 3x" (vs prior asm.js), regardless of document size; 2018 follow-up: large doc 29s → <8s. https://www.figma.com/blog/webassembly-cut-figmas-load-time-by-3x/
- attribution note: compiled code where the profile demands it + scripting UI; the celebrated frontend case involves no Rust — the language brand is incidental.
- supports: attribution hygiene: "Rust-class" wins are really "compiled-kernel" wins; D10 hybrid again.
- transfer limit: C++ WASM carries memory-unsafety into the sandbox; Rust would add safety there, not speed.

### Google · Sheets calc engine — JS → Java compiled to WasmGC (2023–24)
- scope: browser calculation engine | archetype: web-frontend | factors: cpu-tight-loop
- facts: [V(s)] ~**2x** vs the prior JS engine via a WasmGC port of the Java code; WasmGC baseline in all engines since Safari 18.2 (Dec 2024). https://v8.dev/blog/wasm-gc-porting
- attribution note: shared code + near-native execution WITH a GC — no borrow checker involved.
- supports: the stay-managed WASM path exists for GC-shaped codebases (D12/D8 alternative to Rust-wasm).
- transfer limit: 2x, not 20x — browser compute gaps are modest when the JS was already JIT-hot.

### Shopify · YJIT — made Ruby faster instead of leaving Ruby (2021–23)
- scope: JIT built into CRuby, deployed fleet-wide | archetype: backend-crud | factors: (control case for) gc-attribution-risk, benchmark-method-risk
- facts: [V(s)] production (A/B vs JIT-off): 5–10% end-to-end on Ruby 3.2, **+15%** on 3.3; official benchmark suite: **61.2–67.4%** faster — i.e. bench numbers run 4–10x hotter than fleet numbers on the same product; adopted by Discourse fleet-wide. https://railsatscale.com/2023-09-18-ruby-3-3-s-yjit-runs-shopify-s-production-code-15-faster/ · https://speed.ruby-lang.org/
- attribution note: runtime investment; the bench-vs-fleet gap is the quantified benchmark-method-risk coefficient.
- supports: D12: runtime upgrades give double-digit fleet wins with zero freeze risk; and the ÷4–10 discount to apply to any vendor bench.
- transfer limit: 15% ≠ 10x — if the requirement is 10x, neither YJIT nor a language swap helps when D1 is IO-bound.

### Twitch · Go memory ballast → GOMEMLIMIT — GC tuned, no rewrite (2019 → 2022)
- scope: their busiest Go API service | archetype: backend-crud | factors: (control case) gc-attribution-risk
- facts: [V(s)] ~1GB never-touched ballast slice made the GC pacer run far less often; peak tail latency improved; pauses were already single-digit ms. https://blog.twitch.tv/en/2019/04/10/go-memory-ballast-how-i-learnt-to-stop-worrying-and-love-the-heap/ · [V(s)] Go 1.19 `GOMEMLIMIT` (2022) made the ballast hack obsolete; GC CPU capped ~50%. https://tip.golang.org/doc/go1.19
- attribution note: a GC pacing knob — ten lines, then a runtime flag.
- supports: D3 remains unresolved—not pro-Rust—while relevant collector/runtime tuning is untried.
- transfer limit: ballast fixed GC CPU churn — not a Discord-style resident-cache scan pathology; the two shapes differ.

### Netflix · Generational ZGC — JVM collector swap on JDK 21 (2024)
- scope: >half of critical streaming services | archetype: backend-crud | factors: (control case) gc-attribution-risk
- facts: [V(s)] default G1 → generational ZGC: consistently **sub-millisecond pauses** independent of heap size; removed GC as a source of gRPC tail-latency/timeout/retry storms — no language change. https://netflixtechblog.com/bending-pause-times-to-your-will-with-generational-zgc-256629c9386b
- attribution note: runtime version + collector choice.
- supports: D3: "GC pause" in 2024+ is a configuration/runtime-version problem before it is a language problem.
- transfer limit: memory-density economics survive sub-ms pauses (Hertz-Berger 3–5x heap, §6) — GC cost moved to RAM, it didn't vanish.

### GitHub · stayed Ruby on Rails (2023)
- scope: ~2M LOC monolith, 1000+ engineers, up to 20 deploys/day | archetype: backend-crud | factors: (control case) rewrite-freeze-risk avoided
- facts: [V(s)] upgrades Rails weekly via automated PRs tracking Rails main; dual CI against Ruby HEAD; on Ruby 3.2 within a month of release — explicitly instead of replatforming. https://github.blog/engineering/architecture-optimization/building-github-with-ruby-and-rails/
- attribution note: continuous upgrade beats starting over for a CRUD-shaped product.
- supports: D12/D11: a "legacy" monolith can ship 20x/day — the migration's opportunity cost is the argument.
- transfer limit: the same org built Blackbird in Rust (§1) — stay-the-monolith and build-the-engine-in-Rust coexist.

### Stack Overflow · tiny .NET footprint (2016)
- scope: one of the top sites on Earth on 9 primary web servers | archetype: backend-crud | factors: (control case) gc-attribution-risk
- facts: [V(s)] (baseline-age 2016) 209,420,973 HTTP req/day on 9 web servers, C#/.NET + SQL Server; later moved to .NET Core in place. https://nickcraver.com/blog/2016/02/17/stack-overflow-the-architecture-2016-edition/
- attribution note: perf culture + SQL/caching discipline; the GC language ceiling was never the constraint.
- supports: D1 for CRUD: the language is rarely the binding constraint at even extreme read scale.
- transfer limit: dated snapshot, but the shape (IO-bound CRUD on a GC runtime) recurs everywhere.

### jaq — the "ecosystem already shipped the Rust version" shape (2020–)
- scope: independent Rust reimplementation of jq (not a migration by the jq project) | archetype: cli-quick | factors: ecosystem-pull, startup-time
- facts: [V] README: "a clone of the JSON data processing tool jq", "focussed on correctness, speed, and simplicity"; own benchmarks: jaq-3.0 fastest on 20 of the suite's benchmarks vs jq-1.8.1 on 5 and gojq-0.12.18 on 6; original motivation included jq 1.6's ~50ms startup; two NLnet-funded security audits; >500-test suite. https://github.com/01mf02/jaq
- attribution note: a greenfield third-party reimplementation — evidence that "X but in Rust" may already exist without X's maintainers writing a line.
- supports: the D9/D12 move for maintainers and users: check whether the ecosystem already shipped the Rust option before funding a rewrite; adoption can relieve, without erasing, the original C safety pressure.
- transfer limit: author-run benchmarks; "drop-in" compatibility holds "in most cases", not byte-for-byte — the compatibility tax moves to the adopter.

### Prettier · pure-JavaScript CLI, 3x — same language, post-bounty (2023)
- scope: formatter CLI rework by a hired engineer, zero Rust | archetype: compiler-buildtool | factors: (control case) attribution
- facts: [V] ~3x (e18e reproduced 29s → 9s) via profiling, caching and IPC fixes — announced days after Biome claimed the Rust bounty. https://prettier.io/blog/2023/11/30/cli-deep-dive · https://e18e.dev/blog/prettier-speed-up.html
- attribution note: the baseline was unoptimized JS, not JS.
- supports: D12 favors a funded current-stack option when profiling exposes optimizations never attempted in the baseline.
- transfer limit: 3x still ≪ Biome's claimed ~25x — both facts belong in the same sentence.

## 4 · Reversals, refusals, failures

### remacs · in-place Emacs C → Rust, abandoned (2016-11 → 2021-04)
- scope: GNU Emacs C core ported function-by-function inside a hard fork | archetype: native-desktop-gui | factors: memory-safety-from-c, contributor-experience, scope-economics
- facts: [V] at the final commit `a684a4c2`, 30,133 lines of Rust across 88 files against 309,205 lines of C still in `src/` (119 files); subtracting 3,308 lines of port machinery (proc macro, bindgen driver, FFI mirror, build script) leaves **26,825 lines of converted behaviour**. [V] primitives tell a different story from lines: 666 `#[lisp_fn]` in Rust against 748 `DEFUN` in C — **47% of primitives, ~8% of the code**, because `xdisp.c` is 33,281 lines holding 14 of them. [V] only **5 of 126** upstream `.c` files were retired in four years and four months (four more went with dropped MS-DOS support, not with Rust). [V] 919 `unsafe` occurrences in 66 of 75 files under `rust_src/src`. https://github.com/remacs/remacs
- attribution note: Rust's safety mechanism does not survive inside a C-managed heap — the Rust holds `Lisp_Object`s that a C mark-and-sweep collector traces through 164 `staticpro` roots the borrow checker never sees. A contributor recorded it in issue #1532: *"we're back to the C world of 'If you don't want memory corruption you have to be really careful, the compiler won't keep you safe'."*
- supports: D6 cannot be claimed for Rust code whose objects are owned and traced by a foreign collector; D11 prices in-place ports of large C cores against contributor supply.
- transfer limit: indicts in-place porting under a foreign GC, not C→Rust generally — fish shell finished the same shape at a fortieth of the scope.

### xi-editor · Rust editor with a Swift front end, abandoned (2016 → ~2020)
- scope: editor core in Rust, native macOS front end in a separate repository, async plugins over JSON-RPC | archetype: native-desktop-gui | factors: architecture-attribution-risk, scope-economics
- facts: [V] at `a2dea305`, 39,292 lines of Rust in 103 files. The cross-process machinery — rpc, plugin-lib, lsp-lib, core-lib's plugins module, `rpc.rs`, `client.rs`, `line_cache_shadow.rs` and the rpc integration test — is **7,601 lines across 29 files against the 3,089 lines of editing operations it existed to deliver (2.46×)**. [V] **100 wire methods** a front end must implement, counted as leaf variants of the protocol enums in `rust/core-lib/src/rpc.rs`, on a protocol that never got version negotiation. [V] `rust/rope/src/engine.rs:16-30` states the CRDT exists because it *"is sufficient for asynchronous plugins that can only have one pending edit in flight each."* https://github.com/xi-editor/xi-editor · https://raphlinus.github.io/xi/2020/06/27/xi-retrospective.html
- attribution note: the causal chain runs Rust-2016 → no native GUI → process split → async plugins → CRDT. Only the last two links draw negative verdicts from the author; the language shaped the architecture without being the defect.
- supports: D10 prices cross-process boundaries that exceed the payload they carry; the extractable kernel survived where the architecture did not — `lapce-xi-rope` has 129,043 downloads and shipped 0.4.0 in December 2025, and `xi-unicode` has 8,463,481.
- transfer limit: a dead project whose kernel is still shipping is evidence for extraction, not against Rust editors.

### Lapce vs Zed · same language, same target, opposite outcome (2021 → 2026)
- scope: two Rust editors aiming at VS Code, one funded and one not | archetype: native-desktop-gui | factors: contributor-experience, scope-economics
- facts: [V] on a matched basis (`git ls-files '*.rs' | xargs wc -l`) Lapce is **67,928 lines across 141 files** and Zed is **1,539,358 across 1,926** — Lapce is 4.4% of Zed. [V] Lapce also carries a GUI toolkit written on the side: floem at `31fa8f44` is **54,002 lines** excluding examples, pinned as a git dependency at `Cargo.toml:79-89`. [V] commits on master fell **1,897 (2022) → 624 → 467 → 44 (2025)**; one person holds 2,023 of 3,636; Zed has **23 contributors** above Lapce's second-place contributor. https://github.com/lapce/lapce · https://github.com/zed-industries/zed
- attribution note: the language is held constant across both, so it cannot explain the divergence. What differs is headcount, funding, and whether the team also had to build its own GUI toolkit.
- supports: D11 is decisive for editor-scale rewrites; use this pair whenever a proposal argues that Rust itself will make a small team competitive with a funded one.
- transfer limit: not evidence that unfunded Rust projects fail — evidence that editor-scale scope is priced in people, not in language.

### Spacedrive · a Rust file manager whose bottleneck was I/O structure (2022 → 2026)
- scope: Tauri desktop file explorer, Rust core, React UI | archetype: native-desktop-gui | factors: attribution-error, amdahl-omission, scope-economics
- facts: [V] the repository's own committed benchmark (`core/benchmarks/results/`, 100,000 files, Apple M3 Max) puts content identification at **95.5% of index wall clock** — 1,340.8s against 60.15s for discovery alone, 13.4 ms per file. [V] the cause is in the code: `core/src/volume/backend/local.rs:133` opens the file inside every `read_range`, and the sampled hash performs six per file, awaited in sequence; with `MINIMUM_FILE_SIZE` = 102,400 B the phase reads at most **7.6 MB/s**, while the benchmark CSV's throughput column overstates it ~1,160× by dividing logical file size rather than bytes read. [V] optimising traversal yields **1.047× end-to-end** (share 0.045) against the ~13.4× the project's own docs imply. [V] 36,463 lines — 18.5% of `core/` — are P2P and sync machinery; highest non-prerelease tag is 0.4.3. https://github.com/spacedriveapp/spacedrive
- attribution note: a per-file syscall pattern, not the language, sets the ceiling. Rust survives here on distribution grounds — one workspace ships desktop, headless server, CLI and mobile cores — while the performance justification does not.
- supports: D2 must come from a profile, never from a line-count share; this is the cleanest available example of a first-party benchmark that refutes its own project's marketing number.
- transfer limit: prices this project's scope and I/O structure, not Tauri or Rust file tooling in general.

### Prisma · deleted its Rust query engine — Rust → TypeScript (2025)
- scope: ORM core moved to TS; a small WASM query-plan compiler retained | archetype: lib-with-bindings | factors: (reversal) boundary-tax
- facts: [V] their own numbers AFTER removing Rust: findMany 25k rows 185ms → 55ms (**3.4x faster**); complex joins 207 → 130ms; bundle ~14MB → 1.6MB (~90% smaller); reasons verbatim: "data must be serialized from JavaScript to Rust and then back to JavaScript"; per-OS/OpenSSL binaries; Rust+TS dual-skill shrank the contributor pool; edge runtimes can't carry the binary. GA v6.16.0 (Sept 2025), default in Prisma 7. https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm
- attribution note: per-call serialization across a chatty JS↔Rust boundary swamped the native gains — the boundary, not the language, was the bottleneck.
- supports: D10 favors the current architecture when callers cross a chatty runtime boundary per operation; here removing that boundary was the optimization.
- transfer limit: does not indict coarse-boundary Rust kernels (pydantic, tokenizers); it prices the chatty ones.

### curl · dropped the hyper backend — C → Rust HTTP internals, abandoned at ~95% (2020 → Dec 2024)
- scope: one backend of curl; 4 years, ISRG-funded, nearly full test-suite parity | archetype: security-parser | factors: memory-safety-from-c (failed on people, not tech)
- facts: [V] Stenberg: "There simply were no users asking for it and there were almost no developers interested or knowledgeable enough to work on it"; the C↔Rust glue needed rare dual expertise ("the overlap in the Venn diagram of the two universes is not big enough"); removed in curl 8.12.0 (Feb 2025). Date correction: the drop post is **Dec 21, 2024**, often misdated 2023. Meanwhile rustls (TLS) and quiche (QUIC/HTTP3) backends SURVIVED — "hooked in more cleanly and easier to maintain." https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/
- attribution note: no user pull + unstaffable maintainer pool; library seams outlive deep integrations.
- supports: D11 kills technically-sound safety migrations at 95% complete; the surviving rustls/quiche seams are the D10 lesson inside the failure.
- transfer limit: not evidence Rust can't do HTTP — evidence that migrations without contributors and demand die regardless of merit.

### Microsoft · TypeScript compiler → Go, Rust rejected (tsgo/Corsa, 2025)
- scope: tsc + language service, ported 1:1 for behavioral compatibility | archetype: compiler-buildtool | factors: cpu-tight-loop (achieved), refusal of Rust
- facts: [V] Microsoft's preview table: VS Code repo compile 77.8s → 7.5s (10.4x); editor project load 9.6s → 1.2s (8x); ~half the memory. https://devblogs.microsoft.com/typescript/typescript-native-port/ · [V] the official “Why Go?” discussion emphasizes cyclic graph compatibility, native execution, GC, and portability; a behavior-preserving **port, not a redesign**, was the constraint. https://github.com/microsoft/typescript-go/discussions/411
- attribution note: Hejlsberg's own split: ~3–3.5x native code + value types, the rest shared-memory parallelism — obtained WITH a GC; GC was a feature for cyclic ASTs.
- supports: D12 must include a GC'd native alternative when cyclic data and behavioral compatibility matter.
- transfer limit: compilers are the best case for native ports; says little about IO-bound services.

### esbuild · chose Go over Rust (2020–)
- scope: bundler written from scratch by evanw | archetype: compiler-buildtool | factors: startup-time, refusal of Rust
- facts: [V] repo-reproducible (`make bench-three`): esbuild 0.39s vs webpack5 41.21s (~106x); the FAQ's four factors, each "only a somewhat significant speedup," combined "multiple orders of magnitude": (1) native AOT — CLIs are "a worst-case performance situation for a JIT-compiled language"; (2) shared-memory parallelism (JS workers must serialize); (3) everything from scratch with consistent data structures; (4) memory efficiency — exactly three AST passes. https://esbuild.github.io/faq/
- attribution note: every advertised Rust-rewrite advantage, achieved in a GC'd language.
- supports: the four-factor decomposition is a useful evidence checklist for D1/D5/D7 on build tools.
- transfer limit: single-author greenfield; the 106x is vs JS webpack, not vs another native tool.

### Mozilla · Servo as Gecko replacement — never shipped (2012–2020)
- scope: whole-browser-engine replacement moonshot | archetype: native-desktop-gui | factors: memory-safety-from-c, scope-economics
- facts: [V] Holley: a full Gecko replacement "would probably require thousands of engineer-years" while Mozilla "could only afford a handful of heads"; Aug 2020: ~250 laid off including the whole Servo team; project moved to Linux Foundation; components (Stylo §2, WebRender) shipped instead. https://bholley.net/blog/2017/stylo.html · https://en.wikipedia.org/wiki/Servo_(software)
- attribution note: scope economics, not language quality — the ocean-boil got cancelled, the extraction became the flagship.
- supports: rewrite-freeze-risk at maximum scale; with Stylo it forms the canonical D10 pair cited in `dimensions.md`.
- transfer limit: Servo seeded the shipped components — the R&D wasn't wasted, the replacement goal was.

### Alacritty · "fastest terminal emulator in existence" vs the measurements (2017–)
- scope: claim audit of a greenfield Rust + OpenGL terminal | archetype: native-desktop-gui | factors: claim-metric-ambiguity
- facts: [C] the README superlative; [V(s)] Dan Luu measured its latency mid-pack and called throughput dumps "as useless a benchmark as I can think of". https://danluu.com/term-latency/ · [V(s)] LWN: ancient xterm/mlterm beat every modern terminal on worst-case latency; a 2022 macOS light-sensor test put kitty (C/Python) lowest at 29.2ms. https://lwn.net/Articles/751763/
- attribution note: "fastest" without a metric definition is branding; GPU throughput ≠ input latency.
- supports: the benchmark-method-risk tell in its purest form: superlative + no metric + no harness.
- transfer limit: Alacritty is a fine terminal; only the claim fails audit.

### LogLog Games · leaving Rust gamedev after 3 years (2024)
- scope: 3+ years, >100k LOC (own engine, Bevy, Macroquad) abandoned for shipping games | archetype: game | factors: iteration-cost
- facts: [V(s)] core claims: Rust fights rapid "is this fun?" iteration; problems "don't go away unless you're willing to constantly refactor and treat programming as puzzle-solving"; ecosystem rebuilds everything instead of reusing mature C/C++ stacks. Aras Pranckevičius: half the post is really about "hype cycles, tech zealotry, the search for silver bullets." https://loglog.games/blog/leaving-rust-gamedev/
- attribution note: iteration-speed-dominated domain — borrow-checker rigor is a tax on the core loop, not a benefit.
- supports: D11/velocity realism for prototype-shaped work; the game archetype's D9 drag.
- transfer limit: (N=1) indie account; engine-scale C++ teams weigh differently.

### Fixie (Matt Welsh) · Rust at a startup — first-party cautionary tale (2022)
- scope: velocity report from a CEO/ex-Google systems researcher | archetype: backend-crud | factors: rewrite-freeze-risk, iteration-cost
- facts: [V(s)] "Rust is awesome, for certain things. But think twice before picking it up for a startup that needs to move fast"; hiring hard; Rust "makes roughing out new features very hard." https://mdwdotla.medium.com/using-rust-at-a-startup-a-cautionary-tale-42ab823d9454
- attribution note: learning curve + prototyping drag ahead of product-market fit.
- supports: D11 can make a migration option uncompetitive when rapid product iteration and hiring dominate the decision.
- transfer limit: one account; Google's ramp data (1/3 productive at 2 months, §6) is the counterweight.

### Tauri on Linux · the WebKitGTK reality (2023–26)
- scope: Rust-shell desktop apps on system webviews | archetype: electron-desktop | factors: memory-footprint (marketed); (failure mode) benchmark-method-risk
- facts: [V(s)] official "Linux Graphics Issues" page (blank windows, NVIDIA DMABUF workarounds); maintainer: "we can't fully recommend Tauri for Linux right now," WebKitGTK "getting worse each release"; one app measured 40fps on WebKitGTK vs 240fps after converting to Electron. https://github.com/tauri-apps/tauri/discussions/8524 · https://github.com/tauri-apps/tauri/issues/14963
- attribution note: bundle-size marketing hides a rendering engine you don't control; on Windows, WebView2 IS Chromium and RAM ≈ Electron (§6 row).
- supports: D8/D9 for Electron-replacement proposals: the webview is the product surface; "smaller installer" is not "better UX".
- transfer limit: fine where WebKitGTK is acceptable or Linux is out of scope; macOS numbers (Hopp, §6) are real but (N=1).

## 5 · Evidence for the symmetric challenge audit

Use these prompts on both the migration and staying cases. Report `HIT`, `PASS`, or
`UNKNOWN` with evidence; do not diagnose motives.

### Challenge the migration case

- **M1 · End-to-end reach** — a component multiplier is shown without its share of
  user-felt time or boundary cost. Canon: pydantic-core's large kernel gain becomes a
  smaller application gain (§2); Notion and Linear moved I/O/round-trips (§3).
- **M2 · Causal attribution** — architecture, algorithm, data model, database, or
  cache changed alongside the language. Canon: Pingora's own architecture attribution,
  Discord's storage-engine swap, Blackbird's index design, and InfluxDB's columnar
  engine (§1).
- **M3 · Baseline and regime** — the benchmark uses a stale runtime, synthetic warm
  path, selected vendor workload, or incompatible feature set. Canon: Discord's Go
  1.9.2 baseline, Turbopack's launch benchmark, uv warm vs cold, and YJIT benchmark vs
  fleet results.
- **M4 · Safety/runtime transfer** — C/C++ vulnerability data or a pathological GC
  case is transferred to a memory-safe or differently tuned target. Canon: Android's
  numbers are C/C++-relative; Twitch/Netflix changed collector configuration without a
  language migration (§3/§6).
- **M5 · Boundary and compatibility** — call frequency, copies, serialization,
  behavior parity, platform matrix, or ABI cost is missing. Canon: Prisma and the VS
  Code native buffer failed at chatty boundaries; Figma and Stylo succeeded at coarse
  ones (§2–§4).
- **M6 · Delivery ownership** — dual-run, freeze exposure, maintainer pool, on-call,
  and rollback are absent. Canon: curl-hyper died near completion while rustls/quiche
  survived; Servo's components shipped while whole-engine replacement did not (§4).

### Challenge the staying case

- **S1 · Status-quo expertise** — incumbent familiarity is treated as product value
  rather than priced transition cost. Canon: Android, fish, and Grab invested in Rust
  capability when security/cost requirements justified it (§1–§2).
- **S2 · Hypothetical perfect counterfactual** — “optimize the current stack” is
  asserted without an owner, budget, design, or acceptance date. Canon: ruff/uv show
  that integrated native tooling can clear a gap that incremental scripting-language
  tuning may not (§1).
- **S3 · Cost of inaction** — continuing cloud spend, missed SLOs, vulnerability
  exposure, or compatibility limits are omitted. Canon: Grab's 20→4.5 core result,
  Discord's tail issue, and Android's unsafe-new-code program (§1–§2).
- **S4 · Unsafe-surface omission** — a memory-safe application label hides C/C++
  dependencies, parsers, privileged helpers, or FFI. Canon: sudo-rs and Android's
  scoped parser/component replacements (§1–§2).
- **S5 · Native-advantage denial** — startup, density, no-runtime deployment,
  parallelism, or ecosystem pull is dismissed without measurement. Canon: ruff, uv,
  Firecracker, Codex CLI, and Grab (§1).
- **S6 · Endless optimize-first treadmill** — tuning has no stop condition, so the
  migration can never be reconsidered. Canon: Aurora DSQL and Discord Read States
  show cases where a bounded experiment after real tuning changed the answer (§1).

## 6 · Reference numbers — quote only with the listed regime and caveat

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
| Rewrite consulting dataset | Crosslake reports 50+ rewrite projects typically landed 1.5–2x over both budget and schedule | 2022 | [C] | https://crosslaketech.com/how-long-does-a-complete-rewrite-of-a-software-application-take/ |
| Tauri vs Electron, measured | bundle 8.6 MiB vs 244 MiB; RAM ~172 vs ~409 MB after 6 windows (macOS, N=1, author uses Tauri); build 81s vs 16s | 2025 | [V] | https://www.gethopp.app/blog/tauri-vs-electron |
| Tauri RAM caveat on Windows | WebView2 IS Chromium — memory ≈ Electron once shared pages counted | 2023 | [V(s)] | https://github.com/tauri-apps/tauri/issues/5889 |
| Rust-native GUI maturity | 43 crates surveyed; overwhelming majority not production-ready (a11y, IME); viable-with-caveats: Dioxus/Slint/egui/iced | 2025 | [V(s)] | https://www.boringcactus.com/2025/04/13/2025-survey-of-rust-gui-libraries.html |
| Native-to-native natural experiment | Bun Zig→Rust selected benchmarks: +2.2–4.8% | 2026 | [V] | https://bun.com/blog/bun-in-rust |
| Go→Rust steady-state cost win | Grab: 20 → 4.5 cores at 1K QPS; p99 "similar or perhaps even slightly worse" | 2025 | [V] | https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust |
