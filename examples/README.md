# Case gallery — twenty real projects, twenty decisions

Twenty open-source projects, each run through the same four proof gates. Every report is
a self-contained HTML file you can open in a browser.

The gallery is in two batches. **Desktop applications** come first: apps — mostly Mac
apps — whose teams believed a Rust rewrite was the answer. Four of them tried and left
the evidence behind. **Systems and developer tooling** is the second batch.

**What these are.** Static, read-only analyses of public repositories at a named commit.
Line counts, file counts, symbol counts and module counts were measured on shallow clones
and are cited in each report's methodology section. **No build, test, benchmark or network
call was run against any target project.** Published numbers from other sources keep their
URL, workload regime and source class. Where a decisive measurement does not exist, the
report says `UNKNOWN` instead of estimating it.

**Every repository number was re-verified independently** against the same clone, on a
matched counting basis, after the reports were drafted. That pass changes real figures
every time. In this round it caught a `.ts` extension that turned out to be Qt Linguist
XML rather than TypeScript — counted naively, KeePassXC reads as 73% TypeScript — and a
vendored-versus-fetched mixup that had 97% of Ghostty's "own C++" belonging to an upstream
amalgamation. The corrected numbers are what you see here.

**Every report is bilingual.** English and 中文 both ship inside the same HTML file; the
button in the masthead switches between them, and a second button switches light and dark.
Verdict words, evidence states, file paths and numbers stay in English on both sides, so a
Chinese reader and an English reader are looking at the same evidence.

**What these are not.** They are not audits, and they are not advice to any of these
projects. They are worked examples of a decision method — including several cases where
the method declines to give a clean answer.

---

# Batch 1 · Desktop applications

| Project | Stack | Scope | Authorization | Report says |
|---|---|---|---|---|
| [remacs](remacs-why-not-rust.html) | Rust → dead | `STAY` | `REJECT` | It ran out of people before it ran out of C |
| [xi-editor](xi-editor-why-not-rust.html) | Rust → dead | `EXTRACT` | `APPROVE` | Take the kernel that survived, not the architecture that didn't |
| [lapce](lapce-why-not-rust.html) | Rust | `EXTRACT` | `APPROVE` | Take the kernel, rent the editor |
| [spacedrive](spacedrive-why-not-rust.html) | Rust + Tauri | `STAY` | `REJECT` | Rust stays. The feature scope does not |
| [zed](zed-why-not-rust.html) | Rust + GPUI | `MIGRATE` | `APPROVE` | It shipped — and the mechanism is not the advertised one |
| [fish-shell](fish-shell-why-not-rust.html) | C++ → Rust | `MIGRATE` | `APPROVE` | The one everybody talks about and almost nobody finishes |
| [ghostty](ghostty-why-not-rust.html) | Zig + Swift | `STAY` | `REJECT` | Stay in Zig — the cheap fix has not been priced |
| [bitwarden-desktop](bitwarden-desktop-why-not-rust.html) | Electron + Rust | `STAY` | `REJECT` | The split it already has is the answer |
| [signal-desktop](signal-desktop-why-not-rust.html) | Electron | `STAY` | `REJECT` | The shell stays; the memory-unsafety is somewhere else |
| [keepassxc](keepassxc-why-not-rust.html) | C++ / Qt | `STAY` | `REJECT` | Stay native; the migration buys a new UI, not a safer parser |

Six of these ten already bet on Rust and left the evidence behind. Two are dead (remacs,
xi-editor), two have stalled or gone sporadic (lapce, spacedrive), and two are thriving
(zed, fish-shell). Same language, opposite outcomes — which is the batch's actual finding.
The variable was never the language.

---

## 1 · remacs — `STAY` / `REJECT`

A serious, four-year, community-backed effort to rewrite GNU Emacs in Rust, in place.

- **666 of 1,414 Lisp primitives** moved to Rust — 47%. But only **26,825 lines** of
  Emacs behaviour converted, against **309,205 lines** of C still standing in `src/`.
  Small primitives are plentiful and cheap; `xdisp.c` is 33,281 lines holding 14 of them.
