# why-not-rust

**A Claude Code skill that answers "should we rewrite this in Rust?" with evidence, not vibes.**

Point it at any repository and it produces a verdict — **STAY / EXTRACT / PARTIAL /
MIGRATE** — backed by a 12-dimension scorecard, matched industry precedents from a
40+ case library (every number carries a URL), and a self-contained HTML report
designed to be read in three seconds and defended in a design review.

<p align="center"><img src="docs/sample-report.png" width="720" alt="sample report"></p>

## Why this exists

The industry is full of "we rewrote it in Rust and it got 25× faster" stories, and
they create a systematic bias: teams migrate interaction-layer apps, DB-bound CRUD
services, and already-memory-safe TypeScript codebases to Rust expecting wins that
physically cannot come from a language swap. The receipts:

- **Bun ported 535k lines of Zig to Rust (2026): performance changed 2–5%.** The
  language itself was never the multiplier.
- **Prisma deleted its Rust query engine (2025) and got 3.4× faster in JS** — the
  JS↔Rust boundary serialization *was* the bottleneck.
- **TypeScript's own 10× compiler rewrite chose Go, not Rust** — with a GC.
- **VS Code is the fastest big Electron app** and it got there with architecture
  (process isolation, virtualization), not a language migration.
- **uv's famous "100×" is a warm-cache number**; cold installs are a real-but-8-10×.
- Meanwhile ruff, Pingora, pydantic-core, sudo-rs and the Android Rust program are
  *genuine* wins — with specific, checkable preconditions this skill tests for.

The name is both the question and the default posture: **the burden of proof is on
the migration.** But the skill is honest in both directions — when your project has
the Discord shape (hard tail SLO + measured GC violations) or the ruff shape
(cold-start-dominated CLI) or the sudo shape (C parsing untrusted input), it will
say MIGRATE and show you why.

## Install

```sh
git clone https://github.com/xiaotonng/why-not-rust ~/.claude/skills/why-not-rust
```

Restart Claude Code (or start a new session). The skill auto-triggers on questions
like "should we rewrite this in Rust?" — or invoke it explicitly:

```
/why-not-rust
```

## Usage

```
/why-not-rust                                # analyze the current repo
/why-not-rust quick                          # 5-question gate, short report
/why-not-rust focus on packages/diff-engine  # scope to one target
/why-not-rust 我们有两位资深 Rust 工程师，且必须满足内存安全合规
/why-not-rust review this RFC: docs/rust-migration-rfc.md
```

Free-text constraints (team skills, compliance requirements, fleet economics,
output language/path) are parsed and applied to the scoring weights — and every
adjustment is logged in the report's methodology box.

## What you get

1. **A verdict with confidence** — one of `STAY / EXTRACT / PARTIAL / MIGRATE`,
   capped by hard rules (no profiling evidence → can't exceed EXTRACT; DOM/DB-bound
   → full migration off the table; memory-safe source language → the safety
   argument scores zero).
2. **A 12-dimension diverging scorecard** — blue pulls toward staying, rust-orange
   toward migrating; bar length = score × archetype weight. Dimensions cover
   bottleneck locus, Amdahl ceiling, GC/tail sensitivity, footprint economics,
   startup shape, memory-safety delta, parallelism upside, distribution, ecosystem
   fit, seam quality, team readiness, and the stay-stack counterfactual.
3. **Matched precedents** — 3–5 industry cases with the same archetype and driver
   tags as your project, deliberately mixed (stayed-and-won / hybrid / migrated /
   failed), each with primary-source URLs.
4. **A misconception audit** — which of the 8 classic traps (safety conflation,
   Amdahl blindness, attribution error, GC-phobia, benchmark theater, hybrid
   blindness, rewrite-freeze denial, résumé-driven development) your situation—or
   your prompt—triggered.
5. **A recommended path** — smallest sufficient step first, each step with effort
   and an explicit acceptance threshold (e.g. "wasm PoC counts as a win only if
   end-to-end ≥4× including boundary cost").
6. **A styled, self-contained HTML report** — same visual language every time,
   dark/light, no external assets, printable, CJK-aware.

## What it will not do

- Run or modify your code (read-only probes; the only write is the report file).
- Quote a performance number without a URL, or fabricate a profile it didn't find.
- Flatter the conclusion your prompt was fishing for.

## The case library

`references/case-library.md` ships 40+ migrations, extractions, refusals, and
failures — Discord, Dropbox, Cloudflare Pingora, npm, Figma, InfluxDB, ruff/uv,
swc/oxc/Biome/rolldown, tsgo-chose-Go, esbuild-chose-Go, Bun-Zig→Rust, fish 4.0,
sudo-rs, uutils-in-Ubuntu, curl-dropped-hyper, Servo→Stylo, Prisma-deleted-Rust,
VS Code, Notion, Linear, Shopify YJIT, Twitch ballast, Zed, Tauri-vs-Electron
measurements, the Android memory-safety program, and more — each tagged with its
*true* driver so precedent-matching is mechanical, not vibes.

## License

MIT
