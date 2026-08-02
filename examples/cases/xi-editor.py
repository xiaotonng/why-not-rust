"""xi-editor/xi-editor — the language kept its promises; the pipe between processes did not.

Repository facts were measured read-only on the shallow clone named in
`repository`. History, stars, contributor count and crates.io figures come from
the GitHub and crates.io APIs on 2026-08-02, because the clone is `--depth 1`.
The author's retrospective and his CRDT postmortem are quoted verbatim and
labelled as first-party account, not measurement.
"""

RETRO = "https://raphlinus.github.io/xi/2020/06/27/xi-retrospective.html"
CRDT_POST = "https://github.com/xi-editor/xi-editor/issues/1187#issuecomment-491473599"

CASE = {
    "slug": "xi-editor",
    "project_name": "xi-editor/xi-editor",
    "project_desc": (
        "Rust · discontinued editor core · 39,292 lines of Rust in 103 files · no front end in this repo",
        "Rust · 已停止维护的编辑器内核 · 39,292 行 Rust，103 个文件 · 这个仓库里没有前端",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · editor core behind a cross-process JSON-RPC boundary",
        "native-desktop-gui · 编辑器内核藏在一条跨进程 JSON-RPC 边界后面",
    ),

    "scope_word": "EXTRACT",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "rust-kernel-inproc",
    "scope_chip": (
        "keep the Rust buffer kernel; link it in the UI process, drop the RPC",
        "留下 Rust 缓冲区内核；链进 UI 进程，去掉 RPC",
    ),
    "scope_sub": (
        "take the kernel that survived, not the architecture that didn't",
        "拿走活下来的那个内核，别抄那套架构",
    ),

    "why": (
        "Three choices get blamed as one. xi picked Rust, then a separate core process speaking "
        "JSON-RPC, then async plugins that needed a CRDT to stay consistent. This tree holds 7,601 "
        "lines of protocol, plugin-host and shadow-cache code against 3,089 lines of editing "
        "operations. Levien's verdict on the boundary: \"I now firmly believe that the process "
        "separation between front-end and core was not a good idea.\" On the CRDT: \"a pretty bad case "
        "of YAGNI.\" Rust draws no such sentence. It did force the split, though. In 2016 the language "
        "\"was nowhere near capable of native GUI.\"",

        "三个决定被当成一个来骂。xi 选了 Rust，然后把 core 拆成独立进程走 JSON-RPC，然后让插件异步，异步又"
        "逼出一套 CRDT 来保证一致。这棵树里，协议、插件宿主加影子缓存合计 7,601 行，编辑操作 3,089 行。"
        "Levien 对那条边界的结论：\"I now firmly believe that the process separation between front-end "
        "and core was not a good idea.\" 对 CRDT：\"a pretty bad case of YAGNI.\" Rust 没有得到这样一句"
        "判词。但它确实把那条边界逼出来了——2016 年的 Rust \"was nowhere near capable of native GUI\"。",
    ),
    "trigger": (
        "Conditional on where the boundary sits. The 2016 constraint that forced the split is gone; "
        "Rust draws its own windows now, and two editors shipped on that shape. Put a per-keystroke "
        "IPC hop back in front of the kernel and G4 fails again. This repository is the price list: "
        "100 wire methods, no version negotiation, and a five-op cache-diff program the front end has "
        "to replay before it can paint.",

        "条件是那条边界摆在哪。2016 年逼出进程拆分的约束已经没了：Rust 现在能自己画窗口，而且已经有两个编辑器"
        "按这个形状发出来了。要是把「每次按键过一趟 IPC」重新塞回内核前面，G4 还是会挂。这个仓库就是价目表："
        "100 个 wire 方法、没有版本协商，还有一段前端必须先重放完才能画屏的五操作缓存 diff 程序。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("A 16 ms budget, and the defects it produced are named first-party.",
                           "16 ms 的预算，以及它造成的具体故障，作者自己点了名。"),
         "name": "requirement",
         "evidence": "README.md:16 sets the target: every editing operation commits and paints in under 16 ms. The as-built design missed it in ways the author enumerates — word-wrap races while live-resizing a window, tearing artifacts, and scrolling that \"took months to get it right\". No profile or benchmark result exists anywhere in this tree, so the requirement is carried by first-party account rather than measurement."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果归属"),
         "hero_evidence": ("Contained complexity behind a safe interface. Not speed.",
                           "把复杂度关在安全接口后面。不是速度。"),
         "name": "rust-specific causality",
         "evidence": "The Rust-specific mechanism is containment, and Levien states it about the rope: \"the implementation has complexity, but that complexity is contained. It doesn't leak out.\" Structurally, 16 of the 9,522 lines in rust/rope/src mention unsafe and all 16 sit in one SIMD comparison file. The speed half is not Rust-specific by the project's own README, which says that level of performance \"is possible in C++\" (README.md:108)."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("The kernel is written and published. The boundary shipped nothing.",
                           "内核已经写好并发布。那条边界什么也没交付。"),
         "name": "economics and smallest sufficient option",
         "evidence": "rust/rope is 9,522 lines and shipped as the xi-rope crate; the Lapce fork lapce-xi-rope has 129,043 downloads and released 0.4.0 in December 2025. Against that, 7,601 lines of cross-process machinery produced no usable editor. Levien prescribes the smaller option himself: \"a much brighter future with a simpler, largely synchronous model, that still of course has enough revision tracking to get good results with asynchronous peers like the language server.\""},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("One process, one build, one cargo line to back out.",
                           "一个进程，一次构建，回滚就是删掉一行 cargo 依赖。"),
         "name": "delivery and reversibility",
         "evidence": "Two editors shipped on this shape after xi stopped: Lapce (38,719 stars) links lapce-xi-rope directly, and Zed built its own kernel and its own GPU UI in one process. xi's own shape did not ship. 100 wire methods across a protocol with no version negotiation (docs/docs/frontend-notes.md:32-37), no front end in this repository (README.md:6), and a README that at the final commit still calls the editor \"in its early stages\" and \"missing essentials such as auto-indent\" (README.md:141-145)."},
    ],

    "tiles": [
        (("Stated frame budget", "写明的帧预算"), "16", ("ms", "ms"),
         ("README.md:16 · nothing in this tree measures against it",
          "README.md:16 · 这棵树里没有任何东西对着它测过")),
        (("Cross-process machinery", "跨进程机械"), "7,601", ("lines", "行"),
         ("rpc + plugin-lib + lsp-lib + plugins/ + rpc.rs + client.rs + line_cache_shadow.rs",
          "rpc + plugin-lib + lsp-lib + plugins/ + rpc.rs + client.rs + line_cache_shadow.rs")),
        (("Editing operations behind it", "它背后的编辑操作"), "3,089", ("lines", "行"),
         ("editor, edit_ops, movement, selection… the boundary is 2.46×",
          "editor、edit_ops、movement、selection…… 边界是它的 2.46 倍")),
        (("Wire methods a front end must speak", "前端必须实现的 wire 方法"), "100", ("methods", "个"),
         ("rust/core-lib/src/rpc.rs · protocol never versioned",
          "rust/core-lib/src/rpc.rs · 协议始终没有版本")),
        (("The rope", "那个 rope"), "9,522", ("lines", "行"),
         ("rust/rope · shipped as xi-rope; the Lapce fork still releases",
          "rust/rope · 以 xi-rope 发布；Lapce 的 fork 还在发版")),
        (("Core binary, Linux release build", "core 二进制，Linux release 构建"), "9.3", ("MB", "MB"),
         ("first-party: \"a great deal of that bloat is serialization\"",
          "作者原话：\"a great deal of that bloat is serialization\"")),
    ],

    "options_sub": (
        "One objective for every option. A native desktop UI must commit and paint an edit inside the "
        "stated 16 ms, on a buffer large enough that the data structure matters. Plugins that need to "
        "think slowly still have to work.",
        "所有方案对着同一个目标。原生桌面 UI 要在写明的 16 ms 内提交并画完一次编辑，而且缓冲区大到数据结构会"
        "起作用。那些需要慢慢想的插件也得照样能用。",
    ),
    "options": [
        {"id": "rust-kernel-inproc",
         "name": ("Rust buffer kernel linked into the UI process", "Rust 缓冲区内核链进 UI 进程"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("the UI queries text synchronously; the race class disappears",
                              "UI 同步查文本；那一整类竞态消失"),
         "one_time_cost": "one dependency plus a C ABI shim when the UI is not Rust",
         "recurring_cost": "a Rust toolchain in the app build",
         "cost_cell": ("one dependency; a shim if the UI isn't Rust", "一个依赖；UI 不是 Rust 时要写一层 shim"),
         "time_to_value": ("days to link, weeks to measure", "链进去几天，测出来几周"),
         "compatibility": "in-process library call; no protocol to keep compatible",
         "compat_cell": ("one process · drop the dependency to revert", "单进程 · 删依赖即回滚"),
         "reversibility": "remove the crate",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the option Levien himself prescribes", "推荐 · Levien 自己开的方子"),
         "reason": "Keeps the artifact that survived and removes the boundary the author names as the mistake. Cheapest of the retained options and the only one that is a single build-time decision."},
        {"id": "xi-as-built",
         "name": ("What xi built: core process, JSON-RPC, async plugins, CRDT",
                  "xi 的实际做法：core 独立进程、JSON-RPC、异步插件、CRDT"),
         "implementation": "rust",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("plugins can never block typing; nothing else was delivered",
                              "插件永远卡不住打字；除此之外没交付出什么"),
         "one_time_cost": "39,292 lines of Rust over four years",
         "recurring_cost": "an unversioned protocol against twelve listed front ends",
         "cost_cell": ("39,292 lines; permanent protocol debt", "39,292 行；永久的协议负债"),
         "time_to_value": ("never reached a usable editor", "始终没做出一个能用的编辑器"),
         "compatibility": "100 wire methods, no version negotiation",
         "compat_cell": ("two binaries in lockstep · no rollback", "两个二进制必须同步 · 无回滚"),
         "reversibility": "none", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · the author's own conclusion is against it", "排除 · 作者自己的结论就是反对它"),
         "reason": "Discontinued after 39,292 lines and 134 contributors, with the README still listing auto-indent as missing. Levien's retrospective rejects the front-end process split explicitly."},
        {"id": "same-arch-native",
         "name": ("The same split architecture in C++ or Swift", "同一套拆分架构，改用 C++ 或 Swift 写"),
         "implementation": "non-rust-native",
         "scope": "full", "scope_tag": "NATIVE",
         "benefit_interval": ("no change: every failure in the chain is language-independent",
                              "没有变化：这条链上的每个故障都跟语言无关"),
         "one_time_cost": "the same rewrite, minus a compiler that catches aliasing",
         "recurring_cost": "the same protocol, the same races, the same CRDT",
         "cost_cell": ("same rewrite; same protocol debt", "同样的重写；同样的协议负债"),
         "time_to_value": ("no faster", "不会更快"),
         "compatibility": "identical wire surface",
         "compat_cell": ("identical boundary · no rollback", "边界完全一样 · 无回滚"),
         "reversibility": "none", "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · included to test whether the language is the variable",
                  "排除 · 放进来是为了检验语言到底是不是变量"),
         "reason": "This is the control. Word-wrap races, the shadow line cache, the plugin API ossification and the CRDT all follow from the process split, not from Rust, so swapping the language changes none of them."},
        {"id": "host-language-buffer",
         "name": ("Write the buffer in the UI language", "缓冲区直接用 UI 那门语言写"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("no boundary at all; VS Code ships on this",
                              "根本没有边界；VS Code 就是这么发的"),
         "one_time_cost": "write and tune one data structure",
         "recurring_cost": "runtime and collector behaviour stay in the tail",
         "cost_cell": ("one data structure; keep the runtime", "一个数据结构；运行时留着"),
         "time_to_value": ("months", "数月"),
         "compatibility": "native to the host app",
         "compat_cell": ("no FFI · ordinary refactor to undo", "无 FFI · 普通重构即可撤销"),
         "reversibility": "ordinary refactor", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded counterfactual any Rust kernel must beat",
                  "保留 · 任何 Rust 内核都得先赢过这个已投入的对照"),
         "reason": "VS Code reverted a native buffer and fixed the problem with a piece tree in TypeScript. For a managed-runtime UI this is the cheaper answer; for a native UI nobody has shipped the equivalent."},
        {"id": "adopt-shipped-core",
         "name": ("Adopt an editor core that shipped", "直接采用一个已经发出来的编辑器内核"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("someone else already paid for the parity work",
                              "对齐功能这笔钱别人已经付了"),
         "one_time_cost": "learn someone else's model",
         "recurring_cost": "their roadmap, not yours",
         "cost_cell": ("learning curve; upstream roadmap", "学习成本；跟着上游路线走"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "their extension model",
         "compat_cell": ("their model · fork if it diverges", "跟着他们的模型 · 分道就 fork"),
         "reversibility": "fork", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · this repo's own README points here", "保留 · 这个仓库的 README 自己指向这里"),
         "reason": "The README names Lapce as the spiritual successor, and Lapce links a live fork of xi's rope. Adoption meets the objective for a team that does not need its own editing model."},
    ],

    "lenses_sub": (
        "Each state names the options it applies to. They are not a score. Three lenses sit at UNKNOWN "
        "because nothing in this repository measures latency, and the author's account is testimony "
        "rather than a profile.",
        "每条状态都点明它管哪些方案，这些不是可以相加的分数。三条停在 UNKNOWN，因为这个仓库里没有任何东西测过"
        "延迟；作者的说法是证词，不是 profile。",
    ),
    "na_note": (
        "Two lenses are N/A. D4 fleet economics: a desktop editor runs one instance per user, so there "
        "is no fleet to price. D5 startup shape: the editor is launched once per session. The extra "
        "process spawn and the plugin-catalog load are structural costs nobody measured, and they do "
        "not decide anything here.",
        "两条记为 N/A。D4 机队经济性：桌面编辑器每个用户跑一个实例，没有机队可算。D5 启动形态：一次会话只启动"
        "一次。多起一个进程、加载插件目录，这些是结构性开销，没人量过，也决定不了这里的任何事。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & bottleneck ownership", "需求与瓶颈归属"),
         "label": "UNKNOWN · rust-kernel-inproc, xi-as-built", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN",
         "option_ids": ["rust-kernel-inproc", "xi-as-built"],
         "claim": ("The target is stated plainly: commit and paint in under 16 ms. Nothing in this tree "
                   "measures against it. Six benchmark files exist with no published results, and the "
                   "2,150-line xi_trace crate was built to find latency across the boundary. The "
                   "repository holds no captured trace.",
                   "目标写得很清楚：提交加绘制控制在 16 ms 以内。这棵树里没有任何东西对着它测。六个 benchmark "
                   "文件，没有公开结果；2,150 行的 xi_trace crate 就是为了找跨边界的延迟而写的。仓库里没有一份"
                   "抓下来的 trace。"),
         "source": "README.md:16 · 6 benchmark files under rust/*/benches · rust/trace 2,150 lines · no trace artifact in the tree",
         "regime": "n/a — the measurement was never taken",
         "caveat": "Recorded UNKNOWN rather than inferred from line counts. Converting a line share into a time share is a method error.",
         "change_trigger": "An edit-to-paint profile at a stated file size and window width, taken in-process and across the pipe, would make the latency claim assessable."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-kernel-inproc", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-kernel-inproc"],
         "claim": ("No Amdahl figure appears in this report. The term that would dominate is the "
                   "boundary cost, and nobody timed a JSON round-trip against a keystroke. Without "
                   "that there is no defensible f and no ceiling worth quoting.",
                   "本报告不给 Amdahl 数字。真正会主导结果的是跨界开销，而没有人把一次 JSON 往返和一次按键放在"
                   "一起计时。没有这个，就没有站得住的 f，也就没有值得引用的天花板。"),
         "source": "D1 is UNKNOWN; no boundary timing exists",
         "regime": "n/a",
         "caveat": "The as-built option therefore carries no quantified latency penalty here, only the author's account of the symptoms."},
        {"id": "D3", "name": ("Tail latency & runtime", "尾延迟与运行时"),
         "label": "UNKNOWN · xi-as-built", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["xi-as-built"],
         "claim": ("The 16 ms budget is a tail claim. Neither side has a collector: the core is Rust, "
                   "the macOS front end is Swift with ARC in a separate repository. So no option here "
                   "removes a GC from the tail. Whether the pipe or serde ever blew the budget is "
                   "unrecorded; the author reports the visible symptom, which is tearing during live "
                   "resize.",
                   "16 ms 是一条尾延迟主张。两边都没有 collector：core 是 Rust，macOS 前端是 Swift 加 ARC，还在"
                   "另一个仓库里。所以这里没有哪个方案能从尾延迟里拿掉 GC。管道或者 serde 有没有把预算吃掉，"
                   "没有记录；作者记下来的是可见症状——拖动窗口改大小时画面撕裂。"),
         "source": "README.md:16 · xi-editor/xi-mac is Swift (GitHub API, 2026-08-02) · retrospective, \"Async is a complexity multiplier\"",
         "regime": "first-party account of interactive behaviour, not a trace",
         "caveat": "One Rust-specific tail cost is on the record and belongs to the protocol: the release core is 9.3 MB and the author attributes much of that to serde-generated serialization."},
        {"id": "D4", "name": ("Footprint & fleet economics", "占用与机队经济性"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("A desktop editor runs one instance per user on hardware the user already owns. "
                   "There is no fleet, no utilization curve and no price to multiply.",
                   "桌面编辑器每个用户一个实例，跑在用户自己的机器上。没有机队，没有利用率曲线，也没有单价可以"
                   "乘。"),
         "source": "desktop application shape", "regime": "n/a",
         "caveat": "Binary size is a distribution question and is assessed at D8 instead."},
        {"id": "D5", "name": ("Startup & invocation shape", "启动与调用形态"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("The editor is started once per session. The split adds a process spawn, a "
                   "client_started handshake and a plugin-catalog load, all of which the project "
                   "flagged as a startup risk. None of it was measured and none of it decides this.",
                   "编辑器一次会话只启动一次。拆分多出来的是：起一个进程、走一遍 client_started 握手、加载插件"
                   "目录——项目自己把这当成启动风险标出来过。这些都没量过，也决定不了这里的结论。"),
         "source": "docs/docs/plugin.md, \"Loading plugin info potentially has huge impact on startup time\"",
         "regime": "n/a",
         "caveat": "Kept as N/A rather than promoted to a finding; a desktop editor's startup budget is generous compared with a per-keystroke CLI."},
        {"id": "D6", "name": ("Safety & correctness delta", "安全与正确性差值"),
         "label": "SUPPORTS · rust-kernel-inproc, xi-as-built", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-kernel-inproc", "xi-as-built"],
         "claim": ("There is no C here to escape, so this is not a memory-safety rescue. What the tree "
                   "shows is a kernel whose unsafe surface is confined: 16 lines in rust/rope/src "
                   "mention unsafe and all of them sit in one SIMD comparison file. Against a C++ rope "
                   "that matters. Against a Swift or TypeScript buffer the memory-safety delta is zero.",
                   "这里没有 C 需要逃离，所以谈不上内存安全救援。树里能看到的是：内核的 unsafe 面被圈住了——"
                   "rust/rope/src 里提到 unsafe 的有 16 行，全部落在同一个 SIMD 比较文件里。对着 C++ 写的 rope，"
                   "这有意义；对着 Swift 或 TypeScript 的缓冲区，内存安全差值是零。"),
         "source": "grep -n unsafe rust/rope/src/*.rs, comment lines dropped → 16 lines, all in rust/rope/src/compare.rs",
         "regime": "static count on tracked source, tests and benches excluded",
         "caveat": "Across the whole non-test tree 24 lines mention unsafe; the other 8 are in xi_trace's pid/tid lookups and the syntect plugin."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · rust-kernel-inproc", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-kernel-inproc"],
         "claim": ("The invariant xi needed is snapshot-while-editing. Autosave takes a copy-on-write "
                   "snapshot and writes it out while the buffer stays live, which the README describes "
                   "as nearly free. Ownership encodes that by construction. What Rust does not touch "
                   "is the concurrency xi then chose: rust/rope/src/engine.rs says the mini-CRDT under "
                   "Engine::edit_rev is there so asynchronous plugins can edit against a stale "
                   "revision.",
                   "xi 需要的不变量是「一边编辑一边快照」。自动保存拿一份 copy-on-write 快照写盘，缓冲区照样能"
                   "改，README 说这几乎是免费的。所有权把这件事在编译期钉住了。Rust 碰不到的是 xi 后来选的那种"
                   "并发：rust/rope/src/engine.rs 写着，Engine::edit_rev 下面那个 mini-CRDT 的作用是让异步插件"
                   "能对着一个旧版本改。"),
         "source": "README.md:116-121 · rust/rope/src/engine.rs:16-30 · rust/rope/src/tree.rs 1,284 lines",
         "regime": "structural, read from the source and its doc comments",
         "caveat": "The same file carries a full Engine::merge path for \"peer-to-peer editing\" that xi never shipped. Levien's later verdict on that apparatus: \"the CRDT is not pulling its (considerable) weight.\""},
        {"id": "D8", "name": ("Distribution & embedding", "分发与嵌入"),
         "label": "DISFAVORS · xi-as-built", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["xi-as-built"],
         "claim": ("The split ships two binaries that must move in lockstep, over a protocol with no "
                   "version negotiation, while the README lists twelve front ends. The "
                   "core alone is 9.3 MB in a Linux release build and 88 MB in debug, and the author "
                   "attributes much of that to serialization. In-process there is one binary and "
                   "nothing to version.",
                   "拆分意味着两个二进制必须同步走，中间那条协议没有版本协商，而 README 里列了十二个第三方前端。"
                   "光 core 一个，Linux release 构建 9.3 MB，debug 88 MB，作者把其中很大一部分归给序列化。放在"
                   "同一进程里，只有一个二进制，没有协议要维护版本。"),
         "source": "docs/docs/frontend-notes.md:32-37 · README.md:57-85 (12 front ends listed) · retrospective, JSON section",
         "regime": "shipped artifact sizes reported first-party; file counts from this commit",
         "caveat": "The in-process option has its own distribution cost when the UI is not Rust: it needs a C ABI shim, and no such shim exists in this repository to price."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · rust-kernel-inproc", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-kernel-inproc"],
         "claim": ("This lens explains the architecture. Levien's stated motivation for the split was "
                   "\"to build GUI applications using Rust, even though at the time Rust was nowhere "
                   "near capable of native GUI.\" The gap has since closed. Lapce and Zed each draw "
                   "their own UI in Rust inside one process, and Lapce links a maintained fork of xi's "
                   "rope.",
                   "这一条解释了那套架构从哪来。Levien 说拆分的动机是 \"to build GUI applications using Rust, "
                   "even though at the time Rust was nowhere near capable of native GUI.\" 这个缺口后来补上"
                   "了。Lapce 和 Zed 都在单进程里用 Rust 自己画 UI，而 Lapce 链的是 xi 那个 rope 的活跃 fork。"),
         "source": RETRO + " · lapce/lapce Cargo.toml depends on lapce-xi-rope · crates.io, retrieved 2026-08-02",
         "regime": "ecosystem inventory at 2026-08-02, not at 2016",
         "caveat": "Closing that gap took years of separate work: xi-win became druid, druid's README now reads UNMAINTAINED, and the effort moved on to Xilem and Vello."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · xi-as-built", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["xi-as-built"],
         "claim": ("A front end must speak 100 wire methods, counted from the protocol enums. The "
                   "protocol never got version negotiation. Painting means replaying a five-op "
                   "cache-diff program of copy, skip, invalidate, update and ins. And the core keeps "
                   "325 lines whose only job is tracking the other process's line cache and planning "
                   "updates to it.",
                   "前端要讲 100 个 wire 方法，这是从协议 enum 里数出来的。这条协议始终没有版本协商。画屏"
                   "意味着重放一段五操作的缓存 diff 程序：copy、skip、invalidate、update、ins。core 里还另有 "
                   "325 行，唯一的活就是跟踪另一个进程的行缓存并给它规划更新。"),
         "source": "rust/core-lib/src/rpc.rs (8+3+84+2+3 leaf variants = 100) · docs/docs/frontend-protocol.md:501-540 · rust/core-lib/src/line_cache_shadow.rs 325 lines",
         "regime": "static contract inventory at commit a2dea30",
         "caveat": "Levien separates the two boundaries: \"while the process split with plug-ins is supportable (similar to the Language Server protocol), I now firmly believe that the process separation between front-end and core was not a good idea.\""},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · xi-as-built", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["xi-as-built"],
         "claim": ("39,292 lines of Rust. 134 contributors, 19,817 stars, no shipped editor. At the "
                   "final commit the README still calls it \"in its early stages\" and \"missing "
                   "essentials such as auto-indent\". Levien names the mechanism: \"far too often "
                   "things were blocking on some major architectural re-work (we have to redo the "
                   "plug-in API before you can implement that feature).\"",
                   "39,292 行 Rust。134 位贡献者，19,817 个 star，没做出一个能用的编辑器。到最后一个 commit，"
                   "README 还在说它 \"in its early stages\"、\"missing essentials such as auto-indent\"。"
                   "Levien 点出了机制：\"far too often things were blocking on some major architectural "
                   "re-work (we have to redo the plug-in API before you can implement that feature).\""),
         "source": "git ls-files '*.rs' | xargs wc -l → 39,292 · GitHub API contributors → 134 · README.md:141-145 · " + RETRO,
         "regime": "repository state at a2dea30 plus GitHub API on 2026-08-02",
         "caveat": "Substantive work on the Rust core stopped around late 2020; lint sweeps ran into April 2022, the discontinuation notice landed 2022-12-09, and the last commit of any kind is a dependabot bump on 2023-08-08. The repository is not GitHub-archived."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · host-language-buffer, adopt-shipped-core", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["host-language-buffer", "adopt-shipped-core"],
         "claim": ("Three counterfactuals shipped while xi did not. VS Code kept its buffer in "
                   "TypeScript after reverting a native one. Lapce forked xi's rope and put it "
                   "in-process. Zed wrote its own kernel and its own GPU UI, one process, no protocol. "
                   "All three are funded and running.",
                   "xi 没发出来的这段时间里，有三条对照路线发出来了。VS Code 撤掉原生缓冲区之后，把缓冲区留在 "
                   "TypeScript 里。Lapce fork 了 xi 的 rope，放进同一个进程。Zed 自己写内核、自己写 GPU UI，"
                   "单进程，没有协议。三条都有人投钱，都还在跑。"),
         "source": "VS Code text-buffer post · lapce/lapce (38,719 stars, depends on lapce-xi-rope) · zed-industries/zed",
         "regime": "shipped products, first-party engineering accounts",
         "caveat": "None of the three publishes an edit-to-paint number comparable with xi's 16 ms target, so the comparison is architectural rather than numeric."},
    ],

    "findings": [
        ("rust",
         ("The CRDT's own header says who it is for", "CRDT 自己的文件头写明了它为谁而存在"),
         ("rust/rope/src/engine.rs opens by explaining itself. The mini-CRDT under Engine::edit_rev "
          "exists so an edit can apply against an older revision, \"which is sufficient for "
          "asynchronous plugins that can only have one pending edit in flight each.\" A second and "
          "harder path, Engine::merge, is there for \"full asynchronous and even peer-to-peer "
          "editing.\" xi never shipped collaborative editing. Levien's later verdict on the whole "
          "apparatus: \"In retrospect, this was a pretty bad case of YAGNI.\"",
          "rust/rope/src/engine.rs 一开头就自我说明。Engine::edit_rev 下面那个 mini-CRDT 的存在，是为了让一次"
          "编辑能对着更早的版本生效，\"which is sufficient for asynchronous plugins that can only have one "
          "pending edit in flight each.\" 还有第二条更难的路，Engine::merge，管的是 \"full asynchronous and "
          "even peer-to-peer editing.\" xi 从来没有发布协同编辑。Levien 后来对这整套东西的判断："
          "\"In retrospect, this was a pretty bad case of YAGNI.\""),
         "rust/rope/src/engine.rs:16-30 · 1,778 lines · " + CRDT_POST),
        ("rust",
         ("The boundary is 2.46× the editing code it carries", "边界是它承载的编辑代码的 2.46 倍"),
         ("Add up the cross-process machinery — xi-rpc, plugin-lib, lsp-lib, core-lib's plugins "
          "module, its rpc.rs and client.rs, line_cache_shadow.rs and the rpc integration test. "
          "That is 7,601 lines across 29 "
          "files. The editing operations they exist to deliver come to 3,089: editor, edit_ops, "
          "edit_types, movement, selection, backspace, word boundaries, whitespace. One of the 29 "
          "files exists only to track the other process's line cache and plan its updates.",
          "把跨进程那套机械加起来——xi-rpc、plugin-lib、lsp-lib、core-lib 的 plugins 模块、它的 rpc.rs 和 "
          "client.rs、line_cache_shadow.rs，还有那个 rpc 集成测试。29 个文件，7,601 行。它们要送达的那些编辑操作合计 3,089 行："
          "editor、edit_ops、edit_types、movement、selection、backspace、词边界、空白处理。这 29 个文件里有"
          "一个，除了模拟另一个进程的行缓存什么也不干。"),
         "7,601 lines / 29 files vs 3,089 lines / 8 files · wc -l on tracked .rs"),
        ("current",
         ("Rust chose the boundary before the boundary chose the CRDT",
          "先是 Rust 选了那条边界，然后那条边界选了 CRDT"),
         ("Levien's stated reason for splitting the processes: \"the main motivation was to build GUI "
          "applications using Rust, even though at the time Rust was nowhere near capable of native "
          "GUI. The idea is that you use the best GUI technology of the platform, and communicate via "
          "async pipes.\" So the language did shape the architecture. It could not draw the window, so "
          "a pipe went in between. Closing that gap is what druid, Xilem and Vello were for, and the "
          "druid repository is literally the continued git history of xi-win.",
          "Levien 给出的拆分理由：\"the main motivation was to build GUI applications using Rust, even "
          "though at the time Rust was nowhere near capable of native GUI. The idea is that you use the "
          "best GUI technology of the platform, and communicate via async pipes.\" 所以语言确实塑造了架构。"
          "它画不出窗口，中间就插了一条管道。druid、Xilem、Vello 干的就是补这个缺口，而 druid 仓库本身就是 "
          "xi-win 的 git 历史续下来的。"),
         RETRO),
        ("unknown",
         ("Nothing in this tree measures the 16 ms budget", "这棵树里没有任何东西对着 16 ms 测过"),
         ("README.md:16 sets the goal: commit and paint in under 16 ms. The tree has six benchmark "
          "files and no published results. It also has xi_trace, 2,150 lines written to find latency "
          "across the boundary, and not one captured trace. D1, D2 and D3 are recorded UNKNOWN for "
          "that reason. The defects are on the record as the author's account, not as a profile, and "
          "this report does not upgrade testimony into measurement.",
          "README.md:16 定了目标：提交加绘制在 16 ms 以内。树里有六个 benchmark 文件，没有公开结果。还有 "
          "xi_trace，2,150 行，专门为找跨边界延迟而写，却没有一份抓下来的 trace。D1、D2、D3 因此都记 UNKNOWN。"
          "那些故障留在记录里的身份是作者的说法，不是 profile；本报告不会把证词升级成测量。"),
         "README.md:16 · 6 files under rust/*/benches · rust/trace 2,150 lines · no trace artifact"),
        ("current",
         ("What outlived the project were libraries", "活过这个项目的是几个库"),
         ("xi-unicode has 8,463,481 downloads on crates.io and 16 reverse dependencies, druid among "
          "them. The rope survived as a fork: lapce-xi-rope, 129,043 downloads, 0.4.0 released "
          "December 2025, linked by Lapce. The original xi-rope has not been released since June 2019. "
          "No linebender project depends on either one. The protocol, the plugin API and the CRDT went "
          "nowhere.",
          "xi-unicode 在 crates.io 上有 8,463,481 次下载、16 个反向依赖，druid 是其中之一。rope 是以 fork 的"
          "形式活下来的：lapce-xi-rope，129,043 次下载，0.4.0 发在 2025 年 12 月，Lapce 在用。原版 xi-rope 自 "
          "2019 年 6 月起没再发过版。linebender 名下的项目一个都没依赖这两个。协议、插件 API、CRDT，都没有走"
          "到任何地方。"),
         "crates.io · lapce/lapce Cargo.toml · retrieved 2026-08-02"),
    ],

    "buys": [
        (("A kernel whose complexity stays inside it", "一个把复杂度关在自己肚子里的内核"),
         ("Levien's own argument for the rope: \"the implementation has complexity, but that "
          "complexity is contained. It doesn't leak out.\" 16 of 9,522 lines in rust/rope/src mention "
          "unsafe, all in one SIMD file.",
          "Levien 为 rope 给出的理由：\"the implementation has complexity, but that complexity is "
          "contained. It doesn't leak out.\" rust/rope/src 里 9,522 行中有 16 行提到 unsafe，全在同一个 "
          "SIMD 文件。")),
        (("A library other people can actually pick up", "一个别人真的能拿走用的库"),
         ("xi-unicode is at 8,463,481 downloads, and the rope's Lapce fork released 0.4.0 in December "
          "2025. Cargo is why the artifact outlived the project.",
          "xi-unicode 下载 8,463,481 次，rope 的 Lapce fork 在 2025 年 12 月发了 0.4.0。这些东西能活过项目"
          "本身，靠的是 cargo。")),
        (("Nothing on the 16 ms budget, on this evidence", "16 ms 这条，按现有证据什么也买不到"),
         ("no profile, no benchmark result, no captured trace. The report names the measurement that "
          "would settle it and stops there.",
          "没有 profile，没有 benchmark 结果，没有抓下来的 trace。报告点名了能了结它的那次测量，然后就停在"
          "这里。")),
    ],
    "nobuys": [
        (("A native UI, in 2016", "2016 年的原生 UI"),
         ("Rust could not draw the window, so the core talked to a Swift app through a pipe. That "
          "pipe is the thing the author rejects.",
          "Rust 当时画不出窗口，于是 core 通过一条管道跟一个 Swift 应用说话。作者否掉的正是这条管道。")),
        (("Immunity from the async design", "对异步设计的免疫"),
         ("async plugin edits race user edits, so a CRDT went in. Rust neither charges for that nor "
          "refunds it; C++ or Swift would owe the same machinery.",
          "异步插件的编辑会跟用户的编辑抢，于是塞进一套 CRDT。这笔钱 Rust 不收也不退；换 C++ 或 Swift，同样"
          "得欠这套机械。")),
        (("Escape from an unversioned protocol", "从一份没有版本的协议里脱身"),
         ("100 wire methods and twelve listed front ends, with no version negotiation. A "
          "reimplementation in any language inherits all of it.",
          "100 个 wire 方法、列了十二个前端、没有版本协商。换任何语言重新实现，这些全都继承过来。")),
    ],

    "precedents": [
        {"name": "Mozilla · Servo", "outcome": "NEVER SHIPPED",
         "body": ("A whole-engine replacement that Holley priced at \"thousands of engineer-years\" "
                  "against \"a handful of heads\". The team was laid off in 2020 and the replacement "
                  "goal died. Stylo and WebRender shipped in Firefox instead. The R&D was not wasted; "
                  "the ambition was.",
                  "一次整引擎替换。Holley 给的价码是 \"thousands of engineer-years\"，而手上只有 \"a handful "
                  "of heads\"。2020 年团队被裁，替换这个目标就此结束。真正进 Firefox 的是 Stylo 和 WebRender。"
                  "研发没有白做，白做的是那个野心。"),
         "match": ("same shape almost exactly: an ambitious Rust moonshot that shipped components "
                   "rather than a product",
                   "形状几乎一模一样：一个野心很大的 Rust 登月项目，最后交付的是组件，不是产品"),
         "mismatch": ("a browser engine replacing C++ under commercial pressure; xi had no incumbent "
                      "to replace and no shipping deadline",
                      "那是在商业压力下用 Rust 替换 C++ 的浏览器引擎；xi 没有要替换的现任，也没有发版期限"),
         "regime": "organisational scope economics, first-party account",
         "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Microsoft · VS Code", "outcome": "STAYED",
         "body": ("They tried a native text buffer and reverted it. Their words: \"TL;DR: We tried. "
                  "It didn't work out for us.\" Converting strings across the V8 boundary ate the "
                  "gain. The fix was a better data structure in TypeScript. Meanwhile ripgrep, a Rust "
                  "binary, powers search as a whole subprocess exchanging bulk results.",
                  "他们试过原生文本缓冲区，然后撤了。原话：\"TL;DR: We tried. It didn't work out for us.\" 字符串"
                  "在 V8 边界上来回转换把收益吃掉了。修法是在 TypeScript 里换一个更好的数据结构。同时，Rust 写"
                  "的 ripgrep 以整个子进程的形式承担搜索，批量交换结果。"),
         "match": ("the same product category, and the same finding: a chatty boundary loses, a "
                   "coarse one ships",
                   "同一个产品品类，同一个结论：碎边界输，粗边界能发出来"),
         "mismatch": ("a managed runtime with a GC on the UI side; xi's front end was Swift with ARC",
                      "那边 UI 侧是带 GC 的托管运行时；xi 的前端是 Swift 加 ARC"),
         "regime": "first-party product engineering, 2018 buffer decision",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "Prisma · Rust query engine removed", "outcome": "REVERSED",
         "body": ("Removing the Rust engine measured 3.4× faster on a 25,000-row query, 185 ms down "
                  "to 55 ms, and cut the bundle from about 14 MB to 1.6 MB. Their stated reason: "
                  "\"data must be serialized from JavaScript to Rust and then back to JavaScript.\" "
                  "A WASM query compiler in Rust was kept, because that crossing happens in bulk.",
                  "把 Rust 引擎拿掉之后，25,000 行的查询实测快了 3.4×，185 ms 降到 55 ms，产物从大约 14 MB 降"
                  "到 1.6 MB。他们给的理由：\"data must be serialized from JavaScript to Rust and then back "
                  "to JavaScript.\" 用 Rust 写的 WASM 查询编译器保留了，因为那条缝是批量过一次。"),
         "match": ("per-operation serialization across a process or runtime boundary, priced with "
                   "first-party numbers",
                   "每次操作都要跨进程或跨运行时序列化一次，而且有一方数字给它定了价"),
         "mismatch": ("a library boundary inside one process, and it has real measurements; xi's "
                      "boundary cost was never timed",
                      "那是单进程内的库边界，而且有实测；xi 那条边界的开销从来没有计时过"),
         "regime": "first-party benchmarks, findMany over 25,000 rows",
         "source_label": "first-party · engineering blog",
         "url": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm"},
        {"name": "Zed · GPUI", "outcome": "SHIPPED",
         "body": ("A Rust editor that shipped, with the buffer and the UI in one process and a "
                  "GPU scene graph they had to write themselves. No Rust GUI framework hit their bar, "
                  "so GPUI became part of the product. That cost is the same cost xi paid by not "
                  "paying it.",
                  "一个发出来的 Rust 编辑器：缓冲区和 UI 在同一个进程里，GPU 场景图是自己写的。当时没有 Rust "
                  "GUI 框架够用，于是 GPUI 变成产品的一部分。这笔钱，xi 是靠不付而付的。"),
         "match": ("the in-process shape this report recommends, in the same product category",
                   "本报告推荐的单进程形状，而且是同一个产品品类"),
         "mismatch": ("greenfield with a funded team, and its latency numbers are third-party and "
                      "unaudited",
                      "那是有钱有团队的全新项目，而它的延迟数字是第三方的、没有审计过"),
         "regime": "vendor claims plus unaudited third-party timings",
         "source_label": "vendor blog · third-party timings unaudited",
         "url": "https://zed.dev/blog/videogame"},
    ],

    "path": [
        {"title": ("Link the kernel in-process and measure edit-to-paint",
                   "把内核链进同一个进程，然后测一次 edit-to-paint"),
         "body": ("Whoever is building the editor links the buffer kernel into the UI process and "
                  "measures p99 edit-to-paint at a stated file size and window width. Publish the "
                  "harness. The step passes when p99 sits inside the budget the product actually "
                  "needs. If it misses, profile before adding a process; the buffer may not be where "
                  "the time went. No architecture is chosen here, so there is nothing to undo.",
                  "谁在做编辑器，谁就把缓冲区内核链进 UI 进程，在写明的文件大小和窗口宽度下测 p99 "
                  "edit-to-paint，并把测量脚手架公开。通过标准是 p99 落在产品真正需要的预算内。没达到，就先做 "
                  "profile 再考虑加进程——时间未必花在缓冲区上。这一步不选架构，也没有什么要撤。"),
         "owner": "whoever is building the editor",
         "cost_range": ("1-2 weeks", "1-2 周"),
         "artifact": "a p99 edit-to-paint measurement at a stated file size and window width, with a reproducible harness",
         "acceptance": "p99 sits inside the budget the product needs, with the kernel linked in the UI process",
         "stop": "if it misses, profile before adding a process — the buffer may not own the time",
         "rollback": "measurement only; no architecture chosen"},
        {"title": ("Keep plugins out of process, keep the UI in", "插件放到进程外，UI 留在进程内"),
         "body": ("Write down which peers are allowed to be asynchronous and which are not. Language "
                  "servers, formatters and linters go outside. Indentation, paren matching, selection "
                  "and undo stay synchronous and in-process. The step passes when no synchronous "
                  "editing command crosses a process boundary. If a feature needs a CRDT to behave, "
                  "it is on the wrong side of the line. The boundary is a build-time decision, so "
                  "moving it back is a rebuild.",
                  "把哪些对端可以异步、哪些不行写下来。language server、formatter、linter 放外面。缩进、括号"
                  "匹配、选区、undo 留在进程内同步执行。通过标准是：没有任何同步编辑命令跨进程。要是某个功能"
                  "非得靠 CRDT 才正常，它就站错边了。这条边界是构建期决定的，挪回去就是重新构建一次。"),
         "owner": "the editor's maintainers",
         "cost_range": ("1 week of design", "设计 1 周"),
         "artifact": "a written boundary decision naming which peers are async and which are synchronous",
         "acceptance": "no synchronous editing command crosses a process boundary",
         "stop": "a feature that needs a CRDT to behave correctly is on the wrong side of the line",
         "rollback": "the boundary is a build-time decision; rebuild to move it"},
        {"title": ("Price revision tracking down to undo", "把版本跟踪砍到只够 undo"),
         "body": ("Size the revision machinery against the async peers you actually have, which is "
                  "usually a language server posting annotations. Levien's prescription is the "
                  "target: a largely synchronous model with just enough revision tracking. The step "
                  "passes when no full CRDT merge path is compiled in. If collaborative editing is a "
                  "funded requirement, stop and scope it as its own project. Reducing the engine is a "
                  "library-internal change and reverts with the crate version.",
                  "版本机制的规模，按你真正有的异步对端来定——通常就是一个往上贴标注的 language server。"
                  "Levien 给的方子就是目标：一个基本同步的模型，配上刚够用的版本跟踪。通过标准是：完整的 CRDT "
                  "merge 路径不进编译。如果协同编辑真的有预算，那就停下来，把它当成一个独立项目立项。缩减引擎"
                  "是库内部的改动，回退就是切回上一个 crate 版本。"),
         "owner": "whoever owns the buffer kernel",
         "cost_range": ("2-4 weeks", "2-4 周"),
         "artifact": "an undo and revision design sized against the asynchronous peers that actually exist",
         "acceptance": "no full CRDT merge path is compiled into the product",
         "stop": "if collaborative editing is funded, stop and scope it as its own project",
         "rollback": "library-internal change; revert by crate version"},
        {"title": ("Version any protocol before you publish it", "任何协议在公开之前先加版本"),
         "body": ("If a process boundary survives anywhere, it gets version negotiation on day one. "
                  "xi published 100 wire methods with none, then listed twelve front ends against "
                  "them. The step passes when an old client and a new server refuse each "
                  "other cleanly instead of misrendering. Do not publish a protocol you intend to "
                  "keep changing. Negotiation is additive, so it can be removed if the boundary goes "
                  "away.",
                  "只要还留着任何进程边界，第一天就给它版本协商。xi 公开了 100 个 wire 方法，一个版本号都没有，"
                  "然后在上面挂了十二个第三方前端。通过标准是：旧客户端遇到新服务端会干脆拒绝，而不是画错。"
                  "不要公开一份你打算一直改的协议。协商是加法，边界要是没了它也能删掉。"),
         "owner": "whoever owns the protocol",
         "cost_range": ("days", "几天"),
         "artifact": "a versioned protocol with negotiation at startup",
         "acceptance": "an old client and a new server refuse each other cleanly rather than misrendering",
         "stop": "do not publish a protocol you intend to keep changing",
         "rollback": "negotiation is additive and can be removed with the boundary"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("Five design bets get collapsed into the word \"Rust\". Levien's own list keeps "
                   "them apart, and only the process split and the CRDT draw a negative verdict.",
                   "五个设计赌注被压缩成「Rust」一个词。Levien 自己的清单是分开列的，其中只有进程拆分和 CRDT "
                   "拿到了负面判词。"),
         "evidence": "retrospective, the five novelty points · G2 evidence"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("There is no measurement in this tree at all. The 16 ms figure is a stated goal, "
                   "and the failures are first-party testimony rather than a profile.",
                   "这棵树里根本没有测量。16 ms 是写出来的目标，那些故障是作者的证词，不是 profile。"),
         "evidence": "D1, D2, D3 UNKNOWN · 6 bench files with no results"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("The in-process kernel needs a C ABI shim whenever the UI is not Rust. No such "
                   "shim exists in this repository, so that cost is unpriced here.",
                   "只要 UI 不是 Rust，单进程内核就需要一层 C ABI shim。这个仓库里没有这样的 shim，所以这笔"
                   "成本在这里没有定价。"),
         "evidence": "D8 caveat · no FFI shim in the tree"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("100 wire methods, no version negotiation and a 325-line shadow cache are counted "
                   "and charged to the as-built option, not to the language.",
                   "100 个 wire 方法、没有版本协商、325 行影子缓存，这些都数清了并记在实际做法那个方案头上，"
                   "不是记在语言头上。"),
         "evidence": "D10 · rust/core-lib/src/rpc.rs, line_cache_shadow.rs"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The path puts a measurement before any architecture choice, and names the stop "
                   "condition that sends the team to a profiler instead of to a new process.",
                   "路径把测量放在选架构之前，并写明了停止条件：结果不达标就去用 profiler，不是去加一个进程。"),
         "evidence": "reversible path step 1"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("VS Code's TypeScript piece tree is shipping to the largest professional editor "
                   "audience there is. That is a funded answer to the same buffer problem, and it is "
                   "retained as an option.",
                   "VS Code 那棵 TypeScript piece tree 正服务着专业编辑器里最大的一批用户。这是同一个缓冲区"
                   "问题的一个有钱支撑的答案，方案里保留了它。"),
         "evidence": "D12 · host-language-buffer retained"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Reading xi as \"Rust cannot do desktop\" leaves the usable lesson on the floor. "
                   "The author names a boundary, and boundaries are language-independent.",
                   "把 xi 读成「Rust 做不了桌面」，等于把真正能用的教训扔在地上。作者点的是一条边界，而边界"
                   "跟语言无关。"),
         "evidence": "D9, D10 · retrospective conclusion"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The report counts the unsafe surface it found rather than implying there is none: "
                   "16 lines in one SIMD file, and 24 across the whole non-test tree.",
                   "报告把找到的 unsafe 面数出来了，没有暗示一行都没有：一个 SIMD 文件里 16 行，整棵非测试树 "
                   "24 行。"),
         "evidence": "D6 · rust/rope/src/compare.rs"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("Nowhere does this report claim a host-language buffer is slower. D1 through D3 sit "
                   "at UNKNOWN because nothing here measures either side.",
                   "本报告没有任何一处主张宿主语言写的缓冲区更慢。D1 到 D3 停在 UNKNOWN，因为这里两边都没有"
                   "测量。"),
         "evidence": "D1, D2, D3 UNKNOWN"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("If the in-process kernel misses the budget, the path stops and profiles instead "
                   "of escalating to a new architecture.",
                   "单进程内核没达到预算，路径就停下来做 profile，不是升级到一套新架构。"),
         "evidence": "reversible path step 1 stop condition"},
    ],

    "gaps": [
        (("An edit-to-paint profile, in-process versus across the pipe",
          "一份 edit-to-paint profile，单进程 vs 跨管道"),
         ("This settles D1, D2 and D3 together. While it is missing, the boundary's cost is carried "
          "by the author's account and no latency claim can be authorized in any language.",
          "它一次了结 D1、D2、D3。缺着的时候，那条边界的成本只由作者的说法支撑，任何语言的延迟主张都授权"
          "不了。")),
        (("The FFI shim cost when the UI is not Rust", "UI 不是 Rust 时那层 FFI shim 的成本"),
         ("Changes G3 and G4 for a team whose front end is Swift or TypeScript. This repository "
          "contains no shim, so the figure is absent rather than small.",
          "对前端是 Swift 或 TypeScript 的团队，这会改变 G3 和 G4。这个仓库里没有 shim，所以这个数字是缺失，"
          "不是很小。")),
        (("A root-cause list of xi's user-visible defects", "xi 用户可见故障的根因清单"),
         ("Would separate protocol-caused races from CRDT-caused ones. This tree does not distinguish "
          "them, and the two are priced together at D10 and D11 as a result.",
          "它能把协议造成的竞态和 CRDT 造成的竞态分开。这棵树没有区分，所以 D10 和 D11 只能把两者放在一起"
          "算。")),
    ],

    "assumptions": [
        "The shallow clone at commit a2dea30 represents the final tree; history, dates, stars, contributor count and crates.io figures come from the GitHub and crates.io APIs on 2026-08-02, not from git log.",
        "Line counts are physical lines from wc -l over tracked files, comments and tests included. The plumbing set and the editing set are named file lists chosen from module doc comments, not a compiler-derived call graph.",
        "No specific RFC was supplied, so the proposal under assessment is the one this repository is usually cited for: that xi-editor shows Rust is a poor fit for desktop applications.",
        "The retrospective and the CRDT issue comment are first-party author statements. They are treated as evidence with provenance, never as measurement, and the report does not attribute to Levien any claim about Rust that he did not make.",
    ],
    "objective": {
        "driver": "delivery",
        "requirement": "ship a native desktop text editor that commits and paints every editing operation in under 16 ms, extensible by plugins written in any language",
        "baseline": "39,292 lines of Rust across 103 files, 134 contributors, 19,817 stars, no shipped editor; the README at the final commit still lists auto-indent as missing",
        "target": "a usable editor meeting the stated 16 ms budget; no measurement against that budget exists anywhere in this tree",
    },
    "repository": {
        "path": "https://github.com/xi-editor/xi-editor",
        "commit": "a2dea3059312795c77caadc639df49bf8a7008eb",
        "scope": "the editor core only; the Swift macOS front end lives in the separate xi-mac repository",
        "sampling": "shallow clone; 245 tracked files enumerated; rust/ measured per crate and per file; docs/ and rfcs/ read in full; no build, benchmark, test or run against the project",
    },
    "user_supplied_facts": [],

    "method_title": (
        "xi-editor/xi-editor at a2dea30 · static read-only analysis · why-not-rust method 2.0",
        "xi-editor/xi-editor @ a2dea30 · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/xi-editor/xi-editor at commit a2dea30, shallow clone, 245 tracked "
        "files. Scope: the editor core only. The Swift macOS front end is a separate repository "
        "(xi-mac, 3,002 stars), and that separation is itself part of the evidence. Sampling: 39,292 "
        "lines of Rust across 103 files, which is 96% of the tree's program source on a .rs plus .py "
        "plus .cc basis (39,292 of 40,922). Every percentage in this report uses that basis and never "
        "a whole-tree total. Crate totals: core-lib 17,405, rope 9,522, unicode 2,654, trace 2,150, "
        "plugin-lib 2,100, experimental 1,394, rpc 1,390, lsp-lib 1,353, syntect-plugin 979, src 236, "
        "sample-plugin 109. The cross-process set is 7,601 lines across 29 files: rust/rpc, "
        "rust/plugin-lib, rust/lsp-lib, rust/core-lib/src/plugins, plus rpc.rs, client.rs and "
        "line_cache_shadow.rs and the rpc integration test. The editing set is 3,089 lines across 8 "
        "files: editor, edit_ops, edit_types, movement, selection, backspace, word_boundaries, "
        "whitespace. The 100 wire methods are leaf variants of the protocol enums in "
        "rust/core-lib/src/rpc.rs: CoreNotification 10 minus 2 wrappers, CoreRequest 4 minus 1 "
        "wrapper, EditNotification 84, EditRequest 2, PluginNotification 3. History, stars, the "
        "134-contributor figure and all crates.io download counts come from the GitHub and crates.io "
        "APIs on 2026-08-02, because the clone is depth 1. No build, test, benchmark or network call "
        "was run against the project. Objective: no RFC was supplied, so the assessment takes the "
        "claim this repository is usually cited for. User-supplied facts: none. No Amdahl calculation "
        "appears, because D1 is UNKNOWN and a line-count share is not a time share. D1, D2 and D3 are "
        "UNKNOWN: the tree contains six benchmark files with no published results and a 2,150-line "
        "tracing crate with no captured trace. The decision therefore rests on structural counts and "
        "on first-party author statements, quoted verbatim and labelled as account rather than "
        "measurement. Instruction-like text found while scanning: none. This is a structured decision "
        "protocol, not a statistical predictor.",

        "仓库：github.com/xi-editor/xi-editor，commit a2dea30，shallow clone，245 个纳管文件。范围：只有编辑器"
        "内核。Swift 写的 macOS 前端在另一个仓库（xi-mac，3,002 star），这个分离本身就是证据的一部分。采样："
        "39,292 行 Rust，分布在 103 个文件里；按 .rs 加 .py 加 .cc 的口径，占程序源码的 96%（39,292 / "
        "40,922）。本报告所有百分比都用这个口径，不用整棵树的总行数。各 crate 行数：core-lib 17,405，rope "
        "9,522，unicode 2,654，trace 2,150，plugin-lib 2,100，experimental 1,394，rpc 1,390，lsp-lib 1,353，"
        "syntect-plugin 979，src 236，sample-plugin 109。跨进程那一组是 29 个文件 7,601 行：rust/rpc、"
        "rust/plugin-lib、rust/lsp-lib、rust/core-lib/src/plugins，加上 rpc.rs、client.rs、"
        "line_cache_shadow.rs 和那个 rpc 集成测试。编辑那一组是 8 个文件 3,089 行：editor、edit_ops、"
        "edit_types、movement、selection、backspace、word_boundaries、whitespace。100 个 wire 方法是 "
        "rust/core-lib/src/rpc.rs 里协议 enum 的叶子变体：CoreNotification 10 减去 2 个包装，CoreRequest 4 "
        "减去 1 个包装，EditNotification 84，EditRequest 2，PluginNotification 3。历史、star 数、134 位贡献者"
        "以及所有 crates.io 下载量，都取自 2026-08-02 的 GitHub 与 crates.io API，因为这个 clone 是 depth 1。"
        "没有对项目做过任何构建、测试、基准或网络调用。目标：没有人给出 RFC，因此按这个仓库通常被引用的那个"
        "说法来评估。用户提供的事实：无。本报告没有 Amdahl 计算，因为 D1 是 UNKNOWN，而代码行数占比不等于时间"
        "占比。D1、D2、D3 都是 UNKNOWN：树里有六个 benchmark 文件但没有公开结果，还有一个 2,150 行的 tracing "
        "crate 却没有抓下来的 trace。所以决策落在结构性计数和一方作者的原话上；原话逐字引用，并标明身份是"
        "说法，不是测量。扫描过程中发现的指令式文本：没有。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit a2dea30 · GitHub and crates.io APIs read 2026-08-02 · no build, benchmark or run",
        "公开仓库 · 在 commit a2dea30 上做静态分析 · GitHub 与 crates.io API 读取于 2026-08-02 · 没有构建、基准或运行",
    ),
}