- **5 of 126 C files** were retired by the port in four years and four months. Four more
  disappeared with dropped MS-DOS support and are not conversions.
- Rust's safety mechanism did not survive contact with a C-managed heap. The Rust holds
  `Lisp_Object`s that a C mark-and-sweep collector traces through 164 `staticpro` roots
  the borrow checker never sees. A contributor wrote it down in issue #1532: *"we're back
  to the C world of 'If you don't want memory corruption you have to be really careful,
  the compiler won't keep you safe'."*

> **Tweet.** Rewrite Emacs in Rust. Four years, 4,600 stars, real contributors.
> It converted 47% of Emacs' Lisp primitives — and 8% of the code.
> 5 of 126 C files retired. 919 `unsafe` occurrences in the Rust that landed.
> The GC still traces Rust-held objects through roots the borrow checker can't see.
> Then the README changed to "not maintained anymore."

> **中文版。** 用 Rust 重写 Emacs。四年，4,600 star，真有人在写。
> 最后搬了 47% 的 Lisp primitive，代码量只搬了 8%。
> 126 个 C 文件退役了 5 个。落地的 Rust 里有 919 处 `unsafe`。
> GC 依然在追踪 Rust 持有的对象，而借用检查器看不见那些根。
> 然后 README 改成了「不再维护」。

---

## 2 · xi-editor — `EXTRACT` / `APPROVE`

Raph Levien's Rust editor, started at Google, with a native Swift macOS front end.

- The cross-process machinery grew to **7,601 lines** against the **3,089 lines** of
  editing operations it existed to deliver — a boundary **2.46×** the payload.
- **100 wire methods** a front end had to implement, on a protocol that never got version
  negotiation.
- `rust/rope/src/engine.rs` explains its own existence: the mini-CRDT is there because it
  *"is sufficient for asynchronous plugins that can only have one pending edit in flight
  each."* The causal arrow runs from the async plugin decision to the CRDT — not from Rust.

The verdict is `APPROVE` because the extractable kernel was real and it survived: the rope
lives on as `lapce-xi-rope` (129,043 downloads, 0.4.0 shipped December 2025), and
`xi-unicode` has 8,463,481 downloads. The editor is what died.

> **Tweet.** Google. Raph Levien. A Rust editor designed around a CRDT rope. 19,817 stars.
> The cross-process machinery reached 2.46× the editing code it carried.
> 100 wire methods, on a protocol that never got versioning.
> The CRDT existed to serve the async plugins — a decision, not a language.
> What survived isn't the editor. It's the rope.

> **中文版。** Google，Raph Levien，一个围绕 CRDT rope 设计的 Rust 编辑器，19,817 star。
> 跨进程那套机械最后长到它承载的编辑代码的 2.46 倍。
> 100 个 wire 方法，协议始终没做版本协商。
> CRDT 是为异步插件服务的——那是架构决定，不是语言决定。
> 活下来的不是编辑器，是那个 rope。

---

## 3 · lapce — `EXTRACT` / `APPROVE`

"Lightning-fast and powerful code editor written in Rust." 38,719 stars.

- **67,928 lines** against Zed's **1,539,358** on the same counting basis — **4.4%**.
  Same language, same target, opposite outcome.
- The team also wrote a **54,002-line GUI toolkit** (floem) on the side. That is 44.3% of
  the code this effort owns, and it is not editor.
- Commits on master went **1,897 in 2022 → 44 in 2025**. One person holds 2,023 of 3,636.
  Zed has **23 contributors** above Lapce's second-place contributor.

> **Tweet.** Two editors set out to replace VS Code in Rust.
> Zed: 1,539,358 lines. Lapce: 67,928 — 4.4% of it. Same language, same target.
> Lapce also wrote a 54,002-line GUI toolkit on the side.
> Commits: 1,897 in 2022 → 44 in 2025. One person holds 2,023 of 3,636.
> Rust was never the bottleneck. People were.

