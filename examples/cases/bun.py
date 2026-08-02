"""oven-sh/bun — the migration this method approves, for the reason it actually had.

Repository facts were measured read-only on the shallow clone named in
`repository`. External numbers keep their URL and workload regime. The Amdahl
figures are produced by the skill's own calculator.
"""

CASE = {
    "slug": "bun",
    "project_name": "oven-sh/bun",
    "project_desc": (
        "Rust · JavaScript runtime and toolchain · 1,008,327 lines of Rust across 1,496 files, and zero Zig",
        "Rust · JavaScript 运行时与工具链 · 1,496 个文件、1,008,327 行 Rust，Zig 归零",
    ),
    "date": "2026-08-01",
    "archetype": (
        "cli-longtask · JavaScript runtime whose host layer was written in a manually memory-managed native language",
        "cli-longtask · JavaScript 运行时，宿主层原本用手动管理内存的原生语言写成",
    ),

    "scope_word": "MIGRATE",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "rust-migrate-complete",
    "scope_chip": (
        "the whole Zig host-runtime layer, replaced in Rust",
        "整个 Zig 宿主运行时层，用 Rust 重写",
    ),
    "scope_sub": (
        "the migration that shipped, approved for the reason it actually had",
        "已经上线的迁移，按它真正的理由批准",
    ),

    "why": (
        "Bun's own account names the motive: a persistent stream of use-after-free, double-free and leak "
        "defects across roughly 535,496 lines of Zig. Zig has no compile-time ownership or borrowing to stop "
        "that class. And the class was everywhere — manual lifetime management ran through the whole runtime, "
        "not through one component behind an interface. So no extraction reached it and no module-by-module "
        "scope reached it either; gate 3 takes the whole layer. Speed was never the argument. Selected "
        "first-party benchmarks moved 2.2–4.8%, and a performance-motivated version of this same migration "
        "fails gate 3 on the project's own numbers. At this commit the tree holds 1,008,327 lines of Rust, "
        "zero .zig files and no build.zig. This report grades something that already shipped.",

        "Bun 自己给出的动机是：Zig 实现里长期不断冒出 use-after-free、double-free 和内存泄漏，代码量约 535,496 行。"
        "Zig 没有编译期的所有权与借用检查，拦不住这一类缺陷。而这类缺陷是散开的——手动生命周期管理贯穿整个运行时，"
        "并不藏在某个接口后面的组件里。所以抽取够不着，逐模块迁移也够不着；gate 3 只能取整层。速度从来不是论据。"
        "厂商自选的 first-party 基准只动了 2.2–4.8%，同一次迁移若改用性能理由，用项目自己的数字就过不了 gate 3。"
        "当前 commit 下，树里有 1,008,327 行 Rust、0 个 .zig 文件、没有 build.zig。这份报告评的是已经上线的东西。",
    ),
    "trigger": (
        "One measurement reopens this. Count the incidence of use-after-free, double-free and leak defects "
        "over a stated window after the port, then print it beside the same-length window before it, with "
        "release cadence and triage rules held comparable. Nobody has done that. Until someone does, 10,257 "
        "opening unsafe blocks and 751 of 1,496 Rust files touching unsafe say the class was reduced by "
        "construction and not eliminated. If the measurement lands and the class did not move, the remedy "
        "failed — the requirement still stands. Treat the block count as a coarse proxy in both directions: "
        "a block encapsulated behind a safe API is not the same risk as one whose invariants leak to callers.",

        "重开这个决策只需要一项测量：迁移后某个明确窗口内 use-after-free、double-free、内存泄漏的发生率，"
        "与迁移前同等长度的窗口并排列出，发布节奏和缺陷分类规则保持可比。没人做过。在此之前，"
        "10,257 个 unsafe 起始块、1,496 个 Rust 文件里有 751 个碰到 unsafe，说明这一类缺陷是被结构性削减，"
        "不是被消除。如果测量做出来、这一类没有下降，那么失效的是这套疗法，需求本身仍然成立。"
        "块数在两个方向上都是粗糙的代理指标：被安全 API 封住的 unsafe 块，和把不变量泄漏给调用方的 unsafe 块，"
        "风险并不相同。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS",
         "short": ("Requirement", "需求"),
         "hero_evidence": ("A documented, recurring use-after-free, double-free and leak stream.",
                           "有记录、反复出现的 use-after-free、double-free 与内存泄漏。"),
         "name": "requirement",
         "evidence": "The first-party account names a persistent stream of use-after-free, double-free and leak defects in the Zig implementation as the motive for the port, and reports significant leak fixes afterwards (https://bun.com/blog/bun-in-rust). No defect counts or rates are published in either direction, so the requirement is documented rather than quantified."},
        {"id": "G2", "state": "PASS",
         "short": ("Causality", "因果"),
         "hero_evidence": ("Zig has no ownership-and-borrowing enforcement; Rust does.",
                           "Zig 没有所有权与借用的强制检查，Rust 有。"),
         "name": "rust-specific causality",
         "evidence": "The defect class is manual-lifetime error. Rust's ownership and borrow checking are compile-time enforcement Zig does not provide, and the port was a same-architecture translation, so no algorithm, data-model or architecture change competes for the credit."},
        {"id": "G3", "state": "PASS",
         "short": ("Economics", "经济性"),
         "hero_evidence": ("The class was distributed, so no smaller scope reached it.",
                           "缺陷散布在整层，更小的范围够不着。"),
         "name": "economics and smallest sufficient option",
         "evidence": "Manual lifetimes were the discipline of the whole Zig runtime rather than of one component, so neither an extraction nor a module-by-module port reaches the class. The port cost about 11 days of roughly 64 parallel agents and about $165k in API spend (https://bun.com/blog/bun-in-rust); the closest comparable whole-project port, fish shell's 57k lines of C++, took a volunteer project about two years (https://fishshell.com/blog/rustport/)."},
        {"id": "G4", "state": "PASS",
         "short": ("Delivery", "交付"),
         "hero_evidence": ("It shipped; 19 regressions found and since fixed; releases are the rollback.",
                           "已上线；报出 19 个回归，都已修复；回滚就是钉住旧版本。"),
         "name": "delivery and reversibility",
         "evidence": "The port is in released versions and the tree at this commit contains no Zig; 19 regressions were reported and have since been fixed (https://bun.com/blog/bun-in-rust), and pinning a pre-port release is a real rollback. A third-party account contested the port's production-readiness at publication (https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743), recorded here as a quality signal rather than a measurement."},
    ],

    "tiles": [
        (("Zig left in the tree", "树里还剩多少 Zig"), "0", ("files", "个文件"),
         ("no build.zig · Cargo.toml present · port complete at f91d5c95",
          "没有 build.zig · 有 Cargo.toml · 迁移在 f91d5c95 已完成")),
        (("Rust now shipping", "现在发布的 Rust"), "1,008,327", ("lines", "行"),
         ("1,496 files · 1,005,761 lines under src/",
          "1,496 个文件 · 1,005,761 行在 src/ 下")),
        (("Zig it replaced", "它替掉的 Zig"), "~535,496", ("lines", "行"),
         ("first-party figure · bun.com/blog/bun-in-rust",
          "first-party 数字 · bun.com/blog/bun-in-rust")),
        (("Opening unsafe blocks", "unsafe 起始块"), "10,257", ("blocks", "块"),
         ("roughly one per 98 lines of Rust — class reduced, not removed",
          "约每 98 行 Rust 一个 · 这一类被削减，没有清除")),
        (("Rust files touching unsafe", "碰到 unsafe 的 Rust 文件"), "50.2", "%",
         ("751 of 1,496 files · Android reports ~4% of lines unsafe",
          "1,496 个文件中的 751 个 · Android 报告约 4% 的行是 unsafe")),
        (("Measured end-to-end delta", "实测端到端差值"), "2.2–4.8", "%",
         ("selected first-party benchmarks · never the reason",
          "厂商自选的 first-party 基准 · 从来不是迁移的理由")),
    ],

    "options_sub": (
        "Every option is scored against one objective: eliminate the recurring use-after-free, double-free "
        "and leak class in Bun's runtime implementation, without regressing shipped performance or "
        "JavaScript-facing behaviour.",
        "所有方案对着同一个目标打分：消除 Bun 运行时实现中反复出现的 use-after-free、double-free、内存泄漏"
        "这一类缺陷，同时不让已发布的性能和面向 JavaScript 的行为退化。",
    ),
    "options": [
        {"id": "zig-harden",
         "name": ("Stay in Zig, harden it", "留在 Zig，把它加固"),
         "implementation": "current", "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("lowers incidence; cannot remove the class",
                              "能压低发生率；消不掉这一类"),
         "one_time_cost": "sanitizer, allocator and lifetime-tooling work",
         "recurring_cost": "permanent review discipline",
         "cost_cell": ("instrumentation work; permanent review load", "插桩工作量；长期的评审负担"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "native",
         "compat_cell": ("native · nothing to change", "原生 · 无需改动"),
         "reversibility": "n/a",
         "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the counterfactual nobody ever priced", "保留 · 从来没人给它算过账的反事实方案"),
         "reason": "Zig checks lifetimes by discipline and tooling rather than by the compiler, so hardening lowers incidence without removing the class — and the documented bug stream is what that discipline produced over the life of the Zig implementation. Nobody funded or measured this programme against the port, which the challenge audit records as a hit against the staying case, not as a reason to dismiss it."},
        {"id": "rust-migrate-complete",
         "name": ("Port the whole Zig layer to Rust", "把整个 Zig 层迁到 Rust"),
         "implementation": "rust", "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("class removed by construction wherever the code is safe Rust",
                              "只要代码是 safe Rust，这一类缺陷在结构上就不存在"),
         "one_time_cost": "~11 days, ~64 parallel agents, ~$165k API spend",
         "recurring_cost": "one Rust host layer; 10,257 unsafe blocks still need owners",
         "cost_cell": ("~11 days, ~$165k API spend; unsafe blocks need owners",
                       "约 11 天、约 $165k API 花费；unsafe 块需要有人认领"),
         "time_to_value": ("shipped", "已上线"),
         "compatibility": "behavioural, not an ABI: 19 regressions, since fixed",
         "compat_cell": ("19 regressions, since fixed · pin a pre-port release",
                         "19 个回归，都已修复 · 回滚就钉住迁移前的版本"),
         "reversibility": "pin a pre-port release",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · already executed; 0 .zig files at this commit",
                  "推荐 · 已经做完；当前 commit 下 0 个 .zig 文件"),
         "reason": "The only option that reaches a defect class distributed across the whole runtime, at a one-time cost small against any conventional rewrite of that size. It is also done: the tree at f91d5c95 carries 1,008,327 lines of Rust and no Zig, which is why this case is evidence rather than a forecast."},
        {"id": "rust-incremental",
         "name": ("Port module by module over years", "按模块迁移，做上几年"),
         "implementation": "rust", "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("class removed in ported modules only; live in the remainder",
                              "只在已迁的模块里消除；其余部分照旧"),
         "one_time_cost": "multi-year, module by module",
         "recurring_cost": "a Zig-Rust boundary for the whole duration",
         "cost_cell": ("multi-year; dual-stack boundary throughout", "多年；全程维护双栈边界"),
         "time_to_value": ("per module", "按模块逐个见效"),
         "compatibility": "internal boundary churn",
         "compat_cell": ("internal boundary churn · per-module revert", "内部边界反复变动 · 按模块回退"),
         "reversibility": "per module",
         "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · a distributed class is not contained by a module boundary",
                  "排除 · 模块边界关不住一类散开的缺陷"),
         "reason": "Manual lifetime management was the discipline of the whole runtime, so no module boundary contains the class; the option pays a Zig-Rust boundary for years and still leaves the requirement unmet in whatever is not yet ported. It is the normally correct shape — Android and Stylo both won that way — and it is the wrong shape for a defect class that has no component to sit behind."},
        {"id": "rust-for-speed",
         "name": ("The same port, justified on speed", "同一次迁移，改用速度当理由"),
         "implementation": "rust", "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("1.048x end-to-end at the best selected figure; a 1.5x target is missed",
                              "用最好的自选数字算，端到端 1.048x；1.5x 目标达不到"),
         "one_time_cost": "identical to the selected option",
         "recurring_cost": "identical to the selected option",
         "cost_cell": ("same cost; benefit does not meet the target", "成本相同；收益够不到目标"),
         "time_to_value": ("never — the target is not met", "永远不会——目标本就达不到"),
         "compatibility": "same as the selected option",
         "compat_cell": ("same as selected · same rollback", "与选定方案相同 · 回滚方式相同"),
         "reversibility": "same as the selected option",
         "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · this migration is the natural experiment that refutes it",
                  "排除 · 这次迁移本身就是推翻它的自然实验"),
         "reason": "Selected first-party benchmarks moved 2.2–4.8%. With the whole program as the kernel, the best selected figure as the kernel speedup and no boundary cost, end-to-end is 1.048x against a 1.5x target, so gate 3 fails on this project's own numbers. The identical migration therefore passes on safety and fails on speed — the axis, not the scope, is what decides it."},
        {"id": "adopt-rust-runtime",
         "name": ("A consumer adopts a Rust-cored runtime", "下游改用 Rust 内核的运行时"),
         "implementation": "external", "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("requirement met for that one consumer", "只满足那一个下游自己的需求"),
         "one_time_cost": "per consumer migration",
         "recurring_cost": "a different compatibility target to track",
         "cost_cell": ("per consumer; different compatibility target", "每个下游各付各的；兼容目标不同"),
         "time_to_value": ("days to weeks per project", "每个项目数天到数周"),
         "compatibility": "different API and ecosystem surface",
         "compat_cell": ("different API surface · consumer's own revert", "API 面不同 · 由下游自己回退"),
         "reversibility": "consumer-side",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · valid for a consumer, not a decision Bun can make",
                  "保留 · 对下游成立，但不是 Bun 能替他们做的决定"),
         "reason": "A Rust-cored JavaScript runtime already exists, so a consumer whose own requirement is memory safety in the runtime layer has an option today without waiting for anyone. It does nothing about Bun's own implementation, which is the subject of this decision."},
    ],

    "amdahl": {
        "share": 1.0,
        "kernel_speedup": 1.048,
        "boundary": 0.0,
        "target": 1.5,
        "note": (
            "The whole program is the candidate kernel, so share=1.00 and there is no Amdahl wall: the "
            "infinite-kernel ceiling is unbounded. Kernel speedup is the best selected first-party figure, "
            "Bun.serve +4.8% (https://bun.com/blog/bun-in-rust). End-to-end comes out at 1.048x. A 1.5x target "
            "is therefore physically possible and still NOT met by this candidate. The wall is empirical "
            "rather than structural — the measured native-to-native delta. On that axis the same migration "
            "fails gate 3; on the safety axis it passes.",

            "候选内核就是整个程序，所以 share=1.00，根本没有 Amdahl 墙：无限加速下的上限是 unbounded。"
            "内核加速比取厂商自选数字里最好的那个，Bun.serve +4.8%，来源 https://bun.com/blog/bun-in-rust。"
            "端到端算出来 1.048x。也就是说 1.5x 目标在物理上做得到，而这个候选方案仍然 NOT met。"
            "这里的墙是经验性的，不是结构性的——就是实测的原生到原生差值。走这条轴，同一次迁移过不了 gate 3；"
            "走安全那条轴，它过。",
        ),
    },

    "lenses_sub": (
        "Each state is evidence scoped to a named option. Nothing here adds up to a score. D6 appears twice: "
        "the mechanism and the measured outcome point different ways, and merging them would bury the one "
        "that sets robustness. Repository claims were measured on the commit named in the methodology. "
        "Amdahl figures come from scripts/decision_math.py, with the inputs disclosed there.",

        "每一条状态都是绑定到具体方案的证据，不能相加成分数。D6 出现了两次：机制和实测结果指向不同方向，"
        "合并会把决定 robustness 的那一条盖掉。仓库类结论测于方法学里注明的那个 commit。"
        "Amdahl 数字来自 scripts/decision_math.py，输入在那里公开。",
    ),
    "na_note": (
        "One N/A row. D4 fleet footprint carries no part of a defect-class objective, and neither "
        "implementation publishes a per-instance memory delta, a fleet break-even or a cost model. The leak "
        "fixes in the first-party account would push steady-state memory the right way. There is no figure "
        "to cite.",

        "只有一条 N/A。D4 机群占用与「消除某类缺陷」这个目标无关，两个实现都没有公布单实例内存差值、"
        "机群回本点或成本模型。first-party 提到的那些泄漏修复，会把稳态内存往好的方向推。但没有数字可引。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-migrate-complete", "rust-incremental"],
         "claim": ("The unmet requirement is a recurring defect class: use-after-free, double-free, leak. It "
                   "lives entirely in code Bun owns — the runtime implementation itself, roughly 535,496 lines "
                   "of Zig before the port.",
                   "未满足的需求是一类反复出现的缺陷：use-after-free、double-free、内存泄漏。它完全落在 Bun "
                   "自己的代码里——运行时实现本身，迁移前约 535,496 行 Zig。"),
         "source": "https://bun.com/blog/bun-in-rust", "regime": "first-party account of a recurring defect class",
         "caveat": "The account names the class and reports significant leak fixes but publishes no defect counts or rates, so the requirement is documented rather than sized."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "DISFAVORS · rust-for-speed", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-for-speed"],
         "claim": ("The whole program is the candidate kernel. Share is 1.00, the infinite-kernel ceiling is "
                   "unbounded, and there is no Amdahl wall to hit. What stops it is the measured delta. Feed "
                   "the best selected first-party figure in as the kernel speedup and end-to-end is 1.048x, so "
                   "a 1.5x target is physically possible and this candidate misses it.",
                   "候选内核就是整个程序。share 为 1.00，无限加速上限是 unbounded，没有 Amdahl 墙可撞。"
                   "挡住它的是实测差值。把厂商自选数字里最好的那个当内核加速比代进去，端到端是 1.048x；"
                   "1.5x 目标物理上做得到，这个候选方案够不到。"),
         "source": "scripts/decision_math.py · share=1.00, kernel=1.048, boundary=0, target=1.5 · https://bun.com/blog/bun-in-rust",
         "regime": "vendor-selected first-party benchmarks, same architecture, native to native",
         "caveat": "1.048x is Bun's own best selected figure, not an independent same-workload measurement; the decision-relevant quantity is the single-digit order of the delta, not its third decimal."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Nobody asserted a tail-latency requirement for this decision. Neither host-layer "
                   "implementation introduces or removes a managed collector. 311,915 lines of C and 290,842 "
                   "of C++ remain in the tree at this commit, untouched by the port.",
                   "这次决策没有人提出尾延迟需求。宿主层的两个实现都没有引入或去掉托管回收器。当前 commit 下，"
                   "树里仍有 311,915 行 C 和 290,842 行 C++，迁移没碰它们。"),
         "source": "measured at f91d5c95 · 122 .c files, 605 .cpp files",
         "regime": "static file inventory of the shipped tree",
         "caveat": "The leak fixes the first-party account reports are resource-lifetime fixes in the ported layer, not collector behaviour."},
        {"id": "D4", "name": ("Fleet footprint", "机群占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Neither implementation states or publishes a fleet-density objective, a per-instance "
                   "memory delta, or a break-even.",
                   "两个实现都没有提出或公布机群密度目标、单实例内存差值或回本点。"),
         "source": "objective is a defect class, not a cost model", "regime": "n/a",
         "caveat": "Leak fixes plausibly lower steady-state memory, but no measurement exists to cite; if a footprint requirement is stated later, D4 must be recomputed against a real profile."},
        {"id": "D5", "name": ("Startup shape", "启动特征"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Both the Zig baseline and the Rust port are ahead-of-time compiled native binaries with no "
                   "managed runtime in the host layer. No startup mechanism separates them.",
                   "Zig 基线和 Rust 迁移版都是提前编译的原生二进制，宿主层没有托管运行时。"
                   "没有任何启动机制能把两者分开。"),
         "source": "https://bun.com/blog/bun-in-rust — next build +4.5%",
         "regime": "first-party selected benchmark, not a startup decomposition",
         "caveat": "The published set never separates process start from total wall-clock; the one invocation-shaped figure sits inside the same single-digit band as the rest."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-migrate-complete", "rust-incremental"],
         "claim": ("This mechanism is the whole case. Zig maintains lifetimes by discipline; Rust enforces "
                   "ownership and borrowing at compile time. Wherever the ported code is safe Rust, the named "
                   "class is unreachable by construction rather than by review.",
                   "这个机制就是整个论据。Zig 靠纪律维持生命周期，Rust 在编译期强制所有权与借用。"
                   "凡是迁移后代码属于 safe Rust 的地方，这一类缺陷是结构上到不了，而不是靠人评审挡住。"),
         "source": "https://bun.com/blog/bun-in-rust · https://blog.google/security/rust-in-android-move-fast-fix-things/",
         "regime": "structural language property plus the one large published outcome for the same class",
         "caveat": "Android's programme is the closest measured outcome — memory-safety share of vulnerabilities 76% to below 20%, and roughly 0.2 against 1,000 vulnerabilities per million lines — but that comparison is C/C++-relative and is not a prediction for this port."},
        {"id": "D6", "name": ("Safety & correctness — measured outcome", "安全与正确性——实测结果"),
         "label": "UNKNOWN · rust-migrate-complete", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-migrate-complete"],
         "claim": ("The outcome this migration existed to produce has not been measured. 10,257 opening unsafe "
                   "blocks remain, alongside 1,235 unsafe fn, 399 unsafe impl and 966 unsafe extern. 751 of "
                   "1,496 Rust files contain at least one of those four forms. No one has published the "
                   "post-port incidence of use-after-free, double-free or leak defects.",
                   "这次迁移为之存在的结果，至今没有被测量过。树里还有 10,257 个 unsafe 起始块，"
                   "以及 1,235 个 unsafe fn、399 个 unsafe impl、966 个 unsafe extern。1,496 个 Rust 文件里，"
                   "751 个至少含这四种形式之一。迁移后 use-after-free、double-free、内存泄漏的发生率，"
                   "没有任何人公布过。"),
         "source": "measured at f91d5c95 · roughly one opening unsafe block per 98 lines of Rust (1,008,327 / 10,257 = 98.3)",
         "regime": "static pattern count on the shipped tree; no defect-rate data on either side",
         "caveat": "Android reports about 4% of its Rust lines as unsafe; that is a share of lines while this is a block count per line, so the comparison is directional and not an equivalence. Block count is also a coarse proxy for risk: an encapsulated block behind a safe API is not the same exposure as one whose invariants leak to callers."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-migrate-complete", "rust-incremental"],
         "claim": ("Rust encodes ownership handoff and thread-safety in the type system. The closest "
                   "comparable whole-project port says which property settled it, and it was not performance: "
                   "'the killer feature of Rust, from fish-shell's perspective, is Send and Sync'.",
                   "Rust 把所有权交接和线程安全编码进类型系统。最接近的整项目迁移先例明说了是哪条属性定的调，"
                   "而且不是性能：'the killer feature of Rust, from fish-shell's perspective, is Send and Sync'。"),
         "source": "https://fishshell.com/blog/rustport/ · https://bun.com/blog/bun-in-rust",
         "regime": "first-party engineering judgement from two completed native-to-Rust ports",
         "caveat": "Neither account publishes a race or ownership-defect count, so this is a mechanism claim supported by maintainer judgement, not a measured delta."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "SUPPORTS · rust-migrate-complete", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-migrate-complete"],
         "claim": ("First-party reports binaries roughly 20% smaller after the port. For a runtime shipped as "
                   "one downloadable binary, that is a distribution benefit.",
                   "first-party 报告迁移后二进制体积小了约 20%。对一个以单个可下载二进制发布的运行时来说，"
                   "这是分发上的收益。"),
         "source": "https://bun.com/blog/bun-in-rust", "regime": "first-party build-size comparison",
         "caveat": "Size is a side benefit, not part of the requirement, and the build stays multi-language either way: 311,915 lines of C, 290,842 of C++ and 825,147 of TypeScript remain in the tree at this commit."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · adopt-rust-runtime", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-runtime"],
         "claim": ("A Rust-cored JavaScript runtime already exists. That is evidence the Rust ecosystem "
                   "carries this workload. It also means a consumer whose own requirement is runtime-layer "
                   "memory safety has an option today, independent of what Bun decides.",
                   "以 Rust 为内核的 JavaScript 运行时已经存在。这说明 Rust 生态扛得住这类负载。"
                   "同时也意味着，如果某个下游自己的需求是运行时层的内存安全，它今天就有选择，不必等 Bun 表态。"),
         "source": "https://en.wikipedia.org/wiki/Deno_(software)", "regime": "shipped third-party runtime",
         "caveat": "A different runtime with a different API surface and compatibility target; it is an option for a consumer, never a substitute for Bun's own implementation decision."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-incremental", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-incremental"],
         "claim": ("Manual lifetime management is a discipline spread across the runtime, not a component "
                   "behind an interface. So a module-by-module port carries a Zig-Rust boundary for its whole "
                   "duration, and the target class stays live in everything not yet ported. Ending Zig ends "
                   "the boundary question. 0 .zig files and no build.zig at this commit.",
                   "手动生命周期管理是一种散布在整个运行时里的纪律，不是接口后面的一个组件。"
                   "所以逐模块迁移全程都要维护 Zig-Rust 边界，而目标缺陷类在尚未迁移的部分里继续活着。"
                   "Zig 归零，边界问题也就结束了。当前 commit 下 0 个 .zig 文件，没有 build.zig。"),
         "source": "measured at f91d5c95 · https://bun.com/blog/bun-in-rust",
         "regime": "static inventory of the shipped tree plus first-party account",
         "caveat": "The compatibility surface that actually bound here was behavioural rather than an ABI: 19 regressions were reported and have since been fixed."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "SUPPORTS · rust-migrate-complete", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-migrate-complete"],
         "claim": ("Roughly 535,496 lines of Zig were ported in about 11 days. Roughly 64 parallel agents did "
                   "it, at about $165k in API spend. The result is in released versions, with 19 regressions "
                   "reported and since fixed.",
                   "约 535,496 行 Zig 在大约 11 天内完成迁移。执行方是大约 64 个并行 agent，API 花费约 $165k。"
                   "结果已经进入发布版本，报出 19 个回归，都已修复。"),
         "source": "https://bun.com/blog/bun-in-rust · https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743",
         "regime": "first-party account of a completed port; production-readiness contested by a third-party account at publication",
         "caveat": "The cost figure is API spend and does not price the human review, triage and regression work around it. The contested-quality signal is recorded in neutral terms as a signal, not as a measurement, and this report makes no claim about anyone's motives."},
        {"id": "D12", "name": ("Counterfactual", "反事实对照"),
         "label": "DISFAVORS · zig-harden", "css": "current",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["zig-harden"],
         "claim": ("The in-language counterfactual cannot reach the same target. Zig checks lifetimes with "
                   "discipline and tooling, not with the compiler, so hardening lowers incidence without "
                   "removing the class. The documented defect stream is what that discipline produced over the "
                   "life of the Zig implementation.",
                   "留在语言内的反事实方案够不到同一个目标。Zig 靠纪律和工具检查生命周期，不靠编译器，"
                   "所以加固只能压低发生率，消不掉这一类缺陷。有记录的那条缺陷流，"
                   "正是这套纪律在 Zig 实现的整个生命周期里产出的东西。"),
         "source": "https://bun.com/blog/bun-in-rust", "regime": "first-party account of the pre-port implementation",
         "caveat": "Nobody priced a funded Zig hardening programme — sanitizer coverage, allocator instrumentation, review gates — against the port, so the comparison is structural rather than measured. The port's own outcome against the same class is likewise unmeasured, so neither side of this counterfactual has a number."},
    ],

    "findings": [
        ("rust",
         ("There is no Zig left in the tree", "树里已经没有 Zig 了"),
         ("At f91d5c95 the tree carries 1,008,327 lines of Rust across 1,496 files, 1,005,761 of them under "
          "src/. Zero .zig files. No build.zig, and Cargo.toml is present. The decision this report authorizes "
          "has already been executed, so read the case as evidence rather than as a forecast.",
          "在 f91d5c95 上，树里有 1,008,327 行 Rust，分布在 1,496 个文件中，其中 1,005,761 行在 src/ 下。"
          ".zig 文件为 0。没有 build.zig，Cargo.toml 在。这份报告授权的决策已经执行完毕，"
          "所以它可以当证据读，不必当预测读。"),
         "measured at f91d5c95 · 19,034 tracked files"),
        ("current",
         ("Speed was never the reason, and the numbers say so", "速度从来不是理由，数字也是这么说的"),
         ("Selected first-party benchmarks moved 2.2–4.8%: Bun.serve +4.8%, next build +4.5%. Put the best of "
          "those through the same Amdahl calculation, with the whole program as the kernel, and end-to-end is "
          "1.048x. Share is 1.00, so the ceiling is unbounded and a 1.5x target is physically possible at this "
          "scope. The candidate still misses it. This port is the natural experiment against "
          "performance-motivated native-to-native rewrites.",
          "厂商自选的 first-party 基准只动了 2.2–4.8%：Bun.serve +4.8%，next build +4.5%。"
          "把其中最好的一个代进同一套 Amdahl 计算，内核取整个程序，端到端是 1.048x。share 是 1.00，"
          "所以上限 unbounded，1.5x 目标在这个范围上物理可达。候选方案照样够不到。"
          "这次迁移就是针对「原生换原生求性能」这套做法的自然实验。"),
         "https://bun.com/blog/bun-in-rust · decision_math.py share=1.00 kernel=1.048 boundary=0 target=1.5"),
        ("unknown",
         ("10,257 unsafe blocks: the class was reduced, not eliminated",
          "10,257 个 unsafe 块：这一类被削减，没有被消除"),
         ("751 of 1,496 Rust files contain at least one of those four forms, which is 50.2%. Alongside them "
          "sit 1,235 unsafe fn, 399 unsafe impl and 966 unsafe extern, roughly one opening unsafe block per 98 "
          "lines of Rust (1,008,327 / 10,257 = 98.3). Android's programme reports about 4% of its Rust lines "
          "as unsafe. The two are counted differently: share of lines there, block count per line here. Treat "
          "that comparison as directional. And nobody has published a post-port measurement of Bun's target "
          "defect class.",
          "1,496 个 Rust 文件里有 751 个至少含这四种形式之一，占 50.2%。同时还有 1,235 个 unsafe fn、"
          "399 个 unsafe impl、966 个 unsafe extern，平均约每 98 行 Rust 一个 unsafe 起始块"
          "（1,008,327 / 10,257 = 98.3）。Android 的项目报告其 Rust 代码约 4% 的行是 unsafe。"
          "两边口径不同：那边是行占比，这边是每行的块数。这个对比只能看方向。"
          "而且迁移后 Bun 目标缺陷类的测量，没有任何人公布过。"),
         "measured at f91d5c95 · https://blog.google/security/rust-in-android-move-fast-fix-things/"),
        ("current",
         ("19 regressions, reported and fixed", "19 个回归，报出来，修掉了"),
         ("The first-party account reports 19 regressions, since fixed, next to significant leak fixes. Read "
          "that as evidence about acceptance and rollback. Released versions are the rollback path. A "
          "migration this size that ships, breaks 19 things and repairs them is behaving like a delivery "
          "process rather than an accident. A published third-party account contested the port's "
          "production-readiness at publication, recorded here as a quality signal in neutral terms.",
          "first-party 的说法是 19 个回归，都已修复，同时有明显的泄漏修复。把它当成关于验收和回滚的证据来读。"
          "回滚路径就是已发布的版本。这个体量的迁移上线、弄坏 19 处、再修好，表现出来的是一套交付流程，"
          "不是一次事故。有一篇第三方报道在发布时质疑了这次迁移的生产就绪度，这里以中性措辞记为质量信号。"),
         "https://bun.com/blog/bun-in-rust · theregister.com, 14 Jul 2026"),
        ("current",
         ("The Zig layer was migrated; the tree was not", "换掉的只是 Zig 层，树里其他语言还在"),
         ("1,008,327 lines of Rust replaced roughly 535,496 lines of Zig. State the ratio and stop there. Line "
          "counts across languages measure neither effort nor quality, and a mechanical translation inflates "
          "them for reasons unrelated to both. Meanwhile 311,915 lines of C, 290,842 of C++ and 825,147 of "
          "TypeScript are still in the tree at this commit.",
          "1,008,327 行 Rust 替掉了约 535,496 行 Zig。这个比例说一句就够，不必解读。"
          "跨语言的行数既不衡量工作量，也不衡量质量，而机械翻译会因为跟这两者都无关的原因把它抬高。"
          "与此同时，当前 commit 下树里还有 311,915 行 C、290,842 行 C++、825,147 行 TypeScript。"),
         "measured at f91d5c95 · Zig figure from bun.com/blog/bun-in-rust"),
    ],

    "buys": [
        (("Compile-time enforcement of the lifetime discipline", "生命周期纪律的编译期强制"),
         ("the class Bun's own account names (use-after-free, double-free, leak) moves from reviewer "
          "discipline to a checked property everywhere the code is safe Rust.",
          "Bun 自己点名的那一类缺陷（use-after-free、double-free、内存泄漏），从「靠评审人把关」"
          "变成一条被检查的属性，只要代码是 safe Rust 就成立。")),
        (("A single-language host layer with no dual-stack boundary", "单一语言的宿主层，没有双栈边界"),
         ("0 .zig files and no build.zig at this commit. There is no Zig-Rust seam to maintain — the cost a "
          "module-by-module port would have carried for years.",
          "当前 commit 下 0 个 .zig 文件，也没有 build.zig。没有 Zig-Rust 接缝要维护——"
          "那正是逐模块迁移要背上好几年的成本。")),
        (("Smaller shipped binaries", "发布的二进制更小"),
         ("first-party reports binaries roughly 20% smaller after the port. Useful for a runtime distributed "
          "as one download, and no part of the requirement.",
          "first-party 报告迁移后二进制小了约 20%。对以单个下载分发的运行时有用，但不属于需求的一部分。")),
    ],
    "nobuys": [
        (("Speed", "速度"),
         ("selected first-party benchmarks moved 2.2–4.8%. At share 1.00 and the 4.8% best case, end-to-end is "
          "1.048x and a 1.5x target is missed. Frame this migration as a performance project and it fails gate "
          "3 on the project's own numbers.",
          "厂商自选的 first-party 基准只动了 2.2–4.8%。取 share 1.00 和 4.8% 的最好情形，端到端是 1.048x，"
          "1.5x 目标达不到。把这次迁移包装成性能项目，用项目自己的数字就过不了 gate 3。")),
        (("Elimination of the memory-safety class", "把内存安全这一类彻底消除"),
         ("10,257 opening unsafe blocks remain, with 1,235 unsafe fn, 399 unsafe impl and 966 unsafe extern, "
          "and 50.2% of Rust files contain at least one of those forms. Where the code is safe, the class is "
          "unreachable by construction. It is not gone.",
          "树里还剩 10,257 个 unsafe 起始块，另有 1,235 个 unsafe fn、399 个 unsafe impl、966 个 unsafe extern，"
          "50.2% 的 Rust 文件至少含其中一种。代码是 safe 的地方，这一类缺陷结构上到不了。但它没有消失。")),
        (("A verified safety outcome", "一个经过验证的安全结果"),
         ("no measurement of the post-port incidence of the target class exists. The migration is approved on "
          "a documented requirement and an enforced mechanism, not on a demonstrated result.",
          "迁移后目标缺陷类的发生率，没有任何测量。这次迁移获批，靠的是一条有记录的需求和一套被强制执行的机制，"
          "不是靠已经展示出来的结果。")),
    ],

    "precedents": [
        {"name": "fish shell 4.0", "outcome": "MIGRATED",
         "body": ("A whole-project C++ to Rust port. Its own maintainers reported performance 'usually "
                  "slightly better in terms of time taken', with memory use showing a slightly higher floor "
                  "and a lower ceiling. What settled it for them was Send and Sync, not speed. The "
                  "'handwaving, half a year' estimate became roughly two years.",
                  "一次整项目的 C++ 到 Rust 迁移。维护者自己给出的性能说法是 'usually slightly better in terms "
                  "of time taken'，内存占用下限略高、上限更低。真正定调的是 Send 和 Sync，不是速度。"
                  "当初 'handwaving, half a year' 的估计，最后变成了大约两年。"),
         "match": ("whole-project native-to-Rust migration with a near-neutral performance lens and safety "
                   "plus invariants as the motive",
                   "同为整项目的原生到 Rust 迁移，性能维度近乎中性，动机是安全加不变量"),
         "mismatch": ("57k lines of C++ ported by a volunteer project over about two years, against roughly "
                      "535,496 lines of Zig in about 11 days of agent work — the schedule regimes are not "
                      "comparable",
                      "那边是志愿者项目用大约两年迁移 57k 行 C++，这边是约 535,496 行 Zig 在约 11 天的 agent "
                      "工作里完成——两种进度体制不可比"),
         "regime": "first-party maintainer account, no benchmark table", "source_label": "first-party · project blog",
         "url": "https://fishshell.com/blog/rustport/"},
        {"name": "Google · Android memory-safety program", "outcome": "INCREMENTAL",
         "body": ("Memory safety's share of Android vulnerabilities fell from 76% to below 20%. No mass "
                  "rewrite. New code went into safe languages and the old C/C++ was left to decay. Rust "
                  "against C/C++ runs roughly 0.2 against 1,000 vulnerabilities per million lines, with about "
                  "4% of Rust lines reported as unsafe.",
                  "Android 漏洞中内存安全类的占比从 76% 降到 20% 以下。没有做大规模重写。"
                  "新代码用安全语言写，旧的 C/C++ 留着自然衰减。每百万行漏洞数上，Rust 对 C/C++ 约为 0.2 对 1,000，"
                  "其中约 4% 的 Rust 行被报告为 unsafe。"),
         "match": ("the same defect class, and the only large published post-migration measurement of it — the "
                   "measurement this port still lacks",
                   "同一类缺陷，而且是唯一一份大规模、公开的迁移后测量——正是这次迁移还缺的那一份"),
         "mismatch": ("an operating system and a multi-year programme; the vulnerability comparison is "
                      "C/C++-relative, and Android's ~4% is a share of lines while the figure measured here is "
                      "opening-block count per line, so it is directional only",
                      "那边是操作系统和一个跨年项目；漏洞对比是相对 C/C++ 的，而且 Android 的约 4% 是行占比，"
                      "这里测的是每行的起始块数，所以只能看方向"),
         "regime": "2019–2025 vulnerability share", "source_label": "first-party · vendor security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
        {"name": "AWS · S3 ShardStore", "outcome": "VERIFIED",
         "body": ("A Rust rewrite of a storage node. Its correctness claim arrived with roughly nine months of "
                  "lightweight formal-methods work: executable reference models, property tests, Loom, Crux. "
                  "That work caught 16 issues before production. The rewrite alone would not have found them.",
                  "一个存储节点的 Rust 重写。它的正确性主张背后是大约九个月的轻量形式化方法工作："
                  "可执行参考模型、property test、Loom、Crux。这些工作在上生产前抓到了 16 个问题。"
                  "光靠重写本身找不出来。"),
         "match": ("what substantiating a correctness claim for a Rust rewrite actually costs, which is the "
                   "counterweight to an unmeasured safety outcome",
                   "给一次 Rust 重写的正确性主张做实证究竟要付多少代价——这正是「安全结果未测量」的对照"),
         "mismatch": ("more than 40K lines and one storage-node type rather than a whole language runtime, and "
                      "no schedule comparable to an 11-day port",
                      "那边是 40K 行以上、一种存储节点类型，不是整个语言运行时；进度上也没有能和 11 天迁移"
                      "相比的对象"),
         "regime": "SOSP'21 paper", "source_label": "peer-reviewed venue · first-party authors",
         "url": "https://www.cs.utexas.edu/~bornholt/papers/shardstore-sosp21.pdf"},
        {"name": "uutils coreutils", "outcome": "SHIPPED WITH REGRESSIONS",
         "body": ("A GNU C userland reimplemented in Rust, shipped as an Ubuntu 25.10 default, with measured "
                  "regressions. cksum ran up to 17x slower on large files and was later patched. base64 got "
                  "slower, then faster. md5sum behaviour differences broke self-extracting installers.",
                  "把 GNU 的 C 用户态工具集用 Rust 重新实现，作为 Ubuntu 25.10 的默认发布，并测出了回归。"
                  "cksum 在大文件上一度慢到 17x，后来打了补丁。base64 先变慢，再变快。"
                  "md5sum 的行为差异弄坏了自解压安装包。"),
         "match": ("a native-to-Rust replacement at whole-project scope, motivated by resilience rather than "
                   "speed, that shipped with regressions and then fixed them",
                   "同为整项目范围的原生换 Rust，动机是韧性而非速度，带着回归上线，然后把回归修掉"),
         "mismatch": ("hundreds of small independent tools instead of one runtime, and a distribution's "
                      "default choice instead of a project's own release",
                      "那边是几百个互相独立的小工具，不是一个运行时；决定权在发行版的默认选择，"
                      "不在项目自己的发布"),
         "regime": "third-party post-ship benchmarking", "source_label": "third-party · trade press",
         "url": "https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf"},
    ],

    "path": [
        {"title": ("Measure the defect class the port existed to remove", "去测那个迁移为之存在的缺陷类"),
         "body": ("Bun maintainers publish the incidence rate of use-after-free, double-free and leak defects "
                  "for a stated window after the port, printed next to the same-length window before it, with "
                  "release cadence and triage rules held comparable. It passes when the two windows are "
                  "comparable and the direction of the class is stated publicly, whichever way it points. If "
                  "triage labels cannot separate this class from other defect types, publish the method's "
                  "limits instead of a number. Nothing here touches code.",
                  "由 Bun maintainers 公布迁移后某个明确窗口内 use-after-free、double-free、内存泄漏的发生率，"
                  "并把迁移前同等长度窗口的数字并排放上，发布节奏和缺陷分类规则保持可比。"
                  "两个窗口可比、并且公开说明这一类缺陷的走向，无论走向如何，这一步就算过。"
                  "如果分类标签分不开这一类和其他缺陷类型，就公布方法的边界，而不是硬给一个数字。这一步不碰代码。"),
         "owner": "Bun maintainers",
         "cost_range": ("2–4 weeks", "2–4 周"),
         "artifact": "the incidence rate of use-after-free, double-free and leak defects over a stated window after the port, printed next to the same-length window before it, with the release cadence and triage rules held comparable",
         "acceptance": "the two windows are comparable and the direction of the class is stated publicly, whichever way it points",
         "stop": "if triage labels cannot separate this class from other defect types, publish the method's limits instead of a number",
         "rollback": "measurement only; no code changes"},
        {"title": ("Classify the 10,257 unsafe blocks and name their owners",
                   "给 10,257 个 unsafe 块分类，并指定负责人"),
         "body": ("Each subsystem names a Rust owner. Together they split the opening unsafe blocks into four "
                  "buckets: FFI boundary, engine embedding, performance-critical, unclassified. Every cluster "
                  "gets a documented invariant and a safe wrapper. It passes when each cluster has an owner "
                  "and a written invariant, and the unclassified bucket reaches zero. Once encapsulation is "
                  "documented, stop using raw block count as the metric — a wrapped block behind a safe API is "
                  "not the same risk as one whose invariants leak to callers. Documentation and refactoring "
                  "only; no behavioural change.",
                  "每个子系统指定一名 Rust 负责人。他们一起把 unsafe 起始块分成四桶：FFI 边界、引擎嵌入、"
                  "性能关键、未分类。每一簇都要有写下来的不变量和一层 safe 封装。每一簇都有负责人和成文不变量、"
                  "未分类那一桶清零，这一步才算过。封装一旦记录在案，就别再拿原始块数当指标——"
                  "被 safe API 包住的块，和把不变量泄漏给调用方的块，风险不是一回事。只做文档和重构，不改行为。"),
         "owner": "named Rust owners per subsystem",
         "cost_range": ("ongoing", "持续进行"),
         "artifact": "a split of the opening unsafe blocks into FFI boundary, engine embedding, performance-critical and unclassified, with a documented invariant and a safe wrapper for each cluster",
         "acceptance": "every cluster has an owner and a written invariant, and the unclassified bucket reaches zero",
         "stop": "stop treating raw block count as the metric once encapsulation is documented — a wrapped block behind a safe API is not the same risk as one whose invariants leak to callers",
         "rollback": "documentation and refactoring; no behavioural change"},
        {"title": ("Keep the regression channel as the acceptance gate", "把回归通道继续当验收门"),
         "body": ("Release engineering triages regressions on every release after the port and names the "
                  "pinnable pre-port release in the notes. A release passes when each reported regression is "
                  "either fixed or carries a documented fallback version a user can pin. Hold the release if a "
                  "known regression has neither. The rollback is the pin itself.",
                  "release engineering 对迁移后的每个发布做回归分类，并在发布说明里点名可以钉住的迁移前版本。"
                  "每个报出来的回归要么已修，要么有一个用户能钉住的成文回退版本，这个发布才算过。"
                  "已知回归两样都没有，就压住不发。回滚方式就是钉版本本身。"),
         "owner": "release engineering",
         "cost_range": ("per release", "每个发布周期"),
         "artifact": "regression triage for every release after the port, with the pinnable pre-port release named in the notes",
         "acceptance": "each reported regression is either fixed or has a documented fallback version a user can pin",
         "stop": "hold a release if a known regression has neither a fix nor a fallback",
         "rollback": "pin a pre-port release"},
        {"title": ("Do not reuse this port as a performance precedent", "别把这次迁移当性能先例引用"),
         "body": ("Anyone citing this case re-runs the D2 calculation with their own measured kernel share and "
                  "kernel speedup, never Bun's. Their numbers decide whether a performance-motivated migration "
                  "clears their target. When the predicted end-to-end speedup lands below that target, stop "
                  "the performance track — here it is 1.048x against 1.5x. No code was written, so there is "
                  "nothing to undo.",
                  "凡是引用这个案例的人，都要用自己实测的内核占比和内核加速比重跑一遍 D2 计算，不要用 Bun 的。"
                  "性能驱动的迁移能不能达标，由他们自己的数字决定。预测的端到端加速比低于目标，"
                  "就停掉性能这条线——这里是 1.048x 对 1.5x。没有写过代码，也就没有什么要撤销的。"),
         "owner": "anyone citing this case",
         "cost_range": ("1 day per review", "每次评审 1 天"),
         "artifact": "a re-run of the D2 calculation with the citing project's own measured kernel share and kernel speedup, not Bun's",
         "acceptance": "the citing project's own numbers decide whether a performance-motivated migration clears its own target",
         "stop": "stop the performance track when the candidate's predicted end-to-end speedup is below the target, as it is here at 1.048x against 1.5x",
         "rollback": "no code was written"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响面"), "state": "PASS",
         "claim": ("The report claims class reduction by construction only where the code is safe Rust, and "
                   "names both the 10,257 opening unsafe blocks and the C, C++ and TypeScript layers the port "
                   "never touched.",
                   "报告只在代码为 safe Rust 的范围内主张结构性削减，并且点明了 10,257 个 unsafe 起始块，"
                   "以及迁移根本没碰的 C、C++、TypeScript 各层。"),
         "evidence": "D6 records · measured at f91d5c95"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("No performance benefit is credited to Rust: the measured delta is 2.2–4.8% on selected "
                   "first-party benchmarks, and the report states that a performance-motivated version of this "
                   "same migration fails gate 3.",
                   "没有把任何性能收益记在 Rust 头上：厂商自选的 first-party 基准上实测差值是 2.2–4.8%，"
                   "报告也写明同一次迁移若改用性能理由会过不了 gate 3。"),
         "evidence": "D2 · share=1.00, kernel=1.048, target=1.5"},
        {"name": ("Baseline and regime", "基线与测量体制"), "state": "HIT",
         "claim": ("The benchmark figures are vendor-selected first-party runs on the vendor's own workloads, "
                   "and the defect-class motive is a first-party description with no published counts or rates "
                   "on either side of the port.",
                   "基准数字是厂商自选的 first-party 跑分，跑的是厂商自己的负载；缺陷类这个动机也是 first-party "
                   "的描述，迁移前后都没有公布过计数或发生率。"),
         "evidence": "https://bun.com/blog/bun-in-rust"},
        {"name": ("Omitted cost", "被略去的成本"), "state": "HIT",
         "claim": ("The ~$165k figure is API spend; the human review, triage and 19-regression work around it "
                   "is not priced anywhere this report can cite, and a third-party account contested review "
                   "quality at publication.",
                   "约 $165k 只是 API 花费；围绕它的人工评审、缺陷分类和 19 个回归的处理，"
                   "本报告找不到任何可引的计价，而且发布时有第三方报道质疑了评审质量。"),
         "evidence": "D11 · theregister.com, 14 Jul 2026"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The port is in released versions with 19 regressions reported and since fixed, and pinning "
                   "a pre-port release is an available rollback rather than a promised one.",
                   "迁移已经进入发布版本，报出 19 个回归且都已修复；钉住迁移前的版本是一条现成可用的回滚路径，"
                   "不是口头承诺。"),
         "evidence": "G4 · https://bun.com/blog/bun-in-rust"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有预算的反事实方案"), "state": "HIT",
         "claim": ("Nobody priced a funded Zig hardening programme against the port: sanitizer coverage, "
                   "allocator instrumentation, review gates. So 'be more careful in Zig' is an unfunded "
                   "counterfactual rather than a compared option.",
                   "没有人把一套有预算的 Zig 加固方案拿来和迁移比价——sanitizer 覆盖、分配器插桩、评审门禁。"
                   "所以「在 Zig 里更小心一点」是一个没有预算的反事实方案，不是被真正比较过的选项。"),
         "evidence": "D12 · zig-harden retained with WEAK evidence"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying in Zig keeps lifetime management manual, which is precisely the condition that "
                   "produced the documented stream of use-after-free, double-free and leak defects.",
                   "留在 Zig 就意味着生命周期继续手动管理，而这正是产出那条有记录的 use-after-free、"
                   "double-free、内存泄漏缺陷流的条件。"),
         "evidence": "G1 · https://bun.com/blog/bun-in-rust"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("Zig's performance is recorded as parity, not as a deficiency: the port moved selected "
                   "benchmarks by 2.2–4.8%, and the report treats that as evidence against a speed rationale "
                   "rather than against Zig.",
                   "Zig 的性能被记为持平，而不是短板：迁移让自选基准动了 2.2–4.8%，"
                   "报告把这当成反对「速度理由」的证据，不是反对 Zig 的证据。"),
         "evidence": "D2 · https://bun.com/blog/bun-in-rust"},
        {"name": ("Status-quo bias", "现状偏好"), "state": "PASS",
         "claim": ("The report does not defend the incumbent language on familiarity grounds. It grants that "
                   "the class is structural to manual lifetime management and authorizes the migration — the "
                   "only MIGRATE plus APPROVE in this set.",
                   "报告没有拿「熟悉」当理由替原有语言辩护。它承认这一类缺陷是手动生命周期管理的结构性产物，"
                   "并授权了迁移——这是本组案例里唯一一个 MIGRATE 加 APPROVE。"),
         "evidence": "G2 PASS · selected option rust-migrate-complete"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The staying case is not left as an open-ended 'optimize Zig first'. The stop condition is "
                   "attached instead to the migration's own claim: publish the defect-class measurement, or "
                   "the safety outcome stays unverified and robustness stays CONDITIONAL.",
                   "留守方案没有被放成一句开放式的「先优化 Zig」。停止条件挂在迁移自己的主张上：公布缺陷类的"
                   "测量结果，否则安全结果就一直未经验证，robustness 也一直是 CONDITIONAL。"),
         "evidence": "reversible path step 1 · change trigger"},
    ],

    "gaps": [
        (("Post-port incidence of the target defect class", "迁移后目标缺陷类的发生率"),
         ("The entire decision rests on this measurement, and no one has published it. Its absence holds "
          "confidence at MEDIUM and robustness at CONDITIONAL. It does not change the selected scope. It "
          "decides whether anyone can claim the migration worked.",
          "整个决策就压在这项测量上，而没有人公布过。它的缺席把 confidence 钉在 MEDIUM，"
          "把 robustness 钉在 CONDITIONAL。它不改变选定的范围。它决定「这次迁移奏效了」这句话能不能说。")),
        (("Classification and encapsulation of the 10,257 unsafe blocks", "10,257 个 unsafe 块的分类与封装"),
         ("Block count is a coarse proxy for risk. Without a split into FFI boundary, engine embedding and "
          "performance-critical clusters, each with a documented invariant, the residual unsafety of the "
          "selected option stays unquantified.",
          "块数是衡量风险的粗糙代理。不把它们拆成 FFI 边界、引擎嵌入、性能关键几簇，并且每簇配一条成文不变量，"
          "选定方案的残余不安全面就一直没有量化。")),
        (("An independent same-workload benchmark", "一次同负载的独立基准"),
         ("The 2.2–4.8% figures are vendor-selected first-party runs. An independent comparison would firm up "
          "the parity reading in both directions. This is the report's main quantitative performance claim, "
          "and nobody outside the vendor has checked it.",
          "2.2–4.8% 这些数字是厂商自选的 first-party 跑分。一次独立对比可以在两个方向上把「持平」这个判断坐实。"
          "这是报告里主要的量化性能主张，而厂商之外没有人核过它。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; deleted history was not inspected, so the pre-port Zig size is the first-party figure rather than a measurement taken here.",
        "Unsafe surface was counted by pattern across tracked .rs files — opening unsafe blocks, unsafe fn, unsafe impl, unsafe extern — including test and generated code, and the counts do not distinguish an encapsulated block from one whose invariants leak to callers.",
        "The first-party benchmark figures are treated as the best available estimate of the native-to-native delta and used directionally; no independent same-workload measurement of this port exists here.",
        "Line counts across languages are not treated as comparable measures of effort, quality, or complexity in either direction.",
    ],
    "objective": {
        "driver": "safety",
        "requirement": "eliminate the recurring use-after-free, double-free and leak defect class in Bun's runtime implementation without regressing shipped performance or JavaScript-facing behaviour",
        "baseline": "roughly 535,496 lines of Zig whose lifetimes were maintained by discipline rather than by the compiler (https://bun.com/blog/bun-in-rust)",
        "target": "the class unreachable by construction wherever the code is safe, at no worse than performance parity",
    },
    "repository": {
        "path": "https://github.com/oven-sh/bun",
        "commit": "f91d5c95c9e235d65977e6c42446f4f6e7d3ae78",
        "scope": "whole repository; the ported host-runtime layer — Rust at this commit, Zig before it — is the assessed target",
        "sampling": "shallow clone; 19,034 tracked files enumerated; per-extension line and file counts across tracked .rs, .zig, .c, .cpp, .h and .ts files, plus pattern counts of unsafe forms in .rs; no build, test, benchmark or network call was run; deleted history not inspected, so the pre-port Zig size comes from the first-party account rather than from this clone",
    },
    "user_supplied_facts": [],

    "method_title": (
        "oven-sh/bun at f91d5c95 · static read-only analysis · why-not-rust method 2.0",
        "oven-sh/bun 于 f91d5c95 · 只读静态分析 · why-not-rust method 2.0",
    ),
    "method_body": (
        "Repository: github.com/oven-sh/bun at commit f91d5c95, shallow clone, 19,034 tracked files. Scope: "
        "the whole repository, with the ported host-runtime layer as the assessed target. Sampling: 1,008,327 "
        "lines of Rust across 1,496 files, 1,005,761 of them under src/; zero .zig files and no build.zig; "
        "Cargo.toml present; 311,915 lines of C across 122 files, 290,842 of C++ across 605 files, 105,026 of "
        "headers across 808 files, and 825,147 of TypeScript across 3,073 files. Unsafe surface was counted by "
        "pattern across tracked .rs files: 10,257 opening unsafe blocks, 1,235 unsafe fn, 399 unsafe impl, 966 "
        "unsafe extern, with 751 of 1,496 files (50.2%) containing at least one of those four forms. A bare "
        "substring search returns 786 instead; it also matches identifiers such as unsafe_code and prose in "
        "comments, so the narrower four-form count is the one reported. Derived: roughly one opening unsafe "
        "block per 98 lines of Rust (1,008,327 / 10,257 = 98.3). No build, test, benchmark or network call was "
        "run against the project, and deleted history was not inspected, so the roughly 535,496-line pre-port "
        "Zig figure is the first-party one from https://bun.com/blog/bun-in-rust rather than a measurement "
        "taken here. Objective: eliminate the recurring use-after-free, double-free and leak class without "
        "regressing shipped performance or JavaScript-facing behaviour. User-supplied facts: none. Amdahl "
        "inputs, in baseline-time units: share=1.00 because the whole program is the candidate kernel, kernel "
        "speedup=1.048 from the best selected first-party figure (Bun.serve +4.8%), boundary=0, target=1.5 → "
        "end-to-end 1.048x, infinite-kernel ceiling unbounded, target physically possible and NOT met by the "
        "candidate. Read that pair carefully. With the whole program as the kernel there is no Amdahl wall at "
        "all, so the wall is empirical: the measured native-to-native delta of 4.8% at best. On the speed axis "
        "this same migration fails gate 3; on the safety axis it passes. The axis decides it, not the scope. "
        "Why the selected option is the smallest sufficient step: the defect class is a property of manual "
        "lifetime management throughout the runtime rather than of one component behind an interface. No "
        "extraction reaches it. A module-by-module port would pay a Zig-Rust boundary for years while "
        "leaving the requirement unmet in the unported remainder. Evidence gaps and their effect: no post-port "
        "measurement of the target defect class has been published, which holds confidence at MEDIUM and "
        "robustness at CONDITIONAL; the 10,257 opening unsafe blocks are unclassified, so residual unsafety is "
        "unquantified; and the benchmark figures are vendor-selected. A third-party account contested the "
        "port's production-readiness at publication "
        "(https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743); "
        "it is recorded as a contested-quality signal in neutral terms, with no claim about anyone's motives. "
        "Line counts across languages are not treated as comparable measures of effort or quality: 1,008,327 "
        "lines of Rust replacing roughly 535,496 of Zig is a ratio, not a verdict. The framework compares "
        "explicit options through four non-compensatory gates and is a structured decision protocol, not a "
        "statistical predictor.",

        "仓库：github.com/oven-sh/bun，commit f91d5c95，shallow clone，19,034 个受管理文件。"
        "范围：整个仓库，被评估的目标是已迁移的宿主运行时层。采样：1,008,327 行 Rust，分布在 1,496 个文件中，"
        "其中 1,005,761 行在 src/ 下；0 个 .zig 文件，没有 build.zig；Cargo.toml 存在；311,915 行 C 分布在 "
        "122 个文件，290,842 行 C++ 分布在 605 个文件，105,026 行头文件分布在 808 个文件，825,147 行 "
        "TypeScript 分布在 3,073 个文件。unsafe 面通过模式匹配在受管理的 .rs 文件上统计：10,257 个 unsafe "
        "起始块、1,235 个 unsafe fn、399 个 unsafe impl、966 个 unsafe extern，1,496 个文件里有 751 个"
        "（50.2%）至少含这四种形式之一。直接做子串搜索会得到 786，那个数字还会命中 unsafe_code 之类的标识符"
        "和注释里的文字，所以报告采用范围更窄的四形式计数。推导：约每 98 行 Rust 一个 unsafe 起始块"
        "（1,008,327 / 10,257 = 98.3）。没有对项目跑过任何 build、test、benchmark 或网络调用，"
        "也没有查被删除的历史，所以迁移前约 535,496 行 Zig 这个数字来自 first-party 的 "
        "https://bun.com/blog/bun-in-rust，不是在这里测出来的。目标：消除反复出现的 use-after-free、"
        "double-free、内存泄漏这一类缺陷，同时不让已发布的性能和面向 JavaScript 的行为退化。"
        "用户提供的事实：无。Amdahl 输入，单位为基线时间：share=1.00，因为候选内核就是整个程序；"
        "kernel speedup=1.048，取自厂商自选数字里最好的一个（Bun.serve +4.8%）；boundary=0；target=1.5 → "
        "端到端 1.048x，无限内核上限 unbounded，目标物理可达，但候选方案 NOT met。这一对要一起读。"
        "内核取整个程序时根本没有 Amdahl 墙，所以墙是经验性的：实测的原生到原生差值，最好也就 4.8%。"
        "走速度这条轴，同一次迁移过不了 gate 3；走安全那条轴，它过。决定结果的是轴，不是范围。"
        "为什么选定方案是最小充分步骤：这一类缺陷是手动生命周期管理贯穿整个运行时的产物，"
        "不是接口后面某个组件的产物。抽取够不着它。而逐模块迁移要为 Zig-Rust 边界付上好几年，"
        "同时让需求在尚未迁移的部分里一直落空。证据缺口及其影响：迁移后目标缺陷类的测量没有公布过，"
        "这把 confidence 钉在 MEDIUM，把 robustness 钉在 CONDITIONAL；10,257 个 unsafe 起始块尚未分类，"
        "残余不安全面没有量化；基准数字由厂商自选。发布时有第三方报道质疑了这次迁移的生产就绪度"
        "（https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743），"
        "这里以中性措辞记为质量存争议的信号，不对任何人的动机作判断。跨语言的行数不被当作可比的工作量或"
        "质量度量：1,008,327 行 Rust 替掉约 535,496 行 Zig，这是一个比例，不是一个结论。"
        "本框架把明确列出的方案放进四道非补偿性的门里比较，它是一套结构化决策协议，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit f91d5c95 · no build, benchmark or network call",
        "公开仓库 · 在 commit f91d5c95 上做静态分析 · 未运行 build、benchmark 或网络调用",
    ),
}
