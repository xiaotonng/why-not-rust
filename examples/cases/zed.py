"""zed-industries/zed — the 8.33ms budget is a constant in the source.

Repository facts were measured read-only on the shallow clone named in
`repository`. The clone's working tree was emptied by a concurrent process
partway through the session, so the tree was re-materialised into a scratch
directory with `git archive HEAD | tar -x`; HEAD was unchanged and every figure
reproduced.
"""

CASE = {
    "slug": "zed",
    "project_name": "zed-industries/zed",
    "project_desc": (
        "Rust · code editor plus its own GPU UI framework · 1,539,358 lines of Rust across 1,926 files",
        "Rust · 代码编辑器加自研 GPU UI 框架 · 1,539,358 行 Rust，分布在 1,926 个文件里",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · editor with a per-frame input deadline and a hand-written renderer",
        "原生桌面 GUI · 带逐帧输入截止时间的编辑器，渲染器自己写",
    ),

    "scope_word": "MIGRATE",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "STABLE",
    "selected": "rust-gpui",
    "scope_chip": (
        "rebuild the editor in Rust on a purpose-built GPU UI framework",
        "用 Rust 重建编辑器，配一套专门写的 GPU UI 框架",
    ),
    "scope_sub": (
        "the deadline is measurable and the rewrite shipped; the mechanism is not the advertised one",
        "截止时间可量，重写也交付了；起作用的机制不是宣传的那个",
    ),

    "why": (
        "The deadline is in the source. crates/gpui/src/app/bench_context.rs:62 sets the benchmark "
        "harness's default frame budget at 120fps, 8.33ms, and the harness reports how many budgets each "
        "frame blew. A collected runtime inside a DOM cannot promise that. The rewrite shipped anyway: "
        "39,386 commits and 1,275 releases since February 2021. What Rust bought is narrower than the "
        "pitch. Leaving the web view bought the frame rate, and C++ would have bought it too. Rust bought "
        "1,943 spawn sites a compiler checks, and 776 of 1,111 unsafe blocks parked in eleven gpui* crates "
        "instead of spread through 1.5M lines.",
        "截止时间就写在代码里。crates/gpui/src/app/bench_context.rs:62 把 benchmark 的默认帧预算设成 120fps，"
        "也就是 8.33ms，跑完还报出每帧超了几个预算。带 GC 的运行时套在 DOM 上，给不出这个承诺。这次重写确实交付"
        "了：2021 年 2 月至今 39,386 次提交、1,275 个 release。但 Rust 买到的东西比宣传里窄。帧率是靠离开 web "
        "view 拿到的，换 C++ 一样拿得到。Rust 买到的是 1,943 处 spawn 有编译器盯着，以及 1,111 个 unsafe 块里的 "
        "776 个关在十一个 gpui* crate 内，没散进 150 万行。",
    ),
    "trigger": (
        "Stable for Zed. It does not transfer by itself. Copy the decision only if you can name a "
        "per-frame deadline the way bench_context.rs:62 does, and only if no old product has to stay "
        "alive. Zed's delivery gate passed partly on situation: Atom was archived rather than migrated, so "
        "there was no ABI, no data format and no extension ecosystem to preserve. Change either condition "
        "and the scope drops below MIGRATE.",
        "对 Zed 本身，结论稳定。但它不会自动搬到别处。要照抄这个决定，前提是你能像 bench_context.rs:62 那样把逐"
        "帧截止时间说成一个数，而且没有旧产品需要继续养着。Zed 的交付门有一半是靠处境过的：Atom 是归档而不是迁移，"
        "所以没有 ABI、没有数据格式、没有插件生态要保。这两条里改掉任何一条，范围就掉到 MIGRATE 以下。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("8.33ms per frame, written into the harness at bench_context.rs:62.",
                           "每帧 8.33ms，写死在 bench_context.rs:62 的脚手架里。"),
         "name": "requirement",
         "evidence": "crates/gpui/src/app/bench_context.rs:62 sets DEFAULT_FPS to 120 and the harness counts frame-budget overruns from HDR histograms reported at p50/p90/p95/p99. crates/input_latency_ui/src/input_latency_ui.rs:327 ships the same budget to users, bucketing input-to-frame latency into 0-4ms, 4-8ms (120fps), 8-16ms (60fps), 16-33ms, 33-100ms and 100ms+, with a telemetry flush path. 13 [[bench]] targets and a 135-line internal profiling guide at docs/src/performance.md sit behind it."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Threading a compiler checks, and unsafe kept in one place.",
                           "编译器能查的并发，加上 unsafe 只待在一个地方。"),
         "name": "rust-specific causality",
         "evidence": "The frame-budget half is a native-versus-collected effect that C++ or Zig would also deliver; Sublime Text predates Rust. What is Rust-specific here is the scale of the threading and the containment of unsafe: 1,943 cx.spawn and cx.background_spawn call sites across 426 files, 4,734 #[gpui::test] cases on a deterministic scheduler with 215 re-run under explicit seed iterations, and 776 of 1,111 unsafe { blocks confined to the eleven gpui* crates. The attribution is structural. No C++ Zed exists to measure against."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("127,694 lines of UI framework, because no Rust GUI existed.",
                           "127,694 行 UI 框架，因为当年没有现成的 Rust GUI。"),
         "name": "economics and smallest sufficient option",
         "evidence": "The one-time bill is not 1,539,358 lines. 230,346 of those sit in test and fixture paths across 121 files, 784 inline #[cfg(test)] modules are not separated out, and 262,512 belong to the 2024-26 agent stack. The framework that had to be written from nothing is 127,694 lines across 235 files plus 4,050 lines of Metal, HLSL and WGSL shaders. Against a per-frame deadline no cheaper option reaches the target. Against a softer target Electron was cheaper in 2021 and still is."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("39,386 commits, 1,275 releases, nothing to stay compatible with.",
                           "39,386 次提交，1,275 个 release，没有兼容性要背。"),
         "name": "delivery and reversibility",
         "evidence": "GitHub API: the oldest commit in this repository is b400449 on 2021-02-20, 'Start rebuilding with a cleanly-separated UI framework'; v0.1 followed 108 days later on 2021-06-08; 1,275 releases have landed, the newest stable being v1.13.1 on 2026-07-29; 9,444 commits in the last 365 days and 624 in the last 30. Part of this gate is situational. Atom was archived rather than migrated, so no ABI, data format or extension ecosystem had to survive, and nobody needed a rollback."},
    ],

    "tiles": [
        (("Frame budget", "帧预算"), "8.33", ("ms", "ms"),
         ("crates/gpui/src/app/bench_context.rs:62 · DEFAULT_FPS = 120",
          "crates/gpui/src/app/bench_context.rs:62 · DEFAULT_FPS = 120")),
        (("UI framework written from nothing", "从零写出来的 UI 框架"), "127,694", ("lines", "行"),
         ("eleven gpui* crates · 235 files · plus 4,050 lines of shaders",
          "十一个 gpui* crate · 235 个文件 · 另有 4,050 行 shader")),
        (("unsafe blocks at the OS and GPU boundary", "落在 OS 与 GPU 边界上的 unsafe 块"), "776",
         ("of 1,111", "／共 1,111"),
         ("728 of them in the macOS and Windows backends alone",
          "其中 728 个只在 macOS 和 Windows 两个后端里")),
        (("First commit to first release", "首个 commit 到首个 release"), "108", ("days", "天"),
         ("b400449 2021-02-20 → v0.1 2021-06-08 · GitHub API",
          "b400449 2021-02-20 → v0.1 2021-06-08 · GitHub API")),
        (("Releases since", "此后发出的 release"), "1,275", ("releases", "个"),
         ("39,386 commits · 9,444 of them in the last 365 days · GitHub API",
          "39,386 次提交 · 其中 9,444 次在最近 365 天 · GitHub API")),
        (("Published decomposition of one frame", "公开的单帧时间拆解"), "0", ("artifacts", "份"),
         ("why D2 stays UNKNOWN inside an APPROVE", "APPROVE 里 D2 仍然记 UNKNOWN 的原因")),
    ],

    "options_sub": (
        "Every option is judged against one objective: hold input-to-frame latency inside an 8.33ms budget "
        "for a code editor on three desktop platforms, with no previous product that has to keep running.",
        "所有方案对着同一个目标：在三个桌面平台上，把编辑器的「输入到出帧」延迟压在 8.33ms 预算内，同时没有旧产品"
        "需要继续跑着。",
    ),
    "options": [
        {"id": "rust-gpui", "name": ("Rust plus a purpose-built GPU UI framework",
                                     "Rust 加一套专门写的 GPU UI 框架"),
         "implementation": "rust",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("budget met and instrumented in the shipped build",
                              "预算达成，且在发布版里带着测量"),
         "one_time_cost": "127,694 lines of framework plus 4,050 lines of shaders, before any editor code",
         "recurring_cost": "three platform backends, 776 unsafe blocks, a renderer nobody else maintains",
         "cost_cell": ("127,694 lines of framework; three backends forever",
                       "框架 127,694 行；三套后端要养一辈子"),
         "time_to_value": ("108 days to v0.1", "到 v0.1 用了 108 天"),
         "compatibility": "none required — Atom was archived, not migrated",
         "compat_cell": ("nothing to preserve · no rollback needed",
                         "没有东西要保 · 也不需要回滚"),
         "reversibility": "none, and none was wanted",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the only option that owns the whole frame",
                  "推荐 · 唯一把整帧握在自己手里的方案"),
         "reason": "The deadline lands on the paint pipeline, so the paint pipeline has to be yours. 1,275 releases and 9,444 commits in the last year say the scope was deliverable."},
        {"id": "stay-electron", "name": ("Stay on Electron and optimise the architecture",
                                         "留在 Electron，改架构去优化"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("large gains available; the 8.33ms budget is not among them",
                              "能拿到的收益不小；8.33ms 预算不在其中"),
         "one_time_cost": "process isolation, lazy activation, virtualised lists, snapshots",
         "recurring_cost": "a layout and paint pipeline you do not control",
         "cost_cell": ("cheapest by far; the DOM stays yours to route around",
                       "成本最低；但 DOM 只能绕，不能改"),
         "time_to_value": ("per release", "随版本发布"),
         "compatibility": "native to the incumbent stack",
         "compat_cell": ("full · git revert", "完全兼容 · git revert"),
         "reversibility": "git revert",
         "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · VS Code funded this and won a market with it",
                  "保留 · VS Code 走的就是这条，而且赢下了市场"),
         "reason": "The strongest counterfactual and the cheapest option. It reaches everything except a per-frame deadline, which is the one thing Zed's requirement is written as."},
        {"id": "rust-kernel-electron", "name": ("Rust kernel behind N-API, DOM UI kept",
                                                "Rust 内核藏在 N-API 后面，UI 继续用 DOM"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("helps the rope and the parser; leaves layout and paint where they were",
                              "对 rope 和解析器有用；布局和绘制原地不动"),
         "one_time_cost": "one seam plus a parity harness",
         "recurring_cost": "a per-operation boundary on the interactive path",
         "cost_cell": ("small; boundary tax lands on every keystroke",
                       "投入小；边界税落在每次按键上"),
         "time_to_value": ("months", "数月"),
         "compatibility": "internal API only",
         "compat_cell": ("internal API · build-flag rollback", "只动内部 API · 构建开关回滚"),
         "reversibility": "build flag",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the smallest Rust scope, aimed at the wrong layer",
                  "保留 · 最小的 Rust 范围，但打在错误的层"),
         "reason": "The seam is real but the deadline is not behind it. VS Code tried a native text buffer and reverted it because the conversion cost ate the gain."},
        {"id": "cpp-native", "name": ("Native rewrite in C++ on an existing toolkit",
                                      "用 C++ 在现成工具包上做原生重写"),
         "implementation": "non-rust-native",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("same frame budget; Sublime Text shipped this shape years earlier",
                              "同样的帧预算；Sublime Text 多年前就做出来了"),
         "one_time_cost": "comparable rewrite, with Qt or Skia supplying the renderer",
         "recurring_cost": "1.5M lines of manually managed memory instead of 1,111 declared blocks",
         "cost_cell": ("similar rewrite; whole tree becomes the unsafe surface",
                       "重写量相近；整棵树都变成 unsafe 面"),
         "time_to_value": ("comparable", "相当"),
         "compatibility": "none required",
         "compat_cell": ("nothing to preserve · no rollback", "没有东西要保 · 无回滚"),
         "reversibility": "none",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · this is what G2 has to beat, and it only loses on two lenses",
                  "保留 · G2 要赢的是它，而它只在两条维度上输"),
         "reason": "Meets the deadline and would have had a GUI toolkit off the shelf. It loses D6 and D7: no compile-time check over 1,943 spawn sites, and no boundary between safe and unsafe code."},
        {"id": "adopt-native-toolkit", "name": ("Adopt an existing native UI toolkit",
                                                "直接采用现成的原生 UI 工具包"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("solves the chrome; the text surface is the product",
                              "解决外壳；但产品本体是文本那一面"),
         "one_time_cost": "integration, then a custom text surface anyway",
         "recurring_cost": "a toolkit's frame model you do not set",
         "cost_cell": ("low to start; the editor view still has to be written",
                       "起步便宜；编辑器视图照样得自己写"),
         "time_to_value": ("weeks to a window", "几周能出个窗口"),
         "compatibility": "toolkit platform matrix",
         "compat_cell": ("toolkit's matrix · swap the toolkit", "跟着工具包的平台矩阵 · 换掉即可"),
         "reversibility": "swap the toolkit",
         "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · GPUI rasterises its own glyphs; a toolkit will not",
                  "排除 · GPUI 自己栅格化字形，工具包不会替你做"),
         "reason": "crates/gpui/src/text_system.rs:336 and crates/gpui_macos/src/text_system.rs:198 rasterise glyphs into an atlas Zed controls. That is the editing surface, and no toolkit hands it over."},
    ],

    "lenses_sub": (
        "Each state is scoped to named options and none of them add up to a score. Two performance lenses "
        "sit at UNKNOWN even though the verdict is APPROVE: the requirement is written down, the frame it "
        "applies to has never been decomposed in public.",
        "每条状态都绑到具体方案上，加起来也不构成分数。有两条性能维度停在 UNKNOWN，尽管结论是 APPROVE：需求写下来"
        "了，但那一帧的时间去向从来没有公开拆过。",
    ),
    "na_note": (
        "No lens is N/A here. D4 footprint and D5 startup would be the candidates, and both are recorded "
        "UNKNOWN instead. They bear on the decision and the repository does not measure them.",
        "这里没有 N/A。最接近的是 D4 内存占用和 D5 启动，两条都记成了 UNKNOWN。它们跟决策有关，而仓库里没有测量。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · native options", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["rust-gpui", "cpp-native", "adopt-native-toolkit"],
         "claim": ("The requirement is a per-frame deadline and it is written into code, not a blog post. "
                   "bench_context.rs:62 puts the default budget at 120fps. input_latency_ui.rs:327 ships "
                   "the same thresholds to users. window.rs:1592 caps the rate under thermal pressure. "
                   "Every option that compiles to native code can attack this; Rust is not singled out "
                   "here.",
                   "需求是一个逐帧截止时间，而且写进了代码，不是写在博客上。bench_context.rs:62 把默认预算定在 "
                   "120fps，input_latency_ui.rs:327 把同一组阈值发给用户，window.rs:1592 在热压力下降帧。任何"
                   "编译成原生代码的方案都能打这个目标，这一条不专属 Rust。"),
         "source": "crates/gpui/src/app/bench_context.rs:62 · crates/input_latency_ui/src/input_latency_ui.rs:327 · crates/gpui/src/window.rs:1592",
         "regime": "static read of the shipped source at commit 90d024b",
         "caveat": "The deadline is stated and instrumented. Whether the shipped build holds it is a telemetry question, and that telemetry is not public.",
         "change_trigger": "A softer target — 60fps, or 'feels fast' — moves this lens to the incumbent stack, because Electron reaches it."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-gpui", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-gpui"],
         "claim": ("No Amdahl figure appears here and none should. A deadline is not a speedup ratio, so "
                   "the calculator has nothing to work on. What is missing is narrower and more useful: "
                   "nobody has published a split of one 8.33ms frame into layout, glyph rasterisation, "
                   "scene building, GPU submit and compositor wait. The tooling for it is in the tree.",
                   "这里没有 Amdahl 数字，也不该有。截止时间不是加速比，计算器没东西可算。缺的是另一样更有用的："
                   "没有人公开把一帧 8.33ms 拆成布局、字形栅格化、场景构建、GPU 提交和合成器等待。做这件事的工具"
                   "就在仓库里。"),
         "source": "docs/src/performance.md (135 lines) · 13 [[bench]] targets · no published frame decomposition",
         "regime": "n/a — the artifact is absent",
         "caveat": "Zed publishes a first-party latency comparison against other editors. It is not a frame decomposition, and the skill's case library records it as unaudited.",
         "change_trigger": "A published frame decomposition would show how much of the 8.33ms Zed's own code actually owns versus the driver and the compositor."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "SUPPORTS · rust-gpui, cpp-native", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-gpui", "cpp-native"],
         "claim": ("An 8.33ms window has no room for a collector pause, and the baseline had one. This is "
                   "the clearest mechanism in the whole case. It is also the least Rust-specific: any "
                   "compiled stack without a managed runtime removes it. C++ ties on this lens.",
                   "8.33ms 的窗口塞不进一次 GC 停顿，而基线里有。这是整个案子里机制最清楚的一条，也是最不专属 "
                   "Rust 的一条：任何没有托管运行时的编译型栈都能去掉它。这条上 C++ 打平。"),
         "source": "crates/gpui/src/window.rs:1592 frame pacer · no collector in either candidate",
         "regime": "structural property of the runtime, not a measured trace",
         "caveat": "The repository holds no before-and-after trace of GC pauses against the budget. The mechanism is granted on construction, not on measurement."},
        {"id": "D4", "name": ("Fleet footprint", "内存占用"),
         "label": "UNKNOWN · stay-electron, rust-gpui", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["stay-electron", "rust-gpui"],
         "claim": ("Electron carries a Chromium baseline that a native binary does not. That is the usual "
                   "argument and this repository does not settle it. No steady-state resident-memory or "
                   "CPU comparison against a current Electron editor appears anywhere in the tree.",
                   "Electron 背着一份 Chromium 底子，原生二进制没有。常见论证就是这个，而这个仓库结不了它。树里"
                   "找不到任何跟当代 Electron 编辑器对比的稳态内存或 CPU 数据。"),
         "source": "no footprint comparison in the repository",
         "regime": "n/a",
         "caveat": "Installer size is not resident memory, and on Windows a system webview is Chromium anyway. Neither figure is measured here."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "UNKNOWN · rust-gpui, stay-electron", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-gpui", "stay-electron"],
         "claim": ("Atom's headline complaint was boot time, so this lens matters more than it usually "
                   "does for a desktop app. Zed instruments startup at crates/zed/src/main.rs:198 and "
                   "feeds it to hang detection and telemetry. No decomposition of boot into runtime init, "
                   "I/O and useful work is published. Atom's cost is widely attributed to eager module "
                   "loading, which VS Code attacked inside Electron.",
                   "Atom 最出名的抱怨是启动慢，所以这条比一般桌面应用重要。Zed 在 crates/zed/src/main.rs:198 "
                   "记了启动时间，接到 hang 检测和 telemetry 上。但没有公开把启动拆成运行时初始化、I/O 和有效"
                   "工作。Atom 那笔开销普遍被归给模块的急加载，而 VS Code 是在 Electron 内部解决的。"),
         "source": "crates/zed/src/main.rs:198 STARTUP_TIME · no published boot decomposition",
         "regime": "n/a",
         "caveat": "Recorded UNKNOWN on purpose. The repository shows startup is tracked; it does not show a startup requirement only a native binary can meet.",
         "change_trigger": "A boot decomposition for both stacks would move this lens, and it is the cheapest missing measurement in the case."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust-gpui", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-gpui"],
         "claim": ("Against the baseline there is no memory-safety prize to win, because JavaScript was "
                   "already safe. Against C++ there is: 1,111 unsafe { blocks are declared and 776 of them "
                   "sit in the eleven gpui* crates, 728 in the macOS and Windows backends alone. The rest "
                   "of the tree is checked. The residue is C — 24 tree-sitter packages and 47 -sys crates "
                   "in Cargo.lock, and Cargo.toml:856 pins a fork carrying a serialize() buffer-overflow "
                   "fix.",
                   "跟基线比，内存安全这块没奖可拿，因为 JavaScript 本来就是安全的。跟 C++ 比就有：1,111 个 "
                   "unsafe 块是显式声明的，776 个在十一个 gpui* crate 里，光 macOS 和 Windows 后端就占 728 个，"
                   "剩下的树是被检查过的。残留是 C——Cargo.lock 里 24 个 tree-sitter 包、47 个 -sys crate，而 "
                   "Cargo.toml:856 钉的是一个带 serialize() 缓冲区溢出修复的 fork。"),
         "source": "1,111 occurrences of `unsafe {` across *.rs · 776 in crates/gpui and crates/gpui_* · Cargo.toml:856",
         "regime": "static token count at commit 90d024b; comments not excluded",
         "caveat": "Filtering comment-leading lines moves 1,111 to 1,108. The tree-sitter grammars are generated C compiled into the binary, and they parse files the user opens."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · rust-gpui", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-gpui"],
         "claim": ("The whole design is 'keep the foreground thread under the deadline by moving "
                   "everything else off it'. There are 1,943 cx.spawn and cx.background_spawn call sites "
                   "across 426 files. 4,734 #[gpui::test] cases run on a deterministic scheduler, and 215 "
                   "of them re-run under explicit seed iterations to search interleavings. This is the one "
                   "lens where Rust beats the C++ option on evidence rather than on taste.",
                   "整套设计就是「把别的活挪走，让前台线程留在截止时间内」。cx.spawn 和 cx.background_spawn 共 "
                   "1,943 处，分布在 426 个文件。4,734 个 #[gpui::test] 跑在确定性调度器上，其中 215 个用显式 "
                   "seed 迭代反复搜交错。这是唯一一条 Rust 靠证据而不是靠口味赢过 C++ 方案的维度。"),
         "source": "1,489 `cx.spawn` + 454 `cx.background_spawn` across 426 files · 4,734 `#[gpui::test]` · 215 with `iterations =`",
         "regime": "static call-site and attribute counts at commit 90d024b",
         "caveat": "Call-site counts are a proxy for concurrency pressure, not a measurement of races avoided. No incident history is published to anchor the claim."},
        {"id": "D8", "name": ("Distribution & embedding", "分发与嵌入"),
         "label": "SUPPORTS · rust-gpui", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-gpui"],
         "claim": ("Atom ran extensions in-process as JavaScript. Zed runs them as WebAssembly under "
                   "wasmtime 36, against 77 versioned .wit interface files. That is a Rust-ecosystem asset "
                   "doing real architectural work, and it is a different answer to the problem Atom's "
                   "extension model created.",
                   "Atom 的插件是进程内的 JavaScript。Zed 把插件跑成 WebAssembly，宿主是 wasmtime 36，接口是 77 "
                   "个带版本的 .wit 文件。这是 Rust 生态里一个真的在承重的资产，也是对 Atom 插件模型那个问题的另一"
                   "种答法。"),
         "source": "Cargo.toml:880 wasmtime = 36 · 77 tracked *.wit files · crates/extension_host (10,341 lines)",
         "regime": "static manifest and interface inventory",
         "caveat": "wasmtime embeds from C too, and Node has WebAssembly. The advantage is that Rust is the reference host, not that the sandbox is unavailable elsewhere."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "DISFAVORS · rust-gpui", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-gpui"],
         "claim": ("In 2021 Rust had no GUI framework that could hold this budget, so they wrote one. The "
                   "bill is 127,694 lines across 235 files, 4,050 lines of Metal, HLSL and WGSL shaders, "
                   "eight GPU primitive types at scene.rs:222, a glyph rasteriser and atlas, and 776 "
                   "unsafe blocks of platform glue. C++ would have had Qt or Skia off the shelf. This lens "
                   "counts against the option that was chosen.",
                   "2021 年的 Rust 没有能撑住这个预算的 GUI 框架，所以他们自己写了一套。账单是 235 个文件、"
                   "127,694 行，加 4,050 行 Metal、HLSL、WGSL shader，scene.rs:222 里八种 GPU 图元，一套字形栅格"
                   "化和图集，以及 776 个平台胶水的 unsafe 块。C++ 那边 Qt 或 Skia 现成就有。这一条是记在被选方案"
                   "头上的负号。"),
         "source": "127,694 lines across 235 files in crates/gpui and crates/gpui_* · 4,050 lines of *.metal/*.hlsl/*.wgsl · crates/gpui/src/scene.rs:222",
         "regime": "static inventory at commit 90d024b",
         "caveat": "The framework became reusable and is published as a crate, which recovers part of the cost. Against that: 1,862 packages in Cargo.lock show the rest of the ecosystem was there."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-kernel-electron", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-kernel-electron"],
         "claim": ("The cheap Rust option puts a kernel behind N-API and keeps the DOM. The deadline does "
                   "not live behind that seam. It lives in layout, glyph raster and scene submission — the "
                   "exact stretch GPUI owns and a web view does not hand over. VS Code ran this experiment "
                   "with a native text buffer and reverted it.",
                   "便宜那个 Rust 方案是把内核塞到 N-API 后面，UI 继续用 DOM。截止时间不在那条接缝后面，它在布局、"
                   "字形栅格化和场景提交里，正好是 GPUI 自己握着、而 web view 不会交出来的那一段。VS Code 拿原生"
                   "文本缓冲做过这个实验，后来回退了。"),
         "source": "crates/gpui/src/scene.rs:222 (8 primitive types) · crates/gpui/src/text_system.rs:336 · crates/editor/src/element.rs (12,510 lines)",
         "regime": "structural, from the paint path in this commit",
         "caveat": "A coarse seam did work elsewhere in the same product category: VS Code shells out to ripgrep for search. Bulk results at a process boundary are a different shape from per-frame paint."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "SUPPORTS · rust-gpui", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-gpui"],
         "claim": ("This is the lens most rewrites fail, and Zed passes it on shipping evidence. First "
                   "commit 2021-02-20, v0.1 released 108 days later, 1,275 releases since, 39,386 commits, "
                   "9,444 of them in the last 365 days and 624 in the last 30. Three platforms. The 1.5M "
                   "line figure overstates the bill: 230,346 lines sit in test and fixture paths and "
                   "262,512 belong to the agent stack built in 2024-26.",
                   "多数重写死在这条上，Zed 是靠已经交付的证据过的。首个 commit 2021-02-20，108 天后发 v0.1，"
                   "此后 1,275 个 release、39,386 次提交，最近 365 天 9,444 次、最近 30 天 624 次，三个平台。"
                   "150 万行这个数字把账单说大了：230,346 行在测试和 fixture 路径里，262,512 行属于 2024-26 年"
                   "才建的 agent 栈。"),
         "source": "GitHub API repos/zed-industries/zed · 121 files / 230,346 lines in test and fixture paths · 262,512 lines in the agent crates",
         "regime": "GitHub API on 2026-08-02; contributors endpoint reports 482 and caps at 500",
         "caveat": "Zed Industries is a funded company and staffing is not disclosed here. The delivery record proves the scope was shippable by this team, not by any team."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "NEUTRAL · rust-gpui, cpp-native", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["rust-gpui", "cpp-native"],
         "claim": ("On the frame budget the two native options tie, and Sublime Text shipped the C++ "
                   "version of this answer long before Rust was an option. Anyone crediting Rust for "
                   "Zed's frame rate is crediting the wrong variable. The split shows up at D6 and D7 "
                   "instead, and nowhere else.",
                   "在帧预算上，两个原生方案打平，而 Sublime Text 在 Rust 还不是选项的年代就交付了 C++ 版的这个"
                   "答案。把 Zed 的帧率记在 Rust 头上，记错了变量。真正分开的地方在 D6 和 D7，别处没有。"),
         "source": "case-library.md Zed entry attribution note · D3, D6, D7 in this ledger",
         "regime": "cross-option comparison against the same 8.33ms objective",
         "caveat": "No C++ Zed exists, so the tie at D3 is an argument from construction. The split at D7 rests on call-site counts, which is structural evidence and not a controlled comparison."},
    ],

    "findings": [
        ("current",
         ("The 8.33ms budget is a constant, not a slogan", "8.33ms 预算是个常量，不是口号"),
         ("crates/gpui/src/app/bench_context.rs:62 reads `const DEFAULT_FPS: u64 = 120;`. The harness "
          "turns that into a per-frame budget and prints how many budgets each frame overran, from HDR "
          "histograms at p50, p90, p95, p99 and max. The same thresholds ship to users: "
          "input_latency_ui.rs:327 buckets input-to-frame latency at 0-4ms, 4-8ms labelled 120fps, 8-16ms "
          "labelled 60fps, and up to a 100ms+ bucket labelled sluggish. This is what separates the case "
          "from a superlative in a README.",
          "crates/gpui/src/app/bench_context.rs:62 写的是 `const DEFAULT_FPS: u64 = 120;`。脚手架把它换成"
          "每帧预算，再打印每帧超了几个预算，数据来自 HDR 直方图的 p50、p90、p95、p99 和最大值。同一组阈值也发给"
          "用户：input_latency_ui.rs:327 把输入到出帧的延迟分成 0-4ms、标着 120fps 的 4-8ms、标着 60fps 的 "
          "8-16ms，一直到标着 sluggish 的 100ms 以上。这就是它跟 README 里一句形容词的区别。"),
         "crates/gpui/src/app/bench_context.rs:62 · crates/input_latency_ui/src/input_latency_ui.rs:327"),
        ("current",
         ("Rust did not buy the frame rate. Leaving the web view did.",
          "帧率不是 Rust 买来的，是离开 web view 买来的。"),
         ("Removing a collector from an 8.33ms window is the mechanism, and it belongs to 'compiled "
          "native', not to 'Rust'. Sublime Text shipped that answer in C++ years earlier. What Rust "
          "contributes shows up in two places instead: 1,943 cx.spawn and cx.background_spawn sites across "
          "426 files that a compiler type-checks, and 776 of 1,111 unsafe blocks confined to eleven gpui* "
          "crates while the other 1.4M lines stay checked. Attribute the speed to the architecture and the "
          "safety of the architecture to the language.",
          "把 GC 从 8.33ms 窗口里拿掉，机制是这个，而它属于「编译型原生」，不属于「Rust」。Sublime Text 多年前"
          "就用 C++ 交付了这个答案。Rust 的贡献落在另外两处：426 个文件里 1,943 处 cx.spawn 和 "
          "cx.background_spawn 由编译器做类型检查；1,111 个 unsafe 块里 776 个关在十一个 gpui* crate 内，剩下 "
          "140 万行保持被检查。速度记给架构，架构的安全记给语言。"),
         "1,489 `cx.spawn` + 454 `cx.background_spawn` · 776 of 1,111 `unsafe {` in crates/gpui, crates/gpui_*"),
        ("current",
         ("They wrote 127,694 lines of UI framework because there wasn't one",
          "他们写了 127,694 行 UI 框架，因为当时没有"),
         ("The eleven gpui* crates are 127,694 lines across 235 files, plus 4,050 lines of Metal, HLSL and "
          "WGSL. scene.rs:222 defines eight GPU primitive types; text_system.rs:336 rasterises glyphs into "
          "an atlas Zed owns. A C++ team would have started from Qt or Skia. This is the cost of choosing "
          "a language whose GUI ecosystem was not ready, and it is the one lens in this ledger that argues "
          "against the option that was picked.",
          "十一个 gpui* crate 共 235 个文件、127,694 行，另加 4,050 行 Metal、HLSL 和 WGSL。scene.rs:222 定义了"
          "八种 GPU 图元；text_system.rs:336 把字形栅格化进 Zed 自己管的图集。C++ 团队会从 Qt 或 Skia 起步。这是"
          "选了一门 GUI 生态还没准备好的语言要付的钱，也是这本账里唯一一条不利于被选方案的维度。"),
         "crates/gpui + crates/gpui_* · 127,694 lines / 235 files · crates/gpui/src/scene.rs:222"),
        ("current",
         ("Rust top to bottom stops at the parser", "Rust 从头到尾，到解析器就停了"),
         ("Cargo.lock carries 24 tree-sitter packages and 47 -sys crates. The tree-sitter grammars are "
          "generated C, they compile into the binary, and they parse whatever file you open. Cargo.toml:856 "
          "pins a Zed fork of tree-sitter-markdown described in the manifest as carrying a `serialize()` "
          "buffer-overflow fix. The memory-unsafety class did not leave the code path where an editor "
          "meets untrusted input.",
          "Cargo.lock 里有 24 个 tree-sitter 包和 47 个 -sys crate。tree-sitter 的语法是生成出来的 C，会编进"
          "二进制，解析的是你打开的任何文件。Cargo.toml:856 钉的是 Zed 自己 fork 的 tree-sitter-markdown，manifest "
          "里写明它带一个 `serialize()` 缓冲区溢出修复。在编辑器接触不可信输入的那条路径上，内存不安全这个缺陷类"
          "没有离开。"),
         "Cargo.toml:856 · 24 tree-sitter packages and 47 -sys crates in Cargo.lock"),
        ("unknown",
         ("Nobody has published where the 8.33ms goes", "没有人公开过这 8.33ms 花在哪"),
         ("docs/src/performance.md is 135 lines of internal procedure: samply flamecharts, Tracy spans, a "
          "built-in `zed open performance profiler`, and a `warn_if_gt` timer. The instruments exist. The "
          "artifact does not. No public decomposition splits one frame into layout, glyph raster, scene "
          "build, GPU submit and compositor wait, so D2 stays UNKNOWN inside an APPROVE. The requirement is "
          "proven; the share Zed's own code owns is not.",
          "docs/src/performance.md 是 135 行内部流程：samply 火焰图、Tracy span、内置的 `zed open performance "
          "profiler`，还有一个 `warn_if_gt` 计时器。仪器都在，产出物没有。没有一份公开材料把一帧拆成布局、字形"
          "栅格化、场景构建、GPU 提交和合成器等待，所以 D2 在 APPROVE 里仍然是 UNKNOWN。需求成立；Zed 自己代码"
          "占多少，没有。"),
         "docs/src/performance.md (135 lines) · no published frame decomposition"),
    ],

    "buys": [
        (("A tail with no collector in it", "尾延迟里没有 GC"),
         ("an 8.33ms window has no room for a stop-the-world pause. Removing the managed runtime is the "
          "mechanism, and C++ would have removed it too.",
          "8.33ms 的窗口塞不下一次 stop-the-world。去掉托管运行时就是那个机制，换 C++ 也照样能去掉。")),
        (("Threading at a scale you can check", "并发规模大到需要有人替你查"),
         ("1,943 spawn sites across 426 files, with Send and Sync doing the checking, plus 4,734 "
          "deterministic-scheduler tests and 215 of them re-run across seeds. This is the part C++ does "
          "not match.",
          "426 个文件里 1,943 处 spawn，靠 Send 和 Sync 把关，再加 4,734 个确定性调度器测试，其中 215 个跨 seed "
          "反复跑。这块 C++ 跟不上。")),
        (("unsafe with an address", "unsafe 有固定住址"),
         ("776 of 1,111 blocks live in eleven gpui* crates and 728 in two OS backends. Audit that surface "
          "and you have audited the surface.",
          "1,111 个块里 776 个住在十一个 gpui* crate，728 个在两个 OS 后端。审完那一片，就是审完了全部。")),
        (("A sandbox for the thing that killed Atom", "给当年拖垮 Atom 的那部分套上沙箱"),
         ("extensions run as WebAssembly under wasmtime 36 against 77 versioned .wit files, instead of "
          "in-process script.",
          "插件跑成 WebAssembly，宿主 wasmtime 36，对着 77 个带版本的 .wit 文件，而不是进程内脚本。")),
    ],
    "nobuys": [
        (("Credit for the frame rate", "帧率的功劳"),
         ("that belongs to compiled native code and to a renderer Zed controls. Sublime Text made the "
          "point in C++ before Rust was a candidate.",
          "那份功劳属于编译型原生代码和一个 Zed 自己控制的渲染器。Sublime Text 在 Rust 还不是候选之前就用 C++ "
          "证明过了。")),
        (("Memory safety relative to what they left", "相对他们离开的东西谈内存安全"),
         ("Atom was JavaScript. The baseline was already safe, so the safety gain is against the C++ "
          "alternative, not against the incumbent.",
          "Atom 是 JavaScript，基线本来就安全。所以安全上的收益是相对 C++ 那个替代方案，不是相对原来那个。")),
        (("Escape from C at the parser", "在解析器那里摆脱 C"),
         ("24 tree-sitter packages and 47 -sys crates compile in, and one grammar is pinned to a fork for "
          "a buffer-overflow fix.",
          "24 个 tree-sitter 包和 47 个 -sys crate 会编进来，而且有一个语法被钉在带缓冲区溢出修复的 fork 上。")),
        (("A GUI framework", "一套 GUI 框架"),
         ("in 2021 Rust had none that held this budget. 127,694 lines and 4,050 lines of shaders are the "
          "invoice for that gap.",
          "2021 年的 Rust 没有能撑住这个预算的框架。127,694 行代码加 4,050 行 shader 就是这个缺口的账单。")),
    ],

    "precedents": [
        {"name": "Microsoft · VS Code", "outcome": "STAYED",
         "body": ("The same product category, the same Electron baseline, the opposite decision. Their "
                  "native text buffer attempt got reverted: 'TL;DR: We tried. It didn't work out for us' "
                  "— converting between the native representation and V8 ate the gain, and a better "
                  "TypeScript data structure fixed it. Perceived speed came from extension-host isolation, "
                  "lazy activation, virtualised lists and V8 snapshots. Architecture carried the product, "
                  "in the incumbent language.",
                  "同一个产品品类、同一条 Electron 基线、相反的决定。他们试过原生文本缓冲，后来回退了："
                  "'TL;DR: We tried. It didn't work out for us'——原生表示和 V8 之间的转换把收益吃掉了，最后"
                  "靠一个更好的 TypeScript 数据结构解决。用户感知的速度来自扩展宿主隔离、懒激活、虚拟化列表和 "
                  "V8 快照。是架构撑起了产品，语言没换。"),
         "match": ("code editor, Electron baseline, perceived-speed objective — the exact counterfactual "
                   "for stay-electron",
                   "代码编辑器、Electron 基线、以感知速度为目标——正好是 stay-electron 的对照"),
         "mismatch": ("VS Code never adopted a per-frame deadline, so it was never held to Zed's "
                      "requirement",
                      "VS Code 从来没接受逐帧截止时间这个约束，所以从没被按 Zed 的需求要求过"),
         "regime": "first-party engineering blog; 2018 buffer verdict, 2017 ripgrep adoption",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "Amazon · Prime Video living-room UI", "outcome": "MIGRATED",
         "body": ("A steady-60fps goal met by putting a Rust and WASM core under a React UI. 37K lines of "
                  "Rust after about a year; the WASM VM added up to 7.5MB while saving 30MB of JS heap. "
                  "The business logic stayed JavaScript because the seam was coarse enough to hold. This "
                  "is the hybrid option Zed did not take, working, on constrained hardware.",
                  "目标是稳定 60fps，做法是在 React UI 下面塞一个 Rust + WASM 内核。一年左右写了 3.7 万行 Rust；"
                  "WASM 虚拟机最多加 7.5MB，同时省下 30MB 的 JS 堆。业务逻辑留在 JavaScript，因为那条接缝够粗，"
                  "撑得住。这就是 Zed 没走的那个混合方案，在受限硬件上跑通了。"),
         "match": ("a hard frame-rate goal on a UI, met by a native core under a scripting layer",
                   "UI 上有硬帧率目标，靠脚本层下面的原生内核达成"),
         "mismatch": ("a TV client SDK with a coarse seam; Zed's deadline sits in the paint path, which no "
                      "seam isolates",
                      "那是接缝很粗的电视客户端 SDK；Zed 的截止时间在绘制路径上，没有接缝能隔开"),
         "regime": "8,000+ device types, first-party", "source_label": "first-party · engineering blog",
         "url": "https://www.amazon.science/blog/how-prime-video-updates-its-app-for-more-than-8-000-device-types"},
        {"name": "Tauri on Linux · WebKitGTK", "outcome": "STAYED",
         "body": ("The 'just use the system webview' answer, audited. Tauri's own maintainers wrote that "
                  "they cannot fully recommend Tauri on Linux and that WebKitGTK is getting worse each "
                  "release; one app measured 40fps on WebKitGTK against 240fps after converting to "
                  "Electron. A smaller installer is not a frame budget. If the rendering engine is not "
                  "yours, neither is the deadline.",
                  "「直接用系统 webview」这个答案，被审过了。Tauri 自己的维护者写道，现阶段无法完全推荐在 Linux "
                  "上用 Tauri，WebKitGTK 每个版本都在变差；有个应用实测在 WebKitGTK 上 40fps，改成 Electron 后 "
                  "240fps。安装包更小不等于帧预算。渲染引擎不是你的，截止时间也就不是你的。"),
         "match": ("the cheap alternative to writing GPUI, on the same three-platform target",
                   "不写 GPUI 的那个便宜替代，目标平台也是同样三个"),
         "mismatch": ("Tauri is a Rust shell around someone else's renderer; GPUI is the renderer",
                      "Tauri 是包在别人渲染器外面的 Rust 外壳；GPUI 本身就是渲染器"),
         "regime": "maintainer statements and (N=1) app measurement",
         "source_label": "first-party maintainer · issue tracker",
         "url": "https://github.com/tauri-apps/tauri/discussions/8524"},
        {"name": "Alacritty · the fastest-terminal claim", "outcome": "MIGRATED",
         "body": ("A greenfield Rust plus OpenGL desktop app whose performance superlative failed audit. "
                  "Dan Luu measured its latency mid-pack and called throughput dumps 'as useless a "
                  "benchmark as I can think of'. GPU throughput is not input latency. The reason Zed's "
                  "claim survives the same audit is that its metric is defined in code and reported in "
                  "the shipped build.",
                  "一个全新写的 Rust + OpenGL 桌面应用，性能上的最高级形容词没过审计。Dan Luu 实测它的延迟只在"
                  "中游，还说吞吐量转储是「我能想到最没用的 benchmark」。GPU 吞吐不是输入延迟。Zed 的说法能过同一"
                  "道审计，是因为它的指标定义在代码里，而且发布版会报出来。"),
         "match": ("greenfield Rust GPU-rendered desktop app making a latency claim — the failure mode G1 "
                   "has to clear",
                   "全新写的 Rust GPU 渲染桌面应用，提延迟主张——G1 必须避开的正是这个失败模式"),
         "mismatch": ("Alacritty defined no metric and shipped no harness; Zed defines both at "
                      "bench_context.rs:62 and input_latency_ui.rs:327",
                      "Alacritty 没定义指标也没有脚手架；Zed 在 bench_context.rs:62 和 input_latency_ui.rs:327 "
                      "两处都定义了"),
         "regime": "third-party latency measurement, keypress-to-screen",
         "source_label": "third-party · independent measurement",
         "url": "https://danluu.com/term-latency/"},
    ],

    "path": [
        {"title": ("Write the deadline down before you name a language",
                   "先把截止时间写下来，再谈语言"),
         "body": ("Whoever wants the rewrite states the budget as a number and the percentile it must hold "
                  "at. Zed's version is one line: bench_context.rs:62. Put it in the code, wire a harness "
                  "that reports overruns, and give it a name in the shipped build the way "
                  "input_latency_ui.rs:327 does. If you cannot write the number down, stop here. You have "
                  "a preference, not a requirement, and no gate in this method will pass on a preference. "
                  "Nothing ships in this step.",
                  "想推重写的人先把预算写成一个数，并说清它要在哪个分位上守住。Zed 的版本就一行："
                  "bench_context.rs:62。把它放进代码，接一个会报超预算的脚手架，再像 input_latency_ui.rs:327 "
                  "那样在发布版里给它一个名字。写不出这个数就停在这里——你手上是偏好，不是需求，这套方法里没有哪道"
                  "门会为偏好放行。这一步不发任何东西。"),
         "owner": "whoever proposes the rewrite",
         "cost_range": ("1 week", "1 周"),
         "artifact": "a per-interaction budget in milliseconds with the percentile it must hold at, committed as a constant plus a harness that reports overruns against it",
         "acceptance": "the number is in the source and the harness prints overrun counts, as bench_context.rs:62 and input_latency_ui.rs:327 do",
         "stop": "stop if the budget cannot be written as a number and a percentile — that is a preference, not a requirement",
         "rollback": "measurement only; no product code changes"},
        {"title": ("Measure the stack you already have against it",
                   "先拿现有的栈去撞这个数"),
         "body": ("Instrument the current build and publish the histogram before proposing to replace it. "
                  "Split the misses by cause: collector pauses, layout, paint, main-thread I/O. VS Code's "
                  "record is the warning here — process isolation, lazy activation and virtualised lists "
                  "closed most of a similar gap without leaving TypeScript. If architecture inside the "
                  "incumbent stack gets you under the budget, stop, and take the cheap win. Only "
                  "instrumentation is added, so backing out is deleting it.",
                  "在提议替换之前，先给现有构建装上测量并把直方图发出来。把没达标的情况按原因拆开：GC 停顿、布局、"
                  "绘制、主线程 I/O。VS Code 的记录是这里的警告——扩展宿主隔离、懒激活、虚拟化列表，在没离开 "
                  "TypeScript 的情况下就补掉了类似的大半缺口。如果在原栈里改架构就能压进预算，那就停下，把这个便宜"
                  "的收益拿走。这一步只加测量，撤销就是删掉它。"),
         "owner": "the team that owns the current build",
         "cost_range": ("2–4 weeks", "2–4 周"),
         "artifact": "an input-to-frame histogram from the existing stack, with misses attributed to collector pauses, layout, paint and main-thread I/O",
         "acceptance": "the histogram shows the budget missed at the stated percentile and the causes are attributed, not guessed",
         "stop": "stop and take the cheap win if architecture changes inside the incumbent stack close the gap",
         "rollback": "delete the instrumentation"},
        {"title": ("Price the framework, not the application", "算框架的钱，别算应用的钱"),
         "body": ("Inventory what your target language does not supply and cost each piece. Zed's answer "
                  "was 127,694 lines across 235 files, 4,050 lines of shaders, eight GPU primitive types, "
                  "a glyph rasteriser and three platform backends holding 776 unsafe blocks. Renderer, "
                  "text shaping, IME, accessibility and windowing all belong on that list. If an existing "
                  "native toolkit covers them, adopt it and skip the framework entirely. The output is a "
                  "document, so there is nothing to revert.",
                  "把目标语言里没有的东西列出来，逐项估价。Zed 的答案是 235 个文件、127,694 行，4,050 行 shader，"
                  "八种 GPU 图元，一套字形栅格化，以及装着 776 个 unsafe 块的三个平台后端。渲染器、文本排版、IME、"
                  "无障碍、窗口管理都得进这张单子。如果现成的原生工具包覆盖得了，就采用它，框架整块跳过。产出是一份"
                  "文档，没有东西要回退。"),
         "owner": "whoever will maintain the framework",
         "cost_range": ("2 weeks", "2 周"),
         "artifact": "a written inventory of renderer, text shaping, IME, accessibility and platform windowing work the target ecosystem does not supply, with a line estimate for each",
         "acceptance": "every item has an owner and an estimate, and the total is compared against the same list in the strongest non-Rust native language",
         "stop": "adopt an existing native toolkit instead if it covers the inventory",
         "rollback": "a document; nothing to undo"},
        {"title": ("Name everything that has to stay compatible", "把所有必须保持兼容的东西点出来"),
         "body": ("Zed's delivery gate passed partly because Atom was archived rather than migrated. No "
                  "ABI, no data format, no extension ecosystem, no rollback anyone asked for. Write the "
                  "equivalent list for your product: public API, on-disk format, plugin surface, user "
                  "migration, and who owns each one. A long list with a product that must keep running "
                  "caps the scope at PARTIAL, whatever the frame budget says. The current product carries "
                  "on unchanged while this is written.",
                  "Zed 的交付门有一半是因为 Atom 被归档而不是迁移才过的：没有 ABI、没有数据格式、没有插件生态、"
                  "也没人要回滚。给你的产品写一份对应清单：公开 API、磁盘格式、插件面、用户迁移，以及每一项归谁。"
                  "清单很长而且旧产品必须继续跑，那不管帧预算怎么说，范围上限就是 PARTIAL。写这份东西的时候，现有"
                  "产品原样继续。"),
         "owner": "the product owner",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "a written list of the API, on-disk format, plugin surface and user-migration commitments a rewrite must preserve, with an owner against each",
         "acceptance": "each commitment has a named owner and a stated plan, or is explicitly dropped with sign-off",
         "stop": "cap the scope at PARTIAL if the list is long and the existing product must keep running",
         "rollback": "the current product continues unchanged"},
        {"title": ("Keep the budget instrumented after you ship",
                   "发出去之后，测量别拆"),
         "body": ("A deadline you stop measuring is a deadline you stop meeting. Zed keeps the histogram in "
                  "the product and flushes it through telemetry, which is why the requirement is still "
                  "checkable five years on. Treat a percentile drifting above budget across a release as a "
                  "regression with an owner, not as a cost of new features. The instrumentation is "
                  "additive, so removing it is the rollback.",
                  "不再测量的截止时间，就是不再达成的截止时间。Zed 把直方图留在产品里，通过 telemetry 上报，所以"
                  "五年后这个需求仍然可查。某个分位跨版本漂到预算之上，就当成有人负责的回归，不当成新功能的代价。"
                  "测量是加法，回滚就是把它删掉。"),
         "owner": "the team that shipped it",
         "cost_range": ("ongoing", "长期"),
         "artifact": "the shipped build reporting its own input-to-frame histogram, as crates/input_latency_ui does",
         "acceptance": "the stated percentile stays inside the budget across releases, and drift opens a regression with an owner",
         "stop": "treat a percentile above budget for one release as a regression, not as the price of a feature",
         "rollback": "remove the instrumentation; it is additive"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The frame budget is a compiled-native effect, not a Rust effect. C++ removes the "
                   "collector too, and Sublime Text shipped that answer first. The Rust-specific part is "
                   "narrower: the concurrency check and the contained unsafe surface.",
                   "帧预算是编译型原生的效果，不是 Rust 的效果。C++ 一样能去掉 GC，Sublime Text 还更早交付了这个"
                   "答案。属于 Rust 的那部分要窄得多：并发检查，和被圈住的 unsafe 面。"),
         "evidence": "D3, D12 · case-library.md Zed entry attribution note"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("The comparison people make is Zed against Atom. Atom was archived in January 2023 and "
                   "never got the optimisation programme VS Code ran. Measuring against an abandoned 2015 "
                   "Electron app flatters the result.",
                   "大家做的对比是 Zed 对 Atom。Atom 在 2023 年 1 月归档，从来没经历 VS Code 那套优化。拿一个 "
                   "2015 年的、已经放弃的 Electron 应用当基线，结果自然好看。"),
         "evidence": "GitHub API repos/atom/atom: archived=true, last push 2023-01-03"},
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("No published decomposition splits one 8.33ms frame into layout, glyph raster, scene "
                   "build, GPU submit and compositor wait. D2 is UNKNOWN inside an APPROVE, and the report "
                   "says so rather than filling the gap.",
                   "没有公开材料把一帧 8.33ms 拆成布局、字形栅格化、场景构建、GPU 提交和合成器等待。D2 在 "
                   "APPROVE 里仍是 UNKNOWN，报告照实写，没有拿估算把缺口补上。"),
         "evidence": "D2 UNKNOWN · docs/src/performance.md holds the tooling, not the artifact"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("127,694 lines of UI framework, 4,050 lines of shaders and 776 unsafe blocks of platform "
                   "glue are the price of a 2021 Rust GUI ecosystem that could not hold the budget. That "
                   "line item rarely appears in the retelling.",
                   "127,694 行 UI 框架、4,050 行 shader、776 个平台胶水的 unsafe 块，是 2021 年 Rust GUI 生态撑"
                   "不住这个预算要付的钱。复述这个故事的时候，这一项通常不出现。"),
         "evidence": "D9 · crates/gpui and crates/gpui_* · 127,694 lines / 235 files"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The scope shipped and stayed shipped. 39,386 commits, 1,275 releases, three platforms, "
                   "and 624 commits in the last 30 days. This is not a stalled rewrite.",
                   "范围交付了，而且一直在交付。39,386 次提交、1,275 个 release、三个平台，最近 30 天 624 次提交。"
                   "这不是一场停摆的重写。"),
         "evidence": "GitHub API repos/zed-industries/zed · commits and releases"},
    ],
    "staying_checks": [
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying was not a stable option, it was an ending one. GitHub archived Atom and the "
                   "last push was 2023-01-03. Keeping a product on a stack whose vendor is winding it down "
                   "is a cost, and the report counts it.",
                   "留下来不是一个稳定选项，是一个正在结束的选项。GitHub 把 Atom 归档了，最后一次推送是 "
                   "2023-01-03。把产品留在一个上游正在收尾的栈上，本身就是成本，报告把它算进来了。"),
         "evidence": "GitHub API repos/atom/atom: archived=true, pushed_at 2023-01-03"},
        {"name": ("Endless optimise-first", "无限期的「先优化」"), "state": "HIT",
         "claim": ("Optimising a DOM against a per-frame deadline has no end state an application team can "
                   "reach, because layout and paint belong to the engine. Tauri's Linux record shows what "
                   "happens when the renderer is not yours.",
                   "拿 DOM 去撞逐帧截止时间，应用团队达不到终点，因为布局和绘制归引擎。Tauri 在 Linux 上的记录"
                   "说明了渲染器不归自己时会发生什么。"),
         "evidence": "D10 · Tauri maintainer statements; one app 40fps on WebKitGTK vs 240fps on Electron"},
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("VS Code is the funded Electron counterfactual and it won a market. The report keeps it "
                   "retained with STRONG evidence and says plainly that it reaches everything except a "
                   "per-frame deadline.",
                   "VS Code 就是那个有人投钱的 Electron 对照，而且它赢下了市场。报告把它保留为 STRONG 证据，并直说"
                   "它除了逐帧截止时间之外什么都达得到。"),
         "evidence": "option stay-electron, evidence_strength STRONG · D10"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report grants that a collector pause inside an 8.33ms window is a mechanism, not a "
                   "talking point, and grades D3 as SUPPORTS for both native options.",
                   "报告承认 8.33ms 窗口里的一次 GC 停顿是机制，不是说辞，并把 D3 给两个原生方案都记成 SUPPORTS。"),
         "evidence": "D3 SUPPORTS · rust-gpui, cpp-native"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The C surface is disclosed on the Rust side: 24 tree-sitter packages, 47 -sys crates, "
                   "and a grammar pinned to a fork for a buffer-overflow fix at Cargo.toml:856.",
                   "Rust 这边的 C 面被披露了：24 个 tree-sitter 包、47 个 -sys crate，还有 Cargo.toml:856 那个为"
                   "缓冲区溢出修复而钉住的语法 fork。"),
         "evidence": "D6 · Cargo.toml:856 · Cargo.lock package inventory"},
    ],

    "gaps": [
        (("A published decomposition of one 8.33ms frame",
          "一份公开的单帧 8.33ms 时间拆解"),
         ("It would show how much of the budget Zed's own code owns versus the driver, the compositor and "
          "the GPU. Until it exists D2 stays UNKNOWN, and the frame-rate claim rests on construction "
          "rather than on a share.",
          "它能说明这份预算里 Zed 自己的代码占多少，驱动、合成器和 GPU 各占多少。在它出现之前 D2 保持 UNKNOWN，"
          "帧率这条只能靠结构论证，拿不出占比。")),
        (("A boot decomposition for both stacks", "两个栈各自的启动时间拆解"),
         ("Atom's loudest complaint was startup and D5 is UNKNOWN because nobody has split boot into "
          "runtime init, I/O and useful work. This is the cheapest missing measurement in the case.",
          "Atom 被骂最狠的是启动，而 D5 记 UNKNOWN，因为没人把启动拆成运行时初始化、I/O 和有效工作。这是本案里"
          "最便宜的一处缺失测量。")),
        (("A steady-state footprint comparison against a current Electron editor",
          "跟当代 Electron 编辑器的稳态占用对比"),
         ("D4 cannot move without it. Installer size is not resident memory, and on Windows the system "
          "webview is Chromium anyway.",
          "没有它 D4 动不了。安装包大小不是常驻内存，而且在 Windows 上系统 webview 本来就是 Chromium。")),
        (("What the C++ version would have cost", "C++ 版本会花多少"),
         ("No counterfactual build exists, so G2's attribution stays structural. A Qt or Skia estimate "
          "against the 127,694-line framework inventory would sharpen it either way.",
          "不存在对照实现，所以 G2 的归因只能停在结构层面。拿 Qt 或 Skia 对着那份 127,694 行的框架清单估一遍，"
          "两个方向上都会让它更清楚。")),
    ],

    "assumptions": [
        "The shallow clone at commit 90d024b88abc91264d9a0ad260eb4f365fa695c3 represents the shipped tree. Dependency sources are not vendored in it, so every claim about C dependencies rests on Cargo.lock package identity rather than on counted lines.",
        "The proposal assessed is the one the team actually took in 2021 — rebuild the editor in Rust on a purpose-built GPU UI framework — read from the oldest commit in this repository, since no design RFC was published.",
        "Counts of `unsafe {` are occurrences of that literal token with comments included; a filter that drops comment-leading lines moves 1,111 to 1,108. All line counts are physical lines including blanks and comments, on the same basis for every comparison in the report.",
        "The clone's working tree was emptied by a concurrent process during the session (core.sparseCheckout was set to true by something outside this analysis). The tree was re-materialised read-only with `git archive HEAD | tar -x` into a scratch directory; HEAD was unchanged and every figure reproduced there.",
    ],
    "objective": {
        "driver": "a per-frame input deadline on a desktop code editor",
        "requirement": "hold input-to-frame latency inside an 8.33ms budget for a code editor on three desktop platforms, with no previous product that has to keep running",
        "baseline": "Atom on Electron and CoffeeScript/JavaScript: a collected runtime inside a DOM whose layout and paint the application team does not own",
        "target": "the 120fps budget stated at crates/gpui/src/app/bench_context.rs:62 and reported to users at crates/input_latency_ui/src/input_latency_ui.rs:327",
    },
    "repository": {
        "path": "https://github.com/zed-industries/zed",
        "commit": "90d024b88abc91264d9a0ad260eb4f365fa695c3",
        "scope": "the editor and its UI framework as one target; crates/gpui and the ten sibling gpui_* crates are the seam under examination",
        "sampling": "shallow clone, 4,235 tracked files; crates/ (242 crate directories), docs/, tooling/, .github/ and the workspace manifests measured; Cargo.lock read for dependency identity; GitHub API used for history and release facts because the clone has no usable log; no build, test, benchmark or profiling run against the project",
    },
    "user_supplied_facts": [],

    "method_title": (
        "zed-industries/zed at 90d024b · static read-only analysis · why-not-rust method 2.0",
        "zed-industries/zed @ 90d024b · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/zed-industries/zed at commit 90d024b88abc91264d9a0ad260eb4f365fa695c3, "
        "shallow clone, 4,235 tracked files, HEAD dated 2026-08-02. Scope: the editor and its UI framework "
        "assessed as one target, retrospectively — the decision under review is the one taken in 2021, not "
        "a proposal. Sampling: 1,539,358 lines of Rust across 1,926 files. On a general-purpose-source "
        "basis that is 1,539,358 of 1,556,319 lines, or 98.9%, the remainder being 13,682 lines of Python, "
        "1,186 of JavaScript, 1,137 of PowerShell, 835 of shell, 116 of TypeScript and one 5-line "
        "Objective-C bridging header at crates/media/src/bindings.h. Shader source is counted separately: "
        "4,050 lines of Metal, HLSL and WGSL. Tree-sitter query files (.scm, 9,140 lines) and WIT interface "
        "files (.wit, 4,017 lines) are excluded from that basis as neither is a general-purpose language. "
        "The eleven gpui* crates are 127,694 lines across 235 files. 230,346 lines across 121 files sit in "
        "test or fixture paths, and 784 inline #[cfg(test)] modules are not separated out, so the "
        "product-code figure is lower than 1.3M; the largest single .rs file in the tree is a test file, "
        "crates/editor/src/editor_tests.rs at 42,718 lines, and the second largest is a 21,343-line eval "
        "fixture. 262,512 lines belong to the 2024-26 agent crates. 1,111 occurrences of `unsafe {` were "
        "counted across *.rs with comments included; 776 are in crates/gpui and crates/gpui_*, 728 of "
        "those in the macOS and Windows backends, and 335 lie outside the gpui family. Cargo.lock lists "
        "1,862 packages including 47 -sys crates and 24 tree-sitter packages. History, release and "
        "archive facts come from the GitHub API on 2026-08-02 because the clone is shallow: 39,386 "
        "commits, oldest b400449 on 2021-02-20, v0.1 on 2021-06-08, 1,275 releases to v1.13.1 on "
        "2026-07-29, 9,444 commits in the last 365 days, 624 in the last 30; the contributors endpoint "
        "reports 482 and caps at 500. No build, test, benchmark, profiler or network call was run against "
        "the project. Objective: no design RFC was published, so the assessment takes the decision visible "
        "in the oldest commit — rebuild the editor in Rust on a purpose-built GPU UI framework. "
        "User-supplied facts: none. No Amdahl calculation appears: a deadline is not a speedup ratio, and "
        "no published frame decomposition supplies a share, so D2 and D5 are recorded UNKNOWN rather than "
        "estimated. The verdict turns on G1, which is measured in the source, and G4, which is measured in "
        "the release record; G2 passes on structural evidence with the attribution split stated, because "
        "no C++ counterfactual exists. Instruction-like text was found in scanned content: "
        "crates/agent/src/tools/skill_tool.rs:396 contains the string 'Ignore previous instructions.' "
        "inside a prompt-injection test fixture, and .agents/skills/ plus .factory/skills/ hold "
        "assistant-directed SKILL.md files. All of it was treated as data and changed no verdict, gate, "
        "path or number. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/zed-industries/zed，commit 90d024b88abc91264d9a0ad260eb4f365fa695c3，shallow clone，"
        "4,235 个纳管文件，HEAD 日期 2026-08-02。范围：编辑器和它的 UI 框架作为一个目标，回溯评估——被评的是 2021 "
        "年已经做出的决定，不是一份提案。采样：1,539,358 行 Rust，分布在 1,926 个文件。按通用编程语言口径，是 "
        "1,556,319 行里的 1,539,358 行，占 98.9%；其余是 13,682 行 Python、1,186 行 JavaScript、1,137 行 "
        "PowerShell、835 行 shell、116 行 TypeScript，以及 crates/media/src/bindings.h 那个 5 行的 Objective-C "
        "桥接头。shader 单独计：Metal、HLSL、WGSL 合计 4,050 行。tree-sitter 查询文件（.scm，9,140 行）和 WIT "
        "接口文件（.wit，4,017 行）不计入该口径，两者都不是通用语言。十一个 gpui* crate 共 235 个文件、127,694 行。"
        "有 121 个文件、230,346 行落在测试或 fixture 路径里，另有 784 个内联 #[cfg(test)] 模块没有拆出来，所以真正"
        "的产品代码低于 130 万行；树里最大的单个 .rs 是测试文件 crates/editor/src/editor_tests.rs，42,718 行，第二"
        "大的是一个 21,343 行的 eval fixture。2024-26 年的 agent 相关 crate 占 262,512 行。`unsafe {` 在 *.rs 里"
        "出现 1,111 次，未排除注释；其中 776 次在 crates/gpui 和 crates/gpui_* 里，728 次集中在 macOS 和 Windows "
        "后端，另有 335 次在 gpui 家族之外。Cargo.lock 列出 1,862 个包，含 47 个 -sys crate 和 24 个 tree-sitter "
        "包。历史、发布和归档信息取自 2026-08-02 的 GitHub API，因为 clone 是浅的：39,386 次提交，最早的是 "
        "2021-02-20 的 b400449，v0.1 在 2021-06-08，到 2026-07-29 的 v1.13.1 共 1,275 个 release，最近 365 天 "
        "9,444 次提交，最近 30 天 624 次；contributors 接口报 482，上限是 500。没有对项目做过任何构建、测试、"
        "基准、profiling 或网络调用。目标：没有公开的设计 RFC，所以按最早那个 commit 里能看到的决定来评——用 Rust "
        "重建编辑器，配一套专门写的 GPU UI 框架。用户提供的事实：无。本报告没有 Amdahl 计算：截止时间不是加速比，"
        "而且没有公开的单帧拆解能给出占比，所以 D2 和 D5 记 UNKNOWN，不做估算。结论落在 G1 和 G4 上，前者在源码里"
        "可量，后者在发布记录里可量；G2 是靠结构性证据过的，并把归因拆开写明，因为不存在 C++ 的对照实现。扫描到"
        "了指令样式的内容：crates/agent/src/tools/skill_tool.rs:396 在一个 prompt 注入测试 fixture 里含有 "
        "'Ignore previous instructions.' 这串文字，.agents/skills/ 和 .factory/skills/ 下还有面向助手的 SKILL.md。"
        "全部按数据处理，没有改动任何结论、门、路径或数字。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 90d024b · GitHub API for history · no build, benchmark or profiler run",
        "公开仓库 · 在 commit 90d024b 上做静态分析 · 历史信息取自 GitHub API · 未做构建、基准或 profiling",
    ),
}
