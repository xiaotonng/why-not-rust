"""lapce/lapce — 38,719 stars, 67,928 lines, and a GUI toolkit written on the side.

Repository facts were measured read-only on the shallow clone named in
`repository`. floem and zed were measured in separate clones on the same
counting basis; history came from the GitHub API.
"""

CASE = {
    "slug": "lapce",
    "project_name": "lapce/lapce",
    "project_desc": (
        "Rust · code editor · 67,928 lines of Rust, plus a 54,002-line GUI toolkit it had to write",
        "Rust · 代码编辑器 · 自有 Rust 代码 67,928 行，外加一个自己写的 54,002 行 GUI 工具库",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · a VS Code-class editor built ground-up by a volunteer team",
        "原生桌面 GUI · 一个志愿者团队从零开始做的 VS Code 级编辑器",
    ),

    "scope_word": "EXTRACT",
    "auth": "APPROVE",
    "confidence": "HIGH",
    "robustness": "CONDITIONAL",
    "selected": "rust-kernel-extract",
    "scope_chip": (
        "ship the fast kernels as Rust libraries; do not build the editor around them",
        "把快的那几块做成 Rust 库；不要围着它们再造一个编辑器",
    ),
    "scope_sub": (
        "take the kernel, rent the editor",
        "内核自己写，编辑器租别人的",
    ),

    "why": (
        "Two Rust editors set out to replace VS Code. Zed carries 1,539,358 lines of Rust; Lapce carries "
        "67,928. Same language, same target, 4.4% of the code. Nothing here points at Rust. What a small "
        "team runs out of is people, so the scope that survives is the small one: take the kernel, rent the "
        "editor. lapce-xi-rope is already on crates.io, and ripgrep has been VS Code's search backend since "
        "2017.",
        "两个 Rust 编辑器都想替掉 VS Code。Zed 有 1,539,358 行 Rust，Lapce 有 67,928 行。同一门语言，同一个"
        "目标，代码量是人家的 4.4%。这里没有一条证据指向语言。小团队缺的是人，所以能站住的是小的那个范围："
        "内核自己写，编辑器租别人的。lapce-xi-rope 已经在 crates.io 上，ripgrep 从 2017 年起就是 VS Code 的"
        "搜索后端。",
    ),
    "trigger": (
        "Conditional in both directions. Scope moves up if the money arrives: Zed clears the ground-up "
        "build in the same language, with 23 contributors above Lapce's second-most-active. Scope collapses "
        "back to staying if the boundary crossing eats the gain, which is how VS Code's native text buffer "
        "died. Measure the boundary before committing to the kernel.",
        "两个方向都有条件。范围往上走的条件是钱到位：Zed 用同一门语言把从零开始那条路走通了，它有 23 个贡献者"
        "的提交数超过 Lapce 的第二名。范围退回「不动」的条件是边界开销把收益吃掉，VS Code 的原生文本缓冲就是"
        "这么死的。所以押注内核之前，先量边界。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("CPU-bound text and search work is a documented gap, confirmed by others.",
                           "CPU 密集的文本与搜索是有记录的缺口，别人也验证过。"),
         "name": "requirement",
         "evidence": "docs/why-lapce.md documents the incumbents failing first-hand: Vim froze on synchronous linting, and Electron could not deserialize Neovim's draw events fast enough. Microsoft confirmed the same class of gap independently and paid to fix it, adopting ripgrep as VS Code's search backend in 2017. The kernel option targets a gap somebody else already established."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("The kernels already exist as Rust crates. You depend, you don't build.",
                           "内核已经是现成的 Rust crate。你是依赖它，不是造它。"),
         "name": "rust-specific causality",
         "evidence": "This passes on the ecosystem-asset clause, not on raw language speed. The kernels are written, published and reusable: lapce-xi-rope 0.3.2 is pulled from crates.io at Cargo.toml:73, and ripgrep runs as a whole process exchanging bulk results. Native execution on its own is not Rust-specific and C++ supplies it too, which is why D3 stays NEUTRAL across the native options."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("The cost is a version pin. Nothing cheaper reaches the same target.",
                           "成本是一个版本 pin。没有更便宜的东西能打到同一个目标。"),
         "name": "economics and smallest sufficient option",
         "evidence": "One-time cost is a crate or a subprocess; recurring cost is a version pin. Nothing cheaper reaches the CPU-bound target — staying and configuring does not touch it, and the two build-an-editor options cost 121,930 lines of owned code between them. The requirement's other half, remote development with a local editing engine, is cheaper to rent than to write, which is why adopt-funded-editor is retained rather than excluded."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("Already delivered twice, once by Lapce itself.",
                           "已经交付过两次，其中一次是 Lapce 自己。"),
         "name": "delivery and reversibility",
         "evidence": "Rollback is unpinning a dependency, and the host editor's extension API is untouched, so compatibility risk is close to zero. Delivery is not a projection here. The extraction has already shipped twice: Lapce publishes lapce-xi-rope on crates.io, and Microsoft has run ripgrep behind VS Code's search since 2017. The stop condition is the one VS Code found the hard way — if the boundary crossing consumes the gain, unpin."},
    ],

    "tiles": [
        (("Lapce's Rust", "Lapce 的 Rust"), "67,928", ("lines", "行"),
         ("141 tracked .rs files · whole repository", "版本库内 141 个 .rs 文件 · 整个仓库")),
        (("Zed's Rust, same basis", "Zed 的 Rust，同一口径"), "1,539,358", ("lines", "行"),
         ("1,926 files at 90d024b · the funded competitor", "90d024b 上 1,926 个文件 · 有资金的对手")),
        (("GUI toolkit written on the side", "顺路写出来的 GUI 工具库"), "54,002", ("lines", "行"),
         ("floem @ 31fa8f44, library only, examples/ excluded", "floem @ 31fa8f44，只算库，不含 examples/")),
        (("Commits on master in 2025", "2025 年 master 上的提交"), "44", ("commits", "个"),
         ("down from 1,897 in 2022 · GitHub API", "2022 年是 1,897 个 · GitHub API")),
        (("One person's share of master", "一个人在 master 上的占比"), "2,023", ("of 3,636", "/ 3,636"),
         ("dzhou121 · GitHub contributors API", "dzhou121 · GitHub contributors API")),
        (("Zed contributors above Lapce's #2", "提交数超过 Lapce 第二名的 Zed 贡献者"), "23", ("people", "人"),
         ("≥368 commits; Lapce has 2 at that bar", "≥368 个提交；Lapce 在这条线上只有 2 人")),
    ],

    "options_sub": (
        "The requirement has two halves and they do not have the same answer. Native-speed text handling is "
        "the half a small team can own. Remote development with a local editing engine needs a whole "
        "editor, and renting one costs less than writing one. Every option below is priced against both.",
        "需求有两半，答案不一样。原生速度的文本处理，是小团队能自己扛的那一半。本地编辑引擎配远端 proxy 的远程"
        "开发，需要一整个编辑器，而租一个比写一个便宜。下面每个方案都要对着这两半算账。",
    ),
    "options": [
        {"id": "rust-kernel-extract", "name": ("Rust kernels as libraries behind an existing editor",
                                               "Rust 内核做成库，挂在现成编辑器后面"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("the parts Rust is measurably good at, without owning a UI",
                              "拿到 Rust 确实擅长的那几块，同时不用自己养一套 UI"),
         "one_time_cost": "one crate or one subprocess per kernel", "recurring_cost": "a dependency pin",
         "cost_cell": ("per kernel; a version pin", "按内核计；一个版本 pin"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "the host editor's own extension API",
         "compat_cell": ("host's API · unpin to revert", "宿主自己的 API · 取消 pin 即回滚"),
         "reversibility": "unpin the dependency",
         "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · already shipped twice, including by Lapce itself",
                  "推荐 · 已经落地过两次，其中一次就是 Lapce 自己"),
         "reason": "lapce-xi-rope 0.3.2 is a published crate this repository consumes, and ripgrep has served VS Code's search as a subprocess since 2017. The option needs no new editor, no toolkit and no plugin ABI."},
        {"id": "rust-ground-up", "name": ("Build the whole editor in Rust, toolkit and plugin ABI included",
                                          "整个编辑器用 Rust 从零做，含工具库和插件 ABI"),
         "implementation": "rust", "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("native latency, unmeasured; feature surface thin in every category",
                              "原生延迟，未测量；每一类功能都薄"),
         "one_time_cost": "121,930 lines of own code and counting", "recurring_cost": "a GUI toolkit and a plugin protocol, forever",
         "cost_cell": ("121,930 lines; a toolkit to maintain", "121,930 行；外加一个要长期维护的工具库"),
         "time_to_value": ("years; v0.4.6 after 4.5", "数年；4.5 年后停在 v0.4.6"),
         "compatibility": "no published extension runs",
         "compat_cell": ("bespoke ABI · no rollback", "自定 ABI · 无回滚"),
         "reversibility": "none", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · this is what Lapce did, and the numbers are its own",
                  "排除 · 这就是 Lapce 走的路，数字也是它自己的"),
         "reason": "Excluded on economics and delivery capacity, not on the language. The toolkit is 44.3% of the code this effort owns, commits on master fell to 44 in 2025 with 2,023 of the 3,636 held by one person, and the plugin ABI forfeits the published extension library at the moment it is chosen. Zed clears the same scope in the same language with 23 contributors above Lapce's second-most-active, so the binding constraint is headcount rather than Rust."},
        {"id": "rust-app-adopt-toolkit", "name": ("Rust editor on somebody else's GUI toolkit",
                                                  "Rust 编辑器，GUI 工具库用别人的"),
         "implementation": "rust", "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("same native mechanism, 54,002 fewer lines to own",
                              "同样的原生机制，少养 54,002 行"),
         "one_time_cost": "the editor only", "recurring_cost": "upstream toolkit's roadmap, not yours",
         "cost_cell": ("editor only; upstream sets the pace", "只做编辑器；节奏由上游定"),
         "time_to_value": ("months", "数月"),
         "compatibility": "constrained by what the toolkit renders",
         "compat_cell": ("toolkit's limits · swap the crate", "受工具库能力限制 · 换个 crate"),
         "reversibility": "swap the toolkit crate", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · Lapce started here on Druid and left; the org still carries the forks",
                  "保留 · Lapce 起初用 Druid，后来离开了；那些 fork 还挂在 org 里"),
         "reason": "Cuts the largest omitted cost. The lapce org's forks of druid, winit, cosmic-text, parley, swash, font-kit, glutin, glazier, piet-wgpu and vger-rs are the record of why it was hard in 2022; a 2026 team faces a different toolkit market."},
        {"id": "native-nonrust-shell", "name": ("Native editor in a language with a mature GUI toolkit",
                                                "用一门有成熟 GUI 工具库的语言做原生编辑器"),
         "implementation": "non-rust-native", "scope": "full", "scope_tag": "NATIVE",
         "benefit_interval": ("the same native mechanism, no toolkit to write",
                              "同样的原生机制，不用自己写工具库"),
         "one_time_cost": "the editor only", "recurring_cost": "C++ or Go memory discipline",
         "cost_cell": ("editor only; manual memory care", "只做编辑器；内存要自己管"),
         "time_to_value": ("months", "数月"),
         "compatibility": "whatever the toolkit binds to",
         "compat_cell": ("toolkit bindings · conventional", "工具库绑定 · 路子常规"),
         "reversibility": "conventional refactor", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the counterfactual any native-speed claim has to beat",
                  "保留 · 任何「原生更快」的主张都要先赢过这个对照"),
         "reason": "Sublime is C++ and the same author's gonvim was Go with Qt bindings. Both reached native latency without Rust, which is why D3 does not credit the mechanism to the language."},
        {"id": "adopt-funded-editor", "name": ("Adopt an editor somebody else is funding",
                                               "直接用别人在投钱的编辑器"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("the full feature surface, paid for by someone else",
                              "完整功能面，钱是别人出的"),
         "one_time_cost": "per user migration", "recurring_cost": "someone else's product decisions",
         "cost_cell": ("per user; their roadmap", "按人计；路线图归他们"),
         "time_to_value": ("days", "数天"),
         "compatibility": "their extension ecosystem",
         "compat_cell": ("their ecosystem · switch back", "他们的生态 · 可以换回来"),
         "reversibility": "switch back", "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · Zed is 1,539,358 lines of the same language, already built",
                  "保留 · Zed 是同一门语言的 1,539,358 行，已经建好了"),
         "reason": "Meets the objective for a user, not for a project. It is retained because it prices what the ground-up option is actually competing against."},
    ],

    "lenses_sub": (
        "Each state is evidence bound to named options, not a score to add up. The two performance lenses "
        "sit at UNKNOWN because nobody has published a latency measurement for this editor, and the report "
        "does not fill that hole with the competitor's numbers.",
        "每条状态都绑在具体方案上，不是可以相加的分数。两条性能相关的停在 UNKNOWN，因为没有人公开过这个编辑器"
        "的延迟测量；报告也没有拿对手的数字去填这个洞。",
    ),
    "na_note": (
        "One lens is N/A. D4 fleet footprint: this is a desktop application installed per user, so there is "
        "no fleet, no instance count and no price per core to compare.",
        "一条记为 N/A。D4 机队占用：这是按人安装的桌面应用，没有机队，没有实例数，也没有单核价格可比。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["rust-ground-up", "rust-app-adopt-toolkit", "rust-kernel-extract"],
         "claim": ("The requirement is written down and specific. docs/why-lapce.md walks from Vim's "
                   "missing async, through Neovim's whole-canvas draw events, to the one the others could "
                   "not fix: remote development that puts network latency in every keystroke. The editor "
                   "owns its entire input path, so ownership is not in question.",
                   "需求是写下来的，而且很具体。docs/why-lapce.md 从 Vim 没有异步讲到 Neovim 只发整块画布的绘制"
                   "事件，最后落到别人修不了的那一条：远程开发把网络延迟塞进每一次按键。编辑器拥有自己完整的"
                   "输入路径，归属没有疑问。"),
         "source": "docs/why-lapce.md · lapce-app/src/proxy/remote.rs (497 lines) · lapce-rpc (3,760 lines)",
         "regime": "architecture requirement stated by the project",
         "caveat": "The same requirement is met by any native option, including native-nonrust-shell; D1 says the requirement is real, not that Rust is the answer to it."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-ground-up", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-ground-up"],
         "claim": ("No keystroke-to-glyph measurement for Lapce exists in this repository or in public. The "
                   "README says lightning-fast; there is no harness. No Amdahl figure appears here because "
                   "there is no time share to put in it, and a line-count share is not a substitute.",
                   "这个仓库里和公开渠道里都找不到 Lapce 的按键到出字测量。README 写着 lightning-fast，但没有"
                   "测量脚手架。这里不给 Amdahl 数字，因为没有时间占比可填，代码行数占比顶替不了它。"),
         "source": "no published Lapce latency measurement; README.md:8 carries the claim",
         "regime": "n/a — the measurement is absent",
         "caveat": "Zed published ~58ms end-to-end against VS Code's ~97ms, third-party and unaudited. That is Zed's number and it is not transferred here.",
         "change_trigger": "A keystroke-to-glyph harness on stated hardware, run against the incumbent, would make the latency claim assessable for either editor."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all native options", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Every native option removes the same two things: the garbage collector and the "
                   "JavaScript deserialization step that the author actually hit in Electron. None removes "
                   "them better than the others. This lens separates native from Electron, and it does not "
                   "separate Rust from C++ or from Go with Qt bindings.",
                   "所有原生方案拿掉的是同样两样东西：垃圾回收，以及作者当年在 Electron 里真正撞上的那个 "
                   "JavaScript 反序列化步骤。谁也没比谁拿得更干净。这条镜头分得开原生和 Electron，分不开 Rust "
                   "和 C++，也分不开 Rust 和 Go 加 Qt。"),
         "source": "docs/why-lapce.md — the author's own gonvim (Go + Qt) predates the Rust decision",
         "regime": "structural, at the UI boundary",
         "caveat": "Crediting this to Rust rather than to native execution is the attribution error the challenge audit records as a HIT."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("A desktop editor runs one instance per developer on hardware the developer already "
                   "owns. There is no fleet to price, so per-instance memory does not convert into a cost "
                   "case here.",
                   "桌面编辑器是每个开发者一份，跑在开发者自己的机器上。没有机队要算钱，单实例内存在这里也就"
                   "换不成成本论证。"),
         "source": "desktop distribution model", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "UNKNOWN · rust-ground-up", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-ground-up"],
         "claim": ("Cold start is one of the two things people say out loud about Electron editors, and "
                   "nobody has measured it for Lapce either. A native binary should win. Should is not a "
                   "number.",
                   "冷启动是大家提到 Electron 编辑器时会说的两件事之一，而 Lapce 这边同样没人量过。原生二进制"
                   "理应赢。理应不是数字。"),
         "source": "no published cold-start measurement", "regime": "n/a",
         "caveat": "Recorded UNKNOWN rather than assumed. The tree-sitter grammars load lazily from a separate directory, so first-open cost for a new language is a distinct question again."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "STRONG", "option_ids": [],
         "claim": ("Memory safety was never the objective here, and there is almost nothing left to buy. "
                   "13 lines of unsafe code sit in 141 files. The C that matters is in the dependency tree "
                   "regardless: libgit2-sys, a vendored OpenSSL, tree-sitter, libz-sys and zstd-sys are all "
                   "in the lockfile, and grammars load as C shared libraries at runtime.",
                   "内存安全从来不是这里的目标，而且已经几乎没有东西可买了。141 个文件里只有 13 行 unsafe 代码。"
                   "真正要紧的 C 无论如何都在依赖树里：libgit2-sys、内置的 OpenSSL、tree-sitter、libz-sys、"
                   "zstd-sys 都在 lockfile 里，而语法解析器是运行时按 C 动态库加载的。"),
         "source": "13 unsafe code lines across 141 .rs files · lapce-core/src/language.rs:1899 libloading · Cargo.lock, 758 locked packages",
         "regime": "static inventory at this commit",
         "caveat": "One of the 14 grep matches is a comment, so the code count is 13. The single most interesting unsafe block loads an arbitrary C grammar from disk."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-ground-up", "rust-app-adopt-toolkit"],
         "claim": ("The design puts syntax highlighting on another thread and the file layer in another "
                   "process, so nothing blocks the main thread while you type. Rust makes that split "
                   "checkable rather than merely intended. The shape itself is older than the language "
                   "choice.",
                   "这套设计把语法高亮放到另一个线程、文件层放到另一个进程，打字的时候主线程不会被挡住。Rust "
                   "让这个切分是可校验的，而不只是「打算这么做」。至于这个形状本身，比选语言这件事更早。"),
         "source": "lapce-rpc (3,760 lines) is the process boundary · docs/why-lapce.md describes the UI/proxy/plugin split",
         "regime": "shipped architecture",
         "caveat": "The author had already built the same split against Neovim's RPC and against xi, in C and Rust respectively, so the architecture transfers to any language."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-ground-up", "rust-app-adopt-toolkit"],
         "claim": ("The application ships as a native binary with no bundled runtime, packaged for "
                   "Windows, macOS and four Linux families. The binary is self-contained; the language "
                   "support is not. Around 125 languages arrive as platform-specific tree-sitter shared "
                   "libraries downloaded into a grammars directory after install.",
                   "程序以原生二进制发布，不带运行时，为 Windows、macOS 和四个 Linux 系列做了打包。二进制是"
                   "自包含的，语言支持不是。大约 125 门语言是装完之后再下载的、跟平台绑定的 tree-sitter 动态库，"
                   "落在一个 grammars 目录里。"),
         "source": "extra/ packaging (wxs, plist, icns, 4 Dockerfiles, .desktop, lapce.spec) · lapce-core/src/directory.rs:178 · 125 LapceLanguage variants",
         "regime": "shipped packaging at this commit",
         "caveat": "Out-of-band grammars are a real distribution surface: the editor's syntax support depends on a download and a dlopen, not on the binary you shipped."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "DISFAVORS · rust-ground-up", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-ground-up"],
         "claim": ("No Rust GUI toolkit met the bar, so the team wrote one. floem is 54,002 lines of "
                   "library code at the rev this repository pins. The lapce org additionally carries forks "
                   "of druid, winit, cosmic-text, parley, swash, fount, font-kit, glutin, glazier, "
                   "piet-wgpu and vger-rs. That is the ecosystem gap, itemised.",
                   "没有一个 Rust GUI 工具库达到要求，于是团队自己写了一个。在本仓库 pin 的那个 rev 上，floem "
                   "的库代码是 54,002 行。lapce org 里另外还挂着 druid、winit、cosmic-text、parley、swash、"
                   "fount、font-kit、glutin、glazier、piet-wgpu、vger-rs 的 fork。生态缺口就是这张清单。"),
         "source": "Cargo.toml:79-89 pins floem @ 31fa8f44 · GitHub API orgs/lapce/repos",
         "regime": "dependency and org inventory at this commit",
         "caveat": "Zed hit the same wall and wrote GPUI, so this is a fact about 2022-era Rust GUI rather than about Lapce's judgement. It still lands as cost."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-ground-up", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-ground-up"],
         "claim": ("Plugins are WASI modules over a protocol Lapce invented, run on wasmtime 14.0.2. A VS "
                   "Code extension is a Node module against a JavaScript API. Neither can load the other, "
                   "and no adapter exists in this tree. The whole codebase mentions vscode once, in a URL "
                   "for an icon font.",
                   "插件是 WASI 模块，跑在 wasmtime 14.0.2 上，走的是 Lapce 自己定的协议。VS Code 扩展是对着一套 "
                   "JavaScript API 写的 Node 模块。两边谁也装不了谁，这棵树里也没有适配层。整个代码库提到 "
                   "vscode 只有一次，在一个图标字体的 URL 里。"),
         "source": "lapce-proxy/Cargo.toml:59-65 · lapce-proxy/src/plugin/ (6,240 lines) · Cargo.lock wasmtime 14.0.2 · 1 vscode match across 141 .rs files",
         "regime": "static ABI inventory at this commit",
         "caveat": "wasmtime 14.0.0 shipped 2023-10-20 and the protocol spec repo has not been pushed since 2022-11-13, so the boundary is both incompatible and unattended."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-ground-up", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-ground-up"],
         "claim": ("67,928 lines of editor plus 54,002 of toolkit is 121,930 lines owned, and 44.3% of "
                   "that is the toolkit. The competitor is 1,539,358 lines. Commits went 1,897, 624, 467, "
                   "44 across 2022 to 2025. Version 0.4.6 is the latest stable after 35 releases, and its "
                   "changelog is one new file extension and seven bug fixes.",
                   "编辑器 67,928 行加工具库 54,002 行，自有 121,930 行，其中 44.3% 是工具库。对手是 1,539,358 "
                   "行。2022 到 2025 年的提交数依次是 1,897、624、467、44。发过 35 个 release 之后，最新稳定版"
                   "是 0.4.6，它的 changelog 是一个新文件后缀加七个修复。"),
         "source": "git ls-files '*.rs' | xargs wc -l on three clones · GitHub API commits and releases · CHANGELOG.md:11-27",
         "regime": "line counts at named commits; history from the default branch",
         "caveat": "floem has its own contributor base — 327 commits from dzhou121 against 274 from jrmoulton — so its 54,002 lines are not billed entirely to Lapce. They are still lines that had to exist before the editor could."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · rust-kernel-extract", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-kernel-extract"],
         "claim": ("The smaller option is not hypothetical. Lapce already performed it: lapce-xi-rope "
                   "0.3.2 is a published crate, and this repository consumes it from crates.io like anyone "
                   "else can. VS Code has run ripgrep as its search backend since 2017. The kernel path "
                   "ships without an editor attached.",
                   "更小的那个方案不是假想。Lapce 自己已经做过了：lapce-xi-rope 0.3.2 是发布出去的 crate，本仓库"
                   "跟别人一样从 crates.io 拉它。VS Code 从 2017 年起就用 ripgrep 当搜索后端。内核这条路不用配"
                   "一个编辑器也能发。"),
         "source": "Cargo.toml:73 lapce-xi-rope = 0.3.2 from crates.io",
         "regime": "current upstream practice",
         "caveat": "The extraction does not deliver the remote-development architecture from D1. That half needs a whole editor, which is why adopt-funded-editor stays retained rather than excluded."},
    ],

    "findings": [
        ("current",
         ("Lapce is 4.4% of Zed", "Lapce 是 Zed 的 4.4%"),
         ("Both trees were counted the same way: tracked .rs files, wc -l. Lapce is 67,928 lines across "
          "141 files. Zed is 1,539,358 across 1,926. Lapce holds 44.1% of Zed's stars. An editor that "
          "competes with VS Code is a very large amount of software, and Rust does not make you write it "
          "faster.",
          "两棵树用同一种数法——版本库内的 .rs 文件，wc -l——Lapce 是 141 个文件 67,928 行，Zed 是 1,926 个文件 "
          "1,539,358 行。Lapce 拿到了 Zed 的 44.1% 的 star。一个能跟 VS Code 打的编辑器是极大量的软件，Rust 不会"
          "让你写得更快。"),
         "lapce c9e4c33 · zed 90d024b · same command, same basis"),
        ("rust",
         ("The GUI toolkit is 54,002 lines", "GUI 工具库 54,002 行"),
         ("floem is an external git dependency pinned at 31fa8f44, so none of it counts inside Lapce's "
          "67,928. Its library code is 54,002 lines, which makes 44.3% of everything this effort owns a "
          "toolkit rather than an editor. Then there are the forks: druid, winit, cosmic-text, parley, "
          "swash, fount, font-kit, glutin, glazier, piet-wgpu, vger-rs.",
          "floem 是外部 git 依赖，pin 在 31fa8f44，所以它一行都不在 Lapce 那 67,928 行里。它的库代码 54,002 行，"
          "也就是说这场投入自有的东西里有 44.3% 是工具库而不是编辑器。此外还有那些 fork：druid、winit、"
          "cosmic-text、parley、swash、fount、font-kit、glutin、glazier、piet-wgpu、vger-rs。"),
         "Cargo.toml:79-89 · floem @ 31fa8f44, examples/ excluded"),
        ("current",
         ("Commits went 1,897 → 44", "提交数从 1,897 掉到 44"),
         ("Per calendar year on master: 1,897 in 2022, 624 in 2023, 467 in 2024, 44 in 2025, 18 so far in "
          "2026. The cliff is Q4 2024, where 133 commits became 25. One person holds 2,023 of the 3,636, "
          "and the fourth-largest contributor is dependabot. Last commit on master: 2026-04-03.",
          "master 上按自然年算：2022 年 1,897，2023 年 624，2024 年 467，2025 年 44，2026 年至今 18。断崖在 2024 "
          "年第四季度，133 变成 25。3,636 个提交里有 2,023 个属于一个人，第四名贡献者是 dependabot。master 上"
          "最后一次提交：2026-04-03。"),
         "gh api repos/lapce/lapce/commits with since/until · contributors API"),
        ("rust",
         ("The plugin ABI cannot run a VS Code extension", "插件 ABI 跑不了 VS Code 扩展"),
         ("Lapce chose WASI modules over its own protocol, on wasmtime 14.0.2. That is a defensible "
          "architecture and it costs you the whole published extension library on day one. The protocol's "
          "spec repository has not been pushed since 2022-11-13, and the earlier lapce-extensions repo was "
          "archived in October 2022. GitHub code search finds 152 files named volt.toml.",
          "Lapce 选了 WASI 模块加自己的协议，跑在 wasmtime 14.0.2 上。这是个说得通的架构，代价是第一天就放弃"
          "整个已发布的扩展库。协议的 spec 仓库自 2022-11-13 起没有再推过，更早的 lapce-extensions 仓库 2022 年"
          "10 月就归档了。GitHub 代码搜索能找到 152 个叫 volt.toml 的文件。"),
         "lapce-proxy/Cargo.toml:59-65 · lapce-proxy/src/plugin/ 6,240 lines"),
        ("current",
         ("Every VS Code subsystem is present; each one is thin",
          "VS Code 的每个子系统都在，每个都薄"),
         ("This is not a project that skipped the hard parts. LSP, DAP, WASI plugins, terminal, source "
          "control, settings, themes and remote development all exist, behind 11 panel kinds and 125 "
          "language definitions. DAP is 3,098 lines and the terminal is 3,164. The gap against VS Code is "
          "depth in every category at once, which is exactly the thing headcount buys.",
          "这个项目没有跳过难的部分。LSP、DAP、WASI 插件、终端、源码管理、设置、主题、远程开发全都有，撑起 11 "
          "种面板和 125 个语言定义。DAP 3,098 行，终端 3,164 行。跟 VS Code 的差距是每一类都不够深，而深度正是"
          "人头能买到的东西。"),
         "lapce-app/src/panel/kind.rs:10-22 · lapce-core/src/language.rs:194"),
        ("unknown",
         ("Nobody published this editor's latency", "没有人公开过这个编辑器的延迟"),
         ("The README says lightning-fast. No harness in the repository measures it, and no third party has "
          "published one. D2 and D5 are UNKNOWN. Zed's ~58ms against VS Code's ~97ms is unaudited and it is "
          "Zed's number, so it stays where it was measured.",
          "README 写着 lightning-fast。仓库里没有测它的脚手架，也没有第三方发过。D2 和 D5 记为 UNKNOWN。Zed 那个 "
          "~58ms 对 VS Code ~97ms 未经审计，而且是 Zed 的数字，就留在它被测出来的地方。"),
         "README.md:8 · no measurement artifact in 382 tracked files"),
    ],

    "buys": [
        (("Native input, with no collector and no JS step", "原生输入，没有 collector，没有 JS 那一步"),
         ("the boundary the author hit in Electron is real, and Rust removes it. So does C++, which is why "
          "D3 credits native execution rather than the language.",
          "作者当年在 Electron 里撞上的那个边界是真的，Rust 拿得掉。C++ 也拿得掉，所以 D3 把功劳记给原生执行，"
          "不记给语言。")),
        (("A concurrency split you can check at compile time", "一个编译期就能校验的并发切分"),
         ("syntax highlighting off the main thread, files behind a 3,760-line RPC boundary. The design is "
          "older than the language choice; Rust is what keeps it honest.",
          "语法高亮挪出主线程，文件层藏在 3,760 行的 RPC 边界后面。这个设计比选语言更早；Rust 的作用是让它一直"
          "站得住。")),
        (("A kernel other people can use", "一个别人能用的内核"),
         ("lapce-xi-rope 0.3.2 is on crates.io and this repository pulls it from there. The extraction "
          "already happened and it needed no editor.",
          "lapce-xi-rope 0.3.2 在 crates.io 上，本仓库就是从那儿拉的。抽取这件事已经发生过了，而且不需要配一个"
          "编辑器。")),
        (("A toolkit, eventually", "一个工具库，最后确实有了"),
         ("floem has 4,227 stars and two downstream projects in the same org. The side-quest produced "
          "something, the way Servo produced Stylo.",
          "floem 有 4,227 个 star，同一个 org 里还有两个下游项目。这条支线确实产出了东西，跟 Servo 产出 Stylo "
          "是一个路子。")),
    ],
    "nobuys": [
        (("The extension library", "扩展库"),
         ("WASI plus a bespoke protocol cannot load a Node extension. One vscode string exists in 141 "
          "files and it points at an icon font.",
          "WASI 加一套自定协议装不了 Node 扩展。141 个文件里只有一个 vscode 字符串，指向一个图标字体。")),
        (("People", "人"),
         ("1,897 commits in 2022, 44 in 2025. 23 Zed contributors sit above Lapce's second-most-active. No "
          "language adds contributors.",
          "2022 年 1,897 个提交，2025 年 44 个。23 个 Zed 贡献者的提交数超过 Lapce 的第二名。没有哪门语言能"
          "凭空长出贡献者。")),
        (("A GUI toolkit", "一个 GUI 工具库"),
         ("nothing met the bar in 2022, so 54,002 lines got written before the editor could be finished. "
          "Zed made the same call and wrote GPUI.",
          "2022 年没有达标的，于是在编辑器完工之前先写了 54,002 行。Zed 当时做了同样的判断，写出了 GPUI。")),
        (("Memory safety worth paying for here", "在这里值得花钱买的内存安全"),
         ("13 unsafe code lines in 141 files, and libgit2, a vendored OpenSSL and the C grammars stay in "
          "the dependency tree whatever the application is written in.",
          "141 个文件里 13 行 unsafe 代码；不管应用用什么写，libgit2、内置的 OpenSSL 和那些 C 语法解析器都还在"
          "依赖树里。")),
    ],

    "precedents": [
        {"name": "Zed · GPUI", "outcome": "MIGRATED",
         "body": ("The same option, the same language, and it works. Zed also found no Rust GUI framework "
                  "that hit the bar and wrote GPUI. The difference is capacity: 23 contributors above "
                  "Lapce's second-most-active, and 39,386 commits against 3,636. That is the comparison "
                  "that keeps this report off the claim that Rust editors fail.",
                  "同一个方案，同一门语言，而且成了。Zed 同样没找到达标的 Rust GUI 框架，于是写了 GPUI。差别在"
                  "产能：23 个贡献者的提交数超过 Lapce 的第二名，39,386 个提交对 3,636 个。正是这个对比让本报告"
                  "不至于变成「Rust 编辑器做不成」。"),
         "match": ("greenfield Rust editor against Electron incumbents, custom GPU toolkit included",
                   "从零开始的 Rust 编辑器对 Electron 老牌产品，同样自带一套 GPU 工具库"),
         "mismatch": ("venture funding and a paid team; its latency numbers are third-party and unaudited",
                      "有风投和全职团队；它的延迟数字是第三方的，未经审计"),
         "regime": "vendor claims plus unaudited third-party timing",
         "source_label": "first-party · engineering blog",
         "url": "https://zed.dev/blog/videogame"},
        {"name": "Microsoft · VS Code", "outcome": "STAYED",
         "body": ("The incumbent ran the experiment in both directions inside one product. A native C++ "
                  "text buffer was reverted, with the verdict 'We tried. It didn't work out for us' — "
                  "string conversion across the V8 boundary ate the gain. ripgrep, a whole Rust process "
                  "exchanging bulk results, has powered search since 2017.",
                  "老牌产品在同一个产品里把两个方向都试过了。原生 C++ 文本缓冲被回退，结论是 'We tried. It "
                  "didn't work out for us'——跨 V8 边界的字符串转换把收益吃掉了。而 ripgrep 作为一个整进程的 "
                  "Rust 程序批量交换结果，从 2017 年起一直在支撑搜索。"),
         "match": ("the direct precedent for the selected option: native at a coarse seam, not everywhere",
                   "所选方案的直接先例：在粗接缝上用原生，而不是全都换"),
         "mismatch": ("a funded incumbent with the ecosystem already in hand; no remote-architecture requirement",
                      "有资金的老牌产品，生态本来就在手上；也没有远程架构这条需求"),
         "regime": "first-party engineering retrospective",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "Mozilla · Servo", "outcome": "CANCELLED",
         "body": ("A ground-up Rust replacement for a huge feature surface, cancelled in 2020 with the "
                  "team laid off. Bobby Holley's estimate was the whole story: a full Gecko replacement "
                  "'would probably require thousands of engineer-years' while Mozilla 'could only afford a "
                  "handful of heads'. The language was fine. The arithmetic was not.",
                  "一次针对巨大功能面的从零 Rust 替换，2020 年取消，团队被裁。Bobby Holley 的估算就是全部故事："
                  "完整替换 Gecko 'would probably require thousands of engineer-years'，而 Mozilla 'could "
                  "only afford a handful of heads'。语言没问题，算术有问题。"),
         "match": ("scope economics at maximum scale; a volunteer editor team faces the same ratio",
                   "极大规模下的范围经济学；一个志愿者编辑器团队面对的是同一个比例"),
         "mismatch": ("a browser engine is larger again, and Servo had corporate funding Lapce never had",
                      "浏览器引擎的量级还要更大，而且 Servo 有 Lapce 从未有过的公司资金"),
         "regime": "first-party retrospective plus public layoff record",
         "source_label": "first-party blog · public record",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Mozilla · Stylo", "outcome": "EXTRACT",
         "body": ("The same R&D that failed as a replacement shipped as a component. Two engineers started "
                  "late 2015, first pixels April 2016, in Firefox 57 about two years later. Holley again: "
                  "'the desire to throw everything away and start from scratch tends to be an emotional "
                  "one.' Same org, same codebase, opposite outcome.",
                  "同一批研发，作为替换失败，作为组件发了出去。两个工程师 2015 年末动手，2016 年 4 月第一次出"
                  "像素，大约两年后进入 Firefox 57。还是 Holley 的话：'the desire to throw everything away "
                  "and start from scratch tends to be an emotional one.' 同一个组织，同一份代码，相反的结局。"),
         "match": ("the shape of the selected option: one measured kernel inside somebody else's product",
                   "所选方案的形状：把一个量过的内核放进别人的产品里"),
         "mismatch": ("it rode a funded donor project; Lapce's kernel is already published, which is cheaper again",
                      "它是搭在一个有资金的母项目上的；Lapce 的内核已经发布了，那更便宜"),
         "regime": "first-party retrospective",
         "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Alacritty", "outcome": "QUANTIFIED",
         "body": ("A greenfield Rust GPU terminal called itself the fastest in existence. When someone "
                  "measured, its latency came out mid-pack, and Dan Luu called throughput dumps 'as "
                  "useless a benchmark as I can think of'. Lapce's README says lightning-fast and ships no "
                  "harness. Same failure mode, same fix: define the metric.",
                  "一个从零写的 Rust GPU 终端自称世上最快。等到有人真去量，它的延迟落在中游，Dan Luu 说吞吐量"
                  "转储 'as useless a benchmark as I can think of'。Lapce 的 README 写着 lightning-fast，也没"
                  "带测量脚手架。同样的毛病，同样的解法：把指标定下来。"),
         "match": ("same archetype, same superlative-without-a-metric pattern that puts D2 at UNKNOWN",
                   "同一个类型，同一种「有最高级没有指标」的模式，正是 D2 记 UNKNOWN 的原因"),
         "mismatch": ("a terminal is a fraction of an editor's surface; only the claim failed audit, not the product",
                      "终端的表面积只是编辑器的一小部分；审计不过关的是主张，不是产品"),
         "regime": "independent latency measurement",
         "source_label": "third-party · independent measurement",
         "url": "https://danluu.com/term-latency/"},
    ],

    "path": [
        {"title": ("Measure the latency before you pick the language",
                   "先量延迟，再选语言"),
         "body": ("Whoever wants the new editor publishes keystroke-to-glyph latency first, on stated "
                  "hardware, against the editor they intend to replace. The harness has to be runnable by "
                  "someone else. Lapce never published one and neither did anyone else; Zed's figures are "
                  "third-party and unaudited. If the incumbent lands inside the gap you care about, stop "
                  "here. No code moves in this step.",
                  "想做新编辑器的人，先把按键到出字的延迟发出来，写明硬件，对着打算替掉的那个编辑器测。测量"
                  "脚手架要能被别人复跑。Lapce 没发过，别人也没有；Zed 的数字是第三方的，未经审计。如果现有"
                  "编辑器落在你在乎的区间里，就停在这里。这一步不动代码。"),
         "owner": "whoever proposes the new editor",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "a keystroke-to-glyph latency measurement on stated hardware against the incumbent, with a reproducible harness",
         "acceptance": "a third party can re-run the harness and reproduce the gap",
         "stop": "stop if the incumbent already lands inside the latency budget",
         "rollback": "measurement only; no code changes"},
        {"title": ("Ship the kernel as a library first", "内核先做成库发出去"),
         "body": ("Rope, search and syntax go out as crates or subprocesses behind the editor people "
                  "already use. This is not theoretical. lapce-xi-rope 0.3.2 is on crates.io and ripgrep "
                  "has been VS Code's search backend since 2017. The step passes when the kernel beats the "
                  "in-editor implementation on step one's measurement with the boundary cost counted in. "
                  "If the boundary eats the gain, stop — VS Code's native text buffer died exactly there. "
                  "Backing out is unpinning a dependency.",
                  "把 rope、搜索、语法解析做成 crate 或子进程，挂在大家已经在用的编辑器后面。这不是空想："
                  "lapce-xi-rope 0.3.2 就在 crates.io 上，ripgrep 从 2017 年起就是 VS Code 的搜索后端。通过"
                  "标准是：把边界开销算进去之后，内核在第一步那份测量上赢过编辑器内置实现。如果边界把收益吃掉，"
                  "就停——VS Code 的原生文本缓冲就死在这里。回退就是取消一个依赖 pin。"),
         "owner": "the kernel author",
         "cost_range": ("4–8 weeks per kernel", "每个内核 4–8 周"),
         "artifact": "one Rust kernel published as a crate or subprocess behind an existing editor",
         "acceptance": "it beats the host's own implementation on step one's measurement with the boundary cost included",
         "stop": "stop if the boundary crossing consumes the gain",
         "rollback": "unpin the dependency"},
        {"title": ("Name the GUI toolkit before writing one", "写工具库之前，先把它的名字说出来"),
         "body": ("Before any ground-up build is authorized, the proposer names the third-party toolkit "
                  "and the version they will pin. If the answer is that they will write it, then 54,002 "
                  "lines and eleven upstream forks go into the estimate at the top, not discovered in year "
                  "two. Acceptance is a working prototype of the editor's hardest view on a toolkit "
                  "somebody else maintains. If no toolkit qualifies, the honest description is a toolkit "
                  "project with an editor attached, and it should be funded as one.",
                  "任何从零开始的方案获批之前，提案人先说出要用哪个第三方工具库、pin 哪个版本。如果答案是「我们"
                  "自己写」，那 54,002 行和十一个上游 fork 就要在一开始进预算，而不是第二年才发现。通过标准是："
                  "用别人维护的工具库，把编辑器最难的那个视图做出可用原型。如果没有工具库够格，那么诚实的说法是"
                  "这是一个附带编辑器的工具库项目，就该按那个来投钱。"),
         "owner": "the proposer",
         "cost_range": ("2–4 weeks", "2–4 周"),
         "artifact": "a named third-party GUI toolkit at a pinned version, with a prototype of the editor's hardest view",
         "acceptance": "the prototype renders that view acceptably on a toolkit the team does not maintain",
         "stop": "if no toolkit qualifies, re-scope and fund it as a toolkit project",
         "rollback": "prototype only; discard the branch"},
        {"title": ("Decide the extension story in writing, on day one",
                   "扩展这件事，第一天就写成文字"),
         "body": ("The plugin ABI is chosen once and cannot be revisited later, so it gets written down "
                  "before anything is built. State plainly whether published extensions run. WASI plus a "
                  "bespoke protocol means they do not, and Lapce's own record shows what that looks like "
                  "four years on: a spec repo untouched since 2022-11-13, wasmtime pinned at 14.0.2, and "
                  "152 volt.toml files on GitHub. Either produce an adapter that loads a real published "
                  "extension, or write the sentence that says you are forgoing the library.",
                  "插件 ABI 只选一次，后面改不了，所以在动工之前就得写下来。明说一句：已发布的扩展能不能跑。"
                  "WASI 加自定协议的答案是不能，而 Lapce 自己的记录展示了四年后是什么样子：spec 仓库自 "
                  "2022-11-13 起没动过，wasmtime pin 在 14.0.2，GitHub 上 152 个 volt.toml。要么做出一个适配层，"
                  "能加载一个真实发布的扩展；要么写下那句话，承认放弃这个库。"),
         "owner": "the architecture owner",
         "cost_range": ("1 week", "1 周"),
         "artifact": "a written extension-compatibility decision, plus either an adapter loading a real published extension or an explicit forfeit",
         "acceptance": "the decision names which existing extensions run and which do not",
         "stop": "no ground-up build proceeds without that decision on paper",
         "rollback": "document only"},
        {"title": ("Count committers, not stars", "数提交者，不要数 star"),
         "body": ("Before authorizing a multi-year build, count how many people will still have more than "
                  "three hundred commits in it three years out. Zed has 23 above that bar. Lapce has 2, "
                  "and its fourth-largest contributor is dependabot. Five funded committers is the floor "
                  "for a ground-up editor on this evidence. If the honest answer is one person plus "
                  "volunteers, take step two and stop there — that path is reversible and it still ships "
                  "something people use.",
                  "批准一个多年期项目之前，先数一数三年后还会有多少人在里面留下三百个以上的提交。Zed 有 23 个"
                  "在这条线以上。Lapce 有 2 个，而且第四名贡献者是 dependabot。按现有证据，从零做编辑器的地板是"
                  "五个有资金的提交者。如果诚实的答案是一个人加一群志愿者，那就走第二步然后停在那里——那条路可"
                  "回退，而且照样能发出别人真会用的东西。"),
         "owner": "whoever funds the work",
         "cost_range": ("1 day", "1 天"),
         "artifact": "a staffing plan naming the committers and the years they are funded for",
         "acceptance": "at least five funded committers for the ground-up scope",
         "stop": "if the answer is one person plus volunteers, take the extraction option instead",
         "rollback": "planning only"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The proposal credits native latency to Rust. The same author had already reached it in "
                   "Go with Qt bindings, and Sublime got there in C++. D3 records the mechanism as native "
                   "execution.",
                   "提案把原生延迟记在 Rust 头上。同一个作者早就用 Go 加 Qt 绑定做到过，Sublime 用 C++ 也做到"
                   "了。D3 把这个机制记为原生执行。"),
         "evidence": "docs/why-lapce.md · D3 NEUTRAL across native options"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("Neither side of the latency claim has a measurement. The README says lightning-fast "
                   "and 382 tracked files contain no harness, so D2 and D5 stay UNKNOWN.",
                   "延迟这条主张，两边都没有测量。README 写着 lightning-fast，382 个纳管文件里没有测量脚手架，"
                   "所以 D2 和 D5 停在 UNKNOWN。"),
         "evidence": "README.md:8 · D2, D5 UNKNOWN"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("The GUI toolkit is not inside the editor's line count. floem is 54,002 lines at the "
                   "pinned rev, and the org carries eleven more forks of the GUI and text stack.",
                   "GUI 工具库不在编辑器的代码行数里。floem 在 pin 的那个 rev 上是 54,002 行，org 里还挂着十一"
                   "个 GUI 与文本栈的 fork。"),
         "evidence": "D9, D11 · Cargo.toml:79-89"},
        {"name": ("Delivery ownership", "交付归属"), "state": "HIT",
         "claim": ("2,023 of 3,636 commits belong to one person and yearly commits fell to 44 in 2025. The "
                   "ground-up scope needs a team that does not exist here.",
                   "3,636 个提交里 2,023 个属于一个人，年度提交数在 2025 年掉到 44。从零开始那个范围需要的团队，"
                   "这里没有。"),
         "evidence": "GitHub contributors and commits API · rust-ground-up excluded"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "PASS",
         "claim": ("Staying was priced rather than assumed. docs/why-lapce.md documents three specific "
                   "failures of the incumbents, one of which Neovim and xi could not fix.",
                   "「不动」这条是算过的，不是默认的。docs/why-lapce.md 记下了现成编辑器的三处具体失败，其中一处"
                   "是 Neovim 和 xi 修不了的。"),
         "evidence": "D1 SUPPORTS · G1 PASS"},
    ],
    "staying_checks": [
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("The report never says Rust made this slower or harder, and the option it recommends is "
                   "a Rust option. What excludes the ground-up build is headcount and toolkit cost, and "
                   "Zed clears both in the same language.",
                   "报告没有说 Rust 让这件事更慢或更难，而且它推荐的就是一个 Rust 方案。把从零开始那条路排除掉"
                   "的是人头和工具库成本，这两样 Zed 用同一门语言都过了。"),
         "evidence": "rust-kernel-extract selected · rust-ground-up excluded on D9 and D11"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("No latency measurement exists for either editor, so the staying case is unproven on "
                   "speed too. This verdict rests on volume and capacity, not on a benchmark.",
                   "两个编辑器都没有延迟测量，所以「不动」这条在速度上同样没被证明。本结论靠的是体量和产能，"
                   "不是跑分。"),
         "evidence": "D2, D5 UNKNOWN"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("Staying keeps the Electron boundary the author actually hit, and the report does not "
                   "price that away. The extraction option does not deliver the remote architecture from "
                   "D1 either.",
                   "「不动」就意味着作者当年真撞上的那个 Electron 边界还在，报告没有把它抹掉。抽取方案也交付不"
                   "了 D1 里那套远程架构。"),
         "evidence": "D12 caveat · docs/why-lapce.md"},
        {"name": ("Ownership", "归属"), "state": "PASS",
         "claim": ("The toolkit detour produced a reusable asset. floem has 4,227 stars and two downstream "
                   "projects in the same org, which is the Servo-to-Stylo shape rather than pure loss.",
                   "工具库这条弯路产出了可复用的东西。floem 有 4,227 个 star，同一个 org 里还有两个下游项目，"
                   "这是 Servo 到 Stylo 那个形状，不是纯损失。"),
         "evidence": "GitHub API repos/lapce/floem · orgs/lapce/repos"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("824 open issues and 67 open pull requests sit against a stable release whose changelog "
                   "is one file extension and seven fixes. Doing nothing leaves the incumbent's latency "
                   "exactly where it is.",
                   "824 个开着的 issue、67 个开着的 PR，对应的稳定版 changelog 是一个文件后缀加七个修复。什么都"
                   "不做，现有编辑器的延迟就原地不动。"),
         "evidence": "GitHub search API · CHANGELOG.md:11-27"},
    ],

    "gaps": [
        (("A keystroke-to-glyph latency measurement for Lapce",
          "Lapce 的按键到出字延迟测量"),
         ("Settles D2 and D5. While it is missing, no latency claim can be authorized for any editor here, "
          "including the ones this report retains.",
          "它能了结 D2 和 D5。缺着的时候，这里任何编辑器的延迟主张都授权不了，包括本报告保留的那几个。")),
        (("The authoritative plugin count from the registry", "插件注册中心的权威数量"),
         ("The report did not fetch plugins.lapce.dev; the method forbids retrieving URLs found in scanned "
          "code. GitHub code search reports 152 files named volt.toml, which is a floor and not a census.",
          "报告没有去请求 plugins.lapce.dev；方法禁止拉取从扫描代码里读到的 URL。GitHub 代码搜索报告有 152 个 "
          "volt.toml 文件，这是下限，不是普查。")),
        (("Funding and paid headcount for both projects", "两个项目的资金与全职人数"),
         ("G4 rests on commit distribution because payroll is not public. Numbers would sharpen the "
          "capacity finding; they would not change its direction.",
          "G4 建立在提交分布上，因为发薪名单不公开。有数字会让产能这条结论更锐利，但改不了它的方向。")),
        (("Why Druid was left, in the team's own words", "团队自己说的：为什么离开 Druid"),
         ("Would tell you whether adopting a toolkit was ever viable in 2022 or was tried and failed. It "
          "changes how much weight rust-app-adopt-toolkit deserves.",
          "它能说明 2022 年「用别人的工具库」到底可不可行，还是试过并且失败了。这决定 rust-app-adopt-toolkit "
          "该拿多少分量。")),
    ],

    "assumptions": [
        "Every line count is `wc -l` over tracked files of the named extension, blanks and comments included; the same command was used on all three repositories so the comparison is like-for-like.",
        "floem is an external git dependency, not vendored or a submodule, so its lines are not inside Lapce's 67,928. It was measured in a separate clone at rev 31fa8f44, the exact rev Cargo.toml pins.",
        "zed-industries/zed was measured at commit 90d024b as the funded comparator. Neither project was built, run or benchmarked.",
        "Commit and contributor counts come from the GitHub API for the default branch only, and exclude other branches and any squashed history.",
        "The proposal under assessment is the one the project's own docs describe — a native editor with a local editing engine and a remote proxy — since no external RFC was supplied.",
    ],
    "objective": {
        "driver": "CPU-bound text handling, plus a remote-development architecture",
        "requirement": "native-speed rope, search and syntax work in the editor developers already use; and, separately, a local editing engine paired with a remote proxy",
        "baseline": "Electron could not deserialize Neovim's draw events fast enough, and Neovim and xi both put network latency into every keystroke under remote development (docs/why-lapce.md)",
        "target": "no numeric latency threshold is stated anywhere in the repository; the CPU-bound half is judged on shipped precedent, and the architecture half on the cost of renting an editor against writing one",
    },
    "repository": {
        "path": "https://github.com/lapce/lapce",
        "commit": "c9e4c33948033f10f003991a037d949a708eedf8",
        "scope": "whole repository; the GUI toolkit and the plugin ABI are the two candidate seams",
        "sampling": "shallow clone; 382 tracked files enumerated, 141 .rs files measured; floem measured in a separate clone at the pinned rev 31fa8f44; zed-industries/zed measured at 90d024b on the same basis; GitHub API used for commits, releases and contributors; no build, benchmark or run of the application",
    },
    "user_supplied_facts": [],

    "method_title": (
        "lapce/lapce at c9e4c33 · static read-only analysis · why-not-rust method 2.0",
        "lapce/lapce @ c9e4c33 · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/lapce/lapce at commit c9e4c33, shallow clone, 382 tracked files. Scope: the "
        "whole repository, with the GUI toolkit and the plugin ABI as the candidate seams. Sampling: 141 "
        "tracked .rs files total 67,928 lines — lapce-app 49,393, lapce-proxy 9,450, lapce-core 5,325, "
        "lapce-rpc 3,760. Rust is 100% of the code-extension lines; the 165 .svg files are icons and the 24 "
        ".toml files are manifests and defaults. Two comparison trees were counted with the identical "
        "command, `git ls-files '*.rs' | xargs wc -l`: floem at rev 31fa8f44, the rev Cargo.toml:79-89 "
        "pins, is 60,230 lines across 195 files, of which 54,002 are library code once examples/ is "
        "excluded; zed-industries/zed at commit 90d024b is 1,539,358 lines across 1,926 files. Neither was "
        "built. floem is an external git dependency, not vendored and not a submodule, so its lines are "
        "outside Lapce's total; the 121,930 figure is the sum of the two and is always labelled as such. "
        "Subsystem measurements: lapce-proxy/src/plugin/ is 6,240 lines across 7 files, the DAP surface is "
        "3,098 across 4 files, the terminal surface is 3,164, lapce-app/src/panel/kind.rs declares 11 panel "
        "kinds and lapce-core/src/language.rs declares 125 language variants with 127 SyntaxProperties "
        "records. 14 lines match `unsafe` and one of them is a comment, so 13 are code. History came from "
        "the GitHub API: 3,636 commits on master, of which dzhou121 holds 2,023 across 170 contributors; "
        "per-year commit counts were taken with `gh api repos/lapce/lapce/commits?sha=master&since=…&until=…` "
        "reading the Link rel=\"last\" page count at per_page=1, giving 1,897 for 2022, 624 for 2023, 467 "
        "for 2024, 44 for 2025 and 18 for 2026 to 2026-08-02. 35 releases, latest stable v0.4.6 on "
        "2026-01-21, last commit on master 2026-04-03. Zed's 39,386 commits and its 23 contributors at or "
        "above 368 commits came from the same API. Objective: no external RFC was supplied, so the "
        "assessment takes the architecture the project's own docs/why-lapce.md describes. User-supplied "
        "facts: none. No Amdahl calculation appears, because no latency measurement exists for this editor "
        "and converting a line-count share into a time share is a method error. D2 and D5 are therefore "
        "UNKNOWN rather than refuted. All four gates are graded against the selected option, "
        "rust-kernel-extract, which is what the machine record binds them to, and all four pass: the gap is "
        "documented and was independently confirmed when VS Code adopted ripgrep in 2017, the kernels "
        "already exist as published Rust crates, the cost is a version pin, and the option has shipped "
        "twice in production. The ground-up build's economics and capacity failures are recorded where "
        "they belong — as the exclusion reason on rust-ground-up, and across D9, D10 and D11. Zed runs "
        "that larger option in the same language and delivers it, which is why robustness is CONDITIONAL "
        "and why nothing here is a claim about Rust. "
        "plugins.lapce.dev was not fetched: the method treats URLs found in scanned code as data to render, "
        "never to retrieve. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/lapce/lapce，commit c9e4c33，shallow clone，382 个纳管文件。范围：整个仓库，候选接缝"
        "是 GUI 工具库和插件 ABI。采样：141 个纳管 .rs 文件共 67,928 行——lapce-app 49,393，lapce-proxy 9,450，"
        "lapce-core 5,325，lapce-rpc 3,760。代码类扩展名的行数 100% 是 Rust；165 个 .svg 是图标，24 个 .toml 是"
        "清单和默认配置。两棵对比树用完全相同的命令 `git ls-files '*.rs' | xargs wc -l` 数过：floem 在 "
        "Cargo.toml:79-89 pin 的 rev 31fa8f44 上是 195 个文件 60,230 行，去掉 examples/ 之后库代码 54,002 行；"
        "zed-industries/zed 在 commit 90d024b 上是 1,926 个文件 1,539,358 行。两个都没有构建。floem 是外部 git "
        "依赖，既没内置也不是 submodule，所以它的行数在 Lapce 的总数之外；121,930 这个数字是两者相加，出现时"
        "都会标明。子系统测量：lapce-proxy/src/plugin/ 7 个文件 6,240 行，DAP 面 4 个文件 3,098 行，终端面 "
        "3,164 行，lapce-app/src/panel/kind.rs 声明 11 种面板，lapce-core/src/language.rs 声明 125 个语言变体和 "
        "127 条 SyntaxProperties 记录。匹配 `unsafe` 的有 14 行，其中一行是注释，所以代码是 13 行。历史来自 "
        "GitHub API：master 上 3,636 个提交，170 名贡献者中 dzhou121 占 2,023 个；按年提交数用 "
        "`gh api repos/lapce/lapce/commits?sha=master&since=…&until=…` 在 per_page=1 下读 Link rel=\"last\" 的"
        "页码取得，2022 年 1,897，2023 年 624，2024 年 467，2025 年 44，2026 年到 2026-08-02 为 18。35 个 "
        "release，最新稳定版 v0.4.6 发布于 2026-01-21，master 最后一次提交 2026-04-03。Zed 的 39,386 个提交、"
        "以及提交数不低于 368 的 23 名贡献者，取自同一套 API。目标：没有外部 RFC，因此按项目自己的 "
        "docs/why-lapce.md 所描述的架构来评估。用户提供的事实：无。本报告没有 Amdahl 计算，因为这个编辑器不"
        "存在延迟测量，而把代码行数占比换成时间占比是方法错误。所以 D2 和 D5 记为 UNKNOWN，不是被否证。四道门都是对着所选方案 "
        "rust-kernel-extract 评的，机器记录里也是这么绑定的，四道全过：缺口有记录，并且被 VS Code 2017 年采用 "
        "ripgrep 独立印证；内核已经是发布出去的 Rust crate；成本是一个版本 pin；这个方案在生产里落地过两次。"
        "从零开始那条路在经济性和产能上的失败，记在该在的地方——rust-ground-up 的排除理由，以及 D9、D10、D11。"
        "Zed 用同一门语言把那个更大的方案交付出来了，所以稳健性是 CONDITIONAL，也所以这里没有任何一句是关于 "
        "Rust 的论断。plugins.lapce.dev 没有被访问：方法把扫描代码里读到的 URL 当作只渲染、"
        "不请求的数据。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repositories · static analysis at lapce c9e4c33, floem 31fa8f44, zed 90d024b · GitHub API "
        "for history · no build, benchmark or application run",
        "公开仓库 · 静态分析于 lapce c9e4c33、floem 31fa8f44、zed 90d024b · 历史数据取自 GitHub API · 没有构建、"
        "基准或运行应用",
    ),
}
