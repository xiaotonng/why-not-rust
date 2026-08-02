# Case gallery, batch 2 — systems and developer tooling

Ten well-known systems and developer-tooling projects, each run through the same four
proof gates as the desktop batch. Start at [the main gallery](README.md) for the
desktop applications and for how these reports were produced and verified.

Same rules throughout: static read-only analysis of a public repository at a named
commit, no build or benchmark run against any target, `UNKNOWN` recorded wherever a
decisive measurement does not exist. Every report is bilingual — the masthead button
switches between English and 中文.

| Project | Language | Scope | Authorization | Report says |
|---|---|---|---|---|
| [curl/curl](curl-why-not-rust.html) | C | `EXTRACT` | `APPROVE` | Rust belongs at the backend seam, and only there |
| [sqlite/sqlite](sqlite-why-not-rust.html) | C | `STAY` | `REJECT` | Gates 1 and 2 pass; gates 3 and 4 end it |
| [openssl/openssl](openssl-why-not-rust.html) | C | `STAY` | `DEFER–MEASURE` | The decisive document was never published |
| [FFmpeg/FFmpeg](ffmpeg-why-not-rust.html) | C + asm | `PARTIAL` | `APPROVE` | Rewrite 3.6%, not 100% |
| [redis/redis](redis-why-not-rust.html) | C | `STAY` | `REJECT` | The rewrite cannot deliver its own objective |
| [evanw/esbuild](esbuild-why-not-rust.html) | Go | `STAY` | `REJECT` | Native is not the same claim as Rust |
| [PyCQA/flake8](flake8-why-not-rust.html) | Python | `STAY` | `REJECT` | Real gap; the rewrite already happened elsewhere |
| [prisma/prisma-engines](prisma-engines-why-not-rust.html) | Rust | `STAY` | `REJECT` | Removing Rust was the performance fix |
| [uutils/coreutils](coreutils-why-not-rust.html) | Rust | `PARTIAL` | `APPROVE` | Right migration, wrong rollout unit |
| [oven-sh/bun](bun-why-not-rust.html) | Zig → Rust | `MIGRATE` | `APPROVE` | Approved — and it was never about speed |

Four `APPROVE`, five `REJECT`, one `DEFER–MEASURE`. All four scope words appear.

---

## 1 · curl/curl — `EXTRACT` / `APPROVE`

The most-requested Rust rewrite in open source. curl already did the Rust part.

- `lib/vtls/rustls.c` is **1,468 lines** — a shipped Rust TLS backend behind an
  abstraction that already hosts 16 interchangeable implementations.
- `docs/DEPRECATE.md:62` reads *"hyper (removed in 8.12.0)"*. That was the four-year,
  ISRG-funded attempt to move curl's HTTP internals to Rust. It reached near
  test-suite parity and was deleted anyway — for lack of contributors and user demand.
- The compatibility surface a deeper rewrite owes: **526** documented libcurl API pages
  and **298** command-line options.

> **Tweet.** Everyone wants curl rewritten in Rust.
> curl already did it: 1,468 lines, one TLS backend, still shipping.
> Then it tried going deeper — 4 funded years, near-full test parity — and deleted it in 8.12.0.
> Not a technical failure. A staffing one.
> Verdict: EXTRACT at the seam. Reject the rewrite.

> **中文版。** 所有人都在喊「用 Rust 重写 curl」。
> curl 早就写了：1,468 行，一个 TLS 后端，一直在用。
> 后来它试着往深处走——4 年资金、测试几乎全过——最后在 8.12.0 删掉了。
> 不是技术失败，是没人维护。
> 结论：只在接缝处 EXTRACT，拒绝重写。

---

## 2 · sqlite/sqlite — `STAY` / `REJECT`

The only report where the safety gates pass and the rewrite still loses.

- SQLite reports **155.8 KSLOC** of library code against **92,053.1 KSLOC** of test code
  and scripts — a **590×** ratio — with **100%** branch and MC/DC coverage on the core.
- This commit alone carries **1,021,321 lines** of test material against **182,029**
  lines of core C.
- The project promises the **C API and on-disk format stay backwards compatible**, and
  plans support through **2050**. A rewrite inherits that promise and none of the
  verification behind it.

