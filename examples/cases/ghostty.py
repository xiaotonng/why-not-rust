"""ghostty-org/ghostty — the Mac-native part is 32,377 lines of Swift.

Repository facts were measured read-only on the shallow clone named in
`repository`. Release, tag and advisory history came from the GitHub API,
because the clone is `--depth 1`.
"""

CASE = {
    "slug": "ghostty",
    "project_name": "ghostty-org/ghostty",
    "project_desc": (
        "Zig · terminal emulator · 311,038 lines of Zig, 32,377 lines of Swift in the macOS app, "
        "995 lines of its own C++",
        "Zig · 终端模拟器 · Zig 311,038 行，macOS 应用里 Swift 32,377 行，自有 C++ 995 行",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · a Zig core with a Swift frontend, parsing untrusted VT input from "
        "every process the user runs",
        "原生桌面 GUI · Zig 内核配 Swift 前端，解析用户启动的每个进程送来的不可信 VT 输入",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "stay-safe-build",
    "scope_chip": (
        "keep Zig; price the safety-checked build first",
        "留在 Zig；先把带安全检查的构建代价算出来",
    ),
    "scope_sub": (
        "stay in Zig — the cheap fix has not been priced yet",
        "留在 Zig——便宜那条路的代价还没人算过",
    ),

    "why": (
        "Ghostty ships its tagged release with Zig's safety checks off, and PACKAGING.md says the "
        "maintainer would rather not. So the memory-safety requirement stands. What fails is the "
        "price. A safety-checked macOS build is already codesigned, notarized and published on the "
        "tip channel every commit to main. Nobody has published what it costs, and src/benchmark/ "
        "already holds the harnesses that would say. Meanwhile the quality people praise Ghostty "
        "for is 32,377 lines of Swift, and all five of its published advisories are logic bugs "
        "Rust would not have caught.",
        "Ghostty 的正式发布版关掉了 Zig 的安全检查，PACKAGING.md 里作者自己写了他并不情愿。所以内存安全"
        "这个需求是立得住的。倒下的是价格这一环。带安全检查的 macOS 构建早就在跑：main 每有一次提交，它"
        "都会被签名、公证、发到 tip 通道。可没人公布过它的代价，而 src/benchmark/ 里就摆着能算出这个数的"
        "那套 harness。另一边，大家真正称赞 Ghostty 的那部分是 32,377 行 Swift，而它公开的五个安全公告"
        "全是逻辑缺陷，Rust 一个也拦不住。",
    ),
    "trigger": (
        "Conditional on two measurements that do not exist. Publish the ReleaseFast-versus-ReleaseSafe "
        "cost on src/benchmark's VT harnesses, and classify one release cycle of AFL++ crashes into "
        "spatial, temporal and logic buckets. If the safe build turns out unaffordable and the "
        "temporal bucket is not empty, the VT extraction behind the existing 185-symbol C ABI becomes "
        "the live question.",
        "结论挂在两份还不存在的测量上。第一份：在 src/benchmark 的 VT harness 上把 ReleaseFast 和 "
        "ReleaseSafe 的代价跑出来公布。第二份：把一个发布周期内 AFL++ 找到的崩溃分成空间类、时间类和逻辑"
        "类。如果安全构建确实付不起，而时间类那一桶不是空的，那么在现成的 185 个符号 C ABI 后面抽出 VT "
        "引擎，就成了真问题。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("The shipped release has bounds and overflow checks disabled.",
                           "发布版本关掉了边界检查和溢出检查。"),
         "name": "requirement",
         "evidence": "The tagged release is built -Doptimize=ReleaseFast (.github/workflows/release-tag.yml:177), which disables Zig's bounds, overflow and null checks. PACKAGING.md:111 states the preference for a safe build and calls the safe build too slow. src/terminal is 140,441 lines of Zig terminating VT sequences from arbitrary child processes. The requirement is stated by the project itself."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Rust's ownership model reaches use-after-free; ReleaseSafe does not.",
                           "Rust 的所有权模型管得到 use-after-free，ReleaseSafe 管不到。"),
         "name": "rust-specific causality",
         "evidence": "Zig's ReleaseSafe restores spatial checks but has no ownership model, so use-after-free and double-free survive it. Rust's safe subset removes both classes from code it replaces. Bun ported roughly 535k lines of Zig to Rust and named exactly that stream of bugs as the motive. The mechanism holds. Its reach does not extend to the 32,377-line Swift frontend or to the 995 lines of C++."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("The one-flag alternative already ships. Nobody priced it.",
                           "改一个开关的方案已经在发布了，没人算过它的代价。"),
         "name": "economics and smallest sufficient option",
         "evidence": ".github/workflows/release-tip.yml:929 builds the macOS app with -Doptimize=ReleaseSafe, then codesigns, notarizes and publishes it as ghostty-macos-universal-debug-fast.zip. src/benchmark/ ships 15 harnesses including TerminalParser, TerminalStream and OscParser behind -Demit-bench. No published measurement compares the two modes. A 213,626-line non-test rewrite cannot be the smallest sufficient step while a build flag is unpriced."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("275 exported C symbols, two frontends, and no dual-run plan.",
                           "275 个导出的 C 符号、两套前端，没有并跑方案。"),
         "name": "delivery and reversibility",
         "evidence": "90 export fn ghostty_* symbols plus 185 @export names in src/lib_vt.zig, with no overlap, make 275 exported C symbols. A 32,377-line Swift app and a 28,408-line GTK frontend compile against them. 97,412 lines sit inside Zig test blocks and do not port. 68.8% of 16,557 commits on the default branch come from one person. No dual-run or rollback plan exists for any of it."},
    ],

    "tiles": [
        (("Zig, minus inline tests", "Zig，扣掉内联测试"), "213,626", ("lines", "行"),
         ("755 tracked .zig files; 97,412 lines sit inside test blocks",
          "版本库内 755 个 .zig 文件；其中 97,412 行在 test 块里")),
        (("Swift in the macOS app", "macOS 应用里的 Swift"), "32,377", ("lines", "行"),
         ("macos/Sources · 160 files · 67 import AppKit, 63 import SwiftUI",
          "macos/Sources · 160 个文件 · 67 个 import AppKit，63 个 import SwiftUI")),
        (("Ghostty's own C++", "Ghostty 自己的 C++"), "995", ("lines", "行"),
         ("src/simd/*.cpp · 4 files · portable SIMD via Google Highway",
          "src/simd/*.cpp · 4 个文件 · 靠 Google Highway 做可移植 SIMD")),
        (("Published advisories caused by memory unsafety", "由内存不安全导致的公开公告"),
         "0", ("of 5", "／5"),
         ("CWE-78, CWE-94, CWE-284, an fd leak, an escalation vector",
          "CWE-78、CWE-94、CWE-284、一个 fd 泄漏、一条提权路径")),
        (("Exported C symbols the frontends link", "前端链接的导出 C 符号"), "275", ("symbols", "个"),
         ("90 export fn ghostty_* + 185 @export in src/lib_vt.zig",
          "90 个 export fn ghostty_* 加 src/lib_vt.zig 里 185 个 @export")),
        (("Published measurements of the safe build's cost", "关于安全构建代价的公开测量"),
         "0", ("published", "份"),
         ("ReleaseSafe is already codesigned, notarized and shipped on tip",
          "ReleaseSafe 早已签名、公证，并在 tip 通道发布")),
    ],

    "options_sub": (
        "Every option answers one requirement: remove or downgrade the memory-unsafety class on "
        "Ghostty's VT parsing path, without giving up the native macOS behaviour or the libghostty "
        "C ABI.",
        "所有方案对着同一个需求：把 Ghostty 的 VT 解析路径上的内存不安全缺陷类消除或降级，同时不放弃 "
        "macOS 的原生行为，也不动 libghostty 的 C ABI。",
    ),
    "options": [
        {"id": "stay-safe-build", "name": ("Price ReleaseSafe, then ship it", "先算 ReleaseSafe 的代价，再发布它"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("spatial class becomes a deterministic panic across all 213,626 lines",
                              "全部 213,626 行上，空间类缺陷变成确定的 panic"),
         "one_time_cost": "one benchmark run on existing harnesses; one build-flag change",
         "recurring_cost": "whatever throughput the safe build costs, once measured",
         "cost_cell": ("one benchmark run; one flag", "跑一次基准；改一个开关"),
         "time_to_value": ("days", "数天"),
         "compatibility": "identical ABI and behaviour; failure mode changes from corruption to panic",
         "compat_cell": ("identical ABI · revert one flag", "ABI 不变 · 回退一个开关"),
         "reversibility": "revert one build flag",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · already built, signed and shipping on tip",
                  "推荐 · 已经构建、签名，并在 tip 通道发布"),
         "reason": "Reaches the whole Zig surface for the cost of a measurement, and the artifact it produces already exists in CI. Its cost is the one number nobody has published."},
        {"id": "stay-fuzz", "name": ("Keep the AFL++ programme as it is", "AFL++ 那套照现在继续跑"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("finds defects in the VT path; eliminates no class",
                              "能在 VT 路径上找出缺陷；消除不了任何缺陷类"),
         "one_time_cost": "none new; three harnesses already exist",
         "recurring_cost": "existing maintainer fuzzing and triage time",
         "cost_cell": ("none new; existing triage time", "无新增；用现有的排查时间"),
         "time_to_value": ("continuous", "持续产出"),
         "compatibility": "native", "compat_cell": ("native · nothing to roll back", "原生 · 没什么要回滚"),
         "reversibility": "n/a",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded counterfactual any Rust claim must beat",
                  "保留 · 任何 Rust 主张都得先赢过这条已投入的对照"),
         "reason": "Three AFL++ targets over 4,001 committed corpus files plus 3,524 inline test blocks are shipping work, not a hypothetical. Fuzzing finds bugs; it does not remove the class."},
        {"id": "rust-vt-extract", "name": ("Rust VT engine behind the existing C ABI",
                                           "在现成的 C ABI 后面换一个 Rust 的 VT 引擎"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("both classes removed on the VT path; frontends unchanged",
                              "VT 路径上两类缺陷都消失；前端不动"),
         "one_time_cost": "66,281 non-test lines of src/terminal plus 2,579 test blocks to re-express",
         "recurring_cost": "a Rust toolchain in a build that currently needs only Zig",
         "cost_cell": ("66,281 lines; a second toolchain", "66,281 行；多一套工具链"),
         "time_to_value": ("months to years", "数月到数年"),
         "compatibility": "185 libghostty-vt symbols must stay byte-compatible",
         "compat_cell": ("same C ABI · dual-run possible", "C ABI 不变 · 可以并跑"),
         "reversibility": "keep both engines behind the ABI",
         "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the only Rust scope with a seam already built for it",
                  "保留 · 唯一有现成接缝的 Rust 范围"),
         "reason": "The seam is real and was designed as a C ABI. The benefit is unquantified because nobody has classified what AFL++ actually finds in src/terminal."},
        {"id": "rust-core", "name": ("Rewrite the Zig core in Rust, keep Swift",
                                     "用 Rust 重写 Zig 内核，Swift 保留"),
         "implementation": "rust", "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("both classes removed in Zig; Swift, C++ and simdutf untouched",
                              "Zig 里两类缺陷消失；Swift、C++、simdutf 一点不动"),
         "one_time_cost": "213,626 non-test lines, plus 97,412 lines of Zig tests that do not port",
         "recurring_cost": "re-owning the build graph for 22 pkg/ C dependency wrappers",
         "cost_cell": ("213,626 lines; a new build graph", "213,626 行；一套新的构建图"),
         "time_to_value": ("years", "数年"),
         "compatibility": "275 exported C symbols, a Swift app and a GTK frontend",
         "compat_cell": ("whole C ABI · no rollback", "整套 C ABI · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G3 against a build flag and G4 against 275 symbols",
                  "排除 · G3 输给一个构建开关，G4 输给 275 个符号"),
         "reason": "Pays a full rewrite for a class that a build flag downgrades and a smaller extraction removes outright at the place it matters most."},
        {"id": "rust-everything", "name": ("Rewrite the whole app in Rust, UI included",
                                           "整个应用用 Rust 重写，UI 也算上"),
         "implementation": "rust", "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("one language; loses the AppKit and SwiftUI behaviour",
                              "统一成一门语言；代价是丢掉 AppKit 和 SwiftUI 的行为"),
         "one_time_cost": "213,626 lines of Zig plus 32,377 lines of Swift and a GUI framework",
         "recurring_cost": "owning a macOS GUI layer that Apple's frameworks currently own",
         "cost_cell": ("246,003 lines; plus a GUI framework", "246,003 行；再加一套 GUI 框架"),
         "time_to_value": ("years", "数年"),
         "compatibility": "AppleScript, App Intents, native tabs and four titlebar styles",
         "compat_cell": ("loses platform integration · no rollback", "丢掉平台集成 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · trades the product's most-praised layer for language uniformity",
                  "排除 · 用产品最受称赞的那一层去换语言统一"),
         "reason": "Zed had to build GPUI because no Rust GUI framework met its bar. Ghostty avoided that problem by writing the UI in the platform's own language."},
        {"id": "adopt-rust-terminal", "name": ("Use a terminal already written in Rust",
                                               "改用一个已经用 Rust 写好的终端"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for that user; a different product",
                              "对那位用户来说缺陷类消失了；但换了个产品"),
         "one_time_cost": "per-user config migration",
         "recurring_cost": "a different feature and platform-integration surface",
         "cost_cell": ("per user; different feature set", "按用户计；功能集不同"),
         "time_to_value": ("an afternoon", "一个下午"),
         "compatibility": "no shared config, keybinds or platform integration",
         "compat_cell": ("nothing shared · switch back freely", "毫无共享 · 想换回来就换"),
         "reversibility": "reinstall", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · a user's decision, not the project's", "保留 · 这是用户的决定，不是项目的决定"),
         "reason": "Alacritty and WezTerm exist and are fine terminals. Neither is a plan for Ghostty's own code, and Alacritty's speed superlative failed independent audit."},
    ],

    "lenses_sub": (
        "Each state is evidence about named options. They are not a score and they do not add up. "
        "D2 stays UNKNOWN because no published profile says where Ghostty's frame time goes, and "
        "src/benchmark/ sitting unmeasured in the tree is why.",
        "每条状态都绑到具体方案，不是分数，也不能相加。D2 停在 UNKNOWN，因为没有公开 profile 说明 Ghostty "
        "的帧时间花在哪；src/benchmark/ 就在仓库里却没人跑，正是这条停住的原因。",
    ),
    "na_note": (
        "Two lenses are N/A. D4 fleet footprint: a terminal runs on one machine at a time, so there "
        "is no instance count to price. D5 startup shape: the Mac app is launched once per session "
        "and new windows open in-process.",
        "两条记为 N/A。D4 机队占用：终端一次只在一台机器上跑，没有实例数可以计价。D5 启动形态：Mac 应用一"
        "个会话只启动一次，新窗口在同一进程里开。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · stay-safe-build, rust options", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["stay-safe-build", "rust-vt-extract", "rust-core"],
         "claim": ("The unsafe surface is owned and easy to point at. src/terminal is 140,441 lines "
                   "of Zig, and it terminates VT sequences coming from whatever the user runs. The "
                   "tagged release builds all of it with safety checks off. The project wrote that "
                   "down itself.",
                   "不安全面是自有的，而且一指就到。src/terminal 是 140,441 行 Zig，它直接终结用户所跑程序"
                   "送来的 VT 序列。正式发布版把这些全部在关掉安全检查的模式下编译。这件事是项目自己写下"
                   "来的。"),
         "source": "PACKAGING.md:111 · .github/workflows/release-tag.yml:177 · src/terminal 140,441 lines across 141 files",
         "regime": "static inventory at commit 46edeee; build flags read from the release workflows",
         "caveat": "66,281 of those 140,441 lines fall outside test blocks; the rest are inline Zig tests that ship with the source.",
         "change_trigger": "A tagged release built ReleaseSafe would close the spatial half of this requirement without any language change."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-vt-extract, rust-core", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN",
         "option_ids": ["rust-vt-extract", "rust-core"],
         "claim": ("No Amdahl figure appears here. Nobody has published where Ghostty's frame time "
                   "goes, so there is no f worth defending. src/benchmark/ holds 15 harnesses that "
                   "could produce one. Using a line share as a stand-in for a time share would be a "
                   "method error.",
                   "这里不给 Amdahl 数。没人公开过 Ghostty 的帧时间花在哪里，所以没有站得住的 f。"
                   "src/benchmark/ 里有 15 个 harness 能跑出来。拿代码行数占比顶替时间占比，是方法错误。"),
         "source": "src/benchmark/ · 18 files including TerminalParser, TerminalStream, OscParser, CodepointWidth",
         "regime": "n/a — the measurement exists as code but no result is published",
         "caveat": "No proposal assessed here states a performance target either, so there is nothing to test a ceiling against.",
         "change_trigger": "A published run of -Demit-bench at ReleaseFast, split by harness, would make both the safe-build and extraction questions quantitative."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Neither Zig nor Rust has a collector or a JIT, so no option removes a runtime "
                   "mechanism from the frame budget. There is none to remove. Rendering goes through "
                   "Metal on macOS and OpenGL elsewhere, and that driver time is shared by every "
                   "option on the table.",
                   "Zig 和 Rust 都没有 collector，也没有 JIT，所以没有哪个方案能从帧预算里拿掉一个运行时"
                   "机制——本来就没有。渲染在 macOS 走 Metal，其他平台走 OpenGL，这部分驱动时间对所有方案"
                   "都一样。"),
         "source": "src/renderer/Metal.zig · src/renderer/OpenGL.zig · src/renderer/shaders/shaders.metal",
         "regime": "shipped renderer backends at this commit",
         "caveat": "Allocator behaviour differs between a Zig arena style and a Rust equivalent, but no trace here separates that from GPU and compositor time."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Ghostty is a desktop app. There is no instance count, no utilization figure and "
                   "no price per hour to multiply. Per-window memory is dominated by scrollback, "
                   "which the project already compresses.",
                   "Ghostty 是桌面应用。没有实例数、没有利用率、也没有每小时价格可乘。单窗口内存主要由回滚"
                   "缓冲决定，而项目已经在压缩它了。"),
         "source": "src/terminal/compress/ · desktop distribution", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("The Mac app launches once per session and opens new windows in-process. Launch "
                   "time is AppKit's, and no core-language change touches it. CLI actions exist under "
                   "src/cli, but they are not the product.",
                   "Mac 应用一个会话启动一次，新窗口在同一进程里开。启动时间归 AppKit，换内核语言碰不到"
                   "它。src/cli 下面确实有命令行动作，但那不是产品本身。"),
         "source": "macos/Sources/App/ · src/cli/ 27 files", "regime": "n/a",
         "caveat": "A libghostty consumer embedding the VT engine in a short-lived process would score this lens differently."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-vt-extract", "rust-core", "rust-everything"],
         "claim": ("Zig's ReleaseSafe restores bounds, overflow and null checks. It has no ownership "
                   "model, so use-after-free and double-free live through it. Rust's safe subset "
                   "removes both classes from code it replaces. Bun's team ported roughly 535k lines "
                   "of Zig and named that exact stream of bugs as the reason.",
                   "Zig 的 ReleaseSafe 会恢复边界、溢出和空值检查。但它没有所有权模型，所以 "
                   "use-after-free 和 double-free 照样活着。Rust 的 safe 子集在它替换掉的代码里把两类都"
                   "清掉。Bun 团队移植了约 53.5 万行 Zig，给出的理由正是这一串 bug。"),
         "source": "PACKAGING.md:111 · https://bun.com/blog/bun-in-rust · GHSA advisory list (5 entries)",
         "regime": "structural, at the VT input boundary; Bun figures are first-party and selected",
         "caveat": "Classified against D6's taxonomy, all five of Ghostty's published advisories are language-independent: CWE-78, CWE-94, CWE-284, an fd leak and an escalation vector. None is eliminated-by-construction by any option here.",
         "change_trigger": "AFL++ crashes in src/terminal classified as temporal-class would move this from mechanism to realized defect."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Ghostty already splits render, terminal I/O and app work across threads, and the "
                   "boundaries are few and coarse. No race incident appears in the advisory history. "
                   "fish shell called Send and Sync the killer feature of its own port, so this lens "
                   "could move — but it would need an incident, not an argument.",
                   "Ghostty 已经把渲染、终端 I/O 和应用逻辑分到不同线程，边界数量少而且粗。公告历史里没有"
                   "竞态事故。fish shell 说过 Send 和 Sync 是它那次移植真正的杀手特性，所以这一条不是不能"
                   "动；但要动它得靠一次事故，不是靠论证。"),
         "source": "src/renderer/Thread.zig · src/termio/ 9 files · https://fishshell.com/blog/rustport/",
         "regime": "existing thread design at this commit",
         "caveat": "Absence of a published race incident is weak evidence in both directions; nobody has audited Ghostty's thread boundaries in public."},
        {"id": "D8", "name": ("Distribution & embedding", "分发与嵌入"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Nothing about distribution is unmet. Ghostty ships a notarized universal macOS "
                   "binary with a Sparkle update channel, a GTK app on Linux, plus flatpak and snap. "
                   "libghostty-vt builds for Windows and for WebAssembly without libc. Rust could "
                   "reach all of those too.",
                   "分发上没有未满足的约束。Ghostty 发布经过公证的 macOS 通用二进制，带 Sparkle 更新通道；"
                   "Linux 上是 GTK 应用，另有 flatpak 和 snap。libghostty-vt 能编到 Windows，也能编到 "
                   "WebAssembly，且不依赖 libc。Rust 同样都能做到。"),
         "source": "flatpak/ · snap/ · dist/ · include/ghostty/vt/wasm.h · .github/workflows/release-tag.yml",
         "regime": "shipped distribution channels at this commit",
         "caveat": "The Zig build compiles the C dependencies itself through 22 pkg/ wrappers; reproducing that build graph is priced at D11, not here."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-vt-extract", "rust-core", "rust-everything"],
         "claim": ("Zig has not reached 1.0. build.zig.zon pins minimum_zig_version 0.16.0, and "
                   "breaking compiler changes between minor versions are the normal cost of that. "
                   "Rust has kept its language stable since 2015. This is the strongest point against "
                   "staying, and it has nothing to do with speed.",
                   "Zig 还没到 1.0。build.zig.zon 把 minimum_zig_version 钉在 0.16.0，小版本之间的破坏性"
                   "语言变更就是这么来的常态成本。Rust 从 2015 年起语言层面保持稳定。这是反对「不动」最强的"
                   "一条，而且跟速度无关。"),
         "source": "build.zig.zon:6 · pkg/macos 3,273 lines of Zig bindings to Apple frameworks across 56 files",
         "regime": "toolchain state at this commit",
         "caveat": "Cutting the other way: Zed had to build GPUI because no Rust GUI framework met its bar, and Ghostty's UI problem is solved in Swift instead. Ghostty also hand-wrote its Apple framework bindings, which a port would re-own.",
         "change_trigger": "A Zig 1.0 release with a stability guarantee would remove this lens's support for the Rust options."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-core, rust-everything", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG",
         "option_ids": ["rust-core", "rust-everything"],
         "claim": ("The compatibility surface is 275 exported C symbols across two APIs, plus 11,353 "
                   "lines of headers under include/. A 32,377-line Swift app and a 28,408-line GTK "
                   "frontend compile against them. The extraction option inherits that seam for free, "
                   "which is the whole reason it survives.",
                   "兼容面是两套 API 上 275 个导出 C 符号，加 include/ 下 11,353 行头文件。一个 32,377 行"
                   "的 Swift 应用和一个 28,408 行的 GTK 前端就是对着它们编译的。抽取方案能白拿这条接缝，"
                   "这也正是它没被排除的全部原因。"),
         "source": "90 export fn ghostty_* in src/ (71 in src/apprt/embedded.zig) · 185 @export names in src/lib_vt.zig · include/ 11,353 lines across 34 files",
         "regime": "static contract inventory at this commit; the two symbol sets do not overlap",
         "caveat": "libghostty-vt's API signatures are described as still in flux in README.md, so the 185 are less frozen than the 90 the Mac app depends on."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-core, rust-everything", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE",
         "option_ids": ["rust-core", "rust-everything"],
         "claim": ("213,626 non-test lines of Zig, and another 97,412 inside test blocks that do not "
                   "port. One person authored 68.8% of the 16,557 commits on the default branch. fish "
                   "shell estimated half a year for 57k lines of C++ and took about two. Ghostty's "
                   "non-test Zig is 3.7 times that.",
                   "非测试的 Zig 有 213,626 行，另有 97,412 行在 test 块里，而这些搬不过去。默认分支上 "
                   "16,557 次提交里，68.8% 出自一个人。fish shell 当年估计半年搞定 5.7 万行 C++，实际花了"
                   "约两年。Ghostty 的非测试 Zig 是那个体量的 3.7 倍。"),
         "source": "gh api repos/ghostty-org/ghostty/contributors --paginate · 425 contributors listed, 16,557 contributions, top author 11,397 · https://fishshell.com/blog/rustport/",
         "regime": "default-branch commit counts from the GitHub API; the contributors endpoint is capped and counts the default branch only",
         "caveat": "Single-author concentration is a risk for staying as well; it is recorded here because it bounds how fast any rewrite could be reviewed."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-safe-build, stay-fuzz", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["stay-safe-build", "stay-fuzz"],
         "claim": ("Two in-stack options are already running. A ReleaseSafe macOS build is "
                   "codesigned, notarized and published on the tip channel on every commit to main, "
                   "with its own Sentry dSYM upload. AFL++ covers three VT targets over 4,001 "
                   "committed corpus files. A Rust proposal has to beat both on one measurement.",
                   "栈内有两条路已经在跑。ReleaseSafe 的 macOS 构建每次 main 提交都会被签名、公证、发到 "
                   "tip 通道，还配了自己的 Sentry dSYM 上传。AFL++ 覆盖三个 VT 目标，语料库入库 4,001 个"
                   "文件。Rust 提案得在同一份测量上赢过这两条。"),
         "source": ".github/workflows/release-tip.yml:929, 1036, 1044 · test/fuzz-libghostty/ · 3 harnesses, 4,001 corpus files · 3,524 inline test blocks in src/",
         "regime": "current upstream CI and test practice at this commit",
         "caveat": "Neither removes the temporal class. ReleaseSafe downgrades spatial defects to panics; fuzzing raises detection. Elimination is what the Rust options offer and these do not."},
    ],

    "findings": [
        ("current",
         ("The Mac-native part is 32,377 lines of Swift", "Mac 原生那部分是 32,377 行 Swift"),
         ("160 Swift files sit under macos/Sources. 67 import AppKit, 63 import SwiftUI, 36 import "
          "Cocoa. Twelve files implement AppleScript support and twelve more implement App Intents. "
          "There are four separate titlebar implementations, two of them named for macOS versions. "
          "Whichever core language Ghostty had picked, this layer would still be Swift.",
          "macos/Sources 下有 160 个 Swift 文件。67 个 import AppKit，63 个 import SwiftUI，36 个 import "
          "Cocoa。十二个文件做 AppleScript 支持，另外十二个做 App Intents。标题栏有四套独立实现，其中两套"
          "按 macOS 版本命名。不管内核选哪门语言，这一层还是 Swift。"),
         "macos/Sources · 160 .swift files · 32,377 lines"),
        ("unknown",
         ("A safety-checked build already ships, and nobody priced it",
          "带安全检查的构建早就在发布，没人算过它的代价"),
         (".github/workflows/release-tip.yml:929 builds the macOS app with -Doptimize=ReleaseSafe. "
          "The job then codesigns it with production certificates, notarizes it through Apple, and "
          "publishes it as ghostty-macos-universal-debug-fast.zip on the tip release and to R2. "
          "PACKAGING.md:111 says the tagged build uses ReleaseFast because the safe build is "
          "currently too slow. No measurement backs that, and src/benchmark/ already contains the "
          "harnesses that would produce one.",
          ".github/workflows/release-tip.yml:929 用 -Doptimize=ReleaseSafe 构建 macOS 应用。同一个 job "
          "接着用生产证书签名、送 Apple 公证，然后以 ghostty-macos-universal-debug-fast.zip 的名字发到 "
          "tip release 和 R2。PACKAGING.md:111 写的是：正式版用 ReleaseFast，因为安全构建目前太慢。这句话"
          "背后没有测量，而 src/benchmark/ 里已经放着能跑出这个数的 harness。"),
         ".github/workflows/release-tip.yml:929 · release-tag.yml:177 · PACKAGING.md:111"),
        ("current",
         ("Zero of five published advisories are memory-safety bugs",
          "五个公开公告里，内存安全类是零"),
         ("The GHSA list holds five entries: command execution through control characters in paste "
          "and drag-and-drop (CWE-78), code injection through window title sequences (CWE-94), "
          "world-readable files from write_*_file actions (CWE-284), file descriptors leaked to the "
          "shell, and use as a privilege-escalation vector. Rust prevents none of them. This says "
          "nothing about whether Ghostty is safe; it says which class its shipped defects belong to.",
          "GHSA 列表里五条：粘贴与拖放中的控制字符导致命令执行（CWE-78）、窗口标题序列导致代码注入"
          "（CWE-94）、write_*_file 生成的文件全局可读（CWE-284）、文件描述符泄漏给 shell，以及被当作提权"
          "路径使用。Rust 一条都拦不住。这不能说明 Ghostty 安全不安全，只说明它已发生的缺陷属于哪一类。"),
         "gh api repos/ghostty-org/ghostty/security-advisories · 5 entries"),
        ("current",
         ("Ghostty writes C++ on purpose", "Ghostty 是有意去写 C++ 的"),
         ("Four .cpp files in src/simd total 995 lines, and they exist to use Google Highway's "
          "portable-SIMD templates plus simdutf. simdutf's amalgamation is vendored in-tree at "
          "52,566 lines; Highway itself is fetched at build time. Zig reaches them with a bare "
          "extern \"c\" fn declaration and keeps scalar Zig fallbacks behind -Dsimd. One language did "
          "not cover this problem and the project stopped pretending it did.",
          "src/simd 下四个 .cpp 一共 995 行，存在的理由是用 Google Highway 的可移植 SIMD 模板加 simdutf。"
          "simdutf 的合并源码入库 52,566 行；Highway 本身在构建时才拉。Zig 用一行 extern \"c\" fn 声明就"
          "接上了，同时在 -Dsimd 后面留着纯 Zig 的标量兜底。一门语言没能盖住这个问题，项目也就不再假装"
          "它能。"),
         "src/simd/vt.cpp:1-9 · src/simd/vt.zig:6 · pkg/simdutf/vendor/ 52,566 lines"),
        ("rust",
         ("The temporal class is where the Rust argument actually lives",
          "Rust 的论点真正落在时间类缺陷上"),
         ("ReleaseSafe restores bounds, overflow and null checks. Zig has no ownership model, so "
          "use-after-free and double-free walk straight through it. Bun's team ported roughly 535k "
          "lines of Zig to Rust and named that stream of bugs as the motive; their selected "
          "benchmarks moved 2.2 to 4.8%. Ghostty's answer today is AFL++ over three VT targets with "
          "4,001 committed corpus files and 3,524 inline test blocks. Fuzzing finds. It does not "
          "eliminate.",
          "ReleaseSafe 会恢复边界、溢出和空值检查。Zig 没有所有权模型，所以 use-after-free 和 double-free "
          "直接穿过去了。Bun 团队把约 53.5 万行 Zig 移到 Rust，理由就是这一串 bug；他们挑出来的基准变化是 "
          "2.2% 到 4.8%。Ghostty 现在的答案是 AFL++ 打三个 VT 目标，语料库入库 4,001 个文件，外加 3,524 "
          "个内联 test 块。fuzz 能找到问题。它消不掉缺陷类。"),
         "test/fuzz-libghostty/ · 3 harnesses, 4,001 corpus files · https://bun.com/blog/bun-in-rust"),
    ],

    "buys": [
        (("The temporal class, which no build flag reaches", "时间类缺陷，任何构建开关都管不到"),
         ("use-after-free and double-free leave any Zig that Rust replaces. ReleaseSafe cannot do "
          "that, because Zig has no ownership model to check.",
          "凡是被 Rust 换掉的 Zig，use-after-free 和 double-free 就从那里消失。ReleaseSafe 做不到，因为 "
          "Zig 没有所有权模型可查。")),
        (("A seam that was already built for it", "一条本来就是为它准备好的接缝"),
         ("185 symbols exported from src/lib_vt.zig were designed as a C ABI. A Rust VT engine could "
          "sit behind them without the Swift or GTK frontends noticing.",
          "src/lib_vt.zig 导出的 185 个符号本身就是按 C ABI 设计的。Rust 写的 VT 引擎可以藏在后面，Swift "
          "和 GTK 前端都察觉不到。")),
        (("A compiler that does not move under you", "一个不会在脚下移动的编译器"),
         ("build.zig.zon pins Zig 0.16.0, pre-1.0. Rust has held its language stable since 2015, and "
          "that is a cost of staying which no measurement here removes.",
          "build.zig.zon 把 Zig 钉在 0.16.0，还在 1.0 之前。Rust 的语言从 2015 年起保持稳定。这是「不动」"
          "要付的一笔钱，本报告里没有任何测量能把它抹掉。")),
    ],
    "nobuys": [
        (("The quality people actually praise", "大家真正称赞的那个品质"),
         ("native tabs, AppleScript, App Intents and four titlebar styles are 32,377 lines of AppKit "
          "and SwiftUI. They stay Swift under every option here.",
          "原生标签页、AppleScript、App Intents、四套标题栏样式，是 32,377 行 AppKit 和 SwiftUI。在这里的"
          "每个方案下，它们都还是 Swift。")),
        (("Any of the five published advisories", "五个公开公告里的任何一个"),
         ("command execution through pasted control characters, code injection through window titles, "
          "file permissions, an fd leak. All language-independent.",
          "粘贴控制字符导致命令执行、窗口标题导致代码注入、文件权限、fd 泄漏。全都与语言无关。")),
        (("Freedom from C++", "从 C++ 里解脱"),
         ("src/simd's 995 lines and simdutf's 52,566 exist because portable SIMD needed them. A Rust "
          "core links them or rewrites them; it does not make them go away.",
          "src/simd 的 995 行和 simdutf 的 52,566 行之所以存在，是因为可移植 SIMD 需要它们。Rust 内核要么"
          "继续链接，要么自己重写；它们不会因此消失。")),
    ],

    "precedents": [
        {"name": "Bun · Zig → Rust port", "outcome": "MIGRATED",
         "body": ("Roughly 535k lines of Zig were ported to Rust, and the motive was a persistent "
                  "stream of use-after-free, double-free and leak bugs. Selected first-party "
                  "benchmarks moved 2.2 to 4.8%. Binaries came out about 20% smaller. Nineteen "
                  "regressions landed and were fixed. Zig's creator publicly disputed the port's "
                  "quality at the time.",
                  "约 53.5 万行 Zig 被移植到 Rust，动机是一直冒出来的 use-after-free、double-free 和内存"
                  "泄漏。他们挑出来的第一方基准变化在 2.2% 到 4.8% 之间。二进制小了约 20%。出了 19 处回归"
                  "，后来修掉了。当时 Zig 作者公开质疑过这次移植的质量。"),
         "match": ("the same source language, the same defect class, and a codebase of comparable order",
                   "同一门源语言、同一类缺陷，代码体量也是同一个量级"),
         "mismatch": ("a JS runtime with no GUI layer and no C ABI that third-party frontends compile against",
                      "那是个 JS 运行时，没有 GUI 层，也没有第三方前端对着编译的 C ABI"),
         "regime": "selected first-party benchmarks; production readiness contested at publication",
         "source_label": "first-party · engineering blog",
         "url": "https://bun.com/blog/bun-in-rust"},
        {"name": "Alacritty · the \"fastest terminal\" claim", "outcome": "CLAIM FAILED AUDIT",
         "body": ("A greenfield Rust and OpenGL terminal called itself the fastest in existence. Dan "
                  "Luu measured its latency mid-pack and called throughput dumps about as useless a "
                  "benchmark as he could think of. LWN reported that ancient xterm beat every modern "
                  "terminal on worst-case latency. Alacritty is a fine terminal. Only the "
                  "superlative failed.",
                  "一个从零写的 Rust + OpenGL 终端自称是现存最快的。Dan Luu 实测它的延迟处在中游，并说吞吐"
                  "量 dump 是他能想到的最没用的基准之一。LWN 报道过：在最坏情况延迟上，老旧的 xterm 打败了"
                  "所有现代终端。Alacritty 是个不错的终端。倒下的只是那个最高级形容词。"),
         "match": ("the same archetype and the same domain: a native terminal emulator written in Rust",
                   "同一个原型、同一个领域：用 Rust 写的原生终端模拟器"),
         "mismatch": ("a claim audit rather than a migration; Ghostty's proposals here are about safety, not speed",
                      "那是对一句主张的审计，不是一次迁移；这里针对 Ghostty 的提案讲的是安全，不是速度"),
         "regime": "third-party latency measurement; no first-party harness published",
         "source_label": "third-party · measured",
         "url": "https://danluu.com/term-latency/"},
        {"name": "Zed · GPUI", "outcome": "MIGRATED",
         "body": ("A greenfield Rust editor had to build its own GPU UI framework, because no "
                  "existing Rust GUI framework hit the bar. Third-party unaudited numbers put "
                  "end-to-end open at about 58ms against VS Code's 97ms. The framework cost is real "
                  "and it belongs in the ledger, not in the footnotes.",
                  "一个从零开始的 Rust 编辑器不得不自己造一套 GPU UI 框架，因为现成的 Rust GUI 框架没有一"
                  "个达标。第三方未经审计的数字是：端到端打开约 58ms，VS Code 约 97ms。造框架这笔成本是实"
                  "打实的，该记在账本里，不该塞进脚注。"),
         "match": ("a native desktop GUI in Rust, and the direct precedent for what rust-everything would owe",
                   "用 Rust 做原生桌面 GUI，正是 rust-everything 那笔账的直接先例"),
         "mismatch": ("greenfield rather than a migration, and Zed never had a Swift layer to give up",
                      "那是从零开始，不是迁移；而且 Zed 从来没有一层 Swift 要放弃"),
         "regime": "third-party unaudited timings; first-party framerate claims",
         "source_label": "first-party claim · third-party timings",
         "url": "https://zed.dev/blog/videogame"},
        {"name": "fish shell 4.0 · C++ → Rust", "outcome": "MIGRATED",
         "body": ("57k lines of C++ became 75k lines of Rust over about two years, against a "
                  "handwaved estimate of half a year. The team's own performance summary was parity: "
                  "usually slightly better on time, a slightly higher memory floor with a lower "
                  "ceiling. They called Send and Sync the killer feature, and the contributor funnel "
                  "mattered as much as the code.",
                  "5.7 万行 C++ 变成 7.5 万行 Rust，花了约两年，而当初随口估的是半年。团队自己给的性能结论"
                  "是打平：时间上通常略好，内存下限略高但上限更低。他们说真正的杀手特性是 Send 和 Sync，而"
                  "贡献者漏斗跟代码本身一样要紧。"),
         "match": ("a terminal-adjacent tool, a manual-memory source language, and a safety-and-"
                   "maintainability motive rather than a speed one",
                   "同属终端周边工具、源语言同样手动管内存，动机同样是安全与可维护性而不是速度"),
         "mismatch": ("57k lines against Ghostty's 213,626 non-test, and no C ABI or GUI frontend to keep compiling",
                      "5.7 万行对 Ghostty 的 21.3 万非测试行，而且那边没有要继续编译的 C ABI 和 GUI 前端"),
         "regime": "first-party migration retrospective with stated method",
         "source_label": "first-party · engineering blog",
         "url": "https://fishshell.com/blog/rustport/"},
        {"name": "Microsoft · VS Code text buffer", "outcome": "STAYED",
         "body": ("A native text buffer was tried and reverted. Converting strings across the "
                   "boundary compromised any performance gained, and the fix turned out to be a "
                   "better data structure in the original language. The same product adopted Rust "
                   "successfully as a whole subprocess for search. The boundary decided both "
                   "outcomes.",
                  "他们试过原生文本缓冲区，然后回滚了。字符串在边界两侧来回转换，把拿到的性能又赔掉了；最后"
                  "的解法是在原语言里换一个更好的数据结构。同一个产品把 Rust 用成整个搜索子进程，那次成"
                  "了。两次结果都是边界决定的。"),
         "match": ("the boundary-cost test that separates rust-vt-extract from rust-core here",
                   "正是这道边界成本的测试，把这里的 rust-vt-extract 和 rust-core 分开"),
         "mismatch": ("a managed-runtime host crossing into native code; Ghostty's boundary is already a C ABI",
                      "那是托管运行时跨到原生代码；Ghostty 这边的边界本来就是 C ABI"),
         "regime": "first-party engineering retrospective",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
    ],

    "path": [
        {"title": ("Publish what the safe build costs", "把安全构建的代价公布出来"),
         "body": ("Build -Demit-bench twice, once at ReleaseFast and once at ReleaseSafe, then run "
                  "TerminalStream, TerminalParser and OscParser on the same corpus and the same "
                  "machine. Publish both numbers per harness as a percentage delta. If ReleaseSafe "
                  "lands inside the frame budget, go to step 2 and the spatial half of this question "
                  "closes for the price of a flag. Nothing is written to the tree; this is a "
                  "measurement.",
                  "用 -Demit-bench 构建两次，一次 ReleaseFast，一次 ReleaseSafe，然后在同一份语料、同一台"
                  "机器上跑 TerminalStream、TerminalParser 和 OscParser。按 harness 分别公布两组数字，给出"
                  "百分比差值。如果 ReleaseSafe 落在帧预算之内，就走第 2 步，空间类那一半问题用一个开关的价"
                  "格就结了。这一步不往仓库里写东西，它只是一次测量。"),
         "owner": "whoever argues Ghostty needs a memory-safe rewrite",
         "cost_range": ("1 week", "1 周"),
         "artifact": "a published ReleaseFast-versus-ReleaseSafe comparison on src/benchmark's TerminalStream, TerminalParser and OscParser harnesses, same corpus and same machine",
         "acceptance": "both modes are reported per harness as a percentage delta, and a third party can re-run the harness from the tree",
         "stop": "if ReleaseSafe lands inside the frame budget, proceed to step 2 and close the spatial half of the requirement",
         "rollback": "measurement only; no code changes"},
        {"title": ("Make ReleaseSafe the tagged default if it fits",
                   "代价够低就把 ReleaseSafe 设成正式版默认"),
         "body": ("Change one flag in .github/workflows/release-tag.yml. The safe build is already "
                  "codesigned, notarized and shipping on tip, so the artifact path is proven. Accept "
                  "it when the published delta stays inside a stated budget and the tip channel's "
                  "Sentry crash rate does not get worse over one release cycle. If the cost exceeds "
                  "budget, keep ReleaseFast and go to step 3. Backing out is one line.",
                  "改 .github/workflows/release-tag.yml 里的一个开关。安全构建早就在签名、公证并从 tip 通道"
                  "发布，产物链路已经验证过了。通过标准是：公布出来的差值落在事先说定的预算内，并且一个发布"
                  "周期里 tip 通道的 Sentry 崩溃率没有变差。代价超预算就继续用 ReleaseFast，转第 3 步。要退"
                  "回去，改一行。"),
         "owner": "Ghostty maintainers",
         "cost_range": ("days", "数天"),
         "artifact": "a one-flag change to the tagged release workflow, plus one release cycle of crash-rate comparison against the tip ReleaseSafe channel",
         "acceptance": "the published delta stays inside a stated performance budget and the crash rate does not regress over one release cycle",
         "stop": "if the measured cost exceeds the stated budget, keep ReleaseFast and escalate to step 3",
         "rollback": "revert one build flag"},
        {"title": ("Classify what AFL++ actually finds in src/terminal",
                   "把 AFL++ 在 src/terminal 里找到的东西分类"),
         "body": ("Take one release cycle of AFL++ output from the three harnesses and sort every "
                  "crash into three buckets: spatial defects that ReleaseSafe would have caught, "
                  "temporal defects it would not, and logic defects. The count in the temporal bucket "
                  "is the only realized-defect basis a Rust extraction has. If that bucket is empty "
                  "across a cycle, close the extraction track and say so. No code moves.",
                  "取一个发布周期里三个 harness 产出的 AFL++ 结果，把每个崩溃分进三桶：ReleaseSafe 本来能"
                  "拦住的空间类、它拦不住的时间类、以及逻辑类。时间类那一桶的数量，是 Rust 抽取方案唯一的"
                  "已发生缺陷依据。如果一整个周期这桶是空的，就把抽取这条线关掉，并且把话说明白。这一步不动"
                  "代码。"),
         "owner": "Ghostty maintainers",
         "cost_range": ("2–4 weeks", "2–4 周"),
         "artifact": "a classification of one release cycle of AFL++ crashes into spatial, temporal and logic buckets, with counts",
         "acceptance": "every crash found in the window is classified and counted, and the corpus and harness versions are named",
         "stop": "close the extraction track if the temporal bucket is empty across a full release cycle",
         "rollback": "analysis only; no code changes"},
        {"title": ("Reopen the extraction only with a plan for 275 symbols",
                   "275 个符号有交代了，才谈重开抽取"),
         "body": ("Whoever proposes the Rust VT engine writes the parity plan first. It names which "
                  "of the 275 exported C symbols change signature, who owns the resulting Swift and "
                  "GTK breakage, and how both engines process the same VT stream during dual-run. "
                  "Without that document no extraction proceeds. Until one exists the current Zig "
                  "implementation continues unchanged.",
                  "提出 Rust VT 引擎的人先把对等方案写出来。方案要点名 275 个导出 C 符号里哪些会改签名、由"
                  "谁负责随之而来的 Swift 和 GTK 破坏，以及并跑期间两个引擎怎么处理同一条 VT 流。没有这份"
                  "文档，抽取一律不往下走。在它出现之前，现在的 Zig 实现原样继续。"),
         "owner": "whoever proposes the Rust VT engine",
         "cost_range": ("2 weeks per review", "每轮评审 2 周"),
         "artifact": "a written parity and dual-run plan covering all 275 exported C symbols and both frontends",
         "acceptance": "the plan names the symbols whose signatures change, the owner of Swift-side and GTK-side breakage, and the dual-run comparison method",
         "stop": "no extraction proceeds without the document",
         "rollback": "the current Zig implementation continues unchanged"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The quality Ghostty is praised for lives in 32,377 lines of Swift, and all five "
                   "published advisories are language-independent. Only an unrealized class attaches "
                   "to the core language.",
                   "Ghostty 被称赞的那个品质住在 32,377 行 Swift 里，而五个公开公告全部与语言无关。真正挂在"
                   "内核语言上的，是一个还没发生过的缺陷类。"),
         "evidence": "macos/Sources 32,377 lines · GHSA list, 5 entries, 0 memory-safety"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("The full options leave 995 lines of Ghostty's own C++ and 52,566 vendored lines "
                   "of simdutf in place, and they re-own a build graph that currently compiles C "
                   "dependencies through 22 pkg/ wrappers.",
                   "整体方案会留下 Ghostty 自己那 995 行 C++ 和入库的 52,566 行 simdutf，还要接手一整套构建"
                   "图——现在那套是通过 22 个 pkg/ 包装器来编译 C 依赖的。"),
         "evidence": "src/simd/*.cpp 995 lines · pkg/simdutf/vendor 52,566 lines · 22 pkg/ directories"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("Any speed comparison has to run against the shipped ReleaseFast build, not a "
                   "Debug one. No published profile of Ghostty's frame time exists in either "
                   "direction, so D2 is UNKNOWN rather than settled.",
                   "任何速度对比都要跟实际发布的 ReleaseFast 构建比，不能拿 Debug 版当基线。Ghostty 的帧时"
                   "间没有任何公开 profile，两个方向都没有，所以 D2 是 UNKNOWN，不是已经有答案。"),
         "evidence": ".github/workflows/release-tag.yml:177 · src/benchmark/ 15 harnesses, no published result"},
        {"name": ("Delivery ownership", "交付归属"), "state": "HIT",
         "claim": ("68.8% of the 16,557 default-branch commits come from one author, and 97,412 lines "
                   "of inline Zig tests do not port. Review capacity bounds any rewrite before "
                   "engineering does.",
                   "默认分支 16,557 次提交里，68.8% 出自一位作者；另有 97,412 行内联 Zig 测试搬不过去。约束"
                   "任何重写的第一个瓶颈是评审带宽，不是工程量。"),
         "evidence": "gh api contributors · 425 listed, top author 11,397 of 16,557"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("The 275-symbol C ABI is named and priced against the full options, and the "
                   "extraction option is retained precisely because it inherits that seam instead of "
                   "breaking it.",
                   "275 个符号的 C ABI 被点名，并计入整体方案的成本；抽取方案之所以保留，正是因为它继承这条"
                   "接缝而不是打断它。"),
         "evidence": "D10 · 90 export fn + 185 @export, no overlap"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("Neither in-stack option is hypothetical. The ReleaseSafe build is codesigned and "
                   "published on every commit to main, and AFL++ covers three VT targets over 4,001 "
                   "committed corpus files.",
                   "栈内这两条路都不是假想。ReleaseSafe 构建每次 main 提交都会签名并发布；AFL++ 覆盖三个 "
                   "VT 目标，语料库入库 4,001 个文件。"),
         "evidence": ".github/workflows/release-tip.yml:929 · test/fuzz-libghostty/"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("The tagged release parses hostile VT input with bounds and overflow checks off. "
                   "PACKAGING.md says the project would rather not. Staying without pricing the safe "
                   "build leaves that exactly as it is.",
                   "正式发布版在关掉边界和溢出检查的状态下解析敌意 VT 输入。PACKAGING.md 里项目自己说了并不"
                   "情愿。不算安全构建的代价就继续待着，这个状态一点不变。"),
         "evidence": "PACKAGING.md:111 · release-tag.yml:177"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The C++ is counted, not hidden behind a memory-safe framing. 995 lines of "
                   "Ghostty's own plus 52,566 vendored lines of simdutf compile into the binary under "
                   "every option here.",
                   "C++ 是被计入的，没有藏在「应用是内存安全的」这种说法后面。Ghostty 自有 995 行加入库的 "
                   "52,566 行 simdutf，在这里每个方案下都会编进二进制。"),
         "evidence": "src/simd/*.cpp · pkg/simdutf/vendor/simdutf.cpp 42,510 + .h 10,056"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report never claims Rust would be slower or that the extraction is a bad "
                   "idea. D2 is UNKNOWN, and the path names the benchmark that would settle it.",
                   "报告没有主张 Rust 会更慢，也没说抽取方案是个坏主意。D2 记为 UNKNOWN，路径里点名了能了结"
                   "它的那次基准测试。"),
         "evidence": "D2 UNKNOWN · path step 1"},
        {"name": ("Toolchain risk dismissal", "轻视工具链风险"), "state": "HIT",
         "claim": ("Ghostty pins a pre-1.0 compiler. Breaking language changes between Zig minor "
                   "versions are a standing cost of staying, and no measurement in this report "
                   "removes it.",
                   "Ghostty 钉住的是一个 1.0 之前的编译器。Zig 小版本之间的破坏性语言变更是「不动」要长期付"
                   "的钱，本报告里没有任何测量能把它抹掉。"),
         "evidence": "build.zig.zon:6 · minimum_zig_version 0.16.0"},
    ],

    "gaps": [
        (("A published ReleaseFast-versus-ReleaseSafe measurement on src/benchmark's VT harnesses",
          "在 src/benchmark 的 VT harness 上公布 ReleaseFast 与 ReleaseSafe 的对比"),
         ("This is the number the whole decision turns on. PACKAGING.md calls the safe build too "
          "slow; nothing published supports or refutes that. The harnesses are already in the tree.",
          "整个决策就压在这个数字上。PACKAGING.md 说安全构建太慢，但没有任何公开材料支持或否证它。harness "
          "本来就在仓库里。")),
        (("A classification of AFL++ findings in src/terminal into spatial, temporal and logic",
          "把 src/terminal 里 AFL++ 的发现分成空间类、时间类、逻辑类"),
         ("Without it the Rust extraction rests on a mechanism rather than a realized defect. It "
          "would also tell the safe build how much of the class it actually covers.",
          "没有它，Rust 抽取方案只站在机制上，站不到已发生的缺陷上。它同时也能告诉安全构建：这个缺陷类里它"
          "真正覆盖了多少。")),
        (("Any published profile of where Ghostty's frame time goes",
          "任何一份关于 Ghostty 帧时间去向的公开 profile"),
         ("D2 stays UNKNOWN while it is missing, so no performance claim about any option here can be "
          "authorized in either direction.",
          "它缺着的时候 D2 就停在 UNKNOWN，因此这里任何方案的性能主张，往哪个方向都授权不了。")),
    ],

    "assumptions": [
        "The shallow clone at commit 46edeee represents the shipped tree; vendored source under pkg/*/vendor is counted as it ships, and dependencies fetched at build time are named but not counted.",
        "Test-block line counts come from an awk pass that opens on a line matching /^test[ \"{]/ and closes at the next line equal to '}', which relies on zig fmt keeping top-level closing braces in column 0; the figure is approximate and slightly conservative.",
        "The exported C symbol count treats each unique 'export fn ghostty_*' name in src/ and each unique '@export' name in src/lib_vt.zig as one entry point; the two sets were checked for overlap and share none.",
        "Commit-share figures come from the GitHub contributors endpoint, which is capped and counts the default branch only.",
        "No specific migration RFC was supplied, so the assessment takes the commonly argued proposal: that a terminal emulator parsing untrusted input should be written in Rust rather than Zig.",
    ],
    "objective": {
        "driver": "memory safety",
        "requirement": "remove or downgrade the memory-unsafety class on Ghostty's VT parsing path, without giving up the native macOS behaviour or the libghostty C ABI",
        "baseline": "the tagged release is built -Doptimize=ReleaseFast, which disables Zig's bounds, overflow and null checks; a ReleaseSafe macOS build is already codesigned, notarized and published on the tip channel with no measured cost",
        "target": "class elimination or safe-failure on the VT path; no proposal assessed here states a performance target",
    },
    "repository": {
        "path": "https://github.com/ghostty-org/ghostty",
        "commit": "46edeee407ff1cd15fb7db3837025386b2f3a327",
        "scope": "whole repository; src/terminal behind the libghostty C ABI is the candidate seam",
        "sampling": "shallow clone, 5,815 tracked files enumerated; src/, macos/, pkg/, include/, test/fuzz-libghostty/ and .github/workflows/ measured; release, tag and advisory history read through the GitHub API because the clone is --depth 1; no build, benchmark or run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "ghostty-org/ghostty at 46edeee · static read-only analysis · why-not-rust method 2.0",
        "ghostty-org/ghostty @ 46edeee · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/ghostty-org/ghostty at commit 46edeee407ff1cd15fb7db3837025386b2f3a327, "
        "shallow clone, 5,815 tracked files. Scope: the whole repository, with src/terminal behind the "
        "libghostty C ABI as the candidate seam. Sampling: 755 tracked .zig files hold 311,038 lines, "
        "of which 97,412 sit inside test blocks, leaving 213,626. src/terminal is 140,441 lines across "
        "141 files, 74,160 of them inside test blocks. macos/Sources holds 160 .swift files and 32,377 "
        "lines; 67 import AppKit, 63 import SwiftUI, 36 import Cocoa. macos/Tests and "
        "macos/GhosttyUITests add 2,201 lines. src/apprt is 28,408 lines, 79 of its files under gtk/. "
        "Ten C++ translation units are tracked: four are Ghostty's own in src/simd at 995 lines, one is "
        "simdutf's vendored amalgamation at 42,510 lines (52,566 with its header), three are Highway "
        "shims totalling 240 lines, and the remaining two are an imgui binding and an example. Google "
        "Highway's own source is fetched at build time, not vendored, so it is named and not counted. "
        "The include/ tree is 11,353 lines across 34 files. Exported C symbols: 90 unique "
        "'export fn ghostty_*' names in src/ (71 in src/apprt/embedded.zig, 13 in src/config/CApi.zig, "
        "5 in src/main_c.zig, 1 in src/benchmark/CApi.zig) plus 185 unique '@export' names in "
        "src/lib_vt.zig, with zero overlap between the two sets, for 275 total. Zig source carries "
        "3,524 inline test blocks, 2,579 of them in src/terminal. test/fuzz-libghostty ships three "
        "AFL++ harnesses and 4,001 committed corpus files. Build flags were read from the workflows: "
        ".github/workflows/release-tag.yml:177 builds the tagged macOS release ReleaseFast, while "
        ".github/workflows/release-tip.yml:929 builds a ReleaseSafe macOS app that is then codesigned, "
        "notarized and published as ghostty-macos-universal-debug-fast.zip. PACKAGING.md:111 states the "
        "reason. build.zig.zon:6 pins minimum_zig_version 0.16.0. GitHub API: 5 published security "
        "advisories (CWE-78, CWE-94, CWE-284, plus two without a CWE), none memory-safety; 12 version "
        "tags from v1.0.0 on 2024-12-26 to v1.3.1 on 2026-03-13; 425 contributors listed with 16,557 "
        "contributions, the top author holding 11,397. No build, test, benchmark or run was performed "
        "against the project. Objective: no specific RFC was supplied, so the assessment takes the "
        "commonly argued proposal that a terminal parsing untrusted input should be Rust rather than "
        "Zig. User-supplied facts: none. No Amdahl calculation appears: D2 is UNKNOWN because no "
        "published profile locates Ghostty's frame time, and a line share is not a time share. The "
        "decision turns on G3 and G4. G3 fails because the smaller option is a build flag whose cost "
        "has never been published, and G4 fails on 275 exported C symbols across two frontends written "
        "in other languages. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/ghostty-org/ghostty，commit 46edeee407ff1cd15fb7db3837025386b2f3a327，shallow "
        "clone，5,815 个纳管文件。范围：整个仓库，候选接缝是 libghostty C ABI 后面的 src/terminal。采样："
        "755 个纳管 .zig 文件共 311,038 行，其中 97,412 行在 test 块内，余 213,626 行。src/terminal 是 141 "
        "个文件、140,441 行，其中 74,160 行在 test 块内。macos/Sources 有 160 个 .swift 文件、32,377 行；67 "
        "个 import AppKit，63 个 import SwiftUI，36 个 import Cocoa。macos/Tests 与 macos/GhosttyUITests 另"
        "有 2,201 行。src/apprt 是 28,408 行，其中 79 个文件在 gtk/ 下。纳管的 C++ 翻译单元共十个：四个是 "
        "Ghostty 自有的，在 src/simd，995 行；一个是 simdutf 入库的合并源码，42,510 行（含头文件 52,566 "
        "行）；三个是 Highway 的胶水层，合计 240 行；剩下两个是 imgui 绑定和一个示例。Google Highway 自身的"
        "源码在构建时才拉，没有入库，所以只点名不计数。include/ 树是 34 个文件、11,353 行。导出 C 符号：src/ "
        "里 90 个不重复的 'export fn ghostty_*'（src/apprt/embedded.zig 71 个，src/config/CApi.zig 13 个，"
        "src/main_c.zig 5 个，src/benchmark/CApi.zig 1 个），加 src/lib_vt.zig 里 185 个不重复的 "
        "'@export'，两组之间零重叠，合计 275 个。Zig 源码里有 3,524 个内联 test 块，其中 2,579 个在 "
        "src/terminal。test/fuzz-libghostty 提供三个 AFL++ harness 和 4,001 个入库语料文件。构建开关取自 "
        "workflow：.github/workflows/release-tag.yml:177 用 ReleaseFast 构建正式的 macOS 发布版，而 "
        ".github/workflows/release-tip.yml:929 构建的是 ReleaseSafe 的 macOS 应用，随后签名、公证，并以 "
        "ghostty-macos-universal-debug-fast.zip 发布。PACKAGING.md:111 写了原因。build.zig.zon:6 把 "
        "minimum_zig_version 钉在 0.16.0。GitHub API：5 条公开安全公告（CWE-78、CWE-94、CWE-284，另两条没有 "
        "CWE），无一属于内存安全；12 个版本 tag，从 2024-12-26 的 v1.0.0 到 2026-03-13 的 v1.3.1；列出 425 "
        "位贡献者、16,557 次贡献，头号作者占 11,397 次。没有对项目做过任何构建、测试、基准或运行。目标：没有"
        "人给出具体 RFC，因此按常见的那个说法评估——解析不可信输入的终端应该用 Rust 而不是 Zig。用户提供的事"
        "实：无。本报告没有 Amdahl 计算：D2 是 UNKNOWN，因为没有公开 profile 定位 Ghostty 的帧时间，而代码行"
        "数占比不等于时间占比。决策落在 G3 和 G4。G3 失败，是因为更小的那个方案只是一个构建开关，而它的代价"
        "从来没被公布过；G4 失败，是因为 275 个导出 C 符号背后是两套用别的语言写的前端。这是一套结构化决策流"
        "程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 46edeee · GitHub API for release and advisory "
        "history · no build, benchmark or run",
        "公开仓库 · 在 commit 46edeee 上做静态分析 · 发布与公告历史取自 GitHub API · 没有构建、基准或运行",
    ),
}