> **中文版。** 两个编辑器都想用 Rust 取代 VS Code。
> Zed 一百五十三万行，Lapce 六万八——4.4%。同一种语言，同一个目标。
> Lapce 还顺手写了一个 54,002 行的 GUI 工具包。
> master 上的提交：2022 年 1,897 次，2025 年 44 次。3,636 次里有 2,023 次来自一个人。
> 瓶颈从来不是 Rust，是人。

---

## 4 · spacedrive — `STAY` / `REJECT`

A VC-funded, Tauri-based file explorer with a Rust core. 38,686 stars.

- Its **own committed benchmark** says content identification is **95.5% of index wall
  clock** — 13.4 ms per file, 74.58 files/s on an M3 Max.
- The cause is in the code, not the language: `local.rs:133` opens the file inside every
  `read_range`, and the sampled hash makes six of them per file, awaited in sequence. That
  phase reads at most **7.6 MB/s**, while the benchmark CSV's throughput column overstates
  it **1,160×** by dividing logical file size rather than bytes read.
- Optimising traversal caps out at **1.047× end-to-end**. The project's own docs ask for
  13.4×. Meanwhile **36,463 lines** — 18.5% of `core/` — are P2P and sync machinery, and
  the highest non-prerelease tag is 0.4.3.

`STAY` here means keep the Rust. The language survives on distribution grounds — one
workspace ships desktop, a headless server, a CLI and mobile cores. What fails is the
justification and the scope.

> **Tweet.** A Rust file manager. VC-funded. 38k stars.
> Its own committed benchmark: content identification is 95.5% of index time, 13.4ms/file.
> Why? `local.rs:133` reopens the file inside every read — six sequential opens per file.
> Effective read rate: 7.6 MB/s. The CSV's throughput column overstates it 1,160×.
> Optimising traversal caps at 1.047×. The docs ask for 13.4×. That's not a language problem.

> **中文版。** 一个 Rust 写的文件管理器，拿了 VC 的钱，38k star。
> 它自己提交的 benchmark：内容识别占索引总耗时的 95.5%，每个文件 13.4 毫秒。
> 为什么？`local.rs:133` 每次 read 都重新 open 一遍文件，每个文件顺序开六次。
> 实际读取速率 7.6 MB/s。CSV 里那列吞吐量把它夸大了 1,160 倍。
> 优化遍历的天花板是 1.047 倍，文档要的是 13.4 倍。这不是语言的问题。

---

## 5 · zed — `MIGRATE` / `APPROVE`

The team that built Atom rebuilt their editor in Rust, with their own GPU UI framework.

- A real, compiled-in deadline: **8.33 ms**. `crates/gpui/src/app/bench_context.rs:62`
  sets `DEFAULT_FPS = 120`, and the harness prints overrun counts from HDR histograms.
  That is what separates this from a marketing superlative.
- **127,694 lines** of UI framework written from nothing, plus 4,050 lines of shaders,
  because in 2021 no Rust GUI could hold that budget.
- **776 of 1,111 `unsafe` blocks** sit in eleven `gpui*` crates while 1.4M lines stay
  checked.

The report approves it and still refuses to credit Rust for the headline: **leaving the
web view bought the frame rate**, and C++ or Zig would have delivered that too. What is
Rust-specific is narrower — Send/Sync type-checking across 1,943 async spawn sites, and
the `unsafe` quarantine above.

> **Tweet.** Zed is the Rust rewrite that worked. Read why carefully.
> 8.33ms frame budget, compiled in at `bench_context.rs:62`, measured against.
> But removing a GC from that window is a *native* win — C++ or Zig do it too.
> Sublime shipped that answer before Rust was a candidate.
> What Rust actually bought: 776 of 1,111 unsafe blocks quarantined, 1.4M lines checked.