> **Tweet.** "Just rewrite SQLite in Rust."
> Gate 1 passes: it parses untrusted SQL and untrusted DB files in C.
> Gate 2 passes: Rust removes that class.
> Gates 3 and 4 end it. SQLite's asset isn't 155,800 lines of C — it's 92,053,100 lines of tests and 100% MC/DC coverage. That doesn't port.
> Verdict: REJECT.

> **中文版。** 「把 SQLite 用 Rust 重写不就行了。」
> 第一道门过了：它用 C 解析不可信的 SQL 和数据库文件。
> 第二道门也过了：Rust 能消除这类缺陷。
> 第三、四道门直接判死。SQLite 的资产不是那 155,800 行 C，而是 92,053,100 行测试和 100% MC/DC 覆盖率——这些搬不走。
> 结论：REJECT。

---

## 3 · openssl/openssl — `STAY` / `DEFER–MEASURE`

The strongest memory-safety case in open source, and the report returns **LOW**
confidence. On purpose.

- `util/libcrypto.num` and `util/libssl.num` list **6,357 exported symbols** across
  **116** public headers. That is the contract any reimplementation owes.
- The attacker-facing decoders — `crypto/asn1` plus `crypto/x509` — are **50,902 lines**,
  **6.3%** of the C.
- Nobody has published OpenSSL's advisory history split by component and root cause. So
  candidate Rust scopes span **16,772 to 808,625 lines** on identical evidence, and
  `providers/fips-sources.checksums` means the validated module's sources are
  checksum-pinned.

> **Tweet.** OpenSSL is the strongest memory-safety argument in open source.
> The report still refuses to approve a rewrite — and returns LOW confidence, INDETERMINATE robustness.
> Why: nobody has published which components produced OpenSSL's memory-safety advisories. So "rewrite 16,772 lines" and "rewrite 808,625" rest on the same evidence: none.
> Verdict: DEFER–MEASURE.

> **中文版。** OpenSSL 是开源界最强的内存安全论据。
> 报告依然拒绝授权重写，而且给出 LOW 置信度、INDETERMINATE 稳健性。
> 原因：没有任何人公开过 OpenSSL 的漏洞按组件归因。于是「重写 16,772 行」和「重写 808,625 行」依据的是同一份证据——没有证据。
> 结论：DEFER–MEASURE（先去测量）。

---

## 4 · FFmpeg/FFmpeg — `PARTIAL` / `APPROVE`

The report authorizes rewriting 2.9% of it, and names exactly why the rest is off the
table.

- Total measured: **2,021,868 lines** of C, headers and assembly.
- The container demux and bitstream parse layer — the first code to touch attacker
  bytes — is **59,433 lines** across 142 files. **2.9%**.
- **194,278 lines** are hand-written assembly across seven architecture subtrees. A Rust
  rewrite inherits none of it, and none of it serves the safety objective.
- The seam already exists: **300** demuxers register through one struct at
  `libavformat/avformat.h:565`. Mozilla ships a Rust ISO-BMFF parser behind a C API in
  Firefox today.

> **Tweet.** FFmpeg is 2,021,868 lines.
> The report approves rewriting 59,433 of them in Rust — 2.9%, the demuxers, where attacker bytes land first.
> It rejects the other 97%. Reason: 194,278 lines of that are hand-written assembly. A rewrite inherits none of it, and none of it makes you safer.
> Verdict: PARTIAL.

> **中文版。** FFmpeg 有 2,021,868 行。
> 报告批准用 Rust 重写其中 59,433 行——2.9%，就是 demuxer，攻击者的字节最先到达的地方。
> 剩下 97% 被拒。理由：其中 194,278 行是手写汇编。重写一行都继承不到，而且它跟安全目标毫无关系。
> 结论：PARTIAL。

---

## 5 · redis/redis — `STAY` / `REJECT`

The rewrite fails on its own stated objective, before economics even come up.

- `src/ae.c`, the event loop most proposals are actually picturing, is **516 lines**.
- `deps/` ships **200,299 lines** of vendored C — including jemalloc at **126,264** and
  Lua at **32,246**. Rewriting Redis's own 209,442 lines leaves **158,510 lines** of
  allocator and interpreter C linked into the binary.
- `src/redismodule.h` exports **402** `REDISMODULE_API` entry points that third-party
  modules compile against, alongside **459** command definitions.
- No public end-to-end Redis profile exists, so the performance half is recorded
  `UNKNOWN` — not refuted.

