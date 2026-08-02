"""curl/curl — the most-requested Rust rewrite in open source.

Every repository fact below was measured read-only on the shallow clone named in
`repository`. External numbers keep their URL and workload regime.
"""

CASE = {
    "slug": "curl",
    "project_name": "curl/curl",
    "project_desc": (
        "C · network client library + CLI · 258,953 lines of C across 757 files",
        "C · 网络客户端库 + 命令行工具 · 757 个文件、258,953 行 C",
    ),
    "date": "2026-08-01",
    "archetype": ("security-parser · library with a stable ABI", "安全解析器 · 带稳定 ABI 的库"),

    "scope_word": "EXTRACT",
    "auth": "APPROVE",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "rust-backend-seam",
    "scope_chip": ("one pluggable backend behind the existing vtls API", "既有 vtls 接口后面的一个可插拔后端"),
    "scope_sub": ("keep Rust at the backend seam curl already ships", "把 Rust 留在 curl 已经发布的那道后端接缝上"),

    "why": (
        "curl parses attacker-controlled bytes in C at a network trust boundary. It has already found "
        "the seam where Rust pays: lib/vtls/rustls.c, 1,468 lines behind an abstraction that already "
        "hosts six backends. Pushing Rust deeper cost four ISRG-funded years — the hyper HTTP backend "
        "reached near test-suite parity and was still removed in 8.12.0, for lack of contributors and "
        "users. G4 authorizes the seam and stops there.",
        "curl 在网络信任边界上用 C 解析攻击者可控的字节。它已经找到了 Rust 能兑现价值的那道接缝："
        "lib/vtls/rustls.c，1,468 行，挂在一个已经托管六个后端的抽象后面。往更深处推的代价是 ISRG 资助的四年——"
        "hyper HTTP 后端做到了接近测试套件对等，仍然在 8.12.0 被移除，原因是缺贡献者、缺用户。"
        "G4 只授权这道接缝，到此为止。",
    ),
    "trigger": (
        "Stable. Two things reopen it. The rustls or quiche backend loses its maintainer. Or a funded "
        "team with dual C/Rust expertise commits to the deeper HTTP layer with a named on-call owner — "
        "the exact resource whose absence killed hyper.",
        "STABLE。两件事会重开它。rustls 或 quiche 后端失去维护者。或者一支有 C/Rust 双栈能力的资助团队接手"
        "更深的 HTTP 层，并指定 on-call 负责人——正是这项资源的缺席终结了 hyper。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("C parsing attacker-controlled bytes across TLS, HTTP and QUIC.",
                           "TLS、HTTP、QUIC 三层的攻击者可控字节，都由 C 解析。"),
         "name": "requirement",
         "evidence": "176,402 lines of C and headers in lib/ terminate untrusted network input; curl runs a formal advisory process (docs/VULN-DISCLOSURE-POLICY.md, docs/SECURITY-ADVISORY.md)."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果归属"),
         "hero_evidence": ("Memory-safe TLS state machine is a Rust-class change, not a redesign.",
                           "内存安全的 TLS 状态机靠换语言就能拿到，不需要重新设计。"),
         "name": "rust-specific causality",
         "evidence": "The safety delta comes from replacing manual-lifetime C at a hostile boundary; no algorithm, protocol, or architecture change is required to obtain it."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("1,468-line backend vs the deleted whole-HTTP-layer attempt.",
                           "1,468 行的后端，对上那个已被删除的整层 HTTP 尝试。"),
         "name": "economics and smallest sufficient option",
         "evidence": "lib/vtls/rustls.c is 5.8% of the 25,481-line vtls layer and 0.8% of lib/; the deeper alternative consumed four funded years and shipped nothing durable."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("Six selectable backends share one interface; 2,056 cases gate parity.",
                           "六个可选后端共用一个接口；2,056 个用例把住对等性。"),
         "name": "delivery and reversibility",
         "evidence": "Six interchangeable TLS backends share the vtls interface, so rollback is a configure flag; tests/ carries 232,601 lines and 2,056 test cases as the parity harness."},
    ],

    "tiles": [
        (("Rust already in tree", "树里已有的 Rust"), "1,468", ("lines", "行"),
         ("lib/vtls/rustls.c · shipped TLS backend", "lib/vtls/rustls.c · 已发布的 TLS 后端")),
        (("Rust removed from tree", "从树里删掉的 Rust"), "8.12.0", ("release", "版本"),
         ("docs/DEPRECATE.md:62 — hyper HTTP backend", "docs/DEPRECATE.md:62 — hyper HTTP 后端")),
        (("Backend seam width", "后端接缝的宽度"), "5.8", ("%", "%"),
         ("rustls.c share of the 25,481-line vtls layer", "rustls.c 在 25,481 行 vtls 层里的占比")),
        (("C the seam does not touch", "接缝够不到的 C"), "176,402", ("lines", "行"),
         ("lib/ .c and .h — protocol, transfer, ABI", "lib/ 的 .c 和 .h — 协议、传输、ABI")),
        (("Parity harness", "对等性测试台"), "2,056", ("cases", "用例"),
         ("tests/data · inside a 232,601-line tests/ tree", "tests/data · 位于 232,601 行的 tests/ 树内")),
        (("Public API surface", "公开 API 面"), "526", ("pages", "页"),
         ("docs/libcurl/**/*.md — the compatibility contract", "docs/libcurl/**/*.md — 兼容性契约")),
    ],

    "options_sub": (
        "Same objective for every option: remove the memory-unsafety class from curl's handling of "
        "attacker-controlled bytes without breaking the libcurl ABI.",
        "每个方案的目标相同：在不破坏 libcurl ABI 的前提下，从 curl 处理攻击者可控字节的路径上，"
        "消除内存不安全这一整类问题。",
    ),
    "options": [
        {"id": "c-harden", "name": ("Harden C in place", "就地加固 C"), "implementation": "current", "scope": "stay",
         "scope_tag": "STAY", "benefit_interval": ("reduces, does not eliminate", "降低，不消除"),
         "one_time_cost": "continuous", "recurring_cost": "fuzzing + review time",
         "cost_cell": ("continuous; fuzz + review", "持续投入；fuzz + 评审"),
         "time_to_value": ("already running", "已经在跑"),
         "compatibility": "native", "compat_cell": ("native · no risk", "原生 · 无风险"), "reversibility": "n/a",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · necessary, not sufficient", "保留 · 必要，但不充分"),
         "reason": "Fuzzing and review lower incident rate but leave the memory-unsafety class reachable in 176,402 lines of C and headers."},
        {"id": "rust-backend-seam", "name": ("Rust backends at vtls/vquic", "在 vtls/vquic 上挂 Rust 后端"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("eliminates the class inside the selected backend", "在所选后端内部消除该类问题"),
         "one_time_cost": "already paid for rustls", "recurring_cost": "one backend maintainer",
         "cost_cell": ("already paid; 1 maintainer", "成本已付；1 名维护者"),
         "time_to_value": ("shipped", "已发布"),
         "compatibility": "compile-time backend choice",
         "compat_cell": ("configure flag · full rollback", "configure 开关 · 可完全回滚"),
         "reversibility": "select another backend", "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · already in the tree and surviving", "推荐 · 已在树里，而且活了下来"),
         "reason": "Smallest option that removes the class where it matters, with rollback by build flag."},
        {"id": "rust-http-layer", "name": ("Rust HTTP internals (hyper)", "把 HTTP 内部换成 Rust（hyper）"),
         "implementation": "rust",
         "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("wider class removal, never realized", "覆盖面更大，但从未兑现"),
         "one_time_cost": "4 funded years, reached ~parity", "recurring_cost": "dual C/Rust expertise",
         "cost_cell": ("4 funded years; dual-skill on-call", "4 年资助投入；双栈 on-call"),
         "time_to_value": ("never reached", "从未达到"),
         "compatibility": "deep glue layer",
         "compat_cell": ("deep glue · removed in 8.12.0", "深层胶水 · 已在 8.12.0 移除"),
         "reversibility": "deleted", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · failed G4 on people, not on technology", "排除 · G4 卡在人手，不在技术"),
         "reason": "Removed in curl 8.12.0: no user demand and too few developers able to work on the C/Rust glue."},
        {"id": "rust-full", "name": ("Full Rust rewrite of curl", "把 curl 整体重写为 Rust"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE", "benefit_interval": ("no evidence it clears the seam option", "没有证据说明它能胜过接缝方案"),
         "one_time_cost": "unbudgeted, multi-year", "recurring_cost": "two toolchains for every platform",
         "cost_cell": ("multi-year; every platform twice", "以年计；每个平台都要做两遍"),
         "time_to_value": ("years", "以年计"),
         "compatibility": "526 API pages + 279 CLI options",
         "compat_cell": ("whole ABI + CLI · poor rollback", "整个 ABI + CLI · 回滚很难"),
         "reversibility": "poor", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails the smallest-sufficient-option gate", "排除 · 过不了「最小充分方案」这道门"),
         "reason": "The hyper experiment shows the deeper layer is unstaffable at a fraction of this scope."},
        {"id": "adopt-rust-client", "name": ("Users adopt a Rust HTTP client", "使用方改用 Rust HTTP 客户端"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("full class removal for that caller only", "只对那一个调用方彻底消除该类问题"),
         "one_time_cost": "per consumer", "recurring_cost": "loses curl protocol breadth",
         "cost_cell": ("per consumer; narrower protocol set", "按使用方计；协议覆盖变窄"),
         "time_to_value": ("days per project", "每个项目几天"),
         "compatibility": "different API", "compat_cell": ("different API · caller's choice", "API 不同 · 由调用方定"),
         "reversibility": "caller-side", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · valid for consumers, not a curl decision", "保留 · 对使用方成立，但不是 curl 的决定"),
         "reason": "Solves the objective for one application without addressing curl's own surface."},
    ],

    "lenses_sub": (
        "States are option-scoped evidence, not additive points. Every repository claim was measured on "
        "the commit named in the methodology section.",
        "每个状态都是针对具体方案的证据，不是可以相加的分数。所有仓库层面的数字，都在方法一节标明的 commit 上测得。",
    ),
    "na_note": (
        "N/A lenses: D2 end-to-end reach, D3 tail latency, D4 fleet footprint and D5 startup shape carry "
        "no part of a memory-safety objective for a client library invoked inside a caller's process.",
        "标为 N/A 的维度：D2 端到端影响、D3 尾延迟、D4 机队占用、D5 启动形态。对一个跑在调用方进程里的客户端库来说，"
        "内存安全这个目标不落在这三项上。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"), "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-backend-seam", "rust-http-layer", "rust-full"],
         "claim": ("176,402 lines of C and headers in lib/ own the parsing of attacker-controlled TLS records, HTTP messages and QUIC frames.",
                   "lib/ 里 176,402 行 C 和头文件，负责解析攻击者可控的 TLS 记录、HTTP 报文和 QUIC 帧。"),
         "source": "lib/ · 386 tracked C and header files", "regime": "static structure of the shipped library",
         "caveat": "Structural evidence of exposure, not a per-component advisory attribution."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("No performance requirement is asserted; curl's own release notes make no throughput claim for any TLS backend.",
                   "本次没有提出性能要求；curl 自己的发布说明也没有为任何 TLS 后端声称过吞吐收益。"),
         "source": "objective is memory safety, not latency", "regime": "n/a",
         "caveat": "If a throughput target is later stated, D2 must be recomputed with a real profile."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("curl has no managed runtime and no collector; there is no runtime mechanism in any tail to remove.",
                   "curl 没有托管运行时，也没有 GC；尾部没有任何运行时机制可以拿掉。"),
         "source": "C library, no GC", "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("curl runs inside the caller's process; there is no fleet whose density this decision changes.",
                   "curl 跑在调用方进程里；不存在一支会因这个决定改变部署密度的机队。"),
         "source": "embedded library invocation model", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Process startup is dominated by DNS and TLS handshake round-trips, not by library initialization.",
                   "进程启动时间由 DNS 和 TLS 握手的往返主导，库初始化不是大头。"),
         "source": "network-bound invocation", "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"), "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-backend-seam", "rust-http-layer", "rust-full"],
         "claim": ("curl maintains a formal disclosure policy and advisory pipeline, which is direct evidence that the unsafe surface produces findings.",
                   "curl 维护着正式的披露政策和公告流程，这直接说明不安全面确实在持续产出漏洞。"),
         "source": "docs/VULN-DISCLOSURE-POLICY.md · docs/SECURITY-ADVISORY.md · SECURITY.md",
         "regime": "project security process", "caveat": "The advisories are not classified by memory-safety root cause in-repo, so the eliminated-by-construction share is unquantified here."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("curl's multi interface is single-threaded and event-driven by design; no data-parallel work is blocked by the language.",
                   "curl 的 multi 接口设计上就是单线程、事件驱动；没有哪块数据并行的活是被语言卡住的。"),
         "source": "lib/multi.c event model", "regime": "library concurrency model",
         "caveat": "Callers supply their own threading; this decision does not change it."},
        {"id": "D8", "name": ("Distribution", "分发"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": ("curl ships on platforms where a C compiler is the only guaranteed toolchain; a full Rust rewrite would require a Rust target for every one of them.",
                   "curl 会发到一些只保证有 C 编译器的平台上；整体 Rust 重写要求这些平台每一个都有 Rust target。"),
         "source": "configure.ac · 22 m4 files · Windows CE and VS2008 support only recently removed",
         "regime": "supported platform matrix", "caveat": "A single optional backend does not carry this cost; a full rewrite does."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"), "label": "SUPPORTS · rust-backend-seam", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-backend-seam"],
         "claim": ("Production-grade Rust TLS and QUIC crates already exist and are already wired in; curl did not have to build them.",
                   "生产级的 Rust TLS 和 QUIC crate 已经存在，也已经接进来了；curl 不用自己造。"),
         "source": "lib/vtls/rustls.c · lib/vquic/cf-quiche.c", "regime": "shipped backend inventory",
         "caveat": "Backend availability varies by platform and build configuration."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"), "label": "SUPPORTS · rust-backend-seam", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-backend-seam"],
         "claim": ("The vtls abstraction already carries six interchangeable backend implementations, so a Rust backend needs no new seam and no ABI change.",
                   "vtls 抽象已经挂着六个可互换的后端实现，所以再加一个 Rust 后端不需要新接缝，也不动 ABI。"),
         "source": "lib/vtls/ · 6 backends registered in vtls.c:705, 33 files, 25,481 lines", "regime": "existing internal interface",
         "caveat": "The seam is coarse for TLS but not for HTTP internals — which is where the deeper attempt failed."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"), "label": "DISFAVORS · rust-http-layer, rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-http-layer", "rust-full"],
         "claim": ("The deeper Rust integration died with no users asking for it and almost no developers able to work on the C/Rust glue, after four ISRG-funded years at near test-suite parity.",
                   "更深的那次 Rust 集成，在 ISRG 资助的四年后已经接近测试套件对等，最后还是死了：没有用户提出需求，"
                   "能碰 C/Rust 胶水层的开发者也几乎没有。"),
         "source": "https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/ · docs/DEPRECATE.md:62",
         "regime": "first-party maintainer account of a completed attempt",
         "caveat": "A staffing and demand outcome, not a statement about Rust's technical fitness for HTTP."},
        {"id": "D12", "name": ("Counterfactual", "反事实对照"), "label": "NEUTRAL · c-harden vs rust-backend-seam", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["c-harden", "rust-backend-seam"],
         "claim": ("Continuous fuzzing and review remain funded and running; they are complementary to the backend seam rather than an alternative to it.",
                   "持续 fuzzing 和代码评审仍有资金、仍在运行；它们与后端接缝互补，谈不上二选一。"),
         "source": "curl CI and fuzzing configuration in tests/ and .github/",
         "regime": "current engineering practice",
         "caveat": "No published experiment isolates the incident-rate contribution of either practice."},
    ],

    "findings": [
        ("rust", ("The seam that survived is 1,468 lines", "活下来的那道接缝是 1,468 行"),
         ("curl's Rust TLS backend sits behind an abstraction that already hosts six interchangeable "
          "implementations. Adding it required no ABI change, no protocol change, and no new interface. "
          "It is still in the tree.",
          "curl 的 Rust TLS 后端挂在一个已经托管六个可互换实现的抽象后面。加它不需要改 ABI，不需要改协议，"
          "也不需要新接口。它至今还在树里。"),
         "lib/vtls/rustls.c · 1,468 lines of 25,481 in lib/vtls"),
        ("current", ("hyper reached near parity and was deleted anyway", "hyper 做到了接近对等，还是被删了"),
         ("The hyper backend moved curl's HTTP internals to Rust and reached near test-suite parity over "
          "four ISRG-funded years. It was deleted anyway. The maintainer's published reasons: no user "
          "demand, and too few developers able to work on the C/Rust glue.",
          "hyper 后端把 curl 的 HTTP 内部搬到了 Rust，在 ISRG 资助的四年里做到接近测试套件对等。它还是被删了。"
          "维护者公开给出的理由是：没有用户提需求，能碰 C/Rust 胶水层的开发者也太少。"),
         "docs/DEPRECATE.md:62 · daniel.haxx.se, 21 Dec 2024"),
        ("current", ("Depth costs 526 API pages and 279 CLI options", "深度的代价是 526 页 API 加 279 个选项"),
         ("A rewrite has to preserve 526 documented libcurl API pages and 279 command-line options, on "
          "every platform curl supports. Adding a backend touches none of it. That gap is the distance "
          "between 'rewrite it in Rust' and 'add a Rust backend'.",
          "重写必须在 curl 支持的每一个平台上，原样保住 526 页 libcurl API 文档和 279 个命令行选项。"
          "加一个后端一样都不碰。这个差距，就是「用 Rust 重写」和「加一个 Rust 后端」之间的距离。"),
         "docs/libcurl/**/*.md · src/tool_listhelp.c · 279 entries"),
        ("rust", ("The parity harness makes the seam safe to try", "对等性测试台让这道接缝可以放心试"),
         ("2,056 test cases sit inside a 232,601-line tests/ tree, so a backend swap can be verified "
          "before release. Swap it, run the suite, read the result. Options with a comparable harness are "
          "cheap to attempt. Options without one are not.",
          "232,601 行的 tests/ 树里有 2,056 个用例，所以换后端可以在发布前验完。换掉、跑套件、看结果。"
          "有这种测试台的方案，试一次很便宜；没有的，不便宜。"),
         "tests/data/test* · tests/ 2,615 files"),
        ("unknown", ("Nobody has published curl's advisories by root cause", "没有人按根因公布过 curl 的历史公告"),
         ("curl runs a formal disclosure process. The repository does not sort that advisory history into "
          "eliminated-by-construction, downgraded-to-safe-failure, and language-independent. Without the "
          "split, the size of the win from any Rust scope is bounded by argument, not measurement.",
          "curl 有正式的漏洞披露流程。但仓库里没有把历史公告拆成「按构造消除」「降级为安全失败」「与语言无关」"
          "三类。没有这个拆分，任何 Rust 范围能拿到多大收益，都只能靠论证撑住，测不出来。"),
         "docs/SECURITY-ADVISORY.md · no in-repo root-cause classification"),
    ],

    "buys": [
        (("Class elimination inside one backend", "在单个后端内部消除整类问题"),
         ("memory-unsafety in the selected TLS implementation stops being reachable, with no change to callers.",
          "所选 TLS 实现里的内存不安全不再可达，调用方什么都不用改。")),
        (("A maintainable integration shape", "一种能长期维护的集成形状"),
         ("curl's own experience is that library-shaped seams outlive deep integrations; rustls and quiche survived while hyper did not.",
          "curl 自己的经验是：库形状的接缝比深度集成活得久。rustls 和 quiche 还在，hyper 没了。")),
        (("Reversibility by build flag", "靠编译开关就能回滚"),
         ("a backend is chosen at configure time, so the rollback path is a build option rather than a revert.",
          "后端在 configure 阶段选定，回滚就是改一个构建选项，不用 revert 代码。")),
    ],
    "nobuys": [
        (("Safety for the other 176,402 lines", "另外那 176,402 行的安全性"),
         ("protocol state machines, transfer logic and the ABI layer stay in C; the seam does not reach them.",
          "协议状态机、传输逻辑和 ABI 层还是 C，接缝够不到它们。")),
        (("Any measured throughput gain", "任何实测的吞吐提升"),
         ("no performance requirement is stated and no backend claims one; treat 'faster' as unevidenced here.",
          "本次没有提出性能要求，也没有哪个后端声称有；这里的「更快」没有证据。")),
        (("A staffed path to deeper Rust", "一条有人手的深水区路线"),
         ("the resource that decided the last attempt was contributors with dual C/Rust expertise, and the report cannot conjure them.",
          "上一次尝试的胜负手是有 C/Rust 双栈能力的贡献者，这份报告变不出这些人。")),
    ],

    "precedents": [
        {"name": "curl · hyper backend", "outcome": "ABANDONED",
         "body": ("Four ISRG-funded years took a Rust HTTP backend to near test-suite parity inside curl "
                  "itself. 8.12.0 removed it. No users had asked for it, and almost no developers could "
                  "work on the C/Rust glue.",
                  "ISRG 资助的四年，把一个 Rust HTTP 后端在 curl 内部做到了接近测试套件对等。8.12.0 把它删了。"
                  "没有用户提过这个需求，能碰 C/Rust 胶水层的开发者也几乎没有。"),
         "match": ("same project, same language pair, same trust boundary", "同一个项目、同一对语言、同一条信任边界"),
         "mismatch": ("a deeper layer than the vtls seam this report selects", "层次比本报告选的 vtls 接缝更深"),
         "regime": "first-party maintainer account", "source_label": "first-party · maintainer blog",
         "url": "https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/"},
        {"name": "Mozilla · Stylo vs Servo", "outcome": "EXTRACT SHIPPED",
         "body": ("The same organisation shipped a Rust CSS engine into Firefox in about two years while "
                  "the whole-engine replacement was cancelled and its team laid off. The seam shipped; the "
                  "replacement did not.",
                  "同一家机构用大约两年，把一个 Rust CSS 引擎装进了 Firefox；同期整引擎替换被取消，团队被裁。"
                  "接缝发出去了，替换没有。"),
         "match": ("extraction-versus-replacement inside one C/C++ codebase", "同一份 C/C++ 代码库里，抽取与替换的正面对照"),
         "mismatch": ("browser engine, and the extraction was performance- as well as safety-motivated",
                      "对象是浏览器引擎，而且那次抽取除了安全还有性能动机"),
         "regime": "shipped in Firefox 57", "source_label": "first-party · engineer account",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Trifecta · sudo-rs", "outcome": "MIGRATED",
         "body": ("A scoped, privileged C tool was replaced in Rust and became an Ubuntu default. The "
                  "stated rationale was attack-surface reduction. No performance framing at all.",
                  "一个范围明确的特权 C 工具被 Rust 重写，成了 Ubuntu 的默认实现。公开给出的理由是缩小攻击面。"
                  "全程没有提性能。"),
         "match": ("C on a hostile boundary; safety is the whole objective", "敌意边界上的 C；目标只有安全"),
         "mismatch": ("a small standalone binary, not a library with a 526-page documented ABI",
                      "那是个独立的小二进制，不是带 526 页文档 ABI 的库"),
         "regime": "distribution default, 2025", "source_label": "first-party · project blog",
         "url": "https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/"},
        {"name": "Google · Android memory-safety program", "outcome": "INCREMENTAL",
         "body": ("Memory-safety's share of Android vulnerabilities fell from 76% to below 20%. New code "
                  "went into safe languages while old C/C++ was left to decay. Mass rewriting was "
                  "explicitly not the plan.",
                  "Android 漏洞里内存安全类的占比，从 76% 降到 20% 以下。新代码用安全语言写，"
                  "旧的 C/C++ 让它自然老去。大规模重写被明确排除在外。"),
         "match": ("same class of requirement, same interop-over-rewrite conclusion", "需求属于同一类，结论同样是互操作优于重写"),
         "mismatch": ("an operating system with far more entry points than one client library",
                      "那是操作系统，入口点比一个客户端库多得多"),
         "regime": "2019–2025 vulnerability share", "source_label": "first-party · vendor security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
    ],

    "path": [
        {"title": ("Publish curl's advisories by root cause", "按根因公布 curl 的历史公告"),
         "body": ("The curl security team sorts the advisory history into three buckets: "
                  "eliminated-by-construction, downgraded-to-safe-failure, language-independent. Each "
                  "entry names its component. It passes when every advisory in the published set is "
                  "classified and attributed. If public advisory data will not support the "
                  "classification, stop — that nobody can compute it yet is itself the result. No code "
                  "changes here.",
                  "curl 安全团队把历史公告分成三类：按构造消除、降级为安全失败、与语言无关。每一条都标出所属组件。"
                  "通过标准是已公布集合里的每一条都完成分类和归属。如果凭公开公告数据做不到分类，就停下——"
                  "「现在还算不出来」本身就是结论。这一步不动任何代码。"),
         "owner": "curl security team",
         "cost_range": ("2–4 weeks", "2–4 周"),
         "artifact": "a table splitting the advisory history into eliminated-by-construction, downgraded-to-safe-failure and language-independent, with the component for each",
         "acceptance": "every advisory in the published set is classified and attributed to a component",
         "stop": "stop if the classification cannot be completed from public advisory data",
         "rollback": "documentation only; no code changes"},
        {"title": ("Keep the surviving seams staffed", "把活下来的接缝养住"),
         "body": ("Put names on the rustls and quiche backends: an on-call owner each, plus a written "
                  "bus-factor plan. The bar is two people per backend who can review and release changes "
                  "to it. Below one active maintainer, mark that backend experimental rather than letting "
                  "it rot. Rollback stays cheap. Deselect it at configure time and the other backends are "
                  "unaffected.",
                  "给 rustls 和 quiche 各指定一名 on-call 负责人，并写下 bus-factor 计划。达标线是每个后端有两个人"
                  "能评审并发布它的改动。活跃维护者一旦掉到一人以下，就把这个后端标成 experimental，别让它烂在树里。"
                  "回滚很便宜：在 configure 阶段取消选择即可，其他后端不受影响。"),
         "owner": "named backend maintainers",
         "cost_range": ("ongoing", "长期"),
         "artifact": "a named on-call owner for the rustls and quiche backends plus a documented bus-factor plan",
         "acceptance": "each Rust backend has at least two people who can review and release changes to it",
         "stop": "if a backend drops below one active maintainer, mark it experimental rather than letting it rot",
         "rollback": "deselect the backend at configure time; other backends are unaffected"},
        {"title": ("Widen only where the root-cause table points", "只在根因表指向的地方拓宽"),
         "body": ("Maintainers pick one more component, and the reason has to be the step-1 table showing "
                  "the class concentrates there. The proposal names the interface the Rust code would sit "
                  "behind. Three things must hold before anyone writes code: a coarse existing interface, "
                  "a parity path through the 2,056-case suite, and two committed reviewers. No reviewers, "
                  "no proposal. That is the resource whose absence ended hyper. The component keeps its C "
                  "implementation as the default build.",
                  "维护者再挑一个组件，理由必须来自第 1 步那张表：该类问题确实集中在那里。提案要写明这段 Rust 代码"
                  "挂在哪个接口后面。动手写代码之前有三个前提：已有一个粗粒度接口、能在 2,056 个用例的套件里走通"
                  "对等性、两名承诺到位的评审者。评审者不到位，提案就停。终结 hyper 的正是这项资源。"
                  "该组件的默认构建仍然用 C 实现。"),
         "owner": "curl maintainers",
         "cost_range": ("per component, scoped", "按组件计，范围可控"),
         "artifact": "a proposal for one additional component chosen because the table shows the class concentrates there, with the interface it would sit behind",
         "acceptance": "the component has a coarse existing interface, a parity path in the 2,056-case suite, and two committed reviewers before any code is written",
         "stop": "no proposal proceeds without the two reviewers — the resource whose absence ended hyper",
         "rollback": "the component keeps its C implementation as the default build"},
        {"title": ("Re-run these gates when demand changes", "需求变了就重跑这几道门"),
         "body": ("Two events reopen this file: a funded team appears, or a distributor requires "
                  "memory-safe HTTP internals. Maintainers then spend a day on a short re-assessment. It "
                  "passes only if it names who maintains the result five years out. No funded owner, "
                  "close the review. Until then the current backend strategy runs unchanged.",
                  "两件事会重开这份文件：出现一支有资金的团队，或者某个发行方要求 HTTP 内部必须内存安全。"
                  "届时维护者花一天做一次简短复评。通过的条件只有一条：复评里写明五年之后由谁维护这个结果。"
                  "没有出资的负责人，就把复评关掉。在那之前，现有的后端策略照旧。"),
         "owner": "curl maintainers",
         "cost_range": ("1 day per review", "每次复评 1 天"),
         "artifact": "a short re-assessment triggered by a funded team or a distributor requirement for memory-safe HTTP internals",
         "acceptance": "the review names who maintains the result five years out",
         "stop": "close the review if no funded owner exists",
         "rollback": "the current backend strategy continues unchanged"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响"), "state": "PASS",
         "claim": ("The report claims class elimination only inside the selected backend and states the 176,402 lines it does not reach.",
                   "报告只在所选后端内部主张消除该类问题，并写明了它够不到的那 176,402 行。"),
         "evidence": "lib/ line count vs lib/vtls/rustls.c"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("No performance benefit is claimed for any Rust option, so no redesign effect can be miscredited to the language.",
                   "没有为任何 Rust 方案主张性能收益，所以不会把重新设计的效果记到语言头上。"),
         "evidence": "D2 recorded as N/A"},
        {"name": ("Baseline and regime", "基线与口径"), "state": "HIT",
         "claim": ("The size of the safety win rests on structural exposure, because curl's advisories are not classified by root cause in-repo.",
                   "安全收益的大小只能靠结构性暴露面来估，因为仓库内没有按根因分类的公告数据。"),
         "evidence": "docs/SECURITY-ADVISORY.md"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("The seam is an existing internal abstraction with six implementations; no ABI or protocol change is required.",
                   "接缝是一个已有的内部抽象，带 16 个实现；不需要改 ABI，也不需要改协议。"),
         "evidence": "lib/vtls/vtls.c:705 · 6 registered backends"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The path requires two named reviewers before any widening, which is the specific resource whose absence ended the hyper attempt.",
                   "路径要求任何拓宽之前先配齐两名具名评审者，也就是 hyper 当年缺的那项资源。"),
         "evidence": "https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有资金的反事实对照"), "state": "PASS",
         "claim": ("Continuous fuzzing and review are funded, running, and credited in the ledger rather than dismissed.",
                   "持续 fuzzing 和评审有资金、在运行，账本里给了它们应有的位置，没有一笔带过。"),
         "evidence": "D12 · curl CI and fuzzing configuration"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying entirely in C keeps the memory-unsafety class reachable in every line that touches network input.",
                   "完全留在 C，意味着每一行接触网络输入的代码里，内存不安全这类问题都还可达。"),
         "evidence": "lib/ 176,402 lines of C and headers on the trust boundary"},
        {"name": ("Unsafe-surface omission", "回避不安全面"), "state": "PASS",
         "claim": ("The report names the unsafe surface explicitly instead of hiding it behind the project's good security record.",
                   "报告明确点出了不安全面，没有拿项目良好的安全记录把它遮过去。"),
         "evidence": "D1 and D6 records"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The Rust backends already in the tree are recorded as an ecosystem advantage, not dismissed as hype.",
                   "树里已有的 Rust 后端被当作一项生态优势记录在案，没有被当成炒作打发掉。"),
         "evidence": "D9 · lib/vtls/rustls.c, lib/vquic/cf-quiche.c"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("Widening is gated on a published root-cause table and two committed reviewers, so 'harden C forever' is not the default answer.",
                   "拓宽的前置条件是公布根因表，加两名承诺到位的评审者，所以「永远加固 C」不是默认答案。"),
         "evidence": "reversible path steps 1 and 3"},
    ],

    "gaps": [
        (("Advisory root-cause classification", "公告的根因分类"),
         ("Without it, the magnitude of any Rust scope's safety win stays argued rather than measured; the seam decision does not depend on it, but widening does.",
          "没有它，任何 Rust 范围的安全收益都只能论证、无法测量。接缝这个决定不依赖它，拓宽依赖。")),
        (("Backend maintainer continuity", "后端维护者的延续性"),
         ("If the rustls or quiche backend loses its owner, G4 for that backend becomes UNKNOWN and it should be marked experimental rather than relied on.",
          "rustls 或 quiche 后端一旦失去负责人，该后端的 G4 就变成 UNKNOWN，应当标为 experimental，不能再当作可依赖项。")),
        (("Funded dual-skill team for deeper layers", "面向更深层的双栈资助团队"),
         ("Absent this, any proposal beyond the backend seam repeats the staffing condition that ended hyper, and stays excluded.",
          "没有这个，任何超出后端接缝的提案都会撞上终结 hyper 的那套人手条件，只能继续排除在外。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; deleted history was not inspected.",
        "curl's supported-platform matrix continues to include targets where a C toolchain is the only guarantee.",
        "No performance requirement is attached to this decision; if one appears, D2 must be recomputed with a real profile.",
    ],
    "objective": {
        "driver": "safety",
        "requirement": "remove the memory-unsafety class from curl's handling of attacker-controlled bytes without breaking the libcurl ABI",
        "baseline": "176,402 lines of C and headers in lib/ terminate untrusted network input",
        "target": "class elimination in the components where advisories concentrate, at a scope curl can staff",
    },
    "repository": {
        "path": "https://github.com/curl/curl",
        "commit": "527573490eb2564b3d7c9dd51d8bff963b5d6303",
        "scope": "whole repository, with the vtls/vquic backend layer as the candidate seam",
        "sampling": "shallow clone; 4,437 tracked files enumerated; lib/, src/, tests/, docs/ measured; deleted history not inspected",
    },
    "user_supplied_facts": [],

    "method_title": (
        "curl/curl at 5275734 · static read-only analysis · why-not-rust method 2.0",
        "curl/curl @ 5275734 · 只读静态分析 · why-not-rust method 2.0",
    ),
    "method_body": (
        "Repository: github.com/curl/curl at commit 5275734, shallow clone, 4,437 tracked files. Scope: "
        "the whole repository, with lib/vtls and lib/vquic as the candidate seam. Counting conventions "
        "matter here. The 258,953 figure counts .c files only; per-directory figures such as lib/ 176,402 "
        "count .c and .h together, and each lens states which. The backend count comes from the "
        "available_backends[] table at lib/vtls/vtls.c:705 (six), not from the 16 .c files in that "
        "directory. The 279 command-line options come from src/tool_listhelp.c, not from the 298 files in "
        "docs/cmdline-opts/, 19 of which are manpage-section includes. Sampling: line counts and file "
        "inventories were taken from tracked files only. No build, test, benchmark or network call was run "
        "against the project, and deleted history was not inspected. Objective: remove the memory-unsafety "
        "class from curl's handling of attacker-controlled bytes without breaking the libcurl ABI. "
        "User-supplied facts: none. No Amdahl calculation appears because no performance requirement is "
        "asserted; D2 is recorded N/A rather than filled with an invented time share. One external source "
        "decided this report: curl's own account of removing the hyper backend. It is a first-party "
        "maintainer statement about staffing and demand, not an independent evaluation of Rust's fitness "
        "for HTTP. The framework compares explicit options through four non-compensatory gates. It is a "
        "structured decision protocol, not a statistical predictor.",
        "仓库：github.com/curl/curl，commit 5275734，浅克隆，4,437 个被跟踪文件。范围：整个仓库，"
        "候选接缝是 lib/vtls 和 lib/vquic。计数口径必须说清楚。258,953 这个数只统计 .c 文件；"
        "像 lib/ 176,402 这类按目录的数字，把 .c 和 .h 一起算，每个维度都会注明用的是哪一种。"
        "后端数量取自 lib/vtls/vtls.c:705 的 available_backends[] 表（六个），不是该目录下的 16 个 .c 文件。"
        "279 个命令行选项取自 src/tool_listhelp.c，不是 docs/cmdline-opts/ 下的 298 个文件——其中 19 个是 "
        "manpage 章节的 include。抽样：行数和文件清单只统计被跟踪文件。没有对该项目做任何构建、测试、基准或"
        "网络调用，也没有检查已删除的历史。目标：在不破坏 libcurl ABI 的前提下，从 curl 处理攻击者可控字节的"
        "路径上消除内存不安全这一整类问题。用户提供的事实：无。没有 Amdahl 计算，因为本次没有提出性能要求；"
        "D2 记为 N/A，而不是塞一个编造的时间占比。决定这份报告的外部证据只有一个：curl 自己关于移除 hyper "
        "后端的说明。那是维护者的第一方陈述，讲的是人手和需求，不是对 Rust 是否适合做 HTTP 的独立评估。"
        "本框架用四道非补偿性证据门比较明确列出的方案。它是一套结构化的决策协议，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 5275734 · no build, benchmark or network call",
        "公开仓库 · 在 commit 5275734 上做静态分析 · 无构建、无基准、无网络调用",
    ),
}