> **中文版。** Zed 是那个成功的 Rust 重写。但要看清楚它成功在哪。
> 8.33 毫秒的帧预算，写死在 `bench_context.rs:62`，而且真的在拿它做测量。
> 但把 GC 从这个窗口里拿掉，是「原生」带来的，C++ 和 Zig 一样能做到。
> Sublime 在 Rust 还不是选项的时候就给出过这个答案。
> Rust 真正买到的是：1,111 个 unsafe 块里 776 个被圈进 GPU 后端，其余一百四十万行受检。

---

## 6 · fish-shell — `MIGRATE` / `APPROVE`

The port everybody talks about and almost nobody finishes. fish finished it.

- **78,532 lines of C++ at tag 3.6.0 → 0 files at HEAD.** No tracked file contains a
  `namespace`, a `template`, or `#include <vector>`. Two non-Rust files survive: a
  100-line macOS launcher stub and a 284-line test helper that deliberately misbehaves.
- The plan said *"Handwaving, 6 months?"* It took **338 days** to delete the C++ and
  **761** to ship 4.0.0 — with **345 days between releases** and nothing shipped meanwhile.
- Distinct commit authors went **96 → 154** across matched 12-month windows. That is the
  RFC's first-listed goal and the only one with a number attached.

An `APPROVE` that still bills the project: of four stated goals, two landed. Concurrent
function execution — the argument that picked Rust over Go, Zig and modern C++ — has not
shipped, and issue 238 has been open since 2012.

> **Tweet.** fish did the thing everyone talks about and almost nobody finishes.
> 78,532 lines of C++ → zero files. Not "mostly." Zero.
> The plan said "Handwaving, 6 months?" It took 338 days to delete the C++, 761 to ship.
> 345 of those days had no release at all.
> Authors went 96 → 154. The feature that justified picking Rust still hasn't shipped.

> **中文版。** fish 做成了那件所有人都在谈、几乎没人做完的事。
> 78,532 行 C++ 变成 0 个文件。不是「基本上」，是 0。
> 计划里写的是「Handwaving, 6 months?」，实际删完 C++ 用了 338 天，发版用了 761 天。
> 其中 345 天一个版本都没发。
> 贡献者从 96 涨到 154。而当初用来选 Rust 的那个特性，到现在还没做出来。

---

## 7 · ghostty — `STAY` / `REJECT`

Mitchell Hashimoto's terminal: 59,070 stars, fast, Mac-native — and written in Zig.

- The part people praise is **32,377 lines of Swift** across 160 files in `macos/Sources`
  — 67 importing AppKit, 63 SwiftUI. No choice of core language would have produced it.
- **0 of 5 published advisories** are memory-safety bugs: CWE-78, CWE-94, CWE-284, an fd
  leak, an escalation vector. Rust prevents none of them.
- Ghostty **already ships a safety-checked build** — the tip channel builds `ReleaseSafe`,
  codesigns and notarizes it. `PACKAGING.md:111` says the safe build is *"currently too
  slow"*, with **0 published measurements** behind that, while 15 benchmark harnesses sit
  in the tree.

G2 passes: Rust's ownership model does reach use-after-free where Zig's `ReleaseSafe`
cannot. It fails on price. A 213,626-line rewrite cannot be the smallest sufficient step
while a build flag goes unmeasured.

> **Tweet.** Everyone insists a fast Mac terminal has to be Rust.
> Ghostty is Zig. The part people actually praise is 32,377 lines of Swift.
> 0 of its 5 published advisories are memory-safety bugs.
> It already ships a `ReleaseSafe` build — codesigned, notarized, on the tip channel.
> The docs call it "too slow" with zero measurements, next to 15 unused benchmark harnesses.

> **中文版。** 所有人都觉得，Mac 上快的终端必须用 Rust 写。
> Ghostty 是 Zig 写的。而大家真正夸的那部分，是 32,377 行 Swift。
> 它公开的 5 个安全公告里，0 个是内存安全问题。
> 它其实已经在发带安全检查的构建了——签名、公证、走 tip 通道。
> 文档说那个构建「太慢」，一个测量数据都没有，旁边躺着 15 个没人跑的 benchmark。