> **Tweet.** "Rewrite Redis in Rust for safety and speed."
> The event loop you're imagining is 516 lines.
> The vendored C that survives your rewrite is 200,299 — jemalloc and the Lua interpreter EVAL depends on.
> So "memory-safe Redis" isn't what the rewrite delivers. And no one has published a profile for the speed half.
> Verdict: REJECT.

> **中文版。** 「用 Rust 重写 Redis，又安全又快。」
> 你脑子里那个事件循环，516 行。
> 重写之后依然留在二进制里的第三方 C，200,299 行——jemalloc，和 EVAL 依赖的 Lua 解释器。
> 所以「内存安全的 Redis」根本不是这个方案能交付的东西。至于「更快」，没人公开过任何 profile。
> 结论：REJECT。

---

## 6 · evanw/esbuild — `STAY` / `REJECT`

Gate 1 fails before gate 2 gets a turn.

- The repository ships `make bench-three`. The author's published result: **0.39 s** for
  esbuild against **41.21 s** for webpack 5 on the same input.
- The author also published the attribution — four factors, each described as only
  somewhat significant alone: native ahead-of-time compilation, shared-memory
  parallelism, from-scratch consistent data structures, and exactly three AST passes.
  **Zero of the four are Rust properties.** All four were obtained with a garbage
  collector.
- The parallelism is **23** `go func` launch sites across **149,016** lines of Go.
- Microsoft ran the same comparison for the TypeScript compiler — 77.8 s → 7.5 s — and
  also chose Go over Rust.

> **Tweet.** esbuild is ~106× faster than webpack. It's written in Go.
> Its author published why: native AOT, shared-memory parallelism, from-scratch data structures, exactly 3 AST passes.
> Zero of the four are Rust properties. All four were achieved with a GC.
> Gate 2 asks what Rust specifically changes. Nothing here.
> Verdict: REJECT.

> **中文版。** esbuild 比 webpack 快约 106 倍。它是 Go 写的。
> 作者自己公布了原因：原生 AOT 编译、共享内存并行、从零设计的一致数据结构、精确三遍 AST。
> 四条里没有一条是 Rust 独有的。四条全部是在带 GC 的语言里拿到的。
> 第二道门问的是「Rust 具体改变了什么」。在这里：什么都没有。
> 结论：REJECT。

---

## 7 · PyCQA/flake8 — `STAY` / `REJECT`

A genuine order-of-magnitude gap, and the rewrite is still the wrong move.

- flake8's own source is **4,741 lines** across 33 files. It declares three dependencies
  — pycodestyle, pyflakes, mccabe — that do the actual checking.
- Its product is the plugin table at `setup.cfg:40`. A native binary cannot host Python
  plugins without embedding an interpreter.
- Grant the orchestrator a generous **30%** of lint wall-clock and make it *infinitely*
  fast: the ceiling is **1.43×**. The calculator returns *target physically IMPOSSIBLE*
  for a 10× goal.

> **Tweet.** flake8 has a real 10× performance gap. Gates 1 and 2 both pass.
> The report still says REJECT.
> flake8's own source is 4,741 lines — the checking happens in three other Python packages. Give the orchestrator 30% of the time and infinite speed: ceiling is 1.43×.
> The rewrite already happened. It wasn't yours. Adopt it.

> **中文版。** flake8 确实有 10 倍的性能差距，第一二道门都过了。
> 报告依然判 REJECT。
> flake8 自己的代码只有 4,741 行——真正干活的是另外三个 Python 包。就算给编排层 30% 的时间占比、无限加速，天花板也只有 1.43×。
> 那个重写早就发生过了，只不过不是你写的。直接用它。

---

## 8 · prisma/prisma-engines — `STAY` / `REJECT`

The one case in the set where removing Rust was the performance fix.

- Prisma's own published figures: a 25,000-row `findMany` went **185 ms → 55 ms** after
  the Rust query engine was removed. Bundle **~14 MB → 1.6 MB**.
- Feed that into the boundary formula with the TypeScript implementation as baseline:
  added boundary cost was **2.36× the baseline's entire runtime**. Even an infinitely
  fast Rust kernel tops out at **0.42×**. Parity was physically impossible.
- The nuance the headline hides: **394,195 lines of Rust are still in this repository**,
  including a retained WASM query-plan compiler at 73,675 lines. The reversal removed a
  *chatty* boundary, not a language.

