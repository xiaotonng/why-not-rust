"""prisma/prisma-engines — the one report where removing Rust was the performance fix.

Repository facts were measured read-only on the shallow clone named in
`repository`. The boundary math is produced by the skill's own calculator from
Prisma's own published before/after numbers.
"""

CASE = {
    "slug": "prisma-engines",
    "project_name": "prisma/prisma-engines",
    "project_desc": (
        "Rust · ORM engines · 394,195 lines of Rust · the query engine went; the language stayed",
        "Rust · ORM 引擎 · 394,195 行 Rust · 撤掉的是查询引擎，Rust 还在树里",
    ),
    "date": "2026-08-01",
    "archetype": (
        "lib-with-bindings · Rust core under a JavaScript host",
        "lib-with-bindings · JavaScript 宿主下的 Rust 内核",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "ts-query-execution",
    "scope_chip": (
        "query execution in TypeScript; Rust kept where the boundary is coarse",
        "查询执行放在 TypeScript；边界粗的地方仍然用 Rust",
    ),
    "scope_sub": ("keep query execution in the host language", "查询执行留在宿主语言里"),

    "why": (
        "This is the one case in the set where the measurement pointed away from Rust. Prisma "
        "published both halves: a 25,000-row query at 185 ms through the Rust query engine, 55 ms "
        "without it. Feed that pair into the boundary formula and the added crossing cost is 2.36× "
        "the TypeScript baseline's entire runtime. Even an infinite kernel speedup misses parity. "
        "G2 fails on call frequency. The data crossed the boundary on every operation, and "
        "execution speed never got to matter.",

        "这批案例里，只有这一次实测把矛头指向了 Rust。Prisma 自己公布了两组数：25,000 行的查询，走 Rust "
        "查询引擎 185 ms，不走 55 ms。把这一对数字放进边界公式，多出来的跨界开销等于 TypeScript 基线整段"
        "运行时间的 2.36×。内核提速到无穷大，也追不平。G2 挂在调用频率上。数据每做一次操作就要过一次边界，"
        "执行速度根本没轮到上场。"
    ),
    "trigger": (
        "Stable for a chatty per-operation boundary. It does not transfer to coarse seams. This "
        "repository still holds 394,195 lines of Rust, including the WASM query compiler that was "
        "kept on purpose — those crossings happen in bulk, not per call.",

        "对「每次操作过一次边界」这种形态，结论是稳的。换成粗接缝就不成立。这个仓库里还留着 394,195 行 "
        "Rust，其中包括特意保留的 WASM 查询编译器——那条缝是批量过一次，不是每次调用过一次。"
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("Measured: 185 ms on a 25,000-row query, plus a ~14 MB bundle.",
                           "实测：25,000 行查询 185 ms，外加约 14 MB 的产物。"),
         "name": "requirement",
         "evidence": "The requirement was measured, not assumed: findMany over 25,000 rows at 185 ms, complex joins at 207 ms, per-OS/OpenSSL binaries, and a bundle edge runtimes could not carry."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果归属"),
         "hero_evidence": ("Boundary cost was 2.36× the baseline's total runtime.",
                           "跨界开销是基线总运行时间的 2.36×。"),
         "name": "rust-specific causality",
         "evidence": "Computed from Prisma's own before/after: with an infinite kernel speedup and the measured boundary cost, the ceiling is 0.42× — a slowdown. No Rust-specific advantage survives a per-operation JavaScript boundary at this call frequency."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("Dropping the boundary measured 3.4× faster and ~90% smaller.",
                           "把边界去掉，实测快 3.4×，体积小约 90%。"),
         "name": "economics and smallest sufficient option",
         "evidence": "185 ms → 55 ms and roughly 14 MB → 1.6 MB, while also widening the contributor pool by dropping the Rust-plus-TypeScript dual-skill requirement."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("It shipped: GA in v6.16.0, default in Prisma 7.",
                           "已经发出去了：v6.16.0 GA，Prisma 7 默认。"),
         "name": "delivery and reversibility",
         "evidence": "The change reached general availability and became the default, with the previous engine available by version pin during the transition. This repository's own layout confirms the outcome."},
    ],

    "tiles": [
        (("Measured, before → after", "实测 前 → 后"), "185 → 55", ("ms", "ms"),
         ("findMany 25,000 rows · first-party benchmark", "findMany 25,000 行 · 一方基准")),
        (("Boundary cost", "跨界开销"), "2.36", ("× baseline", "× 基线"),
         ("derived from Prisma's own before/after", "由 Prisma 自己的前后数据推出")),
        (("Ceiling with an infinite kernel", "内核无穷快时的天花板"), "0.42", ("×", "×"),
         ("decision_math.py · share=1.0, b=2.3636", "decision_math.py · share=1.0, b=2.3636")),
        (("Bundle size", "产物体积"), "14 → 1.6", ("MB", "MB"),
         ("roughly 90% smaller after removal", "移除之后小了大约 90%")),
        (("Rust still in this repo", "仓库里仍然有的 Rust"), "394,195", ("lines", "行"),
         ("1,647 files — the reversal was scoped", "1,647 个文件——这次回退是有范围的")),
        (("Retained Rust component", "保留下来的 Rust 组件"), "43,995", ("lines", "行"),
         ("query-compiler/*.rs · 230 files, incl. the WASM crate",
          "query-compiler/*.rs · 230 个文件，含 WASM crate")),
    ],

    "options_sub": (
        "Same objective for every option: cut ORM query latency and shipped bundle size for "
        "JavaScript and TypeScript applications, including edge runtimes.",
        "所有选项对着同一个目标：降低 JavaScript 和 TypeScript 应用的 ORM 查询延迟与发布产物体积，"
        "边缘运行时也要能跑。"
    ),
    "options": [
        {"id": "rust-query-engine", "name": ("Keep the Rust query engine", "保留 Rust 查询引擎"),
         "implementation": "rust",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("measured 3.4× slower than the alternative", "实测比另一条路慢 3.4×"),
         "one_time_cost": "already sunk", "recurring_cost": "per-OS binaries; dual-skill contributor pool",
         "cost_cell": ("sunk; per-OS binaries + dual skills", "已沉没；每 OS 一套二进制 + 双语言技能"),
         "time_to_value": ("n/a", "不适用"),
         "compatibility": "cannot ship to edge runtimes",
         "compat_cell": ("no edge support · n/a", "不支持边缘运行时 · 不适用"),
         "reversibility": "n/a", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · measured worse on the stated objective", "排除 · 在既定目标上实测更差"),
         "reason": "Per-operation serialization across the JavaScript boundary dominated the native execution gain."},
        {"id": "ts-query-execution", "name": ("Query execution in TypeScript", "查询执行改用 TypeScript"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("measured 3.4× on 25k rows; ~90% smaller bundle",
                              "25k 行实测 3.4×；产物小约 90%"),
         "one_time_cost": "one major-version transition", "recurring_cost": "single-language maintenance",
         "cost_cell": ("one major version; single-language", "一个大版本；单语言维护"),
         "time_to_value": ("shipped in v6.16.0", "v6.16.0 已发布"),
         "compatibility": "same client API; edge runtimes now work",
         "compat_cell": ("same API · version pin to roll back", "API 不变 · 锁版本即可回退"),
         "reversibility": "pin the previous major", "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · shipped, measured, and default in Prisma 7",
                  "推荐 · 已发布、已实测，Prisma 7 里是默认"),
         "reason": "Removes the boundary that the math shows was the bottleneck, and meets both halves of the objective."},
        {"id": "rust-coarse-wasm", "name": ("Rust retained at a coarse seam", "在粗接缝上保留 Rust"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("keeps query-plan compilation native", "查询计划编译继续走原生"),
         "one_time_cost": "already built", "recurring_cost": "one WASM artifact, not per-OS binaries",
         "cost_cell": ("already built; one WASM artifact", "已经建好；只有一个 WASM 产物"),
         "time_to_value": ("shipped alongside", "与主变更同期发布"),
         "compatibility": "compiles plans, does not execute queries",
         "compat_cell": ("coarse seam · replaceable", "粗接缝 · 可替换"),
         "reversibility": "swap the compiler", "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · in the tree today; the part the headline hides",
                  "保留 · 今天还在树里；标题盖住的就是这一块"),
         "reason": "A batch-in/batch-out seam crossed once per query plan, not once per row, so the boundary tax does not apply."},
        {"id": "rust-tune-boundary", "name": ("Keep Rust, batch the boundary", "保留 Rust，把跨界改成批量"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("unmeasured; would have to beat 55 ms", "没测过；得先打赢 55 ms"),
         "one_time_cost": "redesign the protocol and the client", "recurring_cost": "still per-OS binaries",
         "cost_cell": ("protocol redesign; per-OS binaries remain", "重做协议；每 OS 一套二进制照旧"),
         "time_to_value": ("months", "数月"),
         "compatibility": "client protocol change",
         "compat_cell": ("new wire protocol · hard rollback", "新的传输协议 · 回滚困难"),
         "reversibility": "poor", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the steelman for keeping Rust, recorded and priced",
                  "保留 · 留住 Rust 的最强论证，记录在案并已标价"),
         "reason": "Batching and zero-copy could reduce the crossing cost, but it would not remove the per-OS binary and edge-runtime constraints that were also part of the requirement."},
        {"id": "adopt-other-orm", "name": ("Adopt a different ORM", "换一个 ORM"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("depends on the application's own measurement", "取决于各应用自己的测量"),
         "one_time_cost": "per application migration", "recurring_cost": "different schema tooling",
         "cost_cell": ("per application; new schema tooling", "按应用逐个迁移；换一套 schema 工具"),
         "time_to_value": ("weeks per project", "每个项目数周"),
         "compatibility": "different API and migrations",
         "compat_cell": ("different API · switch back", "API 不同 · 可以换回来"),
         "reversibility": "switch back", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · a consumer's option, not the project's", "保留 · 这是使用方的选项，不是项目的"),
         "reason": "Available to any application, and it does not address the engine architecture question this decision is about."},
    ],

    "amdahl": {
        "share": 1.0,
        "kernel_speedup": float("inf"),
        "boundary": 2.3636,
        "target": 1.0,
        "note": "Derived from Prisma's published findMany 25,000-row figures: 185 ms with the Rust query engine, 55 ms without it. Taking the TypeScript implementation as baseline, the added boundary cost is (185-55)/55 = 2.3636 in baseline-time units, and the whole query path is treated as the candidate kernel (share=1.0). Even an infinite kernel speedup yields 0.4230834320528008x — a slowdown — so parity (target 1.0x) was physically impossible at that boundary.",
    },

    "lenses_sub": (
        "States are option-scoped evidence, not additive points. The boundary figure is derived "
        "from Prisma's own published before/after and recomputed with scripts/decision_math.py.",
        "每个状态都绑定具体选项，不是可以相加的分数。边界数值取自 Prisma 公布的前后对比，再用 "
        "scripts/decision_math.py 重算一遍。"
    ),
    "na_note": (
        "N/A lenses: D5 startup shape and D7 concurrency do not bear on this objective — the "
        "engine runs inside a long-lived Node process and query execution was never blocked by "
        "host-language parallelism.",
        "N/A 维度：D5 启动形态和 D7 并发与这个目标无关——引擎跑在长驻的 Node 进程里，查询执行也从来"
        "不是被宿主语言的并行能力卡住的。"
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · all options", "css": "neutral",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["ts-query-execution", "rust-tune-boundary", "rust-coarse-wasm", "rust-query-engine", "adopt-other-orm"],
         "claim": ("Prisma measured the gap on their own benchmark: 185 ms for a 25,000-row "
                   "findMany, 207 ms for complex joins. The bundle was also too big for edge "
                   "runtimes to carry.",
                   "Prisma 在自家基准上量出了这个差距：25,000 行 findMany 185 ms，复杂 join 207 ms。"
                   "产物体积也超出了边缘运行时能承载的范围。"),
         "source": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm",
         "regime": "first-party internal benchmark, 25,000-row findMany",
         "caveat": "First-party numbers with no published harness; the direction is corroborated by the bundle-size and edge-runtime constraints, which are structural."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响"),
         "label": "DISFAVORS · rust-query-engine", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-query-engine"],
         "claim": ("Take the TypeScript implementation as baseline and the Rust path's added "
                   "boundary cost is 2.36 in baseline-time units. Give the kernel an infinite "
                   "speedup and the ceiling is still 0.42×. Parity was physically out of reach.",
                   "以 TypeScript 实现为基线，Rust 路径多出来的跨界开销是 2.36 个基线时间单位。把内核"
                   "提速设成无穷大，天花板仍然是 0.42×。追平在物理上做不到。"),
         "source": "scripts/decision_math.py · share=1.0, kernel=inf, boundary=2.3636, target=1.0",
         "regime": "derived from the first-party 185 ms / 55 ms pair",
         "caveat": "The derivation assumes the whole query path was the candidate kernel; a narrower kernel would make the ceiling worse, not better."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Neither side reports a GC-correlated tail violation. The reported latency "
                   "difference is serialization work, not collector pauses.",
                   "两边都没有报告与 GC 相关的尾延迟违约。报告里的延迟差来自序列化，不是回收停顿。"),
         "source": "first-party account attributes the cost to serialization",
         "regime": "first-party attribution", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队足迹"),
         "label": "SUPPORTS · ts-query-execution", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["ts-query-execution"],
         "claim": ("The shipped artifact fell from roughly 14 MB to 1.6 MB, about 90%. That lands "
                   "directly on serverless cold starts and edge deployment limits.",
                   "发布产物从大约 14 MB 降到 1.6 MB，约 90%。这直接打在 serverless 冷启动和边缘部署的"
                   "体积上限上。"),
         "source": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm",
         "regime": "first-party bundle measurement",
         "caveat": "Bundle size is a deployment constraint here rather than a steady-state compute cost."},
        {"id": "D5", "name": ("Startup shape", "启动形态"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("For the primary deployment target the engine lives inside a long-lived Node "
                   "process. Startup folds into the bundle-size constraint recorded at D4.",
                   "在主要部署目标上，引擎跑在长驻的 Node 进程里。启动这件事已经并入 D4 记录的产物"
                   "体积约束。"),
         "source": "long-lived host process", "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Both sides are memory-safe at application scope. Across 394,195 lines of Rust "
                   "there are 17 `unsafe` keyword occurrences, 12 of them outside comments, "
                   "against 15 crate roots declaring #![deny(unsafe_code)]. Safety is not part of "
                   "this objective.",
                   "在应用层面两边都是内存安全的。394,195 行 Rust 里出现 17 处 `unsafe` 关键字，注释"
                   "之外 12 处，同时有 15 个 crate 根声明了 #![deny(unsafe_code)]。这个目标里不包含"
                   "任何安全性主张。"),
         "source": "17 unsafe keyword occurrences · 15 deny(unsafe_code) declarations · *.rs, this commit",
         "regime": "static count", "caveat": ""},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Query execution is I/O-bound on the database. Host-language parallelism was "
                   "never the constraint.",
                   "查询执行受限于数据库 I/O。宿主语言的并行能力从来不是瓶颈。"),
         "source": "database round-trip bound workload", "regime": "n/a", "caveat": ""},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "DISFAVORS · rust-query-engine, rust-tune-boundary", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-query-engine", "rust-tune-boundary"],
         "claim": ("A native engine meant per-OS and per-OpenSSL binaries. Edge runtimes that "
                   "refuse native binaries could not run it at all. No amount of boundary tuning "
                   "removes that.",
                   "原生引擎意味着按 OS、按 OpenSSL 各出一套二进制。不接受原生二进制的边缘运行时根本"
                   "跑不起来。这条约束再怎么调边界也去不掉。"),
         "source": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm",
         "regime": "first-party account of the deployment constraint",
         "caveat": "WASM is the exception. That is what the retained component is built as."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Database drivers exist in both ecosystems, and consumers have alternative "
                   "ORMs. Ecosystem availability did not decide this.",
                   "两个生态都有数据库驱动，使用方也有别的 ORM 可选。生态供给不是这次决策的决定因素。"),
         "source": "driver and ORM landscape", "regime": "market inventory", "caveat": ""},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-query-engine", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-query-engine"],
         "claim": ("The first-party diagnosis is explicit: data was serialized from JavaScript "
                   "into Rust and back to JavaScript. That crossing happened once per operation. "
                   "Per-operation is the shape that lets a boundary dominate.",
                   "一方给出的诊断很直接：数据要从 JavaScript 序列化进 Rust，再序列化回 JavaScript。"
                   "这次跨界每做一次操作就发生一次。按操作计频，正是让边界吃掉全部收益的那种形态。"),
         "source": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm",
         "regime": "first-party root-cause statement",
         "caveat": "This is a statement about call frequency and copies, not about Rust's execution speed."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-query-engine", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-query-engine", "rust-tune-boundary"],
         "claim": ("An open-source ORM that demands both Rust and TypeScript competence draws "
                   "from a smaller pool. Maintaining per-OS binaries sits on top of that.",
                   "一个开源 ORM 同时要求 Rust 和 TypeScript 能力，能招到的人就少了一截。每 OS 一套"
                   "二进制的维护还压在上面。"),
         "source": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm",
         "regime": "first-party account of contributor dynamics",
         "caveat": "A staffing observation from one project; it does not generalize to teams that are already polyglot."},
        {"id": "D12", "name": ("Counterfactual", "反事实"),
         "label": "SUPPORTS · ts-query-execution, rust-coarse-wasm", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["ts-query-execution", "rust-coarse-wasm"],
         "claim": ("The counterfactual was run and shipped, which is rare. Query execution moved "
                   "to TypeScript; the Rust WASM query-plan compiler stayed. The repository "
                   "carries both halves of that outcome.",
                   "反事实这次真的跑过，也发布了，这种情况少见。查询执行搬到 TypeScript，Rust 的 WASM "
                   "查询计划编译器留在原地。仓库里两半都能看到。"),
         "source": "query-compiler/*.rs 43,995 lines incl. query-compiler-wasm · query-engine/ reduced to connectors and a test kit",
         "regime": "static layout of this commit",
         "caveat": "Layout is consistent with the published account; it is structural corroboration, not an independent benchmark."},
    ],

    "findings": [
        ("current",
         ("The boundary cost exceeded the entire baseline runtime", "跨界开销超过了整段基线运行时间"),
         ("Prisma's own 185 ms and 55 ms put the added crossing cost at 2.36 times the TypeScript "
          "implementation's total time. Feed that to the boundary formula with an infinite kernel "
          "speedup and the ceiling is 0.42×. There was no fast-enough Rust engine to write.",
          "用 Prisma 自己的 185 ms 和 55 ms 换算，多出来的跨界开销是 TypeScript 实现总耗时的 2.36 倍。"
          "把它放进边界公式，内核提速取无穷大，天花板是 0.42×。那台「够快的 Rust 引擎」根本写不出来。"),
         "decision_math.py · share=1.0, kernel=inf, b=2.3636"),
        ("current",
         ("The diagnosis was call frequency, not language speed", "诊断结论是调用频率，不是语言速度"),
         ("The first-party root cause: data serialized from JavaScript into Rust and back, on "
          "every operation. A boundary crossed once per query plan behaves nothing like one "
          "crossed once per row. Same language, same compiler, different bill.",
          "一方给出的根因是：每做一次操作，数据都要从 JavaScript 序列化进 Rust 再回来。每个查询计划过"
          "一次的边界，和每行过一次的边界，完全是两回事。同一门语言，同一个编译器，账单不一样。"),
         "prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm"),
        ("rust",
         ("394,195 lines of Rust are still in this repository", "这个仓库里仍然有 394,195 行 Rust"),
         ("The reversal had a scope. query-compiler/ holds 43,995 lines of Rust including a WASM "
          "crate; schema-engine/ holds 135,240. What went away was the per-operation execution "
          "path — the one seam where the boundary tax was charged.",
          "这次回退是有范围的。query-compiler/ 有 43,995 行 Rust，含一个 WASM crate；schema-engine/ "
          "有 135,240 行。被拿掉的是按操作走的执行路径——收边界税的就是那一条缝。"),
         "query-compiler/*.rs 230 files · schema-engine/*.rs 463 files"),
        ("current",
         ("The query-engine directory tells the story on its own", "query-engine 目录自己就把事情说清楚了"),
         ("At this commit, query-engine/ holds connectors and a connector test kit. The engine "
          "binary is gone. So is its per-operation Node boundary. The compiler that produces "
          "query plans is still there, shipping as WASM.",
          "在这个 commit 上，query-engine/ 里只剩连接器和一套连接器测试工具。引擎二进制没了。它那条"
          "按操作走的 Node 边界也没了。生成查询计划的编译器还在，以 WASM 形式发布。"),
         "query-engine/{connectors, connector-test-kit-rs}"),
        ("current",
         ("Distribution ruled the native option out on its own", "分发这一条自己就把原生方案否掉了"),
         ("Per-OS and per-OpenSSL native binaries cannot ship to an edge runtime at all. Boundary "
          "tuning does not touch that. It is why the 'keep Rust and batch the crossings' option "
          "stays on the table but is not selected.",
          "按 OS、按 OpenSSL 编出来的原生二进制，在边缘运行时上根本发不出去。调边界改变不了这一点。"
          "所以「保留 Rust、把跨界改成批量」这个选项留着，但没被选中。"),
         "D8 · first-party account"),
    ],

    "buys": [
        (("Nothing at a per-operation boundary", "在按操作计频的边界上，什么都买不到"),
         ("when the caller crosses once per row, serialization can exceed the entire baseline "
          "runtime — as it did here, by 2.36×.",
          "调用方每行过一次边界时，序列化开销可以超过整段基线运行时间——这里就超了 2.36×。")),
        (("Value where the seam is coarse", "接缝够粗的地方，买得到东西"),
         ("the retained WASM query-plan compiler crosses once per plan, and it stayed for exactly "
          "that reason.",
          "保留下来的 WASM 查询计划编译器每个计划才过一次边界，它留下来就是因为这个。")),
        (("A number to carry into the next proposal", "一个可以带进下一份提案的数字"),
         ("2.36× baseline is a measured boundary cost from a system that shipped. Put it in the "
          "sensitivity analysis of every extraction proposal.",
          "2.36× 基线是从一个真正发布过的系统上量出来的边界开销。把它放进每一份抽取提案的敏感性分析里。")),
    ],
    "nobuys": [
        (("Faster ORM queries in a JavaScript host", "在 JavaScript 宿主里跑更快的 ORM 查询"),
         ("measured 3.4× slower on the project's own 25,000-row benchmark once the boundary is "
          "counted.",
          "把边界算进去之后，在项目自己的 25,000 行基准上实测慢 3.4×。")),
        (("Edge-runtime deployment", "边缘运行时部署"),
         ("per-OS native binaries cannot ship where native binaries are not accepted; only the "
          "WASM path can.",
          "不接受原生二进制的地方，按 OS 编出来的二进制就是发不进去；只有 WASM 那条路走得通。")),
        (("A wider contributor pool", "更大的贡献者池"),
         ("requiring Rust and TypeScript together narrowed it, by the project's own account.",
          "按项目自己的说法，同时要求 Rust 和 TypeScript 反而把池子收窄了。")),
    ],

    "precedents": [
        {"name": "Microsoft · VS Code native text buffer", "outcome": "REVERTED",
         "body": ("They tried a native buffer implementation. Then they abandoned it: converting "
                  "strings between the native representation and V8 'compromised any performance "
                  "gained'. The fix was a better data structure in TypeScript.",
                  "他们试过原生缓冲区实现。后来放弃了：在原生表示和 V8 之间来回转换字符串，"
                  "'compromised any performance gained'。真正的解法是在 TypeScript 里换一个更好的"
                  "数据结构。"),
         "match": ("identical failure mode — a chatty boundary between a native core and a "
                   "JavaScript host",
                   "失效模式完全一样——原生内核和 JavaScript 宿主之间一条话很多的边界"),
         "mismatch": ("an editor text buffer rather than database query execution",
                      "对象是编辑器的文本缓冲区，不是数据库查询执行"),
         "regime": "first-party engineering account", "source_label": "first-party · project blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "pydantic · pydantic-core", "outcome": "EXTRACT",
         "body": ("The same pairing with the opposite result. A Rust validation core behind an "
                  "unchanged Python API keeps its native win, because the seam is coarse. The "
                  "reported kernel gain was around 17×, with application-level gains around 2–3×.",
                  "同样的搭配，结果相反。Rust 验证内核藏在没有改动的 Python API 后面，原生收益留住了，"
                  "原因是接缝够粗。内核层面报出来大约 17×，应用层面大约 2–3×。"),
         "match": ("the coarse-versus-chatty boundary distinction this decision turns on",
                   "这次决策的关键分野——接缝是粗的还是话多的"),
         "mismatch": ("Python rather than JavaScript, and validation is CPU-bound where ORM work "
                      "is I/O-bound",
                      "语言是 Python 不是 JavaScript；验证是 CPU 密集，ORM 是 I/O 密集"),
         "regime": "vendor benchmark plus user-reported figures", "source_label": "first-party · vendor article",
         "url": "https://pydantic.dev/articles/pydantic-v2"},
        {"name": "ast-grep · measured napi tax", "outcome": "QUANTIFIED",
         "body": ("An independent measurement of the Node native-binding boundary puts a "
                  "synchronous parse at roughly 6% overhead. Pass whole trees across and "
                  "serialization takes over.",
                  "对 Node 原生绑定边界的一次独立测量显示，同步解析的开销大约 6%。一旦把整棵树传过去，"
                  "序列化就占了大头。"),
         "match": ("quantifies the same boundary this decision failed on",
                   "量化的正是这次决策栽进去的那条边界"),
         "mismatch": ("a parser rather than an ORM, and a much lower call frequency",
                      "对象是解析器不是 ORM，调用频率也低得多"),
         "regime": "third-party benchmark of TypeScript parsers", "source_label": "third-party · author benchmark",
         "url": "https://medium.com/@hchan_nvim/benchmark-typescript-parsers-demystify-rust-tooling-performance-025ebfd391a3"},
        {"name": "Amazon · Prime Video living-room UI", "outcome": "EXTRACT SHIPPED",
         "body": ("A Rust and WASM core sits under a JavaScript UI, and it works. The seam is "
                  "why. The WASM VM adds up to 7.5 MB while saving 30 MB of JavaScript heap on "
                  "constrained devices.",
                  "JavaScript UI 下面挂着一个 Rust + WASM 内核，而且是成的。成在接缝上。WASM 虚拟机"
                  "最多多占 7.5 MB，却在受限设备上省下 30 MB 的 JavaScript 堆。"),
         "match": ("Rust-plus-WASM under a JavaScript host, which is the shape Prisma retained",
                   "JavaScript 宿主下的 Rust + WASM，正是 Prisma 留下来的那个形态"),
         "mismatch": ("a rendering core on embedded devices, not a database access layer",
                      "是嵌入式设备上的渲染内核，不是数据库访问层"),
         "regime": "first-party account across 8,000+ device types", "source_label": "first-party · research blog",
         "url": "https://www.amazon.science/blog/how-prime-video-updates-its-app-for-more-than-8-000-device-types"},
    ],

    "path": [
        {"title": ("Measure the boundary before choosing a seam", "先量边界，再挑接缝"),
         "body": ("Whoever proposes the native core builds a null-kernel benchmark first. Cross "
                  "the boundary at the real call frequency and do no work on the other side. "
                  "Express the crossing cost in baseline-time units and put it beside the target "
                  "speedup. If crossing alone costs more than the kernel could ever return, stop. "
                  "That is what happened here, at 2.36×. Nothing ships, so there is nothing to "
                  "roll back.",
                  "提出原生内核的那一方先做一个空内核基准。按真实调用频率过边界，另一边什么都不做。把"
                  "跨界开销换算成基线时间单位，和目标加速比摆在一起看。如果光是过边界就比内核能还回来的"
                  "还多，就停。这里就是这么停的，2.36×。这一步不发任何东西，也就没有回滚。"),
         "owner": "the team proposing a native core",
         "cost_range": ("2–3 days", "2–3 天"),
         "artifact": "a null-kernel benchmark that crosses the boundary at the real call frequency and does no work on the other side",
         "acceptance": "the measured crossing cost is expressed in baseline-time units and compared with the target speedup",
         "stop": "stop if crossing cost alone exceeds the benefit the kernel could deliver — as it did here at 2.36×",
         "rollback": "measurement only"},
        {"title": ("Let call frequency pick the seam", "让调用频率来决定接缝在哪"),
         "body": ("The architect writes a seam proposal with two numbers in it: crossings per "
                  "user-visible operation, and bytes carried by each. It passes when that count "
                  "is bounded and constant. Proportional to result-set size is a reject. Any seam "
                  "whose crossings scale with rows, nodes or events goes back. No code exists "
                  "yet, so the whole loss is a week of design.",
                  "架构师写一份接缝提案，里面要有两个数：每次用户可见操作跨界多少次，每次带多少字节。"
                  "跨界次数有界且恒定才算通过。跟结果集大小成正比就退回。任何跨界次数随行数、节点数或"
                  "事件数增长的接缝都退回。这一步还没写代码，最多损失一周设计时间。"),
         "owner": "the architect", "cost_range": ("1 week", "1 周"),
         "artifact": "a written seam proposal stating how many crossings occur per user-visible operation and how much data each carries",
         "acceptance": "crossings per operation are bounded and constant, not proportional to result-set size",
         "stop": "reject any seam whose crossing count scales with rows, nodes or events",
         "rollback": "no code written yet"},
        {"title": ("Price distribution as a hard constraint", "把分发当成硬约束来定价"),
         "body": ("The platform owner lists the deployment targets that cannot accept a native "
                  "binary, and says for each whether WASM covers it. Every required target is "
                  "either supported by the chosen artifact format or explicitly dropped. If a "
                  "required target cannot take the artifact, the native-binary option stops "
                  "there. Benchmark results do not override this. It is a document; there is "
                  "nothing to undo.",
                  "平台负责人列出所有不能接受原生二进制的部署目标，并逐个说明 WASM 覆不覆盖得了。每一个"
                  "必需目标要么被选定的产物格式支持，要么被明确放弃。只要有一个必需目标装不下这个产物，"
                  "原生二进制方案就到此为止。基准成绩推翻不了这一条。这一步只产出文档，没有什么要撤销的。"),
         "owner": "the platform owner",
         "cost_range": ("2–3 days", "2–3 天"),
         "artifact": "the list of deployment targets that cannot accept a native binary, and whether WASM covers them",
         "acceptance": "every required target is either supported by the chosen artifact format or explicitly dropped",
         "stop": "stop the native-binary option if a required target cannot accept it, regardless of benchmark results",
         "rollback": "documentation only"},
        {"title": ("Keep the reversal reversible", "让这次回退本身可以回退"),
         "body": ("The release owner ships this as a major-version transition, keeps the previous "
                  "engine reachable by version pin, and publishes a migration note. Consumers can "
                  "pin the old behaviour for at least one release cycle. Hold the default flip "
                  "until the parity report is clean. If it goes wrong, pin the previous major. "
                  "That is the rollback.",
                  "发布负责人把这次变更做成一个大版本切换，旧引擎通过锁版本仍然可达，并配一篇迁移说明。"
                  "使用方至少能在一个发布周期里锁住旧行为。对等性报告没跑干净之前，默认值先不翻。出问题"
                  "就锁回上一个大版本。回滚就是这一句。"),
         "owner": "the release owner",
         "cost_range": ("one major version", "一个大版本"),
         "artifact": "a major-version transition with the previous engine reachable by version pin, and a published migration note",
         "acceptance": "consumers can pin the previous behaviour for at least one release cycle",
         "stop": "hold the default flip until the parity report is clean",
         "rollback": "pin the previous major version"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响"), "state": "HIT",
         "claim": ("The Rust option's boundary cost exceeded the whole baseline runtime. No "
                   "kernel speedup could have delivered parity.",
                   "Rust 方案的边界开销超过了整段基线运行时间。任何内核加速都换不来对等。"),
         "evidence": "decision_math.py · ceiling 0.42×"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("The report puts the outcome on call frequency and copies rather than on "
                   "Rust's execution speed, and states that in the text.",
                   "报告把结果归到调用频率和拷贝上，而不是 Rust 的执行速度，并且是明写出来的。"),
         "evidence": "D10 · first-party root-cause statement"},
        {"name": ("Baseline and regime", "基线与测量口径"), "state": "HIT",
         "claim": ("The 185 ms and 55 ms figures are first-party, with no published harness. "
                   "Bundle size and edge runtimes are structural constraints, and they point the "
                   "same way.",
                   "185 ms 和 55 ms 是一方数据，没有公开的测量脚手架。产物体积和边缘运行时是结构性"
                   "约束，指向同一个方向。"),
         "evidence": "D1 caveat"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("Boundary cost is quantified in baseline-time units instead of described in "
                   "adjectives, and the retained coarse seam is kept distinct from the removed "
                   "chatty one.",
                   "边界开销用基线时间单位量化，没有停留在形容词上；保留的粗接缝和被移除的高频接缝"
                   "分开记录。"),
         "evidence": "D2, D12"},
        {"name": ("Scope control", "范围控制"), "state": "PASS",
         "claim": ("The report does not generalize to every Rust extraction. 394,195 lines of "
                   "Rust remain in the tree, and the WASM compiler is recorded as correctly "
                   "retained.",
                   "报告没有推广到所有 Rust 抽取场景。树里仍有 394,195 行 Rust，WASM 编译器被记录为"
                   "「保留得对」。"),
         "evidence": "query-compiler/*.rs 43,995 lines"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "反事实有没有真做"), "state": "PASS",
         "claim": ("The TypeScript option was built, measured and shipped as the default. Nothing "
                   "hypothetical about it.",
                   "TypeScript 方案是真做出来、量过、并且作为默认发布的。没有一点假设成分。"),
         "evidence": "GA v6.16.0; default in Prisma 7"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "PASS",
         "claim": ("Keeping the Rust engine meant a measured 185 ms baseline, a ~14 MB bundle, "
                   "and no edge-runtime support. The report names all three.",
                   "继续用 Rust 引擎的代价是：实测 185 ms 的基线、约 14 MB 的产物、边缘运行时不可用。"
                   "这三条报告里都写了。"),
         "evidence": "D1, D4, D8"},
        {"name": ("Native-advantage denial", "有没有否认原生优势"), "state": "PASS",
         "claim": ("Nothing here denies native value. A Rust WASM query-plan compiler was kept "
                   "because its seam is coarse.",
                   "这里没有否认原生的价值。Rust 的 WASM 查询计划编译器被留下来，就是因为它的接缝够粗。"),
         "evidence": "D12 · rust-coarse-wasm retained"},
        {"name": ("Hypothetical perfect counterfactual", "完美反事实假设"), "state": "HIT",
         "claim": ("The 'keep Rust and batch the crossings' option is retained and steelmanned. "
                   "Nobody ever measured it. This report rules it out on distribution, not on "
                   "latency.",
                   "「保留 Rust、把跨界改成批量」这个选项被保留，也做了最强论证。它从来没有被测过。"
                   "这份报告只能从分发上排除它，延迟上排除不了。"),
         "evidence": "rust-tune-boundary · WEAK evidence"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The transferable rule is narrow and testable: crossings per operation must be "
                   "bounded and constant, not proportional to result size.",
                   "可迁移的规则很窄，也能验证：每次操作的跨界次数必须有界且恒定，不能随结果集大小增长。"),
         "evidence": "reversible path step 2"},
    ],

    "gaps": [
        (("A published benchmark harness for the 185/55 ms pair", "185/55 ms 这一对数字缺公开的测量脚手架"),
         ("The figures are first-party. An independent reproduction would move D1 and D2 from "
          "strong-with-caveat to fully checkable. The structural constraints stand either way.",
          "这两个数是一方给的。有人独立复现，D1 和 D2 就能从「强但有保留」变成完全可核对。结构性约束"
          "无论如何都在。")),
        (("A measured batched-boundary variant", "批量边界的版本没有实测"),
         ("Nobody published a Rust engine with batched, zero-copy crossings. Until one exists, "
          "'keep Rust and tune the boundary' is excluded on distribution grounds and not on "
          "latency.",
          "没有人公布过采用批量、零拷贝跨界的 Rust 引擎。在它出现之前，「保留 Rust、调边界」只能以分发"
          "理由排除，延迟上排除不了。")),
        (("Per-operation crossing count for other workloads", "其他负载的单次操作跨界次数"),
         ("The 2.36× figure belongs to this query shape at this call frequency. Any transfer "
          "requires the target's own crossing count.",
          "2.36× 这个数字属于这种查询形态、这个调用频率。要搬到别处，先数清楚目标自己的跨界次数。")),
    ],

    "assumptions": [
        "The boundary derivation treats the whole query path as the candidate kernel; a narrower kernel would make the ceiling worse, not better.",
        "Prisma's published 185 ms and 55 ms figures describe the same workload on comparable hardware, as their post states.",
        "The shallow clone at the named commit reflects the post-reversal layout; directory contents are read as shipped.",
    ],
    "objective": {
        "driver": "performance and distribution",
        "requirement": "cut ORM query latency and shipped bundle size for JavaScript and TypeScript applications, including edge runtimes",
        "baseline": "185 ms for a 25,000-row findMany and roughly a 14 MB bundle, with the Rust query engine",
        "target": "at minimum parity on latency, plus deployability where native binaries are not accepted",
    },
    "repository": {
        "path": "https://github.com/prisma/prisma-engines",
        "commit": "9bae2a3a63b4f966c4855ad11503f44f50f4db47",
        "scope": "the query-execution path; the schema engine and query compiler are separate targets",
        "sampling": "shallow clone; 2,794 tracked files enumerated; query-engine/, query-compiler/, schema-engine/, libs/ and psl/ measured; no build or benchmark was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "prisma/prisma-engines at 9bae2a3 · static read-only analysis · why-not-rust method 2.0",
        "prisma/prisma-engines 于 commit 9bae2a3 · 只读静态分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/prisma/prisma-engines at commit 9bae2a3, shallow clone, 2,794 "
        "tracked files. Scope: the query-execution path. Sampling: 394,195 lines of Rust across "
        "1,647 files. query-engine/ holds 100,992 lines and now contains only connectors and a "
        "connector test kit — no engine binary and no node-api crate exists anywhere in the "
        "workspace. query-compiler/ holds 43,995 lines including query-compiler-wasm; "
        "schema-engine/ holds 135,240. 68 files carry wasm in their path. 17 `unsafe` keyword "
        "occurrences, 12 outside comments, against 15 crate roots declaring #![deny(unsafe_code)]. "
        "Per-directory figures count .rs only, so they are comparable with the 394,195 total. No "
        "build, test, benchmark or network call was run against the project. Objective: cut ORM "
        "query latency and shipped bundle size for JavaScript and TypeScript applications "
        "including edge runtimes. User-supplied facts: none. Amdahl/boundary inputs: share=1.0, "
        "kernel speedup=infinite, boundary=2.3636, target=1.0 → end-to-end 0.4230834320528008x, "
        "infinite-kernel ceiling 0.4230834320528008x, target physically IMPOSSIBLE. The boundary "
        "figure comes from Prisma's published 185 ms (with Rust) and 55 ms (without) on a "
        "25,000-row findMany, taking the TypeScript implementation as baseline: (185-55)/55 = "
        "2.3636 in baseline-time units. This is the one case in the published set where the "
        "evidence points away from Rust on a performance objective. The finding concerns the "
        "shape of the boundary rather than the speed of the language, which is why 394,195 lines "
        "of Rust remain in the tree. This is a structured decision protocol, not a statistical "
        "predictor.",

        "仓库：github.com/prisma/prisma-engines，commit 9bae2a3，浅克隆，2,794 个受控文件。范围：查询"
        "执行路径。采样：Rust 共 394,195 行，分布在 1,647 个文件里。query-engine/ 有 100,992 行，现在"
        "只剩连接器和一套连接器测试工具——整个 workspace 里既没有引擎二进制，也没有 node-api crate。"
        "query-compiler/ 有 43,995 行，含 query-compiler-wasm；schema-engine/ 有 135,240 行。路径里带 "
        "wasm 的文件 68 个。`unsafe` 关键字出现 17 次，注释之外 12 次，对应 15 个 crate 根声明了 "
        "#![deny(unsafe_code)]。分目录数字只统计 .rs，因此可以和 394,195 的总数对齐。没有对项目执行"
        "任何构建、测试、基准或网络调用。目标：降低 JavaScript 和 TypeScript 应用的 ORM 查询延迟与发布"
        "产物体积，含边缘运行时。用户提供的事实：无。Amdahl/边界输入：share=1.0，kernel "
        "speedup=infinite，boundary=2.3636，target=1.0 → 端到端 0.4230834320528008x，内核无穷快时的"
        "天花板 0.4230834320528008x，目标在物理上 IMPOSSIBLE。边界数值来自 Prisma 公布的 25,000 行 "
        "findMany 数据：带 Rust 185 ms，不带 55 ms；以 TypeScript 实现为基线，(185-55)/55 = 2.3636 个"
        "基线时间单位。在已发布的这批案例里，只有这一次证据在性能目标上指向「不要 Rust」。结论说的是"
        "边界的形态，而不是语言的速度，所以树里还留着 394,195 行 Rust。这是一套结构化决策流程，不是"
        "统计预测器。"
    ),
    "footer": (
        "public repository · static analysis at commit 9bae2a3 · no build, benchmark or network call",
        "公开仓库 · 在 commit 9bae2a3 上做静态分析 · 未执行构建、基准或网络调用",
    ),
}