---

## 8 · bitwarden-desktop — `STAY` / `REJECT`

A password manager that took the smallest sufficient option before anyone demanded a rewrite.

- **28,301 lines of Rust** in 13 crates sit behind exactly **38 functions** in a 491-line
  generated `.d.ts`, called from **15 files** — every one in the Electron main process.
- The desktop app's own TypeScript is **32,549 lines**, 4.2% of the monorepo. The Rust and
  the UI are already the right size relative to each other.
- **7,851 lines** of that Rust never compile on a Mac at all — Windows WebAuthn, plugin
  authenticator, process isolation.

Rust is already here, already load-bearing, adopted exactly at the seam where it pays.
The rejection is of *expansion*, not of Rust.

> **Tweet.** Should a password manager's desktop app be rewritten in Rust?
> Bitwarden already answered, years ago, without a rewrite.
> 28,301 lines of Rust behind exactly 38 functions, called from 15 files —
> all in the Electron main process, all at the OS seam Electron can't reach.
> Rewriting the Angular UI in Rust moves nothing the threat model cares about.

> **中文版。** 密码管理器的桌面端该不该用 Rust 重写？
> Bitwarden 几年前就回答了，而且没有重写。
> 28,301 行 Rust，暴露出来的正好 38 个函数，15 个文件在调，
> 全都在 Electron 主进程里，全都卡在 Electron 够不到的那条系统接缝上。
> 把 Angular UI 重写成 Rust，威胁模型里没有任何一项会变。

---

## 9 · signal-desktop — `STAY` / `REJECT`

If any app should be rewritten in Rust, it is this one. The answer is still no.

- **555,145 lines** of TypeScript and TSX — the thing a shell rewrite would replace, and
  already memory-safe. Signal's own native code is **308 lines**: one `.c`, one `.cpp`,
  one `.mm`. Zero Rust in this repository.
- The Rust that matters is already shipping: **182,247 lines** in libsignal, replacing
  `libsignal-protocol-c`, shared across iOS, Android and Desktop.
- Electron 43.0.0 bundles Chromium — roughly **36M SLOC** of C++ that Signal does not
  control. Signal's entire lever on it is **one line**: `package.json:245`.

The pattern already in the repo is the answer: `handleVideoAttachment.preload.ts:34` runs
every MP4 through libsignal's Rust `mp4san` parser before Chromium touches it. Cheap,
reversible, extends format by format. A shell rewrite competes with that and loses.

> **Tweet.** If any app earns a Rust rewrite, it's Signal. Nation-state threat model.
> 555,145 lines of TypeScript. Signal's own native code: 308 lines. Zero Rust in the app.
> The Rust is already there — 182,247 lines of libsignal, shared with iOS and Android.
> Meanwhile Electron ships ~36M lines of Chromium, and Signal's lever on it is one line.
> Their real strategy: a Rust MP4 parser in front of the C++ decoder. That's the move.

> **中文版。** 如果说哪个 app 配得上 Rust 重写，那就是 Signal——对手是国家级的。
> 55 万行 TypeScript。Signal 自己写的原生代码：308 行。仓库里 0 行 Rust。
> Rust 早就在了——libsignal 的 182,247 行，iOS、Android、桌面端共用。
> 而 Electron 带进来大约三千六百万行 Chromium C++，Signal 能动的只有一行版本号。
> 他们真正的做法：在 C++ 解码器前面放一个 Rust 的 MP4 解析器。这才是那一手。

---

## 10 · keepassxc — `STAY` / `REJECT`

C++ parsing attacker-supplied vaults. The strongest safety case in the batch — and it loses.

- The mechanism is real: a hostile `.kdbx` reaches `Kdbx4Reader::readHeaderField` before
  the header HMAC is compared, and KDBX 3.1 has no header HMAC at all.