> **Tweet.** Prisma deleted its Rust query engine and got 3.4× faster. Their numbers: 185ms → 55ms on 25k rows.
> Run it through the boundary formula: the crossing cost was 2.36× the baseline's ENTIRE runtime. Even an infinitely fast Rust kernel caps at 0.42×.
> But 394,195 lines of Rust are still in the repo. They removed a chatty boundary, not a language.

> **中文版。** Prisma 把自己的 Rust 查询引擎删了，然后快了 3.4 倍。他们自己的数字：25k 行查询 185ms → 55ms。
> 代入边界公式：跨界成本是基线**总耗时**的 2.36 倍。就算 Rust 内核无限快，上限也只有 0.42×。
> 但仓库里现在还有 394,195 行 Rust。他们删掉的是一个高频边界，不是一门语言。

---

## 9 · uutils/coreutils — `PARTIAL` / `APPROVE`

Right migration. Wrong rollout unit.

- **109** utilities, **251,003 lines** of Rust, and only **275** `unsafe {` blocks. That
  is the measured safety payoff, and it is excellent.
- It shipped as the Ubuntu 25.10 default *with* documented regressions: `cksum` up to
  **17× slower** than GNU on large files, and md5sum behaviour differences that broke
  Makeself self-extracting installers.
- The acceptance instrument already exists in-repo: `GNUmakefile` and
  `.github/workflows/GnuTests.yml`. It just was not made blocking per utility before
  the default flip.

> **Tweet.** Ubuntu 25.10 shipped 109 Rust coreutils as the default.
> The report APPROVES the migration — 275 unsafe blocks in 251,003 lines is a real safety win.
> What fails is gate 4, at the "flip the whole userland at once" scope. And the two things that actually broke — cksum 17× slower, md5sum breaking installers — are exactly what a per-utility acceptance gate catches.

> **中文版。** Ubuntu 25.10 把 109 个 Rust 版 coreutils 设成了默认。
> 报告 APPROVE 这次迁移——251,003 行里只有 275 个 unsafe 块，这是实打实的安全收益。
> 挂掉的是第四道门，卡在「整套 userland 一次性切换」这个粒度上。而现场真正出问题的两件事——cksum 慢 17 倍、md5sum 行为差异搞坏安装器——恰好就是逐个工具的验收门会拦住的东西。

---

## 10 · oven-sh/bun — `MIGRATE` / `APPROVE`

The only `APPROVE` + `MIGRATE` in the set. And it was never about speed.

- The port is complete in this commit: **0** `.zig` files remain, `build.zig` is gone,
  and there are **1,008,327 lines** of Rust across 1,496 files.
- Published result: selected first-party benchmarks improved **2.2–4.8%**. If the
  objective had been performance, gate 3 fails — a 1.5× target *misses* against a
  measured 1.048×.
- The honest caveat that keeps robustness at `CONDITIONAL`: **10,257** `unsafe {` blocks,
  and **786 of 1,496** Rust files touch `unsafe`. The class was reduced, not eliminated,
  and no post-migration measurement of the bug class has been published.

> **Tweet.** The only migration this method APPROVES in a 10-project set is the one that got 2.2–4.8% faster.
> Bun replaced ~535k lines of Zig with 1,008,327 lines of Rust. Zero .zig files left.
> Speed was never the reason — the reason was a stream of use-after-free bugs.
> Robustness stays CONDITIONAL though: 10,257 unsafe blocks. Reduced, not eliminated.

> **中文版。** 十个项目里，这套方法唯一 APPROVE 的迁移，恰好是只快了 2.2–4.8% 的那个。
> Bun 用 1,008,327 行 Rust 换掉了约 53.5 万行 Zig，一个 .zig 文件都不剩。
> 快从来不是理由——理由是一条源源不断的 use-after-free 缺陷流。
> 但稳健性只给 CONDITIONAL：还有 10,257 个 unsafe 块。是减少，不是消除。

---

---

## Suggested posting order

Lead with the biggest contrast, close with the credibility case:

1. **sqlite** — gates 1 and 2 pass and it still loses
2. **prisma-engines** — removing Rust made it faster
3. **esbuild** — the four factors, zero of them Rust
4. **redis** — 516 lines vs 200,299
5. **curl** — already did it, then deleted the deeper attempt
6. **ffmpeg** — approve 2.9%, reject 97%
7. **flake8** — the rewrite already happened, and it wasn't yours
8. **openssl** — LOW confidence, on purpose
9. **coreutils** — right migration, wrong rollout unit
10. **bun** — the one it approves, and speed was never the reason
