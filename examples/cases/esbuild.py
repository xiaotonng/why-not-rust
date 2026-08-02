"""evanw/esbuild — every advertised advantage of a Rust rewrite, already achieved in Go.

Repository facts were measured read-only on the shallow clone named in
`repository`.
"""

CASE = {
    "slug": "esbuild",
    "project_name": "evanw/esbuild",
    "project_desc": ("Go · JavaScript bundler · 149,016 lines of Go across 152 files",
                     "Go · JavaScript 打包器 · 149,016 行 Go，分布在 152 个文件"),
    "date": "2026-08-01",
    "archetype": ("compiler-buildtool · single-binary CLI with a reproducible benchmark",
                  "编译构建工具 · 单二进制 CLI，自带可复现基准"),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "stay-go",
    "scope_chip": ("keep Go; the benefit the rewrite promises is already banked",
                   "继续用 Go；重写承诺的收益已经到账"),
    "scope_sub": ("keep the language that already delivered the win",
                  "保留那门已经把胜利兑现的语言"),

    "why": (
        "Gate 1 fails before gate 2 gets a turn. Nobody has stated a performance requirement that "
        "esbuild misses. The repository's own benchmark puts it about two orders of magnitude ahead of "
        "the JavaScript bundler it replaced. The author has published the decomposition as well: native "
        "ahead-of-time compilation, shared-memory parallelism, from-scratch data structures, exactly "
        "three AST passes. Zero of the four are Rust properties. All four were obtained in a "
        "garbage-collected language.",
        "G1 没过，G2 就没有轮到。没有人写下过 esbuild 达不到的性能要求。仓库自带的基准显示，它比被它取代的那个 "
        "JavaScript 打包器快出大约两个数量级。作者本人也公布过原因拆解：原生 AOT 编译、共享内存并行、数据结构"
        "全部从零自建、AST 恰好三遍。四条里没有一条是 Rust 专属。四条都是在带垃圾回收的语言里拿到的。"
    ),
    "trigger": (
        "Stable. One thing reopens it: a measured requirement Go cannot meet — a hard sub-10 ms "
        "invocation budget, a wasm-only host where the Go runtime is disqualifying, or a memory ceiling "
        "with a published break-even. None is asserted today.",
        "稳定。只有一件事能把它重新打开：一条测量过、而 Go 达不到的要求——硬性的 sub-10 ms 调用预算，只能跑 "
        "wasm、Go 运行时直接出局的宿主，或者带公开盈亏平衡点的内存上限。今天这些都没人提出。"
    ),

    "gates": [
        {"id": "G1", "state": "FAIL", "short": ("Requirement", "要求"),
         "hero_evidence": ("No unmet performance target; the reproducible bench is ~106×.",
                           "没有未达成的性能目标；可复现基准约 106×。"),
         "name": "requirement",
         "evidence": "The repository ships `make bench-three`, and the published result is 0.39 s for esbuild against 41.21 s for webpack 5 on the same input. No SLO, cost ceiling, or memory budget is stated as unmet."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果归因"),
         "hero_evidence": ("All four documented speed factors are non-Rust-specific.",
                           "四条已公布的提速因素，没有一条是 Rust 专属。"),
         "name": "rust-specific causality",
         "evidence": "The author's own four-factor account — native AOT compilation, shared-memory parallelism, consistent purpose-built data structures, and exactly three AST passes — describes properties of compiled languages and of this architecture, not of Rust. All four were achieved with a GC."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("149,016 lines rewritten to chase an unquantified delta.",
                           "重写 149,016 行，去追一个没有量化的差值。"),
         "name": "economics and smallest sufficient option",
         "evidence": "With no target to meet, the benefit interval for any rewrite is undefined, while the cost is a full reimplementation of 140,018 lines of internal packages plus its plugin and API surface."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("Staying has no delivery risk; the current build ships.",
                           "不动没有交付风险；当前构建已经在发货。"),
         "name": "delivery and reversibility",
         "evidence": "The selected option is the status quo: single static binary, cross-compiled, already distributed. There is nothing to dual-run and nothing to roll back."},
    ],

    "tiles": [
        (("Reproducible benchmark", "可复现基准"), "0.39 vs 41.21", ("s", "s"),
         ("make bench-three · esbuild vs webpack 5", "make bench-three · esbuild 对 webpack 5")),
        (("Total Go source", "Go 源码总量"), "149,016", ("lines", "行"),
         ("152 files · internal/ is 140,018 of them", "152 个文件 · 其中 internal/ 占 140,018 行")),
        (("Goroutine launch sites", "goroutine 启动点"), "45", ("sites", "处"),
         ("incl. the per-file parse fan-out · bundler.go:1633",
          "含按文件的解析扇出 · bundler.go:1633")),
        (("AST passes", "AST 遍数"), "3", ("passes", "遍"),
         ("author-documented design constraint", "作者写明的设计约束")),
        (("Speed factors that need Rust", "非 Rust 不可的提速因素"), "0", ("of 4", "/ 4"),
         ("native AOT · parallelism · data structures · passes",
          "原生 AOT · 并行 · 数据结构 · 遍数")),
        (("Unmet requirement on record", "在案的未满足要求"), "0", ("stated", "条"),
         ("why G1 fails before G2 is reached", "G1 就此失败，G2 没有轮到")),
    ],

    "options_sub": ("Every option answers the same objective: reduce bundler wall-clock time against a "
                    "stated target. No such target is currently unmet. That is the finding.",
                    "所有方案回答的是同一个目标：把打包墙钟时间压到某个写明的指标之下。目前没有任何这样的指标"
                    "处在未达成状态。这就是结论。"),
    "options": [
        {"id": "stay-go", "name": ("Keep Go", "继续用 Go"), "implementation": "current", "scope": "stay",
         "scope_tag": "STAY",
         "benefit_interval": ("already at the measured result", "已经处在测得的结果上"),
         "one_time_cost": "none", "recurring_cost": "none new",
         "cost_cell": ("none; none new", "无；无新增"),
         "time_to_value": ("in effect today", "今天就已生效"),
         "compatibility": "native",
         "compat_cell": ("native · nothing to roll back", "原生 · 没有要回滚的东西"),
         "reversibility": "n/a", "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · the requirement is already met", "推荐 · 要求已经满足"),
         "reason": "No stated requirement is unmet, and the reproducible benchmark is in the repository."},
        {"id": "go-profile", "name": ("Profile and optimize in Go", "在 Go 里剖析并优化"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("whatever a profile finds; unbounded upward", "剖析找到多少算多少；上限不封顶"),
         "one_time_cost": "days per finding", "recurring_cost": "none",
         "cost_cell": ("days per finding; none recurring", "每个发现数天；无经常性成本"),
         "time_to_value": ("days", "数天"),
         "compatibility": "native", "compat_cell": ("native · git revert", "原生 · git revert"),
         "reversibility": "git revert", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded first move if a target ever appears",
                  "保留 · 一旦出现指标，这是有预算的第一步"),
         "reason": "If a requirement is ever stated, this is the cheapest option and must be tried before any rewrite."},
        {"id": "rust-hot-extract", "name": ("Rust kernel behind a Go boundary", "Go 边界后面放一个 Rust 内核"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("undefined — no hot kernel is identified", "无从定义——没有识别出热点内核"),
         "one_time_cost": "cgo or IPC boundary plus parity", "recurring_cost": "second toolchain, cgo build complexity",
         "cost_cell": ("boundary + parity; second toolchain", "边界 + 行为对齐；第二套工具链"),
         "time_to_value": ("months", "数月"),
         "compatibility": "shared AST would have to cross",
         "compat_cell": ("AST across a boundary · flag rollback", "AST 要跨边界 · 用编译开关回滚"),
         "reversibility": "build flag", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · recorded to be complete, not because it is promising",
                  "保留 · 记录在案是为了完整，不是因为它有希望"),
         "reason": "esbuild's design shares one AST across all passes in one address space; extracting a kernel would have to serialize or duplicate it, which is the cost esbuild's architecture exists to avoid."},
        {"id": "rust-full", "name": ("Rewrite esbuild in Rust", "用 Rust 重写 esbuild"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("no evidence of any end-to-end gain", "没有任何端到端收益的证据"),
         "one_time_cost": "149,016 lines plus the plugin and JS API surface", "recurring_cost": "new maintainer set for a single-author codebase",
         "cost_cell": ("149,016 lines; new maintainers", "149,016 行；一套新的维护者"),
         "time_to_value": ("years", "数年"),
         "compatibility": "CLI + JS API + plugin behaviour",
         "compat_cell": ("whole surface · no rollback", "整个接口面 · 无法回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G1 and G2", "排除 · G1、G2 都不过"),
         "reason": "No requirement is unmet, and the documented sources of esbuild's speed are not Rust-specific."},
        {"id": "adopt-rust-bundler", "name": ("Adopt a Rust bundler instead", "改用一个 Rust 打包器"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("depends on the project's own measurement", "取决于各项目自己的测量"),
         "one_time_cost": "per project migration", "recurring_cost": "different plugin ecosystem",
         "cost_cell": ("per project; new plugin ecosystem", "按项目计；换一套插件生态"),
         "time_to_value": ("days per project", "每个项目数天"),
         "compatibility": "different config and plugins",
         "compat_cell": ("different config · switch back", "配置不同 · 可以换回来"),
         "reversibility": "switch back", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · a user's choice, and it is not a rewrite of esbuild",
                  "保留 · 这是使用方的选择，不是重写 esbuild"),
         "reason": "A project with a measured need that esbuild misses can adopt another native bundler today; that is a consumer decision, not an argument for rewriting esbuild."},
    ],

    "lenses_sub": ("Each state is evidence scoped to a named option, not a point to be summed. Several "
                   "lenses come out NEUTRAL for one reason: the Go implementation already holds the "
                   "property the Rust option would be adopted to obtain.",
                   "每个状态都是绑定到具体方案的证据，不是可以相加的分数。有几个维度判为 NEUTRAL，原因相同："
                   "Go 实现已经具备了那个「换 Rust 才能拿到」的性质。"),
    "na_note": ("N/A lenses: D6 safety and D10 boundary carry no part of this objective. Go is memory-safe "
                "at application scope, the codebase declares no FFI surface, and the selected option "
                "introduces no new boundary.",
                "判为 N/A 的维度：D6 安全与 D10 边界在这个目标里不承担任何份额。Go 在应用层是内存安全的，"
                "代码库没有声明 FFI 面，选中的方案也不引入新边界。"),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "要求与归属"),
         "label": "DISFAVORS · rust options", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full", "rust-hot-extract"],
         "claim": ("No unmet performance requirement is stated anywhere in the repository or its "
                   "documentation. The repository also ships a reproducible benchmark. It puts the tool "
                   "about two orders of magnitude ahead of the bundler it replaced.",
                   "仓库和文档里都没有写下任何未满足的性能要求。仓库还自带一套可复现基准，显示这个工具比"
                   "被它取代的打包器快出大约两个数量级。"),
         "source": "Makefile bench-three targets · https://esbuild.github.io/faq/",
         "regime": "repository-reproducible benchmark on a fixed input",
         "caveat": "The 106× comparison is against a JavaScript bundler, not against another native tool; it establishes that no gap is unmet, not that esbuild is the fastest possible."},
        {"id": "D2", "name": ("End-to-end reach", "端到端可达"), "label": "UNKNOWN · rust options", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-full", "rust-hot-extract"],
         "claim": ("No kernel share can be computed: no target is identified and no hot kernel is "
                   "identified. With no f and no target, the Amdahl formula has no defensible inputs.",
                   "算不出内核占比：目标没有，热点内核也没有识别出来。没有 f 也没有目标，Amdahl 公式就没有"
                   "站得住的输入。"),
         "source": "no stated target; no identified hot kernel",
         "regime": "n/a", "caveat": "Recorded UNKNOWN rather than assumed zero."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("A batch bundler has no tail-latency SLO. Nobody has filed Go's collector pauses as a "
                   "problem for a process that runs once and exits.",
                   "批处理打包器没有尾延迟 SLO。对一个跑一次就退出的进程，没有人把 Go 的 GC 停顿列为问题。"),
         "source": "batch CLI invocation model",
         "regime": "invocation shape", "caveat": "A long-running dev server changes this question, and is not the assessed target."},
        {"id": "D4", "name": ("Fleet footprint", "机群占用"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("esbuild runs on developer machines and CI runners. No fleet-density objective or "
                   "break-even is stated.",
                   "esbuild 跑在开发者机器和 CI runner 上。没有写明任何机群密度目标或盈亏平衡点。"),
         "source": "developer and CI invocation", "regime": "n/a",
         "caveat": "Memory efficiency is one of the author's four documented factors, and it was achieved in Go."},
        {"id": "D5", "name": ("Startup shape", "启动形态"), "label": "SUPPORTS · stay-go", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-go"],
         "claim": ("For a CLI the property that matters is native ahead-of-time compilation with no "
                   "interpreter and no JIT warmup. The Go implementation already holds it.",
                   "对 CLI 来说，起作用的性质是原生 AOT 编译，没有解释器，也没有 JIT 预热。Go 实现已经具备。"),
         "source": "https://esbuild.github.io/faq/ — factor 1 of 4",
         "regime": "author's published decomposition",
         "caveat": "First-party account; the four factors are described as individually modest and jointly large."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Go is memory-safe at application scope, and the codebase declares no native or FFI "
                   "surface. No memory-safety delta is left to claim.",
                   "Go 在应用层是内存安全的，代码库也没有声明任何原生或 FFI 接口面。这里没有可以主张的"
                   "内存安全增量。"),
         "source": "pure-Go module, no cgo in the build",
         "regime": "n/a",
         "caveat": "Race-freedom claims would need their own incident evidence; none is present."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"), "label": "SUPPORTS · stay-go", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-go"],
         "claim": ("Shared-memory parallelism is the factor JavaScript workers cannot supply, because they "
                   "must serialize. In Go it is already present and load-bearing: 45 goroutine launch "
                   "sites across 149,016 lines, including the per-file parse fan-out, plus 27 in-code "
                   "sync.WaitGroup references.",
                   "共享内存并行是 JavaScript worker 给不了的那一条，它们之间必须序列化。在 Go 这边它已经"
                   "存在，而且承重：149,016 行里有 45 处 goroutine 启动点，含按文件的解析扇出，另有 27 处"
                   "代码内的 sync.WaitGroup 引用。"),
         "source": "internal/bundler/bundler.go:1633 `go parseFile(` · 23 anonymous `go func(` + 22 named launches · 29 sync.WaitGroup lines, 27 outside comments",
         "regime": "static count of parallel constructs in this commit",
         "caveat": "Counting constructs measures intent, not achieved scaling."},
        {"id": "D8", "name": ("Distribution", "分发"), "label": "NEUTRAL · stay-go, rust-full", "css": "neutral",
         "state": "NEUTRAL", "strength": "STRONG", "option_ids": ["stay-go", "rust-full"],
         "claim": ("Go already produces one statically linked, cross-compiled binary with no runtime "
                   "dependency. That is the distribution property a Rust rewrite would be adopted to obtain.",
                   "Go 已经产出单个静态链接、可交叉编译、无运行时依赖的二进制。这正是「为分发而换 Rust」"
                   "想要拿到的性质。"),
         "source": "go.mod single-module build · released platform binaries",
         "regime": "shipped distribution model",
         "caveat": "Rust binaries can be smaller; no size requirement is stated."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Native bundlers exist in both Go and Rust, so ecosystem availability favours neither "
                   "for this objective. A consumer with a measured need can adopt an alternative without "
                   "esbuild changing anything.",
                   "Go 和 Rust 都有原生打包器，就这个目标而言，生态供给不偏向任何一边。使用方如果有测量过的"
                   "需求，可以直接换一个，esbuild 什么都不用动。"),
         "source": "external bundler landscape",
         "regime": "market inventory", "caveat": "Plugin ecosystems differ and are the real switching cost for consumers."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("The selected option introduces no boundary. The extraction option would have to move a "
                   "shared AST across one, which is the cost this architecture exists to avoid.",
                   "选中的方案不引入边界。抽取方案则必须把一份共享 AST 搬过边界，而这套架构存在的目的就是"
                   "避开这笔成本。"),
         "source": "single-address-space AST design", "regime": "n/a",
         "caveat": "That cost is priced under the extraction option rather than here."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": ("This is a 149,016-line codebase whose architecture is documented as deliberately "
                   "from-scratch and internally consistent. A reimplementation has to reproduce that "
                   "coherence, plus the CLI, the JS API and plugin behaviour. Nothing funds it.",
                   "这是一个 149,016 行的代码库，作者写明其架构是刻意从零自建、内部一致的。重新实现必须把"
                   "这份一致性重做一遍，还要加上 CLI、JS API 和插件行为。没有任何收益为它买单。"),
         "source": "internal/ 140,018 lines across 133 files · pkg/ 6,884 lines",
         "regime": "static inventory in this commit",
         "caveat": "Line count is a proxy for effort; the plugin and API compatibility surface may dominate it."},
        {"id": "D12", "name": ("Counterfactual", "反事实对照"), "label": "SUPPORTS · stay-go, go-profile", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-go", "go-profile"],
         "claim": ("The strongest non-Rust native alternative is not hypothetical here; it is the shipping "
                   "implementation. Microsoft reached the same conclusion independently on a comparable "
                   "workload, porting the TypeScript compiler to Go for a measured 77.8 s → 7.5 s and "
                   "choosing it over Rust.",
                   "这里最强的非 Rust 原生方案不是假设，它就是正在发货的那套实现。Microsoft 在一个可比的"
                   "工作负载上独立得出了同样结论：把 TypeScript 编译器移植到 Go，实测 77.8 s → 7.5 s，"
                   "并且是在与 Rust 对比后选的 Go。"),
         "source": "https://devblogs.microsoft.com/typescript/typescript-native-port/",
         "regime": "first-party preview benchmark on the VS Code repository",
         "caveat": "A compiler port, not a bundler; and the choice turned partly on cyclic AST semantics specific to that codebase."},
    ],

    "findings": [
        ("current",
         ("The benchmark ships in the repository, and anyone can run it",
          "基准就在仓库里，谁都能跑"),
         ("The Makefile ships bench-three targets that build the same input with esbuild, rollup, "
          "webpack 5 and parcel 2. The published result is 0.39 s against webpack 5's 41.21 s. Nobody has "
          "to take that on trust. G1 fails cleanly.",
          "Makefile 里有 bench-three 目标，用 esbuild、rollup、webpack 5 和 parcel 2 构建同一份输入。"
          "公布的结果是 0.39 s，webpack 5 是 41.21 s。这一条不需要谁去相信。G1 干净利落地失败。"),
         "Makefile · bench-three targets"),
        ("current",
         ("The author already published the attribution", "归因是作者自己公布的"),
         ("The author lists four factors, each described as only somewhat significant on its own: native "
          "ahead-of-time compilation, shared-memory parallelism, everything written from scratch with "
          "consistent data structures, and exactly three AST passes. Count the Rust properties. There are "
          "none.",
          "作者列了四条，每一条单独看都只是「有点用」：原生 AOT 编译、共享内存并行、所有数据结构从零自建"
          "并保持一致、AST 恰好三遍。数一下里面有几条是 Rust 专属。一条都没有。"),
         "esbuild.github.io/faq/"),
        ("current",
         ("The parallelism is in the parse fan-out", "并行发生在解析扇出上"),
         ("A JavaScript bundler structurally cannot have shared-memory parallelism. Its workers must "
          "serialize. esbuild gets it in Go across 45 goroutine launch sites, and the load-bearing one is "
          "the per-file parse fan-out — every source file goes to its own goroutine over shared memory.",
          "JavaScript 打包器在结构上拿不到共享内存并行，它的 worker 之间必须序列化。esbuild 在 Go 里用 "
          "45 处 goroutine 启动点拿到了它，承重的那一处是按文件的解析扇出：每个源文件交给自己的 goroutine，"
          "走共享内存。"),
         "internal/bundler/bundler.go:1633 · 23 anonymous + 22 named launches"),
        ("current",
         ("Microsoft ran the same comparison and also chose Go", "Microsoft 做过同样的对比，选的也是 Go"),
         ("The TypeScript compiler's native port went from 77.8 s to 7.5 s on the VS Code repository. The "
          "language was Go. It was explicitly picked over Rust for a behaviour-preserving port with "
          "cyclic AST semantics. Native execution and shared-memory parallelism are not Rust-exclusive.",
          "TypeScript 编译器的原生移植在 VS Code 仓库上从 77.8 s 降到 7.5 s。用的语言是 Go。这是明确"
          "对比 Rust 之后的选择，理由是移植要保行为、AST 又是有环的。原生执行和共享内存并行不是 Rust 独有的。"),
         "devblogs.microsoft.com/typescript/typescript-native-port/"),
        ("rust",
         ("What would change this answer", "什么会改变这个答案"),
         ("A stated requirement Go cannot meet. A hard sub-10 ms invocation budget, a wasm-only host where "
          "the Go runtime is disqualifying, or a memory ceiling with a published break-even. They are "
          "named here so the verdict can be falsified.",
          "一条写明了的、Go 达不到的要求。硬性的 sub-10 ms 调用预算，只能跑 wasm、Go 运行时直接出局的宿主，"
          "或者带公开盈亏平衡点的内存上限。把它们列出来，是为了让这个判定可以被证伪。"),
         "change trigger · no such requirement asserted today"),
    ],

    "buys": [
        (("Nothing this objective needs", "这个目标需要的东西，一样也没有"),
         ("the four documented sources of esbuild's speed are already banked in Go. Rust would re-obtain "
          "them, not add to them.",
          "esbuild 提速的四个已公布来源，在 Go 里都已经到账。Rust 只是把它们再拿一遍，不会往上加。")),
        (("A smaller binary and no collector", "更小的二进制，没有 GC"),
         ("both are Rust properties. No stated requirement in this project is satisfied by either one.",
          "这两条确实是 Rust 的性质。但这个项目里没有任何写明的要求靠它们来满足。")),
        (("A different plugin ecosystem for consumers", "给使用方的另一套插件生态"),
         ("projects with a measured need esbuild misses can adopt a Rust bundler today, without esbuild "
          "rewriting anything.",
          "如果某个项目有 esbuild 满足不了的、测量过的需求，今天就可以换一个 Rust 打包器，esbuild 一行都"
          "不用重写。")),
    ],
    "nobuys": [
        (("Speed, on this evidence", "提速，就现有证据而言"),
         ("no unmet target exists and no hot kernel is identified. No end-to-end gain can be predicted at all.",
          "没有未达成的目标，也没有识别出热点内核。端到端收益完全无法预测。")),
        (("Memory safety", "内存安全"),
         ("Go is memory-safe at application scope and the build declares no FFI surface. There is no class "
          "of bug left to eliminate.",
          "Go 在应用层是内存安全的，构建也没有声明 FFI 面。没有哪一类缺陷可以被消掉。")),
        (("Better distribution", "更好的分发"),
         ("Go already ships one statically linked cross-compiled binary with no runtime dependency.",
          "Go 已经在发一个静态链接、交叉编译、无运行时依赖的二进制。")),
    ],

    "precedents": [
        {"name": "Microsoft · TypeScript native port", "outcome": "NON-RUST",
         "body": ("A behaviour-preserving native port of tsc reached 77.8 s → 7.5 s on the VS Code "
                  "repository, at about half the memory. Go won the language call against Rust. Cyclic AST "
                  "graphs and 1:1 compatibility mattered more there than the absence of a collector.",
                  "tsc 的一次保行为原生移植，在 VS Code 仓库上做到 77.8 s → 7.5 s，内存约为原来的一半。"
                  "语言这一关，Go 赢了 Rust。有环的 AST 图和 1:1 兼容，在那边比「没有 GC」更重要。"),
         "match": ("same workload class, same 'native beats JS' finding, explicit Rust-versus-Go comparison",
                   "同一类工作负载，同样得出「原生胜过 JS」，而且是明确的 Rust 对 Go 比较"),
         "mismatch": ("a compiler port rather than a bundler, and a redesign was explicitly forbidden there",
                      "那是编译器移植不是打包器，而且那边明确禁止重新设计"),
         "regime": "first-party preview benchmark", "source_label": "first-party · vendor blog",
         "url": "https://devblogs.microsoft.com/typescript/typescript-native-port/"},
        {"name": "Prettier · pure-JavaScript CLI rework", "outcome": "STAYED",
         "body": ("Roughly 3× came from profiling, caching and IPC fixes, with no language change. It "
                  "landed days after a Rust competitor claimed the speed bounty. The baseline was "
                  "unoptimized JavaScript, not JavaScript.",
                  "大约 3× 来自剖析、缓存和 IPC 修复，语言没有换。落地时间是在一个 Rust 竞品拿走提速悬赏之后"
                  "几天。基线是未经优化的 JavaScript，不是 JavaScript 本身。"),
         "match": ("in-stack optimization as the option that must be priced before a rewrite",
                   "在原栈内优化，是重写之前必须先定价的那个方案"),
         "mismatch": ("Prettier had an unmet gap; esbuild has none stated",
                      "Prettier 当时确有一个未满足的差距；esbuild 没有任何写明的差距"),
         "regime": "reproduced 29 s → 9 s", "source_label": "first-party · project blog",
         "url": "https://prettier.io/blog/2023/11/30/cli-deep-dive"},
        {"name": "Vercel · Turbopack launch benchmark", "outcome": "RETRACTED",
         "body": ("A launch claim of 700× against webpack turned out to compare Turbopack plus SWC against "
                  "Vite plus Babel. Match the configurations and the gap mostly closed. The shipped "
                  "product still landed at a first-party 2–5×.",
                  "发布时宣称对 webpack 有 700×，后来查明比的是 Turbopack 加 SWC 对 Vite 加 Babel。把配置"
                  "对齐之后，差距基本消失。产品本身最终落在第一方口径的 2–5×。"),
         "match": ("the benchmark-method risk that any Rust-versus-Go bundler comparison invites",
                   "任何 Rust 对 Go 的打包器比较都会招来的基准方法风险"),
         "mismatch": ("concerns marketing methodology rather than esbuild's own reproducible harness",
                      "问题出在营销口径，而不是 esbuild 自带的可复现测试台"),
         "regime": "warm-incremental HMR on synthetic trees", "source_label": "third-party · maintainer analysis",
         "url": "https://github.com/yyx990803/vite-vs-next-turbo-hmr/discussions/8"},
        {"name": "Astral · ruff", "outcome": "MIGRATED",
         "body": ("The counterexample. A Rust tool did displace a federation of Python linters, and "
                  "adopter-reported gains ran far above the vendor's claims. The attribution was "
                  "parse-once architecture plus native execution plus GIL-free parallelism.",
                  "反例在这里。一个 Rust 工具确实把一堆 Python linter 挤了出去，采用方自己报的收益远高于"
                  "厂商口径。归因是「只解析一次」的架构，加上原生执行，加上没有 GIL 的并行。"),
         "match": ("same tool category, and it shows a native rewrite can win outright",
                   "同一类工具，而且它证明原生重写可以赢得彻底"),
         "mismatch": ("the baseline was an interpreted federation re-parsing files; esbuild is already a single native tool",
                      "那边的基线是一堆解释型工具反复重解析文件；esbuild 本身已经是单个原生工具"),
         "regime": "adopter-reported and vendor figures", "source_label": "third-party · adopter reports",
         "url": "https://github.com/astral-sh/ruff"},
    ],

    "path": [
        {"title": ("State a requirement or close the question", "要么写下一条要求，要么把问题关掉"),
         "body": ("Whoever wants the rewrite writes the target down: a performance, memory or distribution "
                  "number the current build measurably misses. It has to be a number with a workload "
                  "attached, measured on the repository's own benchmark harness. If no such target exists, "
                  "close the question here. That is today's state, and no code moves.",
                  "想要重写的人先把指标写下来：一个当前构建确实达不到的性能、内存或分发数字。它必须是带"
                  "工作负载的数字，并且在仓库自带的基准台上测出来。如果根本没有这样的指标，问题就到此为止。"
                  "今天就是这个状态，代码一行不动。"),
         "owner": "the proposer",
         "cost_range": ("1 day", "1 天"),
         "artifact": "a written performance, memory or distribution target that the current build measurably misses",
         "acceptance": "the target is a number with a workload, measured on the repository's own benchmark harness",
         "stop": "close the question if no such target exists — that is the current state",
         "rollback": "no code changes"},
        {"title": ("Profile in Go first", "先在 Go 里做剖析"),
         "body": ("A contributor profiles the failing workload for CPU and allocations, and names the top "
                  "contributors. It passes when the profile reproducibly identifies a component holding a "
                  "material share of wall-clock. If the time is spread thin with no dominant component, "
                  "stop. A rewrite would not reach it either.",
                  "由一位贡献者对这个不达标的负载做 CPU 和分配剖析，点名排在前面的贡献者。通过标准是：剖析"
                  "能可复现地指出某个组件占了墙钟时间里可观的一块。如果时间摊得很平、没有主导组件，就停。"
                  "重写同样够不到它。"),
         "owner": "a contributor",
         "cost_range": ("3–5 days", "3–5 天"),
         "artifact": "a CPU and allocation profile of the failing workload with the top contributors named",
         "acceptance": "the profile identifies a component holding a material share of wall-clock, reproducibly",
         "stop": "stop if time is distributed with no dominant component; a rewrite would not help either",
         "rollback": "measurement only"},
        {"title": ("Fund the in-Go fix before considering a boundary", "先给 Go 内的修复出钱，再谈边界"),
         "body": ("The same contributor lands the optimization the profile points at and measures it on the "
                  "same harness. It passes when the stated target is met, or when the leftover gap is "
                  "quantified. Escalate past Go only if that gap survives and is attributable to a "
                  "language-class property Go lacks. Rollback is a git revert; the released binary never "
                  "sees it.",
                  "同一位贡献者把剖析指向的优化落地，并在同一套测试台上测量。通过标准是：写明的指标达成，"
                  "或者剩余差距被量化出来。只有当这个差距仍然存在、并且能归因到 Go 缺失的某项语言级性质时，"
                  "才升级到 Go 之外。回滚就是一条 git revert，已发布的二进制不受影响。"),
         "owner": "a contributor",
         "cost_range": ("days per finding", "每个发现数天"),
         "artifact": "the optimization the profile implies, measured on the same harness",
         "acceptance": "the stated target is met, or the remaining gap is quantified",
         "stop": "escalate only if the gap survives and is attributable to a language-class property Go lacks",
         "rollback": "git revert; the released binary is unaffected"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端可达"), "state": "HIT",
         "claim": ("No kernel and no target are identified, so no end-to-end reach can be argued for any "
                   "Rust option. D2 is UNKNOWN.",
                   "既没有内核也没有目标，任何 Rust 方案都谈不上端到端可达。D2 记为 UNKNOWN。"),
         "evidence": "D2 record"},
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The four documented factors behind esbuild's speed are language-class and "
                   "architectural. None of them is credited to Rust here.",
                   "esbuild 提速的四个已公布因素属于语言级和架构级。这里没有把其中任何一条记在 Rust 头上。"),
         "evidence": "esbuild.github.io/faq/ · G2 FAIL"},
        {"name": ("Baseline and regime", "基线与口径"), "state": "PASS",
         "claim": ("The 106× figure is disclosed as a comparison against a JavaScript bundler, not against "
                   "another native tool. It is used only to show that no gap is unmet.",
                   "106× 这个数字已声明是对 JavaScript 打包器的比较，不是对另一个原生工具。它只用来说明"
                   "没有未满足的差距。"),
         "evidence": "D1 caveat"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("The extraction option is priced with the cost of moving a shared AST across a boundary, "
                   "which is what this architecture exists to avoid.",
                   "抽取方案在定价时算进了「共享 AST 跨边界」的成本，而这套架构存在的目的就是避开它。"),
         "evidence": "D10 · rust-hot-extract reason"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The full-rewrite option is priced with the maintainer question, for a codebase whose "
                   "coherence is one of its documented advantages.",
                   "全量重写方案在定价时算进了维护者问题——这个代码库的内部一致性本身就是它写明的优势之一。"),
         "evidence": "D11 record"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "反事实方案是否有预算"), "state": "PASS",
         "claim": ("The staying option is not hypothetical: the reproducible benchmark is in the repository "
                   "and the profile-first path is specified.",
                   "不动这个方案不是空谈：可复现基准就在仓库里，先剖析的路径也已经写明。"),
         "evidence": "Makefile bench-three · reversible path step 2"},
        {"name": ("Cost of inaction", "不作为的代价"), "state": "PASS",
         "claim": ("No missed SLO, cost overrun or security exposure is on record, so there is no cost of "
                   "inaction to omit.",
                   "在案记录里没有 SLO 未达、成本超支或安全暴露，所以不存在被漏掉的「不作为代价」。"),
         "evidence": "D1 · no stated unmet requirement"},
        {"name": ("Unsafe-surface omission", "是否漏掉不安全面"), "state": "PASS",
         "claim": ("The build is pure Go with no declared FFI surface, checked rather than assumed.",
                   "构建是纯 Go，没有声明 FFI 面。这是查过的，不是假设的。"),
         "evidence": "D6 · no cgo in the build"},
        {"name": ("Native-advantage denial", "是否否认原生优势"), "state": "PASS",
         "claim": ("Rust's advantages are stated plainly: smaller binaries, no collector. The finding is "
                   "that no requirement here needs them.",
                   "Rust 的优势这里直说了：二进制更小，没有 GC。结论只是这里没有任何要求用得上它们。"),
         "evidence": "buys/doesn't-buy columns"},
        {"name": ("Endless optimize-first treadmill", "「先优化」会不会没完没了"), "state": "PASS",
         "claim": ("The path carries an explicit escalation rule: if a quantified gap survives in-Go "
                   "optimization and is attributable to a property Go lacks, the decision reopens.",
                   "路径里写了明确的升级规则：如果一个量化过的差距在 Go 内优化之后仍然存在，并且能归因到 "
                   "Go 缺失的性质，这个决定就重开。"),
         "evidence": "reversible path step 3"},
    ],

    "gaps": [
        (("A stated, measured requirement the current build misses",
          "一条写明并测量过、当前构建确实达不到的要求"),
         ("Decisive. Without one, G1 fails and no Rust option can be assessed on benefit at all — this is "
          "the gap, not an oversight.",
          "决定性。没有它，G1 就是 FAIL，任何 Rust 方案的收益都无从评估——这个缺口本身就是结论，不是疏漏。")),
        (("A CPU and allocation profile of a failing workload", "一份不达标负载的 CPU 与分配剖析"),
         ("Would identify whether any component holds a material share, and therefore whether a boundary "
          "or a rewrite could reach it.",
          "它能判断有没有哪个组件占了可观的一块，进而判断边界或重写有没有可能够得着。")),
        (("Independent benchmarks against other native bundlers", "对其他原生打包器的独立基准"),
         ("The repository's harness compares against JavaScript tooling. A native-versus-native comparison "
          "would sharpen D12 in either direction.",
          "仓库自带的测试台比的是 JavaScript 工具链。原生对原生的比较会让 D12 更锐利，往哪边都算。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; goroutine and WaitGroup counts are static occurrences, not measured parallelism.",
        "The published bench-three figures are the author's own and were not re-run here, since running benchmarks requires the deep mode this analysis did not use.",
        "No requirement beyond bundler wall-clock time is asserted; a wasm-host or binary-size constraint would need its own assessment.",
    ],
    "objective": {
        "driver": "performance",
        "requirement": "reduce bundler wall-clock time against a stated target",
        "baseline": "0.39 s on the repository's own three.js benchmark, against 41.21 s for webpack 5",
        "target": "none stated — this is the finding, not a gap in the analysis",
    },
    "repository": {
        "path": "https://github.com/evanw/esbuild",
        "commit": "6ff1d8b0d8c134e867a397eef39702a223ebef9e",
        "scope": "whole repository",
        "sampling": "shallow clone; 349 tracked files enumerated; internal/, pkg/, Makefile and CHANGELOG measured; no benchmark was executed",
    },
    "user_supplied_facts": [],

    "method_title": ("evanw/esbuild at 6ff1d8b · static read-only analysis · why-not-rust method 2.0",
                     "evanw/esbuild @ 6ff1d8b · 只读静态分析 · why-not-rust 方法 2.0"),
    "method_body": (
        "Repository: github.com/evanw/esbuild at commit 6ff1d8b, shallow clone, 349 tracked files. Scope: "
        "the whole repository. Sampling: 149,016 lines of Go across 152 files, of which internal/ holds "
        "140,018 across 133 files and pkg/ holds 6,884; 45 goroutine launch sites (23 anonymous `go func(` "
        "plus 22 named, among them the per-file parse fan-out at internal/bundler/bundler.go:1633) and 29 "
        "sync.WaitGroup lines, 27 of them outside comments; bench targets read from the Makefile. Nothing "
        "was built, tested, benchmarked or fetched. The 0.39 s versus 41.21 s figures are the author's "
        "published results for the harness that ships in this repository, not measurements taken here. "
        "Objective: reduce bundler wall-clock time against a stated target. User-supplied facts: none. "
        "There is no Amdahl calculation, because there is no target and no identified hot kernel, so the "
        "formula has no defensible inputs; D2 is recorded UNKNOWN. G1 fails. Under this method's "
        "non-compensatory gates that ends the assessment, however good the delivery story for a rewrite "
        "might be. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/evanw/esbuild，commit 6ff1d8b，浅克隆，349 个受版本控制的文件。范围：整个仓库。"
        "采样：149,016 行 Go，分布在 152 个文件，其中 internal/ 占 140,018 行、133 个文件，pkg/ 占 6,884 行；"
        "45 处 goroutine 启动点（23 处匿名 `go func(` 加 22 处具名，其中包括 "
        "internal/bundler/bundler.go:1633 的按文件解析扇出）；29 行 sync.WaitGroup，其中 27 行不在注释里；"
        "bench 目标从 Makefile 读取。没有做任何构建、测试、基准或网络请求。0.39 s 对 41.21 s 这组数字是作者"
        "公布的、针对本仓库自带测试台的结果，不是这里测出来的。目标：把打包墙钟时间压到某个写明的指标之下。"
        "用户提供的事实：无。这里没有 Amdahl 计算，因为既没有目标，也没有识别出热点内核，公式没有站得住的"
        "输入；D2 记为 UNKNOWN。G1 FAIL。在这套方法的非补偿式门槛下，评估到此为止，无论重写的交付故事讲得"
        "多好。这是一套结构化决策协议，不是统计预测器。"
    ),
    "footer": ("public repository · static analysis at commit 6ff1d8b · no build, benchmark or network call",
               "公开仓库 · 在 commit 6ff1d8b 上的静态分析 · 没有构建、基准或网络请求"),
}