- But KeePassXC parses almost none of those bytes itself. Its own share of the KDBX read
  path is **2,003 lines**; XML goes to `QXmlStreamReader`, gzip to zlib, every cipher and
  KDF to Botan. The security-relevant core is **14.1%** of its own source — 16,076 of
  113,863 lines — while `src/gui` alone is 50,344.
- **0 memory-safety CVEs of 6** NVD records since 2015. **476 of 660 files** include a Qt
  header, and 72 Qt Designer files hold 18,677 lines of `.ui` XML with no Rust equivalent.

> **Tweet.** A C++ password manager parsing attacker-supplied vault files.
> Best Rust case in this batch — the hostile bytes really do reach the parser first.
> It still loses: KeePassXC frames 2,003 lines of that path. Qt, zlib and Botan do the rest.
> Security-relevant core: 14.1% of its source. `src/gui` alone is 44%.
> 0 memory-safety CVEs in 11 years. 476 of 660 files include a Qt header.

> **中文版。** 一个用 C++ 写的密码管理器，要解析攻击者能构造的保险库文件。
> 这是本批里 Rust 理由最硬的一个——恶意字节确实先到解析器，再校验 HMAC。
> 它还是输了：这条路上 KeePassXC 自己只写了 2,003 行，其余交给 Qt、zlib 和 Botan。
> 安全相关的核心占自身代码 14.1%，而 `src/gui` 一个目录就占 44%。
> 11 年 0 个内存安全 CVE。660 个文件里 476 个 include 了 Qt 头文件。

---

## Suggested posting order — desktop batch

Lead with the autopsies, land the two approvals in the middle so the thread cannot be read
as anti-Rust, then close on the strongest steelman.

1. **remacs** — the biggest number, the clearest story
2. **spacedrive** — a real bug found in a shipping Rust app
3. **lapce vs zed** — the two-editor comparison; post as one thread if you can
4. **fish-shell** — the migration that finished
5. **zed** — the approval that refuses to credit Rust for the headline
6. **ghostty** — Zig, and 32,377 lines of Swift
7. **xi-editor** — the postmortem everyone half-remembers
8. **bitwarden-desktop** — the boring correct answer
9. **signal-desktop** — one line of `package.json`
10. **keepassxc** — the best case for Rust, argued fully, still rejected

---

# Batch 2 · Systems and developer tooling

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

Full write-ups with tweet copy for this batch are in
[README-systems.md](README-systems.md).

---

## Across both batches

Eight `APPROVE`, eleven `REJECT`, one `DEFER–MEASURE`, and all four scope words appear
across the twenty. That spread is the point: a tool that only ever says no is a
preference, not a method.

The desktop batch runs four `APPROVE` to six `REJECT` — it skews toward rejection because
that is what the evidence in those repositories says, not because desktop apps are a
category that fails. Two of its approvals are the cleanest in the gallery, and one of them
(zed) approves while explicitly declining to credit Rust for the result being advertised.

Also here: [sample-report.html](sample-report.html) — a synthetic golden fixture used to
regression-test the template. It analyses no real repository.

---

## Reproduce any of these

Every report is generated from a case module by the same renderer the skill ships:

```bash
python3 examples/build_cases.py              # render all twenty
python3 examples/build_cases.py zed remacs   # render selected slugs
python3 -m pytest tests/ -q                  # verify against committed output
```

The test suite asserts that the committed HTML is byte-identical to what the renderer
produces, that every Amdahl figure reproduces from the skill's own calculator, that all
twelve evidence lenses are present, that the embedded machine-readable record agrees with
the visible verdict, and that no case violates the decision table — `APPROVE` requires all
four gates and a non-`STAY` scope; `REJECT` and `DEFER–MEASURE` require a gate that did
not pass.

## Run it on your own repository

Point the skill at a repository you actually own and can measure. The gates are designed
to be hard to pass, and the honest answer for most projects is that a decisive measurement
does not exist yet — in which case the method says `DEFER–MEASURE` and names the artifact
that would settle it.
