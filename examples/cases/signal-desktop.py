"""signalapp/Signal-Desktop — the crypto already moved to Rust; the shell has nothing to move.

Repository facts were measured read-only on the shallow clone named in
`repository`. libsignal facts come from a separate shallow clone of
signalapp/libsignal at 622d0d5, counted on the same basis and labelled as such.
"""

CASE = {
    "slug": "signal-desktop",
    "project_name": "signalapp/Signal-Desktop",
    "project_desc": (
        "Electron + TypeScript · private messenger · 555,145 lines of TypeScript and TSX, "
        "308 lines of native code, 0 lines of Rust",
        "Electron + TypeScript · 私密通讯客户端 · TypeScript 与 TSX 共 555,145 行，原生代码 308 行，"
        "Rust 0 行",
    ),
    "date": "2026-08-02",
    "archetype": (
        "electron-desktop · TypeScript shell over a Rust crypto core consumed as a prebuilt binary",
        "electron-desktop · TypeScript 外壳，下面是以预编译二进制引入的 Rust 加密内核",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "stay-harden",
    "scope_chip": (
        "keep the TypeScript shell; spend the safety budget on the native surface",
        "外壳留在 TypeScript；安全预算花在原生面上",
    ),
    "scope_sub": (
        "the shell stays; the memory-unsafety is somewhere else",
        "外壳不动；内存不安全在别的地方",
    ),

    "why": (
        "The crypto already moved. libsignal is 182,247 lines of Rust across 584 files, it replaced "
        "libsignal-protocol-c, and iOS, Android and Desktop all link it. So the follow-up question is a "
        "fair one: should the shell go too? Signal Desktop's shell is 555,145 lines of TypeScript and "
        "TSX. The memory-unsafe code Signal wrote is 308 lines, in three files. Rewriting the shell "
        "removes no memory-unsafety class, because there is none in there to remove. The C++ that decodes "
        "hostile bytes is Chromium 150, shipped by one line of package.json, and that line is Signal's "
        "whole lever on it.",
        "加密那部分已经搬完了。libsignal 是 584 个文件、182,247 行 Rust，它替掉了 libsignal-protocol-c，"
        "iOS、Android、Desktop 三端都链它。所以接着问一句不算过分：外壳要不要也搬？Signal Desktop 的外壳是 "
        "555,145 行 TypeScript 和 TSX。Signal 自己写的内存不安全代码是 308 行，分在三个文件里。重写外壳消不掉"
        "任何内存不安全缺陷类，因为那里面本来就没有可消的。真正解码敌意字节的 C++ 是 Chromium 150，靠 "
        "package.json 里一行带进来，而那一行就是 Signal 对它的全部操作杆。",
    ),
    "trigger": (
        "Stable for the shell question. A Rust decision reopens at a different scope, not this one. If a "
        "memory-safety finding lands in code Signal owns and can replace, the EXTRACT option gets "
        "stronger. The .node addons and the untrusted-byte decoders are that scope; 555,145 lines of "
        "React are not.",
        "对「外壳」这个问题，结论是稳定的。Rust 的决策会在另一个范围上重开，不是在这个范围。如果内存安全问题"
        "落在 Signal 自己拥有、也换得掉的代码里，EXTRACT 方案就更有理。那个范围是 .node 插件和解码不可信字节"
        "的那几段，不是 555,145 行 React。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("Nation-state adversaries are the premise; the unsafe surface is located.",
                           "对手是国家级，这是前提；不安全面也定位清楚了。"),
         "name": "requirement",
         "evidence": "Signal Desktop packages 8 prebuilt .node binaries (package.json:621-629) and ships Chromium 150.0.7871.46 through electron 43.0.0 (package.json:245, Electron's own v43.0.0 release notes). Every image and video attachment reaches a C++ decoder. That exposure exists and this report locates it. It is not in the TypeScript."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果"),
         "hero_evidence": ("555,145 lines of TypeScript hold no memory-unsafety class to remove.",
                           "555,145 行 TypeScript 里没有可消除的内存不安全缺陷类。"),
         "name": "rust-specific causality",
         "evidence": "The proposed scope is the shell. Its 555,145 lines of TS/TSX are memory-safe, and the 308 lines of C, C++ and Objective-C++ Signal wrote sit in three optional platform addons. A Rust host still renders through a C++ webview: WebView2 on Windows is Chromium. The safety benefit lives in a layer the rewrite does not touch."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("Two cheaper options are already shipping in this repository.",
                           "两个更便宜的方案已经在这个仓库里发着了。"),
         "name": "economics and smallest sufficient option",
         "evidence": "MP4 attachments already pass through libsignal's Rust mp4san sanitizer before the renderer sees them (ts/util/handleVideoAttachment.preload.ts:5), and the Electron pin at package.json:245 is how Chromium's own fixes arrive. Neither costs 394,240 lines of rewritten product TypeScript."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("394,240 product lines, 68 locales, 56 stable releases in 12 months.",
                           "产品代码 394,240 行，68 种语言，12 个月 56 个稳定版。"),
         "name": "delivery and reversibility",
         "evidence": "Product TS/TSX is 394,240 lines across 1,971 files, including 746 React component files and 429 aria- attribute lines. _locales holds 68 languages. GitHub's API shows 56 stable releases in the 12 months to 2026-08-01. No dual-run exists for a messenger's UI, and a partial rewrite means shipping two of them."},
    ],

    "tiles": [
        (("TypeScript + TSX", "TypeScript + TSX"), "555,145", ("lines", "行"),
         ("2,764 files · what a shell rewrite replaces · already memory-safe",
          "2,764 个文件 · 重写外壳要换掉的就是这些 · 本来就是内存安全的")),
        (("Native code Signal wrote", "Signal 自己写的原生代码"), "308", ("lines", "行"),
         ("one .c, one .cpp, one .mm · 0.05% of code-extension lines",
          "一个 .c、一个 .cpp、一个 .mm · 占代码类扩展名行数的 0.05%")),
        (("Rust already shipped in libsignal", "libsignal 里已经发出去的 Rust"), "182,247", ("lines", "行"),
         ("584 files · replaced libsignal-protocol-c · shared with iOS and Android",
          "584 个文件 · 替掉了 libsignal-protocol-c · 与 iOS、Android 共用")),
        (("Chromium bundled by Electron 43.0.0", "Electron 43.0.0 带进来的 Chromium"), "~36M", ("SLOC", "行"),
         ("Open Hub via Wikipedia, retrieved 2024-02-19 · whole Chromium tree, wider than Electron's subset",
          "Open Hub 数据经 Wikipedia 引用，2024-02-19 取得 · 整棵 Chromium 树，比 Electron 实际取用的子集大")),
        (("Signal's lever on that C++", "Signal 对那些 C++ 的操作杆"), "1", ("line", "行"),
         ("package.json:245 — the Electron version pin",
          "package.json:245 —— Electron 的版本锁定")),
        (("Windows with the Chromium sandbox off", "关掉 Chromium sandbox 的窗口"), "1", ("of 8", "个 / 共 8 个"),
         ("app/main.main.ts:721 is the main window; the other seven set sandbox: true",
          "app/main.main.ts:721 是主窗口；另外七个都是 sandbox: true")),
    ],

    "options_sub": (
        "One objective for every option: cut the memory-unsafety exposure on the path that handles bytes "
        "a hostile sender chose, without breaking behaviour across Windows, macOS and Linux or the 68 "
        "shipped locales.",
        "所有方案对着同一个目标：降低「处理敌意发送方选定的字节」这条路径上的内存不安全暴露，同时不破坏 "
        "Windows、macOS、Linux 三端行为，也不破坏已经发出去的 68 种语言。",
    ),
    "options": [
        {"id": "stay-harden", "name": ("Harden the native surface, keep the TypeScript",
                                       "加固原生面，TypeScript 保持不动"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("aims at the 8 packaged .node binaries and the Chromium pin",
                              "对准打包进去的 8 个 .node 二进制和 Chromium 的版本锁定"),
         "one_time_cost": "weeks; sandbox work on one window", "recurring_cost": "the Electron upgrade cadence they already run",
         "cost_cell": ("weeks; existing upgrade cadence", "数周；沿用现有升级节奏"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "native", "compat_cell": ("native · per-window rollback", "原生 · 按窗口回滚"),
         "reversibility": "git revert",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the only option pointed at where the C++ actually is",
                  "推荐 · 唯一对准 C++ 真正所在位置的方案"),
         "reason": "Smallest option that reaches the trust boundary where the C++ actually sits. The Chromium pin, the sandbox flag on the main window, and the existing injection-lint discipline all cost less than any rewrite and all aim at code that is memory-unsafe."},
        {"id": "rust-parsers", "name": ("Push more untrusted-byte parsing into libsignal",
                                        "把更多不可信字节的解析推进 libsignal"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed from each decoder that moves behind the sanitizer",
                              "每有一个解码器搬到 sanitizer 后面，那一段的缺陷类就消失"),
         "one_time_cost": "per format; libsignal team owns it", "recurring_cost": "none new for Desktop's build",
         "cost_cell": ("per format; no new Desktop toolchain", "按格式计；Desktop 不新增工具链"),
         "time_to_value": ("months, per format", "数月，按格式推进"),
         "compatibility": "byte-level behaviour of each format",
         "compat_cell": ("same .node seam · feature-flag rollback", "同一道 .node 接缝 · 用开关回滚"),
         "reversibility": "feature flag per format", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the Rust direction with a shape, and it is already running",
                  "保留 · 唯一有形状的 Rust 方向，而且已经在跑了"),
         "reason": "Correct target and a proven seam: mp4san and webpsan already ship inside libsignal and Desktop already calls the MP4 one. Every additional format is an incremental, reversible step owned by the libsignal team, not the Desktop team."},
        {"id": "sqlcipher-swap", "name": ("Replace the C SQLCipher with a memory-safe engine",
                                          "把 C 写的 SQLCipher 换成内存安全的引擎"),
         "implementation": "rust",
         "scope": "component", "scope_tag": "PARTIAL",
         "benefit_interval": ("class removed from the store that holds every message",
                              "存着全部消息的那个引擎里，缺陷类消失"),
         "one_time_cost": "unpriced; file-format and migration parity", "recurring_cost": "a second storage engine to track",
         "cost_cell": ("unpriced; format parity is the hard part", "未定价；难在文件格式对等"),
         "time_to_value": ("a year or more", "一年以上"),
         "compatibility": "on-disk format, encryption, and every existing database",
         "compat_cell": ("on-disk format · restore from backup", "磁盘格式 · 从备份恢复"),
         "reversibility": "hard; the data has migrated", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the largest C surface Signal actually chooses",
                  "保留 · Signal 真正有选择权的最大一块 C"),
         "reason": "Retained because the surface is substantial: @signalapp/sqlcipher is Signal's own C fork and it holds the whole message history. Not selected because the migration is a data-format problem before it is a language problem, and no Rust SQLite has SQLCipher's on-disk compatibility."},
        {"id": "rust-shell", "name": ("Replace Electron with a Rust host", "把 Electron 换成 Rust 宿主"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("no memory-safety gain; footprint claim unmeasured for this app",
                              "拿不到内存安全收益；占用那条对这个应用没量过"),
         "one_time_cost": "394,240 lines of product TS/TSX plus a webview story", "recurring_cost": "three rendering engines instead of one",
         "cost_cell": ("394,240 lines; 3 engines to support", "394,240 行；要养三套渲染引擎"),
         "time_to_value": ("years", "数年"),
         "compatibility": "68 locales, accessibility, IME, three platforms",
         "compat_cell": ("whole UI + a11y + IME · no rollback", "整个 UI + 无障碍 + 输入法 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G2 on its own objective", "排除 · 在自己设的目标上过不了 G2"),
         "reason": "The rewrite target is memory-safe already, and the C++ renderer survives the move — WebView2 on Windows is Chromium. It pays a full rewrite and does not buy the safety it was proposed for."},
        {"id": "native-perplatform", "name": ("Write three native clients instead", "改成写三个原生客户端"),
         "implementation": "external",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("native execution; memory-safety depends entirely on the language chosen",
                              "拿到原生执行；内存安全完全取决于选的语言"),
         "one_time_cost": "three codebases from scratch", "recurring_cost": "three UI teams, permanently",
         "cost_cell": ("3 codebases; 3 teams forever", "三套代码；永久三个团队"),
         "time_to_value": ("years per platform", "每个平台数年"),
         "compatibility": "no shared UI; feature parity by hand",
         "compat_cell": ("nothing shared · no rollback", "没有共享部分 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · retained only to test whether the benefit is native or Rust",
                  "排除 · 保留它只为检验收益到底来自原生还是来自 Rust"),
         "reason": "Kept in the comparison because most of what a Rust shell promises is native execution rather than Rust. Signal already ships Swift and Kotlin clients, so this is the native counterfactual with a track record behind it. It also triples the UI surface and leaves the platform media decoders in C++."},
    ],

    "lenses_sub": (
        "Each state is scoped to named options and none of them add up to a score. D4 is where the Rust "
        "shell has a case worth stating, and the ledger states it.",
        "每条状态都绑定到具体方案，加不成一个总分。D4 是 Rust 外壳唯一说得上话的一条，账本照实记。",
    ),
    "na_note": (
        "One lens is N/A. D5 startup shape: Signal Desktop is launched once per session and the project "
        "already caches the compiled preload bundle, so startup is not an unmet requirement any option "
        "here competes on.",
        "一条记为 N/A。D5 启动形态：Signal Desktop 每次会话只启动一次，而且项目已经把编译好的 preload 缓存"
        "起来了，启动时间不是这里任何方案要争的未满足需求。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "DISFAVORS · rust-shell", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-shell"],
         "claim": ("The exposure is located and it sits outside the shell. Signal writes 308 lines of "
                   "native code. It packages 8 prebuilt .node binaries and ships a whole Chromium. A "
                   "shell rewrite cannot reach any of that.",
                   "暴露面定位清楚了，而且不在外壳里。Signal 自己写的原生代码 308 行，另外打包 8 个预编译 "
                   ".node 二进制，还带一整个 Chromium。重写外壳一个都碰不到。"),
         "source": "308 lines in packages/{lame/wrapper.c,mute-state-change/addon.mm,windows-ucv/addon.cpp} · package.json:245 · package.json:621-629",
         "regime": "static inventory at commit 34fa453",
         "caveat": "Ownership cuts both ways: Signal does not own Chromium's code, but it does choose the version, and it does own the choice of every native dependency.",
         "change_trigger": "A memory-safety finding inside one of the 8 packaged native modules would move this lens onto the EXTRACT and PARTIAL options."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-shell", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-shell"],
         "claim": ("No Amdahl figure appears in this report. Nobody has published a profile of Signal "
                   "Desktop, and the repository contains no perf artifact at all. Substituting a line "
                   "share for a time share would be a method error.",
                   "本报告不给 Amdahl 数字。没有人公开过 Signal Desktop 的 profile，仓库里也没有任何性能"
                   "产物。用代码行数占比顶替时间占比属于方法错误。"),
         "source": "no .cpuprofile, flamegraph, speedscope or heapsnapshot in the tree; no published profile",
         "regime": "n/a — the measurement is absent",
         "caveat": "This is why no speedup or footprint interval is attached to the rust-shell option.",
         "change_trigger": "A published startup and steady-state profile splitting Chromium, V8, the .node addons and Signal's own JavaScript would make a performance claim assessable."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · rust-shell", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["rust-shell"],
         "claim": ("A Rust host does not remove the collector. The UI still runs in a JavaScript engine "
                   "inside whatever webview the platform supplies. V8 stays on Windows because WebView2 "
                   "is Chromium.",
                   "换成 Rust 宿主并不会拿走 collector。UI 还是跑在平台给的那个 webview 里的 JS 引擎上。"
                   "Windows 上 V8 照旧，因为 WebView2 就是 Chromium。"),
         "source": "Tauri issue 5889 · package.json:245 (electron 43.0.0 → Chromium 150.0.7871.46)",
         "regime": "architecture of the proposed replacement",
         "caveat": "A Rust GUI toolkit with no webview would remove V8, and would also remove the rendering engine the product is built on. That is a different and much larger proposal."},
        {"id": "D4", "name": ("Footprint & fleet economics", "占用与规模经济"),
         "label": "SUPPORTS · rust-shell", "css": "rust",
         "state": "SUPPORTS", "strength": "WEAK", "option_ids": ["rust-shell"],
         "claim": ("Here the Rust shell has a case. One measured comparison puts a Tauri app at 8.6 MiB "
                   "bundle and ~172 MB RAM against Electron's 244 MiB and ~409 MB. A desktop messenger "
                   "has no fleet to multiply that by.",
                   "这一条上 Rust 外壳是说得上话的。有一份实测把 Tauri 应用记在 8.6 MiB 包体、约 172 MB "
                   "内存，Electron 是 244 MiB、约 409 MB。但桌面通讯客户端没有一个机队可以拿来乘。"),
         "source": "https://www.gethopp.app/blog/tauri-vs-electron",
         "regime": "macOS, 6 windows, N=1, author uses Tauri",
         "caveat": "Single-machine, single-author, and macOS only. The same table's companion finding is that on Windows WebView2 is Chromium and memory lands near Electron once shared pages are counted.",
         "change_trigger": "A per-platform memory measurement of Signal Desktop against a webview-based Rust prototype would upgrade this from WEAK."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Signal Desktop starts once per session and stays resident. The project already "
                   "caches the compiled preload bundle to cut that cost inside the current stack.",
                   "Signal Desktop 每次会话启动一次，然后常驻。项目已经把编译好的 preload bundle 缓存起来，"
                   "在现有栈内把这块成本压下去了。"),
         "source": "preload.wrapper.ts:12 (preload.bundle.cache) · ts/util/desktopCapturer.preload.ts:271",
         "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust-parsers, sqlcipher-swap", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-parsers", "sqlcipher-swap"],
         "claim": ("Attachments become blob URLs handed to the DOM, so images and video are decoded by "
                   "Chromium's C++. Messages land in a C SQLCipher. Rust removes the class from anything "
                   "it replaces there. It removes nothing from 555,145 lines of TypeScript.",
                   "附件变成 blob URL 交给 DOM，所以图片和视频是 Chromium 的 C++ 在解码。消息落在 C 写的 "
                   "SQLCipher 里。Rust 换掉那里的哪一段，哪一段的缺陷类就消失。而它从 555,145 行 "
                   "TypeScript 里拿不走任何东西。"),
         "source": "ts/types/VisualAttachment.dom.ts:298 (URL.createObjectURL) · package.json:130 (@signalapp/sqlcipher 4.0.3) · https://www.chromium.org/Home/chromium-security/memory-safety/",
         "regime": "structural, at the point untrusted bytes are decoded",
         "caveat": "Chromium's own security team puts memory safety at ~70% of 912 high or critical severity bugs since 2015. That statistic is about C++ and does not transfer to Signal's TypeScript."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · rust-shell", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["rust-shell"],
         "claim": ("Signal Desktop already moves work off the main thread. The SQL layer and the HEIC "
                   "converter both run in node:worker_threads, and main/renderer is process isolation. "
                   "There is no shared-memory race problem here for Rust to encode away.",
                   "Signal Desktop 已经把活挪出主线程了。SQL 层和 HEIC 转换都跑在 node:worker_threads 上，"
                   "main 和 renderer 之间本来就是进程隔离。这里没有共享内存竞争问题给 Rust 去编码消除。"),
         "source": "ts/sql/main.main.ts:586 · ts/workers/heicConverterMain.main.ts:24",
         "regime": "existing concurrency design",
         "caveat": "fish shell's stated motive for its C++ to Rust port was Send and Sync. That motive needs shared mutable state across threads, which this architecture does not have."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "DISFAVORS · rust-shell", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-shell"],
         "claim": ("The reproducible build installs Node, gcc, g++ and python3. No Rust toolchain. The "
                   "Rust already in the product arrives prebuilt and costs this build nothing. A Rust "
                   "host would add a toolchain and swap the rendering engine per platform.",
                   "可复现构建装的是 Node、gcc、g++ 和 python3，没有 Rust 工具链。产品里已有的 Rust 是预编译"
                   "进来的，对这条构建零成本。换成 Rust 宿主则要加工具链，还要按平台换渲染引擎。"),
         "source": "reproducible-builds/Dockerfile:33 · package.json:377 (singleArchFiles prebuilds)",
         "regime": "the shipped release build at this commit",
         "caveat": "Tauri's own maintainers say they cannot fully recommend it on Linux and describe WebKitGTK as getting worse each release. Signal's README commits to Windows, macOS and Linux."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "DISFAVORS · rust-shell", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-shell"],
         "claim": ("Signal ships 68 locales and 429 aria- attribute lines in its components. A 2025 "
                   "survey of 43 Rust GUI crates found the overwhelming majority not production-ready, "
                   "with accessibility and IME the recurring gaps. Those are the two things a messenger "
                   "cannot ship without.",
                   "Signal 发 68 种语言，组件里有 429 行 aria- 属性。2025 年一份对 43 个 Rust GUI crate 的"
                   "调查结论是绝大多数还不能上生产，反复出现的短板正是无障碍和输入法。通讯客户端缺这两样"
                   "就发不出去。"),
         "source": "_locales (68 directories) · 429 aria- lines in ts/components · https://www.boringcactus.com/2025/04/13/2025-survey-of-rust-gui-libraries.html",
         "regime": "third-party crate survey, 2025",
         "caveat": "This disfavours a Rust GUI, not Rust. The Rust ecosystem asset Signal actually needed already exists and Signal adopted it, which is what D10 records."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "SUPPORTS · rust-parsers", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-parsers"],
         "claim": ("The working seam is already built. libsignal enters as a prebuilt .node addon, "
                   "referenced on 147 lines across 102 files, and each call hands over a whole message "
                   "or a whole file. The UI has no seam like that; it is DOM and event loop all the way "
                   "down.",
                   "能用的那道接缝已经建好了。libsignal 以预编译 .node 插件进来，102 个文件里有 147 行引用"
                   "它，每次调用交过去的是一整条消息或一整个文件。UI 没有这样的接缝，它从上到下就是 DOM 和"
                   "事件循环。"),
         "source": "147 lines referencing @signalapp/libsignal-client across 102 files · package.json:622 · ts/util/handleVideoAttachment.preload.ts:34",
         "regime": "static call-site inventory at this commit",
         "caveat": "Prisma deleted its Rust query engine because a per-operation JS-to-Rust boundary cost more than it saved. The sanitizer boundary is per-attachment, which is why it survives that test."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-shell", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-shell"],
         "claim": ("394,240 lines of product TS/TSX, 760 commits in six months, 56 stable releases in "
                   "twelve. A rewrite of that surface competes with the release train for the same "
                   "people. Freeze it and the product stops.",
                   "产品代码 394,240 行 TS/TSX，半年 760 个提交，一年 56 个稳定版。重写这块面要和发布列车"
                   "抢同一批人。冻住它，产品就停了。"),
         "source": "1,971 tracked product TS/TSX files · GitHub API: 760 commits since 2026-02-02, 56 stable releases since 2025-08-01",
         "regime": "GitHub API counts, retrieved 2026-08-02",
         "caveat": "The 56 excludes 66 beta and alpha tags in the same window. Both were counted; the stable figure is the one quoted."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-harden", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-harden"],
         "claim": ("The in-stack security work is funded and visible. Twelve lint rules ban eval, "
                   "innerHTML and dangerouslySetInnerHTML, with 45 recorded exceptions and every single "
                   "one of them in node_modules. Zero in Signal's own code.",
                   "栈内的安全工作有人投入，也看得见。12 条 lint 规则禁掉 eval、innerHTML 和 "
                   "dangerouslySetInnerHTML，登记了 45 条例外，而且 45 条全在 node_modules 里。Signal 自己"
                   "的代码里一条都没有。"),
         "source": "ts/util/lint/rules.json (12 rules) · ts/util/lint/exceptions.json (45 entries, 0 outside node_modules)",
         "regime": "current engineering practice in this commit",
         "caveat": "These rules target injection, not memory safety. They are evidence the team already spends a security budget where its actual defect class lives."},
    ],

    "findings": [
        ("current",
         ("The rewrite target has no memory-unsafety in it",
          "要重写的那块里没有内存不安全"),
         ("Signal Desktop is 555,145 lines of TypeScript and TSX across 2,764 files. The native code "
          "Signal wrote is 308 lines: an MP3 wrapper, a macOS mute-state addon, and a Windows "
          "camera-privacy addon. That is 0.05% of the tree's code-extension lines. Rewriting the other "
          "99.95% in Rust eliminates a defect class that is not present.",
          "Signal Desktop 是 2,764 个文件、555,145 行 TypeScript 和 TSX。Signal 自己写的原生代码 308 行："
          "一个 MP3 包装、一个 macOS 静音状态插件、一个 Windows 摄像头隐私插件。占全树代码类扩展名行数的 "
          "0.05%。把另外 99.95% 用 Rust 重写，消除的是一个并不存在的缺陷类。"),
         "555,145 TS+TSX lines vs 308 lines of .c/.cpp/.mm · 567,505-line code-extension basis"),
        ("rust",
         ("The migration already happened, and it stopped at BoringSSL",
          "迁移早就发生过，而且停在了 BoringSSL"),
         ("libsignal is 182,247 lines of Rust across 584 files. libsignal-protocol-c was archived on "
          "2020-07-31, weeks before the Rust repository was created. iOS, Android and Desktop all link "
          "the result. The migration did not delete all the C, though: rust/core, rust/net, rust/attest "
          "and rust/device-transfer all depend on boring 5.0.2, which is BoringSSL.",
          "libsignal 是 584 个文件、182,247 行 Rust。libsignal-protocol-c 在 2020-07-31 归档，几周之后 "
          "Rust 仓库才建起来。iOS、Android、Desktop 三端链的都是它。但这次迁移并没有把 C 全删掉：rust/core、"
          "rust/net、rust/attest、rust/device-transfer 都依赖 boring 5.0.2，那就是 BoringSSL。"),
         "signalapp/libsignal at 622d0d5 · Cargo.toml:118 · GitHub API archive dates"),
        ("current",
         ("Signal ships Chromium 150 and cannot patch it",
          "Signal 发的是 Chromium 150，而它改不动"),
         ("package.json:245 pins electron 43.0.0. Electron's own release notes for v43.0.0 name Chromium "
          "150.0.7871.46, Node 24.147.0 and V8 15.0. Chromium's security team attributes about 70% of "
          "912 high or critical severity bugs since 2015 to memory safety. Signal's entire lever on that "
          "code is the version string.",
          "package.json:245 把 electron 锁在 43.0.0。Electron 自己的 v43.0.0 发布说明写明 Chromium "
          "150.0.7871.46、Node 24.147.0、V8 15.0。Chromium 安全团队把 2015 年以来 912 个高危或严重缺陷中"
          "约 70% 归因于内存安全。Signal 对这些代码的全部操作杆，就是那个版本号。"),
         "package.json:245 · Electron v43.0.0 release notes · chromium.org memory-safety page"),
        ("rust",
         ("MP4 already passes through a Rust sanitizer first",
          "MP4 已经先过一遍 Rust sanitizer"),
         ("ts/util/handleVideoAttachment.preload.ts:5 imports sanitize from libsignal's Mp4Sanitizer, and "
          "line 34 runs every video/mp4 through it before anything else touches the bytes. libsignal's "
          "signal-media crate is 117 lines wrapping mp4san and webpsan. The safety strategy Signal "
          "actually runs is a Rust parser in front of a C++ decoder.",
          "ts/util/handleVideoAttachment.preload.ts:5 从 libsignal 的 Mp4Sanitizer 引入 sanitize，第 34 行"
          "在任何别的东西碰这些字节之前，把每个 video/mp4 都过一遍。libsignal 的 signal-media crate 是 117 "
          "行，包着 mp4san 和 webpsan。Signal 实际在跑的安全策略，是在 C++ 解码器前面摆一个 Rust 解析器。"),
         "ts/util/handleVideoAttachment.preload.ts:5,34 · libsignal rust/media (117 lines)"),
        ("current",
         ("Seven of eight windows are sandboxed; the eighth is the main one",
          "八个窗口里七个开了 sandbox；剩下那个是主窗口"),
         ("app/main.main.ts creates 8 BrowserWindows. Seven set sandbox: true. The one at line 721 sets "
          "sandbox: false, and that is the window rendering conversations. Its preload uses node:fs and "
          "node:vm, which is the reason. Closing that gap is a scoped piece of work in the current stack "
          "and it beats any rewrite on cost.",
          "app/main.main.ts 建了 8 个 BrowserWindow，其中 7 个设 sandbox: true。第 721 行那个设的是 "
          "sandbox: false，而它正是渲染会话的窗口。它的 preload 用了 node:fs 和 node:vm，这就是原因。补这个"
          "口子是现有栈里一件范围清楚的活，成本上赢过任何重写。"),
         "app/main.main.ts:721 · preload.wrapper.ts:4,6"),
    ],

    "buys": [
        (("Class elimination in any decoder it replaces", "凡是被它替换的解码器，那个缺陷类就消失"),
         ("mp4san already proves the pattern in this product: a Rust parser validates the container "
          "before Chromium's C++ ever sees it.",
          "mp4san 在这个产品里已经把这个模式跑通了：容器先由 Rust 解析器校验，Chromium 的 C++ 才看得到。")),
        (("A seam that is already built and staffed", "一道已经建好、也有人管的接缝"),
         ("libsignal ships prebuilt, so Desktop's release build needs no Rust toolchain and the libsignal "
          "team owns the code.",
          "libsignal 是预编译发布的，所以 Desktop 的发布构建不需要 Rust 工具链，代码也归 libsignal 团队。")),
        (("Cross-client amortisation", "跨端摊销"),
         ("one Rust parser serves iOS, Android and Desktop. A Desktop UI rewrite serves one client.",
          "一个 Rust 解析器同时服务 iOS、Android 和 Desktop。重写 Desktop 的 UI 只服务一个端。")),
    ],
    "nobuys": [
        (("Memory safety in the shell", "外壳的内存安全"),
         ("those 555,145 lines are already memory-safe. There is no class there for Rust to remove.",
          "那 555,145 行本来就是内存安全的，那里没有缺陷类给 Rust 拿走。")),
        (("Escape from the C++ renderer", "摆脱 C++ 渲染器"),
         ("a Rust host still draws through a platform webview, and on Windows that webview is Chromium.",
          "Rust 宿主还是靠平台 webview 绘制，而 Windows 上那个 webview 就是 Chromium。")),
        (("A memory-safe message store", "一个内存安全的消息库"),
         ("@signalapp/sqlcipher stays C under every option except the one that explicitly replaces it.",
          "除了明确去替换它的那个方案，其他方案下 @signalapp/sqlcipher 都还是 C。")),
        (("Relief from the compatibility surface", "从兼容面里解脱"),
         ("68 locales, screen-reader behaviour and IME handling survive any implementation change.",
          "68 种语言、读屏行为和输入法处理，在任何实现变更之后都还在。")),
    ],

    "precedents": [
        {"name": "Signal · libsignal (C → Rust)", "outcome": "MIGRATED",
         "body": ("Signal's own precedent, and the strongest one available. libsignal-protocol-c was "
                  "archived on 2020-07-31; the Rust repository was created on 2020-09-12 and now holds "
                  "182,247 lines across 584 files serving iOS, Android, Desktop and the server. The "
                  "boundary is where it stops mattering: rust/core and rust/net still link BoringSSL, "
                  "and rust/media is 117 lines wrapping two external sanitizer crates.",
                  "Signal 自己的先例，也是手上最强的一个。libsignal-protocol-c 在 2020-07-31 归档；Rust 仓库"
                  "在 2020-09-12 建立，现在是 584 个文件、182,247 行，服务 iOS、Android、Desktop 和服务端。"
                  "关键在它停在哪：rust/core 和 rust/net 仍然链 BoringSSL，rust/media 只有 117 行，包着两个"
                  "外部 sanitizer crate。"),
         "match": ("same organisation, same threat model, same product, and the code replaced was C "
                   "parsing attacker-chosen bytes",
                   "同一个组织、同一套威胁模型、同一个产品，被替换的代码就是解析攻击者选定字节的 C"),
         "mismatch": ("the migrated code was C and served four consumers; the Desktop shell is "
                      "TypeScript and serves one",
                      "被迁移的是 C，服务四个消费方；Desktop 外壳是 TypeScript，只服务一个"),
         "regime": "measured on a shallow clone at 622d0d5, 2026-08-02",
         "source_label": "first-party · repository measurement",
         "url": "https://github.com/signalapp/libsignal"},
        {"name": "Microsoft · VS Code", "outcome": "STAYED",
         "body": ("The closest architectural twin. A C++ text buffer was tried and reverted, with the "
                  "verdict 'We tried. It didn't work out for us' — converting strings across the V8 "
                  "boundary ate the gains. The fix was a better data structure in TypeScript. Rust did "
                  "win once, as ripgrep, a whole subprocess exchanging bulk results.",
                  "架构上最接近的一个。C++ 文本缓冲区试过又退回，结论是 'We tried. It didn't work out for "
                  "us' —— 字符串跨 V8 边界转换把收益吃掉了。真正的解法是在 TypeScript 里换个更好的数据结构。"
                  "Rust 确实赢过一次，就是 ripgrep，一个整进程、批量交换结果。"),
         "match": ("Electron plus TypeScript desktop app, native only at coarse seams, same boundary "
                   "question",
                   "同样是 Electron 加 TypeScript 的桌面应用，只在粗粒度接缝上用原生，同一个边界问题"),
         "mismatch": ("an editor with no crypto core and a far weaker adversary model",
                      "那是个没有加密内核的编辑器，对手模型弱得多"),
         "regime": "first-party engineering blog, 2018 buffer work",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "Tauri on Linux · the WebKitGTK reality", "outcome": "STAYED",
         "body": ("The measured state of the Rust-shell option. Tauri's own maintainers wrote that they "
                  "cannot fully recommend Tauri for Linux and that WebKitGTK is getting worse each "
                  "release; one app was recorded at 40fps on WebKitGTK against 240fps after moving to "
                  "Electron. On Windows the substitute webview is Chromium, so the C++ does not leave.",
                  "Rust 外壳这个方案的实测状态。Tauri 自己的维护者写过，他们没法完全推荐在 Linux 上用 "
                  "Tauri，而且 WebKitGTK 每个版本都更糟；有个应用记录到 WebKitGTK 上 40fps，换成 Electron "
                  "后 240fps。Windows 上替代的 webview 就是 Chromium，所以 C++ 并没有走。"),
         "match": ("exactly the option under assessment, on exactly the three platforms Signal's README "
                   "commits to",
                   "正好是被评估的那个方案，也正好在 Signal README 承诺的那三个平台上"),
         "mismatch": ("issue-tracker and maintainer statements rather than a controlled benchmark of "
                      "Signal itself",
                      "是 issue 记录和维护者说法，不是对 Signal 本身的受控基准"),
         "regime": "maintainer statements and issue reports, 2023-2026",
         "source_label": "first-party · project issue tracker",
         "url": "https://github.com/tauri-apps/tauri/discussions/8524"},
        {"name": "Google · Android memory-safety program", "outcome": "MIGRATED",
         "body": ("The strongest safety numbers anywhere, and they argue for scope discipline. Memory "
                  "safety fell from 76% of Android vulnerabilities in 2019 to under 20% in 2025 without "
                  "a mass rewrite — new code safe, old C/C++ left to decay. Their own decay finding: "
                  "five-year-old code carries 3.4 to 7.4 times lower vulnerability density than new code.",
                  "现存最强的一组安全数字，而它们支持的是范围纪律。Android 漏洞里内存安全的占比从 2019 年 "
                  "76% 降到 2025 年不足 20%，靠的不是大规模重写 —— 新代码用安全语言写，老的 C/C++ 让它自然"
                  "衰减。他们自己的衰减结论是：五年前的代码，漏洞密度比新代码低 3.4 到 7.4 倍。"),
         "match": ("a Signal sibling platform, and the same strategy Signal ran with libsignal: safe "
                   "language at the native layer, no application rewrite",
                   "Signal 的姊妹平台，而且和 Signal 用 libsignal 跑的是同一套策略：原生层换安全语言，应用"
                   "不重写"),
         "mismatch": ("an OS with millions of lines of its own C/C++; Signal Desktop wrote 308",
                      "那是个自己有几百万行 C/C++ 的操作系统；Signal Desktop 写了 308 行"),
         "regime": "Android vulnerability data, 2019-2025",
         "source_label": "first-party · security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
        {"name": "Mozilla · Stylo vs Servo", "outcome": "MIGRATED",
         "body": ("One organisation ran both experiments. The extracted CSS engine shipped in Firefox 57 "
                  "after about two years, started by two engineers. The whole-engine replacement was "
                  "estimated at thousands of engineer-years against a handful of available heads, and in "
                  "2020 the team was laid off. Holley's line: the desire to throw everything away tends "
                  "to be an emotional one.",
                  "一个组织把两个实验都跑了。抽出来的 CSS 引擎在 Firefox 57 上线，用了约两年，起步时两个人。"
                  "整引擎替换的估算是数千工程师年，而实际能投的只有几个人，2020 年团队被裁。Holley 的原话是："
                  "想把一切推倒重来，这种愿望往往是情绪性的。"),
         "match": ("a security-motivated org choosing between a scoped extraction and a whole-shell "
                   "replacement, which is this decision",
                   "一个有安全动机的组织在「限定范围抽取」和「整体替换外壳」之间选，正是这次的决策"),
         "mismatch": ("both sides of that experiment were C++; neither was a memory-safe application "
                      "shell",
                      "那个实验两边都是 C++，没有一边是内存安全的应用外壳"),
         "regime": "first-party retrospective, 2017; layoffs 2020",
         "source_label": "first-party · engineer blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
    ],

    "path": [
        {"title": ("Classify Signal Desktop's own advisories by root cause",
                   "把 Signal Desktop 自己的公告按根因分类"),
         "body": ("Before anyone scopes a rewrite, the security team publishes the breakdown: how many "
                  "past Signal Desktop findings were memory safety, and in which component. Sort them "
                  "into Chromium, a packaged .node module, Signal's own TypeScript, and everything else. "
                  "The step passes when every advisory in the window has a component and a class. If "
                  "almost none land in Signal's own code, the shell question is closed on data rather "
                  "than on this report's structural argument. Nothing ships here.",
                  "在任何人给重写划范围之前，安全团队先把分布公布出来：过去 Signal Desktop 的发现里有多少是"
                  "内存安全问题，分别落在哪个组件。按 Chromium、打包的 .node 模块、Signal 自己的 "
                  "TypeScript、其他四类归档。通过标准是窗口内每条公告都有组件和缺陷类。如果几乎没有一条落在 "
                  "Signal 自己的代码里，外壳这个问题就靠数据结案，而不是靠这份报告的结构论证。这一步不发任何"
                  "东西。"),
         "owner": "Signal security team",
         "cost_range": ("1-2 weeks", "1-2 周"),
         "artifact": "a root-cause classification of Signal Desktop advisories into Chromium, packaged native modules, Signal's own TypeScript, and other",
         "acceptance": "every advisory in the chosen window carries a component and a defect class",
         "stop": "close the shell-rewrite question on data if almost no memory-safety finding lands in code Signal owns",
         "rollback": "measurement only; no code changes"},
        {"title": ("Sandbox the main window, or write down why not",
                   "把主窗口 sandbox 打开，或者写清为什么不能"),
         "body": ("Desktop maintainers take the one window at app/main.main.ts:721 that runs with "
                  "sandbox: false and try to move it to true, relocating whatever the preload needs from "
                  "node:fs and node:vm behind IPC. The step passes when the main renderer runs sandboxed "
                  "with conversations, attachments and calls all working on all three platforms. If some "
                  "capability cannot move, publish which one and why, so the residual risk is named "
                  "instead of implied. Rollback is one boolean.",
                  "Desktop 维护者拿 app/main.main.ts:721 那个 sandbox: false 的窗口，试着改成 true，把 "
                  "preload 需要的 node:fs、node:vm 能力挪到 IPC 后面。通过标准是主渲染进程在 sandbox 下运行，"
                  "会话、附件、通话在三个平台上都正常。如果确实有某个能力挪不动，就把是哪个、为什么公布出来，"
                  "让残余风险被点名而不是被暗示。回滚就是一个布尔值。"),
         "owner": "Signal Desktop maintainers",
         "cost_range": ("4-8 weeks", "4-8 周"),
         "artifact": "the main renderer running with sandbox: true, or a written statement of the capability that blocks it",
         "acceptance": "conversations, attachments and calls all work sandboxed on Windows, macOS and Linux",
         "stop": "stop and publish the blocking capability if a required preload API cannot move behind IPC",
         "rollback": "flip one boolean back at app/main.main.ts:721"},
        {"title": ("Extend the libsignal sanitizer set format by format",
                   "按格式逐个扩大 libsignal 的 sanitizer 覆盖"),
         "body": ("The libsignal team takes the next untrusted format after MP4 and puts a Rust "
                  "sanitizer in front of it, wired the way handleVideoAttachment already wires mp4san. "
                  "webpsan is already in the crate and unused by Desktop, so that is the cheapest first "
                  "move. Each format passes when a corpus of malformed files is rejected without "
                  "crashing and well-formed files round-trip unchanged. If a sanitizer starts rejecting "
                  "files real users send, turn its flag off and keep the format on the old path.",
                  "libsignal 团队在 MP4 之后挑下一个不可信格式，在它前面放一个 Rust sanitizer，接线方式照 "
                  "handleVideoAttachment 现在接 mp4san 的样子。webpsan 已经在 crate 里而 Desktop 还没用，"
                  "所以这是最便宜的第一步。每个格式的通过标准是：一批畸形文件被拒且不崩，正常文件原样往返。"
                  "如果某个 sanitizer 开始拒真实用户发的文件，就把它的开关关掉，那个格式走回老路径。"),
         "owner": "libsignal team, with Desktop wiring the call site",
         "cost_range": ("6-10 weeks per format", "每个格式 6-10 周"),
         "artifact": "one additional format sanitized in Rust before the renderer decodes it, starting with webp",
         "acceptance": "a malformed-input corpus is rejected without crashing and well-formed files round-trip byte-identical",
         "stop": "disable the per-format flag and revert to the old path if real user files start being rejected",
         "rollback": "feature flag per format; the .node seam is unchanged"},
        {"title": ("Price the SQLCipher question separately, and not as a language question",
                   "SQLCipher 单独定价，而且别当成语言问题"),
         "body": ("Someone writes the assessment for @signalapp/sqlcipher on its own terms. It is C, it "
                  "holds every message, and Signal maintains the fork. The document has to answer the "
                  "data question before the language one: what reads existing databases, what the "
                  "migration looks like for a user with years of history, and what happens when it fails "
                  "halfway. No engine swap is authorized without that. Until it exists, the current "
                  "SQLCipher continues.",
                  "找人把 @signalapp/sqlcipher 按它自己的条件评一遍。它是 C，存着全部消息，而且这个 fork 由 "
                  "Signal 维护。文档必须先回答数据问题，再回答语言问题：谁来读已有的库、对一个有多年历史的"
                  "用户迁移长什么样、迁到一半失败了怎么办。没有这份东西，不批准换引擎。在它出现之前，现在的 "
                  "SQLCipher 原样继续。"),
         "owner": "whoever proposes the engine swap",
         "cost_range": ("2-3 weeks for the assessment", "评估 2-3 周"),
         "artifact": "a written assessment of the SQLCipher dependency covering on-disk format compatibility, migration for existing users, and failure recovery",
         "acceptance": "the document answers the data-migration question before the language question",
         "stop": "no engine swap proceeds without it",
         "rollback": "the current SQLCipher continues unchanged"},
    ],

    "migration_checks": [
        {"name": ("Causal attribution", "因果归因"), "state": "HIT",
         "claim": ("The proposal borrows the memory-safety case from libsignal's C predecessor and "
                   "applies it to TypeScript. Those 555,145 lines never had the defect class the "
                   "argument is built on.",
                   "提案把 libsignal 那个 C 前身的内存安全理由借过来，套到 TypeScript 上。那 555,145 行里"
                   "从来没有过这个论证赖以成立的缺陷类。"),
         "evidence": "G2 · 0 tracked .rs files, 308 lines of native code, 555,145 lines of TS/TSX"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "HIT",
         "claim": ("A Rust host swaps the rendering engine rather than removing it. On Windows the "
                   "replacement webview is Chromium, so the C++ that decodes hostile media survives the "
                   "migration intact.",
                   "Rust 宿主是把渲染引擎换掉，不是拿掉。Windows 上替代的 webview 就是 Chromium，所以解码"
                   "敌意媒体的那些 C++ 迁移完照旧。"),
         "evidence": "D3 · Tauri issue 5889 · package.json:245"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("68 locales, 429 aria- attribute lines and IME behaviour are the parts a rewrite "
                   "reproduces last and cannot skip. The 2025 Rust GUI survey names accessibility and "
                   "IME as the recurring gaps.",
                   "68 种语言、429 行 aria- 属性和输入法行为，是重写最后才补得上、又不能跳过的部分。2025 年"
                   "那份 Rust GUI 调查点名的短板正是无障碍和输入法。"),
         "evidence": "D9 · _locales (68) · 429 aria- lines in ts/components"},
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("The footprint half of the proposal rests on one macOS measurement of a different "
                   "application. No profile of Signal Desktop exists, so the report attaches no interval "
                   "to it.",
                   "提案里占用那一半，靠的是对另一个应用在 macOS 上的一次测量。Signal Desktop 没有 "
                   "profile，所以报告不给它任何区间。"),
         "evidence": "D2, D4 · gethopp.app measurement, N=1"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The rewrite's cost is priced against the release train rather than against an idle "
                   "team: 394,240 product lines, 760 commits in six months, 56 stable releases in "
                   "twelve.",
                   "重写的成本是对着发布列车定价的，不是对着一个闲着的团队：产品代码 394,240 行，半年 760 "
                   "个提交，一年 56 个稳定版。"),
         "evidence": "D11 · GitHub API counts retrieved 2026-08-02"},
    ],
    "staying_checks": [
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "HIT",
         "claim": ("Staying leaves C and C++ in the process. Chromium decodes every image, "
                   "SQLCipher holds every message, and ringrtc carries WebRTC. The report names all "
                   "three instead of hiding them behind the word TypeScript.",
                   "不动，就意味着进程里真的还有 C 和 C++。Chromium 解码每一张图，SQLCipher 存着每一条消息，"
                   "ringrtc 里装着 WebRTC。报告把三个都点名，没有拿 TypeScript 这个词把它们盖住。"),
         "evidence": "D6 · package.json:127-130 · 8 packaged .node binaries"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("One of eight windows runs with the Chromium sandbox off, and it is the one rendering "
                   "conversations. Signal's maturity is not counted here as safety; the gap is stated and "
                   "given an owner.",
                   "八个窗口里有一个关着 Chromium sandbox，而它正是渲染会话的那个。这里没有把 Signal 的成熟"
                   "度当成安全；这个口子被写出来了，也指定了负责人。"),
         "evidence": "app/main.main.ts:721 · reversible path step 2"},
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("The in-stack alternatives are shipping, not hypothetical. mp4san runs on every MP4 "
                   "attachment today, and twelve injection lint rules hold at zero exceptions inside "
                   "Signal's own code.",
                   "栈内的替代方案是在发的，不是假想的。mp4san 今天就跑在每个 MP4 附件上，12 条注入类 lint "
                   "规则在 Signal 自己的代码里保持零例外。"),
         "evidence": "D12 · ts/util/handleVideoAttachment.preload.ts:34 · ts/util/lint/exceptions.json"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report records the Tauri footprint result as SUPPORTS for the Rust shell rather "
                   "than dismissing it, and names the measurement that would move it off WEAK.",
                   "报告把 Tauri 的占用结果记为对 Rust 外壳 SUPPORTS，没有一笔抹掉，还点名了能把它从 WEAK "
                   "推上去的那次测量。"),
         "evidence": "D4 SUPPORTS · rust-shell, WEAK, with change trigger"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The staying option carries an escalation rule. If the advisory classification puts "
                   "memory-safety findings in code Signal owns, the EXTRACT and PARTIAL options move up.",
                   "不动这个方案带一条升级规则。如果公告分类显示内存安全问题落在 Signal 自己的代码里，"
                   "EXTRACT 和 PARTIAL 方案就往前排。"),
         "evidence": "reversible path step 1 · D1 change trigger"},
    ],

    "gaps": [
        (("Root-cause classification of Signal Desktop's own advisory history",
          "Signal Desktop 自身历史公告的根因分类"),
         ("No public breakdown exists of which past findings were memory safety and which component held "
          "them. It would either close the shell question on data or move the EXTRACT option up.",
          "没有公开资料说明过去哪些问题属于内存安全、分别落在哪个组件。它要么用数据把外壳问题结案，要么把 "
          "EXTRACT 方案往前推。")),
        (("A startup and steady-state profile of Signal Desktop",
          "Signal Desktop 的启动与稳态 profile"),
         ("Without one, D2 stays UNKNOWN and the footprint half of any shell proposal has no interval in "
          "any language.",
          "没有它，D2 停在 UNKNOWN，任何外壳提案里占用那一半，换什么语言都给不出区间。")),
        (("An audit of what the 8 packaged native modules parse",
          "对打包进去的 8 个原生模块各自解析什么的审计"),
         ("This report reads their manifests and packaging, not their internals. If one of them decodes "
          "attacker-chosen bytes, it belongs in the EXTRACT scope.",
          "本报告读的是它们的清单和打包方式，不是内部实现。如果其中某个在解码攻击者选定的字节，它就该进 "
          "EXTRACT 的范围。")),
        (("A current first-party figure for the C++ Electron actually bundles",
          "Electron 实际打包的那部分 C++ 的当期一手数字"),
         ("The ~36M SLOC figure is a third-party aggregate for the whole Chromium tree, retrieved "
          "2024-02-19. The asymmetry argument does not depend on its precision, and the report does not "
          "lean on it.",
          "~36M SLOC 是第三方对整棵 Chromium 树的汇总，2024-02-19 取得。不对称这个论点不依赖它的精度，"
          "报告也没有把重量压在它上面。")),
    ],

    "assumptions": [
        "The shallow clone at commit 34fa4531bb74725ab2edb04a18a4e3542eea2694 represents the shipped tree; dependencies are read from package.json and pnpm-workspace.yaml as they ship.",
"No RFC was supplied, so the assessment takes the commonly stated proposal: libsignal's C to Rust migration succeeded, therefore rewrite the Signal Desktop app shell in Rust too. It is read as replacing the Electron host and the TypeScript UI, the Tauri-shaped option.",
        "libsignal figures come from a separate shallow clone of signalapp/libsignal at 622d0d5 on 2026-08-02, counted on the same tracked-file basis as Signal Desktop.",
        "Chromium and Node versions for electron 43.0.0 are taken from Electron's own v43.0.0 release notes via the GitHub API, not from a build of Signal Desktop.",
        "'Code-extension lines' means tracked .ts, .tsx, .js, .mjs, .cjs, .c, .cpp and .mm files, 567,505 lines in total. Percentages in this report use that basis and no other.",
    ],
    "objective": {
        "driver": "memory safety against a nation-state adversary",
        "requirement": "reduce memory-unsafety exposure on the path that handles bytes a hostile sender chose, without breaking behaviour on Windows, macOS and Linux or the 68 shipped locales",
        "baseline": "555,145 lines of memory-safe TypeScript and TSX; 308 lines of native code Signal wrote; 8 packaged prebuilt .node binaries; Chromium 150.0.7871.46 shipped via electron 43.0.0",
        "target": "class elimination wherever untrusted bytes are decoded by memory-unsafe code",
    },
    "repository": {
        "path": "https://github.com/signalapp/Signal-Desktop",
        "commit": "34fa4531bb74725ab2edb04a18a4e3542eea2694",
        "scope": "whole repository; the untrusted-byte decode path and the packaged native modules are the candidate seam",
        "sampling": "shallow clone; 4,378 tracked files enumerated; ts/, app/, packages/, protos/, _locales/ and package.json measured; signalapp/libsignal cloned separately at 622d0d5 for comparison; no build, benchmark or profiling was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "signalapp/Signal-Desktop at 34fa453 · static read-only analysis · why-not-rust method 2.0",
        "signalapp/Signal-Desktop @ 34fa453 · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/signalapp/Signal-Desktop at commit "
        "34fa4531bb74725ab2edb04a18a4e3542eea2694, shallow clone, 4,378 tracked files. Scope: the whole "
        "repository, with the untrusted-byte decode path and the 8 packaged native modules as the "
        "candidate seam. Sampling: 1,769 .ts files hold 363,483 lines and 995 .tsx files hold 191,662, "
        "so 2,764 files and 555,145 lines. Each was checked to be TypeScript rather than translation XML. "
        "Tracked .rs files: 0. Native source is 3 files and 308 lines: packages/lame/wrapper.c (58), "
        "packages/mute-state-change/addon.mm (102), packages/windows-ucv/addon.cpp (148). Every "
        "percentage in this report uses one basis, the 567,505 tracked code-extension lines (.ts, .tsx, "
        ".js, .mjs, .cjs, .c, .cpp, .mm); on that basis TS+TSX is 97.8% and native is 0.05%. Excluding "
        "the 11,551 lines of .mjs build tooling the TS+TSX share is 99.85%; both figures are stated so "
        "neither basis is hidden. Product TS/TSX excluding test directories, Storybook stories, fixtures "
        "and tooling is 1,971 files and 394,240 lines. ts/components is 746 files and 154,588 lines. "
        "package.json declares 9 runtime dependencies plus 1 optional; 8 of them are packaged as prebuilt "
        ".node binaries at package.json:621-629, because JavaScript libraries are bundled by rolldown "
        "from devDependencies rather than shipped as node_modules. @signalapp/libsignal-client 0.98.0 is "
        "pinned at package.json:127 and electron 43.0.0 at package.json:245; Electron's own v43.0.0 "
        "release notes, read through the GitHub API, name Chromium 150.0.7871.46, Node 24.147.0 and V8 "
        "15.0. app/main.main.ts constructs 8 BrowserWindows; 7 set sandbox: true and the main window at "
        "line 721 sets sandbox: false. ts/util/lint/rules.json holds 12 injection rules and "
        "exceptions.json holds 45 exceptions, all 45 inside node_modules. _locales holds 68 languages. "
        "libsignal was measured on a separate shallow clone at 622d0d5: 584 tracked .rs files, 182,247 "
        "lines, with rust/net at 59,082, rust/bridge at 40,358, rust/protocol at 25,797 and rust/media at "
        "117. GitHub API facts: libsignal-protocol-c archived, last push 2020-07-31; libsignal created "
        "2020-09-12; 760 Signal-Desktop commits since 2026-02-02; 56 stable and 66 beta or alpha releases "
        "since 2025-08-01. No build, test, benchmark, profiler or packaging step was run against either "
        "project. Objective: no RFC was supplied, so the assessment takes the proposal the brief poses, "
        "reading the Rust shell as a Tauri-shaped replacement of the Electron host and the TypeScript UI. "
        "User-supplied facts: none. No Amdahl calculation appears: the tree contains no perf artifact and "
        "no public profile of Signal Desktop exists, so D2 is UNKNOWN and there is no defensible f. The "
        "one external estimate quoted, ~36M Chromium SLOC, is a third-party aggregate for the whole "
        "Chromium tree retrieved 2024-02-19; it is context and no gate rests on it. The decision turns on "
        "G2, which fails on a direct structural measurement, and is confirmed by G3 and G4. Nothing in "
        "the scanned content attempted to steer this assessment. This is a structured decision protocol, "
        "not a statistical predictor.",
        "仓库：github.com/signalapp/Signal-Desktop，commit 34fa4531bb74725ab2edb04a18a4e3542eea2694，"
        "shallow clone，4,378 个纳管文件。范围：整个仓库，候选接缝是不可信字节的解码路径和打包进去的 8 个"
        "原生模块。采样：1,769 个 .ts 文件 363,483 行，995 个 .tsx 文件 191,662 行，合计 2,764 个文件、"
        "555,145 行。逐一核对过它们确实是 TypeScript，不是翻译用的 XML。纳管的 .rs 文件：0 个。原生源码 3 "
        "个文件、308 行：packages/lame/wrapper.c（58）、packages/mute-state-change/addon.mm（102）、"
        "packages/windows-ucv/addon.cpp（148）。本报告所有百分比只用一个口径，即纳管的 567,505 行代码类"
        "扩展名文件（.ts、.tsx、.js、.mjs、.cjs、.c、.cpp、.mm）；在这个口径下 TS+TSX 占 97.8%，原生占 "
        "0.05%。如果把 11,551 行 .mjs 构建脚本排掉，TS+TSX 占 99.85%；两个数都写出来，哪个口径都不藏。"
        "去掉测试目录、Storybook stories、fixtures 和工具脚本后的产品 TS/TSX 是 1,971 个文件、394,240 行。"
        "ts/components 是 746 个文件、154,588 行。package.json 声明 9 个运行时依赖加 1 个可选依赖；其中 8 个"
        "在 package.json:621-629 以预编译 .node 二进制打包，因为 JavaScript 库是 rolldown 从 "
        "devDependencies 打包进来的，不作为 node_modules 发布。@signalapp/libsignal-client 0.98.0 锁在 "
        "package.json:127，electron 43.0.0 锁在 package.json:245；通过 GitHub API 读到的 Electron v43.0.0 "
        "发布说明写明 Chromium 150.0.7871.46、Node 24.147.0、V8 15.0。app/main.main.ts 建了 8 个 "
        "BrowserWindow，7 个设 sandbox: true，第 721 行的主窗口设 sandbox: false。"
        "ts/util/lint/rules.json 有 12 条注入类规则，exceptions.json 有 45 条例外，45 条全在 node_modules "
        "里。_locales 下有 68 种语言。libsignal 在另一个 shallow clone 上测量，commit 622d0d5：584 个纳管 "
        ".rs 文件、182,247 行，其中 rust/net 59,082 行、rust/bridge 40,358 行、rust/protocol 25,797 行、"
        "rust/media 117 行。GitHub API 事实：libsignal-protocol-c 已归档，最后推送 2020-07-31；libsignal 建"
        "于 2020-09-12；Signal-Desktop 自 2026-02-02 起 760 个提交；自 2025-08-01 起 56 个稳定版、66 个 "
        "beta 或 alpha。没有对任何一个项目做过构建、测试、基准、profiling 或打包。目标：没有人给出 RFC，"
        "因此按任务里提的那个提案评估，并把 Rust 外壳理解为 Tauri 形态的替换，即换掉 Electron 宿主和 "
        "TypeScript UI。用户提供的事实：无。本报告没有 Amdahl 计算：树里没有任何性能产物，也不存在公开的 "
        "Signal Desktop profile，所以 D2 记 UNKNOWN，没有站得住的 f。唯一引用的外部估算 ~36M Chromium "
        "SLOC 是第三方对整棵 Chromium 树的汇总，2024-02-19 取得；它只是背景，没有任何一道门压在它上面。"
        "决策落在 G2 上，这道门是在一项直接的结构测量上失败的，G3 和 G4 予以确认。扫到的内容里没有出现试图"
        "引导本次评估的文本。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 34fa453 · no build, benchmark or network call against the target",
        "公开仓库 · 在 commit 34fa453 上做静态分析 · 没有对目标做构建、基准或网络调用",
    ),
}
