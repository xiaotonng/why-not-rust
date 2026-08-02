"""uutils/coreutils — a real Rust userland that shipped as a distribution default, regressions and all.

Every repository fact below was measured read-only on the shallow clone named in
`repository`. The incumbent GNU C implementation was not cloned, and no claim is made
about its internals. External numbers keep their URL and their regime.
"""

CASE = {
    "slug": "coreutils",
    "project_name": "uutils/coreutils",
    "project_desc": (
        "Rust · GNU coreutils reimplementation · 251,003 lines of Rust across 631 files · "
        "108 utility binaries · shipped as the Ubuntu 25.10 default",
        "Rust · GNU coreutils 重写 · 251,003 行 Rust，631 个文件 · 108 个工具二进制 · "
        "已作为 Ubuntu 25.10 默认发布",
    ),
    "date": "2026-08-01",
    "archetype": (
        "cli-quick · 108 independent single-purpose binaries behind a 40-year behavioural contract",
        "cli-quick · 108 个独立的单一用途二进制，背后是 40 年的行为契约",
    ),

    "scope_word": "PARTIAL",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "per-utility-rollout",
    "scope_chip": (
        "one utility at a time, each behind its own acceptance gate",
        "一次换一个工具，每个都要过自己的验收门",
    ),
    "scope_sub": (
        "replace one utility at a time, not the userland at once",
        "一次替换一个工具，不要整套 userland 一起翻",
    ),

    "why": (
        "The safety case holds and someone else already wrote the code: 251,003 lines of Rust across "
        "109 utilities, with the whole residual unsafe surface enumerable as 275 `unsafe {` blocks and "
        "4 `unsafe fn`. G1, G2 and G3 pass. G4 fails at the larger scope — the simultaneous "
        "whole-userland default flip, which nobody gated on per-utility behavioural acceptance. Both "
        "things that broke in the field are the kind a per-utility gate catches: cksum up to 17× slower "
        "than GNU on large files, and md5sum behaviour differences that broke Makeself self-extracting "
        "installers. The instrument was in the tree the whole time. It just was not blocking.",

        "安全性成立，而且代码别人已经写完了：251,003 行 Rust，覆盖 109 个工具，残留的 unsafe 面可以数清——"
        "275 个 `unsafe {` 块加 4 个 `unsafe fn`。G1、G2、G3 通过。G4 在更大的范围上失败：整套 userland 默认值"
        "同时翻转，翻转前没有把逐工具的行为验收设成阻塞条件。现场炸出来的两件事，都是逐工具验收门能拦下的："
        "cksum 处理大文件时比 GNU 慢至多 17×，md5sum 的行为差异弄坏了 Makeself 自解压安装包。"
        "验收工具一直就在仓库里。只是没设成阻塞。",
    ),
    "trigger": (
        "Conditional. The authorization holds only while every utility carries its own acceptance "
        "record. Re-open it if a utility reaches a default flip without a byte-level output diff and a "
        "throughput comparison against the incumbent. Also re-open it if the promotion order stops "
        "being derived from exposure, or if the GNU pass count stays outside the repository, where a "
        "distributor cannot read parity per release.",

        "有条件。只有每个工具都带着自己的验收记录，这份授权才成立。某个工具没有字节级输出 diff、也没有与现任"
        "实现的吞吐对比就翻默认值——重新评估。晋级顺序不再按暴露面推导，或者 GNU 通过数继续留在仓库之外、"
        "发行方按版本读不到 parity——同样重新评估。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS",
         "short": ("Requirement", "需求"),
         "hero_evidence": ("A manually managed C userland that every script and installer invokes.",
                           "一套人工维护的 C userland，每个脚本、每个安装程序都要调它。"),
         "name": "requirement",
         "evidence": "The incumbent implementation of the default command-line userland is manually managed C, and the distributor's stated motive for changing it is resilience and safety ahead of the LTS rather than speed (why-not-rust case library · uutils coreutils entry · https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf). The same release replaced sudo on the same rationale, with attack-surface reduction stated as the whole objective (https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/)."},
        {"id": "G2", "state": "PASS",
         "short": ("Causality", "因果"),
         "hero_evidence": ("275 unsafe blocks in 251,003 lines — the safety delta is countable.",
                           "251,003 行里 275 个 unsafe 块——安全收益是可以数出来的。"),
         "name": "rust-specific causality",
         "evidence": "The safety delta is the language property and nothing else: 275 `unsafe {` blocks and 4 `unsafe fn` across 631 .rs files and 251,003 lines are the whole surface on which a memory-unsafety defect remains possible, and that surface is enumerable and reviewable. No algorithm, protocol or architecture change is required to obtain it. Android reports roughly 4% of its Rust lines as unsafe (https://blog.google/security/rust-in-android-move-fast-fix-things/); that is a line share and 275 is a block count, so the two are not the same metric, but both describe a small audited subset rather than a whole program."},
        {"id": "G3", "state": "PASS",
         "short": ("Economics", "经济性"),
         "hero_evidence": ("The reimplementation is already written, tested and upstream-maintained.",
                           "重写已经完成，有测试，上游在维护。"),
         "name": "economics and smallest sufficient option",
         "evidence": "An adopter pays for none of the rewrite: 251,003 lines of Rust, 109 utility directories under src/uu/, 34,778 lines across the 82 tracked paths of src/uucore/ and 174,220 lines of tests across 821 tracked paths already exist at this commit. The remaining cost is acceptance testing, which divides by utility and runs in parallel. The cheaper option — keeping the C implementation everywhere — does not meet the safety requirement, and the larger option buys no additional per-utility safety while correlating 108 independent risks into one release event."},
        {"id": "G4", "state": "PASS",
         "short": ("Delivery", "交付"),
         "hero_evidence": ("Per-utility rollback plus an in-tree GNU harness; the whole-userland flip is "
                           "the scope that fails.",
                           "逐工具回滚，加上仓库自带的 GNU 测试套件；失败的是整套 userland 一起翻的那个范围。"),
         "name": "delivery and reversibility",
         "evidence": "PASS for the per-utility scope: each of the 108 shipping utilities under src/uu/ builds its own binary with its own behavioural contract, so promotion and rollback are per utility, and the acceptance instrument is already in the tree — GNUmakefile with .github/workflows/GnuTests.yml and .github/workflows/GnuComment.yml, alongside 174,220 lines of tests. The scope that fails this gate is the simultaneous whole-userland default flip: per-utility behavioural acceptance was not made blocking before the flip, so the field found what the gate would have found — cksum up to 17× slower than GNU on large files (later patched), base64 slower before it was made faster, and md5sum behaviour differences that broke Makeself self-extracting installers (https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf)."},
    ],

    "tiles": [
        (("Rust already written", "Rust 已经写好"), "251,003", ("lines", "行"),
         ("631 .rs files at 0c8a3c7 · the adopter funds none of it",
          "0c8a3c7 上 631 个 .rs 文件 · 采用方一分钱不出")),
        (("Independent acceptance gates", "独立验收门"), "109", ("utilities", "个工具"),
         ("directories under src/uu/ · one binary, one contract each",
          "src/uu/ 下的目录 · 一个二进制，一份契约")),
        (("Residual unsafe surface", "残留 unsafe 面"), "275", ("blocks", "个块"),
         ("`unsafe {` across *.rs · plus 4 `unsafe fn`",
          "*.rs 中的 `unsafe {` · 另有 4 个 `unsafe fn`")),
        (("Acceptance material in tree", "仓库自带的验收材料"), "174,220", ("lines", "行"),
         ("tests/ · 821 tracked paths · GNUmakefile + GnuTests.yml",
          "tests/ · 821 个受控路径 · GNUmakefile + GnuTests.yml")),
        (("GNU parity at announcement", "公告时的 GNU parity"), "500 / 600", ("tests", "项测试"),
         ("case library figure, announcement-time, not current",
          "案例库数据，公告时点，不是当前值")),
        (("Worst field regression", "现场最严重的回退"), "17", ("× slower", "× 慢"),
         ("cksum on large files vs GNU, later patched · phoronix.com",
          "大文件上的 cksum 对比 GNU，后来已修 · phoronix.com")),
    ],

    "options_sub": (
        "Same objective for every option: remove the memory-unsafety class from the default "
        "command-line userland without changing the observable behaviour that scripts, Makefiles and "
        "installers depend on.",

        "每个方案的目标一致：把内存不安全这一类缺陷从默认命令行 userland 中移除，同时不改变脚本、"
        "Makefile 和安装程序依赖的可观测行为。",
    ),
    "options": [
        {"id": "gnu-stay",
         "name": ("Keep the GNU C userland and harden it", "保留 GNU C userland，继续加固"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("no class removal; incidence work only", "不消除类；只做个案修补"),
         "one_time_cost": "none new", "recurring_cost": "review, fuzzing and patch load on C",
         "cost_cell": ("none new; ongoing C patch load", "没有新增；C 的补丁负担持续"),
         "time_to_value": ("already in place", "已经就位"),
         "compatibility": "native — 40 years of accreted behaviour",
         "compat_cell": ("native · nothing to roll back", "原生 · 没有东西需要回滚"),
         "reversibility": "n/a", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the correct default for every utility that has not passed its gate",
                  "保留 · 对每个尚未过门的工具，这就是正确的默认值"),
         "reason": "It is the right state for 108 minus N utilities at any moment and the only option with zero behavioural risk, but it leaves the memory-unsafety class reachable in code every script and installer invokes."},
        {"id": "per-utility-rollout",
         "name": ("Promote utilities one at a time, gated", "逐个工具晋级，每个都设门"),
         "implementation": "rust",
         "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("class eliminated in each utility that passes its gate",
                              "每过一道门，那个工具里的类就消失"),
         "one_time_cost": "acceptance testing per utility", "recurring_cost": "both implementations packaged during the transition",
         "cost_cell": ("per-utility acceptance; dual packaging", "逐工具验收；双份打包"),
         "time_to_value": ("one utility", "一个工具"),
         "compatibility": "byte-level output parity per utility",
         "compat_cell": ("per-utility default · switch one back", "逐工具默认值 · 单个切回"),
         "reversibility": "per-utility default switch", "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the gate the field regressions would have failed",
                  "推荐 · 现场那几个回退过不了的正是这道门"),
         "reason": "Smallest scope that removes the class where it matters while keeping 108 behavioural contracts as 108 separate decisions, with the acceptance instrument already in the repository."},
        {"id": "userland-flip",
         "name": ("Flip the whole userland default at once", "一次性翻转整套 userland 默认值"),
         "implementation": "rust",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("the same per-utility class removal, delivered as one correlated event",
                              "逐工具消除的类一模一样，只是打包成一次相关联的事件交付"),
         "one_time_cost": "one packaging change", "recurring_cost": "post-hoc regression triage across 109 contracts",
         "cost_cell": ("cheap to ship; expensive to triage", "发布便宜；排查昂贵"),
         "time_to_value": ("one release", "一个发行版本"),
         "compatibility": "108 behavioural contracts at once",
         "compat_cell": ("whole userland · rollback is a release", "整套 userland · 回滚等于再发一版"),
         "reversibility": "poor — one switch for 108 utilities", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · fails G4: acceptance was not gated per utility before the flip",
                  "排除 · G4 不过：翻转前没有按工具设验收门"),
         "reason": "It shipped, and the field produced exactly the regressions a per-utility gate exists for: cksum up to 17× slower on large files, base64 slower before it was faster, and md5sum behaviour differences that broke Makeself self-extracting installers. The safety benefit is no larger than the sum of the per-utility promotions; only the risk is."},
        {"id": "gnu-plus-selected",
         "name": ("Adopt a short list of utilities only", "只采用一份短名单里的工具"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed in the few utilities chosen", "只在选中的少数工具里消除该类"),
         "one_time_cost": "acceptance for a frozen short list", "recurring_cost": "dual packaging for those utilities",
         "cost_cell": ("acceptance for a short list", "只为短名单做验收"),
         "time_to_value": ("one release", "一个发行版本"),
         "compatibility": "same parity requirement, smaller surface",
         "compat_cell": ("small surface · easy rollback", "面小 · 回滚容易"),
         "reversibility": "trivial", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the floor of the selected option, and its fallback",
                  "保留 · 推荐方案的下限，也是它的退路"),
         "reason": "Same mechanism as the selected option with the promotion list frozen at the best exposure-to-risk candidates; correct if gates keep failing, but it ends the programme early for utilities that would have passed."},
        {"id": "dual-ship-optin",
         "name": ("Ship both; GNU stays the default", "两套都发；GNU 仍是默认"),
         "implementation": "hybrid",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed only for users who opt in", "只有主动切过去的用户才消除该类"),
         "one_time_cost": "packaging both implementations", "recurring_cost": "two userlands maintained in the archive indefinitely",
         "cost_cell": ("package both; no default change", "打两份包；默认值不动"),
         "time_to_value": ("one release", "一个发行版本"),
         "compatibility": "no default behaviour change",
         "compat_cell": ("opt-in only · nothing to roll back", "仅选择性启用 · 没有东西需要回滚"),
         "reversibility": "user-side", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · phase one of the selected option, and how the gate gets its evidence",
                  "保留 · 推荐方案的第一阶段，也是这道门取证的方式"),
         "reason": "It generates the behavioural evidence the flip lacked at no fleet-wide risk; on its own it delivers no default-path safety benefit, so it is a phase rather than an end state."},
        {"id": "parity-first-defer",
         "name": ("Defer everything until full GNU parity", "等 GNU 完全 parity 之后再说"),
         "implementation": "rust",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("no class removal until the last test passes", "最后一项测试通过之前，什么也不消除"),
         "one_time_cost": "upstream parity work of unknown size", "recurring_cost": "the class stays reachable meanwhile",
         "cost_cell": ("unbounded wait; class stays reachable", "无限期等待；该类始终可达"),
         "time_to_value": ("unknown", "未知"),
         "compatibility": "maximal margin",
         "compat_cell": ("maximal margin · nothing ships", "余量最大 · 什么都发不出去"),
         "reversibility": "n/a", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · the flip's scope error, inverted", "排除 · 把翻转的范围错误反过来犯一次"),
         "reason": "It couples 108 independent decisions into a single no, exactly as the flip coupled them into a single yes, and 'parity' has no in-repository reading: README.md:355 links the pass count out to external coverage docs, so the condition cannot be evaluated from the tree at all."},
    ],

    "lenses_sub": (
        "States are option-scoped evidence, not additive points. Every repository claim was measured on "
        "the Rust candidate at the commit named in the methodology. The incumbent GNU C implementation "
        "was not cloned, and no claim is made about its internals.",

        "每个状态都是绑定到具体方案的证据，不是可以相加的分数。仓库层面的每一项数据，都测自方法一节列出的"
        "那个 commit 上的 Rust 候选实现。现任的 GNU C 实现没有克隆，本报告不对它的内部作任何断言。",
    ),
    "na_note": (
        "N/A lenses: D2 end-to-end reach, D3 tail behaviour and D4 fleet footprint carry no part of this "
        "objective. The stated driver is resilience and safety, not latency or density. Neither "
        "implementation has a managed runtime. No collector either. Inventing a time share from line "
        "counts to fill D2 would be a method error.",

        "N/A 的维度：D2 端到端占比、D3 尾部行为、D4 机队占用，都不承担这个目标的任何部分。发行方给出的"
        "驱动力是韧性与安全，不是延迟或密度。两边都没有托管运行时。也都没有 GC。从代码行数里编一个时间占比"
        "来填 D2，属于方法错误。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["per-utility-rollout", "userland-flip", "gnu-plus-selected", "dual-ship-optin"],
         "claim": ("The requirement comes from the distributor: resilience and safety for the default "
                   "userland ahead of the LTS. The code that has to change is the manually managed C "
                   "implementation of utilities that every script, Makefile and installer invokes.",
                   "需求由发行方提出：在 LTS 之前，让默认 userland 更有韧性、更安全。要改的代码，是那套"
                   "人工维护的 C 实现——每个脚本、每个 Makefile、每个安装程序都在调用它。"),
         "source": "why-not-rust case library · uutils coreutils entry · https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf",
         "regime": "distributor rationale for the Ubuntu 25.10 default, 2025",
         "caveat": "The objective is stated by the distributor, not derived from a published root-cause classification of coreutils advisories; no such classification was measured here, so the size of the class being removed is argued structurally rather than counted."},
        {"id": "D2", "name": ("End-to-end reach", "端到端占比"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Nobody asserts a performance requirement here. The stated driver is resilience and "
                   "safety, not latency. There is no end-to-end time share to compute, and deriving one "
                   "from line counts would be a method error.",
                   "这里没有人提出性能要求。发行方给出的驱动力是韧性与安全，不是延迟。没有端到端时间占比"
                   "可算，从代码行数里推一个出来属于方法错误。"),
         "source": "objective is safety and resilience, not latency", "regime": "n/a",
         "caveat": "The measured throughput regression is not an Amdahl question; it is recorded at D10 as an acceptance failure against a 40-year-tuned baseline."},
        {"id": "D3", "name": ("Tail & runtime", "尾部与运行时"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Neither implementation carries a managed runtime or a collector, so there is no "
                   "runtime mechanism in any tail to remove.",
                   "两边都不带托管运行时，也都不带 GC，尾部里没有可以摘掉的运行时机制。"),
         "source": "ahead-of-time compiled native code on both sides", "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("These utilities are short-lived processes inside someone else's workload. The "
                   "decision changes no fleet density, no instance count, no steady-state footprint.",
                   "这些工具是别人负载里的短命进程。这个决策不改变机队密度，不改变实例数，也不改变稳态占用。"),
         "source": "per-invocation process model", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "UNKNOWN · per-utility-rollout, userland-flip", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["per-utility-rollout", "userland-flip"],
         "claim": ("Coreutils is invoked once per command, so per-invocation cost is the shape that "
                   "matters. Neither implementation was decomposed here into process start, "
                   "initialization, I/O and useful work.",
                   "coreutils 每条命令启动一次，因此单次调用的开销才是要看的形态。这里没有对任何一边做过"
                   "进程启动、初始化、I/O 与有效工作的拆分测量。"),
         "source": "no per-utility invocation profile measured", "regime": "n/a — the measurement is absent",
         "caveat": "Recorded UNKNOWN rather than assumed at parity. The safety objective does not need this number; a default flip does, because the regression the field actually found was a per-invocation cost.",
         "change_trigger": "A per-utility startup and throughput comparison against the incumbent, on the distributor's own workloads, published as part of the promotion record."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["per-utility-rollout", "userland-flip", "gnu-plus-selected", "dual-ship-optin"],
         "claim": ("You can enumerate the entire surface on which a memory-unsafety defect remains "
                   "possible: 275 `unsafe {` blocks and 4 `unsafe fn` across 631 .rs files and 251,003 "
                   "lines. 34,778 of those lines sit in the shared src/uucore/ layer, where the syscall "
                   "work concentrates.",
                   "还可能出现内存不安全缺陷的整个面，可以逐个列出来：631 个 .rs 文件、251,003 行里，"
                   "275 个 `unsafe {` 块和 4 个 `unsafe fn`。其中 34,778 行在共享层 src/uucore/，"
                   "系统调用的活儿集中在那里。"),
         "source": "`unsafe {` 275 · `unsafe fn` 4 · *.rs at 0c8a3c7 · src/uucore/ 34,778 lines across 82 files",
         "regime": "static measurement of the candidate at this commit",
         "caveat": "A block count is not a line share, so this is not the same metric as Android's reported ~4% of Rust lines being unsafe (https://blog.google/security/rust-in-android-move-fast-fix-things/). Correctness is also a separate axis from memory safety, and it is the axis on which this port measurably regressed."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("These are single-purpose stream and filesystem transformations, invoked one command "
                   "at a time. Neither language blocks data-parallel work. The invariants at stake here "
                   "are behavioural, not concurrent.",
                   "这些是单一用途的流与文件系统变换，一次一条命令。两种语言都没有挡住数据并行。这里真正要"
                   "守的不变量是行为上的，不是并发上的。"),
         "source": "per-invocation single-process utility model", "regime": "invocation model of the utility set",
         "caveat": "Individual utilities parallelise internally in both implementations; nothing about that choice is language-determined at this scope."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "SUPPORTS · per-utility-rollout, gnu-plus-selected, dual-ship-optin", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["per-utility-rollout", "gnu-plus-selected", "dual-ship-optin"],
         "claim": ("The unit of distribution is one utility. There are 109 directories under src/uu/, of "
                   "which 108 declare a [[bin]] target. So the packaging system can carry a mixed "
                   "userland and roll one utility back without touching the other 107.",
                   "分发的单位就是一个工具。src/uu/ 下有 109 个目录，其中 108 个声明了 [[bin]] 目标。"
                   "打包系统因此可以承载一套混合 userland，回滚某一个工具而不动其余 107 个。"),
         "source": "src/uu/ · 109 utility directories · 118,595 lines across 855 tracked files",
         "regime": "static structure of the candidate at this commit",
         "caveat": "Shipping the set as a single package converts 108 independent units into one release event. That is a packaging choice rather than a property of the code — and it is the choice that fails G4."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · per-utility-rollout, gnu-plus-selected", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["per-utility-rollout", "gnu-plus-selected"],
         "claim": ("The Rust implementation already exists. Upstream maintains it. It covers 108 "
                   "utilities, carries 174,220 lines of tests across 821 tracked paths, and has already "
                   "shipped as a distribution default. No adopter has to write it or fund it.",
                   "Rust 实现已经存在。上游在维护。它覆盖 108 个工具，带着 821 个受控路径、174,220 行测试，"
                   "并且已经作为某个发行版的默认值发布过。采用方既不用写，也不用出钱。"),
         "source": "251,003 lines of .rs · tests/ 174,220 lines across 821 tracked paths · Ubuntu 25.10 default",
         "regime": "shipped upstream inventory at this commit",
         "caveat": "Existence is not parity: roughly 500 of 600 GNU tests passed at announcement (why-not-rust case library · uutils coreutils entry), and the repository states no current pass count — README.md:355 is the 'GNU test suite compatibility' heading and links the coverage data out to external docs and an evolution chart."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · userland-flip", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["userland-flip"],
         "claim": ("The compatibility contract is 40 years of accreted observable behaviour, not an API: "
                   "exit codes, byte-level output, and localized message text across 212 .ftl files. It "
                   "broke in the field. cksum ran up to 17× slower than GNU on large files, later "
                   "patched. base64 was slower before it was made faster. And md5sum behaviour "
                   "differences broke Makeself self-extracting installers.",
                   "兼容契约是 40 年累积下来的可观测行为，不是一套 API：退出码、字节级输出，以及 212 个 "
                   ".ftl 文件里的本地化消息文本。它在现场断了。cksum 处理大文件时比 GNU 慢至多 17×，后来"
                   "打了补丁。base64 也曾更慢，之后才被优化回来。md5sum 的行为差异弄坏了 Makeself 自解压"
                   "安装包。"),
         "source": "https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf · 212 .ftl localization files at 0c8a3c7",
         "regime": "Ubuntu 25.10 as shipped; press coverage of the first-party patches",
         "caveat": "Two of the three were fixed after release, which is the point rather than a mitigation: each was discoverable before release, per utility, with the harness already in the tree."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "SUPPORTS · per-utility-rollout, gnu-plus-selected", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["per-utility-rollout", "gnu-plus-selected"],
         "claim": ("The reimplementation cost is sunk upstream, and what remains for the adopter divides "
                   "by utility. The GNU compatibility harness ships inside the repository: GNUmakefile, "
                   ".github/workflows/GnuTests.yml and .github/workflows/GnuComment.yml. Making "
                   "acceptance blocking is a CI configuration change. Nobody has to build an instrument.",
                   "重写成本已经在上游沉没，采用方剩下的成本按工具切分。GNU 兼容测试套件就在仓库里："
                   "GNUmakefile、.github/workflows/GnuTests.yml、.github/workflows/GnuComment.yml。"
                   "把验收设成阻塞，只是改一处 CI 配置。没人需要造新工具。"),
         "source": "GNUmakefile · .github/workflows/GnuTests.yml · .github/workflows/GnuComment.yml",
         "regime": "harness present in the candidate at this commit",
         "caveat": "The adopter still inherits a second upstream's fix latency: the cksum and base64 fixes both landed after the default flip rather than before it (https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf)."},
        {"id": "D12", "name": ("Counterfactual", "反事实"),
         "label": "NEUTRAL · gnu-stay vs per-utility-rollout", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["gnu-stay", "per-utility-rollout"],
         "claim": ("The in-stack alternative and the Rust option are not competing programmes. The C "
                   "implementation stays installed. It remains the default for every utility that has "
                   "not passed its gate. Maintaining and hardening it is a precondition of the rollout, "
                   "not an alternative to it.",
                   "栈内的替代方案和 Rust 方案不是互相竞争的两个项目。C 实现继续装在系统里。对每一个尚未"
                   "过门的工具，它继续是默认。继续维护和加固它，是这次推进的前置条件，不是它的替代品。"),
         "source": "selected option keeps the incumbent as the per-utility default",
         "regime": "current engineering practice on both sides",
         "caveat": "GNU coreutils was not cloned or measured for this report, so the residual-risk side of the comparison is unquantified. What is measured is only that a rewrite inherits neither the incumbent's tuning nor its accreted observable behaviour."},
    ],

    "findings": [
        ("rust",
         ("275 unsafe blocks is a number anyone can check", "275 个 unsafe 块，是谁都能自己数的数字"),
         ("The residual unsafe surface of this userland is 275 `unsafe {` blocks and 4 `unsafe fn` "
          "across 631 .rs files and 251,003 lines. That is the safety payoff. You can re-run the count "
          "at a commit. A claim that a language is safe cannot be checked at all. Android's programme "
          "reports roughly 4% of its Rust lines as unsafe; that is a line share against a block count, "
          "so the metrics differ. Both still describe a small reviewable subset instead of a whole "
          "program.",
          "这套 userland 残留的 unsafe 面，是 631 个 .rs 文件、251,003 行里的 275 个 `unsafe {` 块和 "
          "4 个 `unsafe fn`。这就是安全收益。这个数在任意 commit 上都能重新跑一遍。「这门语言是安全的」"
          "这种说法根本没法核对。Android 的项目报告称其 Rust 代码约 4% 的行是 unsafe；那是行占比，这里是块"
          "计数，两个指标不一样。但两者描述的都是一小块可评审的子集，而不是整个程序。"),
         "`unsafe {` 275 · `unsafe fn` 4 · *.rs at 0c8a3c7 · blog.google Rust-in-Android"),
        ("current",
         ("What failed in the field was behaviour, not memory safety", "现场出事的是行为，不是内存安全"),
         ("Three documented regressions shipped with the default. cksum ran up to 17× slower than GNU "
          "on large files, later patched. base64 was slower before it was made faster. md5sum "
          "behaviour differences broke Makeself self-extracting installers. None of the three is a "
          "memory-safety defect. Forty years of GNU tuning is one baseline and forty years of accreted "
          "observable behaviour is another; a rewrite inherits neither.",
          "跟着默认值一起发出去的，是三个有据可查的回退。cksum 处理大文件时比 GNU 慢至多 17×，后来打了"
          "补丁。base64 曾经更慢，之后才优化回来。md5sum 的行为差异弄坏了 Makeself 自解压安装包。三个里"
          "没有一个是内存安全缺陷。GNU 四十年的调优是一条基线，四十年累积的可观测行为是另一条；重写这两条"
          "都继承不到。"),
         "https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf"),
        ("rust",
         ("108 utilities are 108 independent acceptance gates", "108 个工具，就是 108 道彼此独立的验收门"),
         ("The module boundary here is a process boundary. 109 directories sit under src/uu/, and 108 "
          "of them declare a [[bin]] target. Each shipping utility therefore has its own binary and its "
          "own behavioural contract, so promotion, acceptance and rollback all happen one utility at a "
          "time. PARTIAL is the scope word that structure produces. The per-utility rollout can ship "
          "today. The simultaneous flip cannot.",
          "这里的模块边界就是进程边界。src/uu/ 下有 109 个目录，其中 108 个声明了 [[bin]] 目标。因此每个"
          "出货的工具都有自己的二进制、自己的行为契约，晋级、验收、回滚都是一次一个。PARTIAL 这个范围词，"
          "是这套结构自己给出来的。逐工具推进今天就能发。整套同时翻不能。"),
         "src/uu/ · 109 utility directories · 118,595 lines across 855 tracked files"),
        ("rust",
         ("The acceptance instrument was already in the tree", "验收工具本来就在仓库里"),
         ("The gate was never missing. GNUmakefile, .github/workflows/GnuTests.yml and "
          ".github/workflows/GnuComment.yml run the GNU compatibility suite in CI, backed by 174,220 "
          "lines of tests across 821 tracked paths. Nobody made it blocking per utility before the "
          "default changed. That one omission is the whole distance between this report's PASS and the "
          "flip's FAIL at G4.",
          "这道门从来不缺。GNUmakefile、.github/workflows/GnuTests.yml 和 "
          ".github/workflows/GnuComment.yml 在 CI 里跑 GNU 兼容套件，背后是 821 个受控路径、174,220 行"
          "测试。只是在默认值改变之前，没有人把它按工具设成阻塞。这一处遗漏，就是本报告的 PASS 与那次翻转"
          "在 G4 上 FAIL 之间的全部距离。"),
         "GNUmakefile · .github/workflows/GnuTests.yml · .github/workflows/GnuComment.yml · tests/ 821 tracked paths"),
        ("unknown",
         ("The repository does not state a GNU pass count", "仓库里没有 GNU 通过数"),
         ("README.md:355 is the section heading 'GNU test suite compatibility'. It links out to "
          "uutils.org coverage documentation and an evolution chart. The pass count is tracked "
          "externally, not in the tree. The roughly 500 of 600 figure this report carries is an "
          "announcement-time number, and the repository holds no current number to replace it. A "
          "distributor has to go and fetch parity. It cannot be read here.",
          "README.md:355 是标题「GNU test suite compatibility」。它把链接指向 uutils.org 的覆盖率文档和"
          "一张演进图。通过数记在仓库外面，不在树里。本报告带的大约 500 / 600 是公告时点的数字，仓库里"
          "没有当前数字可以替换它。发行方得自己去外部取 parity。在这里读不到。"),
         "README.md:355 · announcement-time figure from the why-not-rust case library"),
    ],

    "buys": [
        (("Class elimination per promoted utility", "每晋级一个工具，就消掉一类缺陷"),
         ("once a utility passes its gate, memory-unsafety stops being reachable in the code path that "
          "every script invoking it uses.",
          "工具一旦过门，调用它的每个脚本所走的代码路径上，内存不安全就不再可达。")),
        (("An unsafe surface you can audit", "一个审计得完的 unsafe 面"),
         ("275 `unsafe {` blocks and 4 `unsafe fn` across 251,003 lines is a review list, not a "
          "codebase-wide condition.",
          "251,003 行里 275 个 `unsafe {` 块和 4 个 `unsafe fn`，那是一份评审清单，不是整个代码库的状态。")),
        (("Per-utility blast radius", "按工具收敛的爆炸半径"),
         ("108 separate binaries mean one regression is one default switch, not a release-wide rollback.",
          "108 个各自独立的二进制，意味着一个回退只需切一个默认值，而不是整版回滚。")),
    ],
    "nobuys": [
        (("Speed", "速度"),
         ("the objective is resilience, not latency, and the field evidence runs the other way — cksum "
          "was up to 17× slower than GNU on large files before it was patched.",
          "目标是韧性，不是延迟，而且现场证据方向相反——打补丁之前，cksum 处理大文件比 GNU 慢至多 17×。")),
        (("Inherited behaviour", "继承来的行为"),
         ("exit codes, byte-level output and localized messages across 212 .ftl files are a 40-year "
          "accretion; a rewrite re-derives all of it rather than inheriting it, and md5sum differences "
          "broke Makeself installers.",
          "退出码、字节级输出，以及 212 个 .ftl 文件里的本地化消息，是 40 年攒下来的；重写只能把它们重新"
          "推导一遍，继承不了，md5sum 的差异就弄坏了 Makeself 安装包。")),
        (("Freedom from the acceptance work", "省掉验收这件事"),
         ("the announcement-time figure was roughly 500 of 600 GNU tests passing and the repository "
          "states no current count; the gate is the work, not a formality.",
          "公告时点的数字是 GNU 测试通过约 500 / 600，仓库里没有当前数；这道门本身就是工作量，不是走个形式。")),
    ],

    "precedents": [
        {"name": "Trifecta · sudo-rs", "outcome": "MIGRATED",
         "body": ("A scoped, privileged C tool was replaced in Rust and shipped as an Ubuntu 25.10 "
                  "default. The stated rationale was attack-surface reduction. No first-party material "
                  "frames it as a performance win.",
                  "一个范围明确的特权 C 工具被 Rust 重写，作为 Ubuntu 25.10 的默认发布。给出的理由是缩小"
                  "攻击面。第一方材料里没有任何地方把它包装成性能收益。"),
         "match": ("same distribution, same release, same C-to-Rust safety objective, same refusal to "
                   "argue speed",
                   "同一个发行版，同一个版本，同样的 C 转 Rust 安全目标，同样不拿速度说事"),
         "mismatch": ("one binary with one behavioural contract rather than 109, and a privilege "
                      "boundary rather than an output contract scripts parse",
                      "只有一个二进制、一份行为契约，不是 109 份；守的是权限边界，不是脚本要解析的输出契约"),
         "regime": "distribution default, 2025", "source_label": "first-party · project blog",
         "url": "https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/"},
        {"name": "Google · Android memory-safety programme", "outcome": "INCREMENTAL",
         "body": ("Memory safety's share of Android vulnerabilities fell from 76% to below 20%. The old "
                  "C/C++ was not mass-rewritten. New code went into safe languages instead. The "
                  "programme also reports roughly 4% of its Rust lines as unsafe, and a density of "
                  "about 0.2 vulnerabilities per million Rust lines against about 1,000 for C/C++.",
                  "内存安全类缺陷在 Android 漏洞中的占比，从 76% 降到 20% 以下。旧的 C/C++ 没有被大规模"
                  "重写。新代码改用安全语言来写。该项目还报告，其 Rust 代码约 4% 的行是 unsafe，缺陷密度约"
                  "为每百万行 Rust 0.2 个，而 C/C++ 约为 1,000 个。"),
         "match": ("same requirement class, and the closest published comparator for this repository's "
                   "measured unsafe surface",
                   "同一类需求，也是本仓库实测 unsafe 面最接近的公开参照"),
         "mismatch": ("an operating system with far more entry points; the density ratio is "
                      "C/C++-relative and does not transfer to memory-safe code, and a line share is "
                      "not a block count",
                      "那是一个入口点多得多的操作系统；密度比是相对 C/C++ 的，无法迁移到内存安全代码上，"
                      "而且行占比不等于块计数"),
         "regime": "2019–2025 vulnerability share", "source_label": "first-party · vendor security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
        {"name": "fish shell 4.0 · C++ → Rust", "outcome": "MIGRATED",
         "body": ("A whole widely used command-line program was ported to Rust. The maintainers graded "
                  "it themselves. Performance is 'usually slightly better in terms of time taken', and "
                  "memory use has a slightly higher floor and a lower ceiling. The 'half a year' "
                  "estimate became about two years.",
                  "一个使用广泛的命令行程序被整体移植到 Rust。维护者自己给出了结论。性能「usually slightly "
                  "better in terms of time taken」，内存占用下限略高、上限更低。当初「half a year」的估计，"
                  "最后变成了大约两年。"),
         "match": ("complete rewrite of a command-line program in the same direction, with a "
                   "near-neutral performance lens stated first-party and a schedule that slipped "
                   "fourfold",
                   "同一方向上对命令行程序的完整重写，第一方自述的性能结论接近中性，工期滑了四倍"),
         "mismatch": ("one shell with one contract and an opt-in user base, not a distribution's "
                      "default userland with 109 contracts",
                      "一个 shell、一份契约、用户自愿安装，不是带 109 份契约的发行版默认 userland"),
         "regime": "first-party post-release account, 2025", "source_label": "first-party · project blog",
         "url": "https://fishshell.com/blog/rustport/"},
        {"name": "Bun · Zig → Rust port", "outcome": "PORTED · CONTESTED",
         "body": ("About 535,000 lines were mechanically ported from Zig to Rust in roughly eleven "
                  "days. The motive was a stream of use-after-free, double-free and leak defects. "
                  "Selected first-party benchmarks moved 2.2–4.8% and binaries shrank about 20%. "
                  "19 regressions surfaced afterwards and were fixed.",
                  "大约 535,000 行代码在约十一天内从 Zig 机械移植到 Rust。动机是一连串 use-after-free、"
                  "double-free 和内存泄漏缺陷。第一方选取的基准测试变动 2.2–4.8%，二进制体积缩小约 20%。"
                  "事后浮出 19 个回退，都已修复。"),
         "match": ("native-to-native port with no architecture change, safety-motivated, and "
                   "regressions that only surfaced once real users ran it",
                   "原生到原生的移植，架构不变，动机是安全，回退都是真实用户跑起来之后才出现的"),
         "mismatch": ("Zig rather than C, no 40-year behavioural contract, not a distribution default, "
                      "and production readiness was publicly contested at publication "
                      "(https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743)",
                      "源语言是 Zig 不是 C，没有 40 年的行为契约，也不是发行版默认；发布时其生产可用性遭到"
                      "公开质疑（https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743）"),
         "regime": "first-party selected benchmarks, 2026", "source_label": "first-party · vendor blog (contested)",
         "url": "https://bun.com/blog/bun-in-rust"},
    ],

    "path": [
        {"title": ("Make the in-tree GNU harness blocking per utility",
                   "把仓库自带的 GNU 套件按工具设成阻塞"),
         "body": ("The distribution's coreutils package maintainers do this with uutils upstream. What "
                  "comes out is a per-utility promotion record from GNUmakefile and "
                  ".github/workflows/GnuTests.yml. Add a byte-level output diff for the documented flag "
                  "set and a throughput comparison against the incumbent on large inputs. Three things "
                  "must pass before a utility is eligible: its GNU test set, byte-identical output on "
                  "the documented flags, and throughput inside a stated tolerance on large inputs. Miss "
                  "the throughput comparison and the utility does not move. cksum shipped without it. "
                  "Rollback is cheap here — CI configuration and documentation, no packaging change.",
                  "由发行版的 coreutils 打包维护者与 uutils 上游一起做。产出是每个工具一份晋级记录，由 "
                  "GNUmakefile 和 .github/workflows/GnuTests.yml 生成。再加上文档化选项集的字节级输出 "
                  "diff，以及大输入下与现任实现的吞吐对比。一个工具要够格，三项都得过：GNU 测试集通过，"
                  "文档化选项下输出逐字节一致，大输入下吞吐落在明示的容差内。缺了吞吐对比，这个工具就不动。"
                  "cksum 当初发出去时，缺的就是它。这一步回滚很便宜——只涉及 CI 配置和文档，不动打包。"),
         "owner": "distribution coreutils package maintainers with uutils upstream",
         "cost_range": ("3–6 weeks", "3–6 周"),
         "artifact": "a per-utility promotion record produced by GNUmakefile and .github/workflows/GnuTests.yml, plus a byte-level output diff for the documented flag set and a throughput comparison against the incumbent on large inputs",
         "acceptance": "a utility becomes eligible only when its GNU test set passes, its output is byte-identical for the documented flags, and its throughput is inside a stated tolerance on large inputs",
         "stop": "do not promote any utility whose record is missing the throughput comparison — that is precisely the record cksum shipped without",
         "rollback": "CI configuration and documentation only; no packaging change"},
        {"title": ("Ship both implementations with the incumbent as default",
                   "两套实现都发，现任实现仍为默认"),
         "body": ("Package maintainers make both userlands installable, allow selection per utility, "
                  "and leave the incumbent as the default. They also open a named channel for "
                  "behavioural reports, so the evidence has somewhere to land. A candidate utility "
                  "passes once it has run a full release cycle of opt-in use with no new behavioural "
                  "report against it. Drop any utility that accumulates reports faster than they get "
                  "closed. No default changes at this step. There is nothing to roll back.",
                  "打包维护者让两套 userland 都能装上，允许按工具选择，默认仍然是现任实现。同时开一个专门"
                  "的渠道收行为问题报告，让证据有地方落。一个候选工具要过关，需要在选择性启用状态下跑满一个"
                  "完整发布周期，期间没有新的行为问题报告。哪个工具的报告攒得比关得快，就把它撤下来。这一步"
                  "不改任何默认值。没有东西需要回滚。"),
         "owner": "package maintainers",
         "cost_range": ("1 release cycle", "1 个发布周期"),
         "artifact": "both userlands installable, per-utility selection available, the incumbent still default, and a named channel for behavioural reports",
         "acceptance": "at least one full release cycle of opt-in use per candidate utility with no new behavioural report against it",
         "stop": "stop the programme for any utility that accumulates behavioural reports faster than they are closed",
         "rollback": "nothing to roll back — no default has changed at this step"},
        {"title": ("Promote utilities one at a time, ordered by exposure",
                   "按暴露面排序，一次晋级一个工具"),
         "body": ("Package maintainers own the order, and each promoted utility gets a named owner of "
                  "its own. The order comes from what breaks worst when behaviour changes, which puts "
                  "checksum tools and anything installers invoke late rather than early. One change per "
                  "utility, and no promotion bundles two. Each one carries its own gate record from "
                  "step 1. If two consecutive utilities produce field regressions after passing their "
                  "gate, freeze promotions — the gate is wrong, not the utility. Rolling back is one "
                  "default switch. The other 107 are untouched.",
                  "顺序由打包维护者定，每个晋级的工具另有一位具名负责人。排序依据是行为一变会坏得最狠的"
                  "地方，因此校验和类工具、以及安装程序会调用的东西都排在后面，不排在前面。一个工具一次变更，"
                  "不允许一次晋级捆两个。每次晋级都带着第 1 步产出的门记录。如果连着两个工具过了门之后仍在"
                  "现场出回退，就冻结晋级——错的是门，不是工具。回滚就是切一个默认值。其余 107 个不受影响。"),
         "owner": "package maintainers, with a named owner per promoted utility",
         "cost_range": ("per utility, scoped", "按工具计，范围明确"),
         "artifact": "a promotion order derived from what breaks worst when behaviour changes, with checksum tools and anything installers invoke placed late rather than early, and one change per utility",
         "acceptance": "each promotion is a separate change carrying its own gate record from step 1, and no promotion bundles two utilities",
         "stop": "freeze promotions if two consecutive utilities produce field regressions after passing their gate — the gate is then wrong, not the utility",
         "rollback": "switch that one utility's default back; the other 107 are untouched"},
        {"title": ("Publish the pass count where the decision can read it",
                   "把通过数发布在做决策的人读得到的地方"),
         "body": ("uutils upstream and the distributor record the GNU test pass count, and the names of "
                  "the failing tests, per release in the repository. README.md:355 currently links that "
                  "data out to external coverage documentation, so a distributor reading the tree alone "
                  "sees nothing. Acceptance is simple: the count and the failing set appear in the "
                  "release artifact the distributor already consumes. If the count cannot be produced "
                  "per release, parity is UNKNOWN and nothing else gets promoted. This step touches "
                  "documentation and release tooling. Nothing else.",
                  "由 uutils 上游与发行方一起，把 GNU 测试的通过数和失败用例名，按版本记进仓库。"
                  "README.md:355 现在把这份数据链到外部覆盖率文档，只读树的发行方什么也看不到。验收标准很"
                  "简单：这个数和失败集合出现在发行方本来就在消费的发布产物里。如果做不到按版本给出这个数，"
                  "parity 就是 UNKNOWN，后面不再晋级任何工具。这一步只动文档和发布工具链。别的都不动。"),
         "owner": "uutils upstream with the distributor",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "the GNU test pass count and the names of the failing tests recorded per release in the repository, since README.md:355 currently links that data out to external coverage documentation",
         "acceptance": "the count and the failing set appear in the release artifact the distributor already consumes",
         "stop": "if the count cannot be produced per release, treat parity as UNKNOWN and promote nothing further",
         "rollback": "documentation and release tooling only"},
        {"title": ("Re-run these gates before the LTS", "在 LTS 之前把这几道门再跑一遍"),
         "body": ("The distributor's release team owns this one. The output is a short re-assessment "
                  "listing which utilities were promoted, which gate records exist, and which field "
                  "regressions turned up after promotion instead of before it. It passes when it names "
                  "an owner for every promoted utility and the residual failing tests that utility "
                  "carries into the LTS. Any utility without a gate record goes back to the incumbent "
                  "default before the LTS freeze. The rollback mechanism is unchanged from step 3: one "
                  "default switch per utility.",
                  "这一步归发行方的发布团队。产出是一份简短的复评，列出哪些工具已晋级、哪些门记录存在、"
                  "哪些现场回退是在晋级之后而不是之前才发现的。复评过关的条件是：为每个已晋级的工具点名"
                  "负责人，并写明它带进 LTS 的残余失败用例。任何没有门记录的工具，在 LTS 冻结前退回现任"
                  "默认实现。回滚机制与第 3 步相同：一个工具切一个默认值。"),
         "owner": "the distributor's release team",
         "cost_range": ("1–2 days per review", "每次复核 1–2 天"),
         "artifact": "a short re-assessment listing which utilities were promoted, which gate records exist, and which field regressions were found after promotion rather than before",
         "acceptance": "the review names the owner of every promoted utility and the residual failing tests it carries into the LTS",
         "stop": "any utility without a gate record returns to the incumbent default before the LTS freeze",
         "rollback": "per-utility default switches, unchanged in mechanism from step 3"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端占比"), "state": "PASS",
         "claim": ("No Rust option here claims a performance benefit. D2 is recorded N/A instead of "
                   "being filled with a time share invented from line counts. The field evidence runs "
                   "the other way.",
                   "这里没有任何 Rust 方案声称性能收益。D2 记为 N/A，而不是拿代码行数编一个时间占比填进去。"
                   "现场证据的方向恰好相反。"),
         "evidence": "D2 N/A · cksum up to 17× slower before patching"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("The safety delta is attributed to the language property, and measured on the "
                   "candidate itself. No redesign, algorithm change or packaging change is credited to "
                   "Rust.",
                   "安全收益归因于语言属性，并且是在候选实现自身上测出来的。没有把任何重新设计、算法改动"
                   "或打包改动记到 Rust 头上。"),
         "evidence": "275 `unsafe {` blocks and 4 `unsafe fn` across 251,003 lines"},
        {"name": ("Baseline and regime", "基线与口径"), "state": "HIT",
         "claim": ("The incumbent was never measured. GNU coreutils was not cloned, so the size of the "
                   "class being removed rests on one structural fact: the incumbent is manually managed "
                   "C. The parity figure carried here is an announcement-time number.",
                   "现任实现从未被测量。GNU coreutils 没有克隆，因此被移除那一类缺陷有多大，只靠一个结构性"
                   "事实支撑：现任实现是人工维护的 C。本报告带的 parity 数字来自公告时点。"),
         "evidence": "no GNU clone · roughly 500 of 600 GNU tests at announcement"},
        {"name": ("Boundary and omitted cost", "边界与被漏掉的成本"), "state": "HIT",
         "claim": ("The original decision omitted two costs: the compatibility surface, and a second "
                   "upstream's fix latency. md5sum behaviour differences broke Makeself installers. The "
                   "cksum and base64 fixes arrived after the flip, not before it.",
                   "原来那个决策漏掉了两项成本：兼容面，以及第二个上游的修复时延。md5sum 的行为差异弄坏了 "
                   "Makeself 安装包。cksum 和 base64 的修复是在翻转之后到的，不是之前。"),
         "evidence": "https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf · 212 .ftl files"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("Every promotion carries a named owner, a gate record and a per-utility rollback. "
                   "The larger option is excluded on this check, not on its technology.",
                   "每次晋级都带着具名负责人、门记录和逐工具回滚。更大的那个方案是在这一项上被排除的，"
                   "不是因为它用什么技术。"),
         "evidence": "G4 · reversible path steps 1–3"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有资源的反事实"), "state": "PASS",
         "claim": ("Continued maintenance of the C implementation is retained as a live option, not "
                   "dismissed. It stays the default for every utility that has not passed its gate.",
                   "继续维护 C 实现，是作为一个仍然有效的选项保留下来的，没有被打发掉。对每个尚未过门的"
                   "工具，它继续是默认值。"),
         "evidence": "D12 · gnu-stay retained"},
        {"name": ("Cost of inaction", "不作为的代价"), "state": "HIT",
         "claim": ("Keeping a manually managed C userland keeps the memory-unsafety class reachable in "
                   "code that every script, Makefile and installer on the system invokes.",
                   "继续用人工维护的 C userland，就是让内存不安全这一类缺陷，在系统上每个脚本、每个 "
                   "Makefile、每个安装程序都会调用的代码里保持可达。"),
         "evidence": "D1 · G1 PASS"},
        {"name": ("Maturity mistaken for safety", "把成熟度当成安全性"), "state": "HIT",
         "claim": ("The staying case leans on forty years of GNU history. That history is evidence "
                   "about tuning and observable behaviour, not about the memory-unsafety class. Age "
                   "does not make C memory-safe.",
                   "不动的理由靠的是 GNU 四十年的历史。这段历史能证明的是调优和可观测行为，证明不了内存"
                   "不安全这一类缺陷。年头长不会让 C 变得内存安全。"),
         "evidence": "case library · 40 years of GNU tuning as a performance and behaviour baseline"},
        {"name": ("Native-advantage denial", "否认原生方案的优势"), "state": "PASS",
         "claim": ("The candidate's advantages are recorded, not waved away. It exists, covers 109 "
                   "utilities, carries 174,220 lines of tests, has already shipped as a default, and "
                   "its unsafe surface is enumerable.",
                   "候选实现的优势被记下来了，没有一笔带过。它已经存在，覆盖 109 个工具，带着 174,220 行"
                   "测试，已经作为默认发布过，而且它的 unsafe 面可以逐个列清。"),
         "evidence": "D6 and D9 records"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("Staying is per utility and bounded by a gate. It is not open-ended. Each utility "
                   "leaves the staying option the moment its record clears. 'Harden C forever' is never "
                   "the default answer.",
                   "「不动」是按工具算的，而且有门卡着。它不是无限期的。任何一个工具，只要记录齐了就离开"
                   "「不动」这一栏。「永远加固 C」从来不是默认答案。"),
         "evidence": "selected option scope · reversible path steps 1–3"},
    ],

    "gaps": [
        (("Per-utility acceptance records for the utilities already flipped",
          "已经翻过默认值的那些工具，缺逐工具验收记录"),
         ("Without them the residual risk of the shipped default is unknown per utility, and the gate "
          "cannot be applied retroactively without the byte-level diffs and throughput comparisons it "
          "needs.",
          "没有它们，已发布默认值的残余风险就无法按工具说清；而缺了所需的字节级 diff 和吞吐对比，这道门"
          "也没法事后补做。")),
        (("A GNU test pass count published per release", "按版本公布的 GNU 测试通过数"),
         ("README.md:355 links the coverage data out to external documentation, so a distributor "
          "reading the repository alone cannot see parity. Parity stays an announcement-time figure, "
          "and the parity-first option cannot even be evaluated.",
          "README.md:355 把覆盖率数据链到外部文档，只读仓库的发行方看不到 parity。parity 因此停留在公告"
          "时点的数字上，而「先等 parity」那个方案连评估都无从谈起。")),
        (("Per-invocation cost decomposition for either implementation", "两边实现都缺单次调用的开销拆分"),
         ("D5 stays UNKNOWN. A per-utility startup and throughput comparison is what turns a "
          "cksum-class regression from a field discovery into a pre-promotion gate.",
          "D5 保持 UNKNOWN。把 cksum 那类回退从「现场才发现」变成「晋级前就拦住」，靠的就是逐工具的启动"
          "与吞吐对比。")),
        (("A measured comparison against the incumbent", "与现任实现的实测对比"),
         ("GNU coreutils was not cloned or measured here, so the eliminated-class size rests on "
          "structural argument and the residual-risk side of the counterfactual is unquantified.",
          "这里没有克隆也没有测量 GNU coreutils，因此被消除那一类缺陷有多大只能靠结构性论证，反事实中"
          "残余风险那一侧也没有量化。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; every count comes from tracked files only, and deleted history was not inspected.",
        "GNU coreutils was not cloned; claims about the incumbent are limited to its implementation language and to the tuning and behaviour baseline recorded in the skill's case library.",
        "No performance requirement is attached to this decision; if a distributor states one, D2 must be recomputed from a real profile rather than from line counts.",
    ],
    "objective": {
        "driver": "safety",
        "requirement": "remove the memory-unsafety class from the default command-line userland without changing the observable behaviour that scripts, Makefiles and installers depend on",
        "baseline": "the incumbent implementation is manually managed C with forty years of accreted tuning and observable behaviour",
        "target": "class elimination per utility, gated on byte-level output parity and a stated throughput tolerance against the incumbent",
    },
    "repository": {
        "path": "https://github.com/uutils/coreutils",
        "commit": "0c8a3c7f366ee77341b95489c00c9ce0ce53e085",
        "scope": "the whole Rust candidate repository, with one utility under src/uu/ as the unit of decision; the incumbent GNU C implementation was not cloned",
        "sampling": "tracked symlinks are followed, so LICENSE symlinks contribute to directory totals; shallow clone; 1,967 tracked files enumerated; 251,003 lines across 631 .rs files, src/uu/ 118,595 lines across 855 tracked files in 109 utility directories, src/uucore/ 34,778 lines across 82 files, tests/ 174,220 lines across 821 tracked paths, 212 .ftl localization files, 275 `unsafe {` blocks and 4 `unsafe fn`; no build, test, benchmark or network call was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "uutils/coreutils at 0c8a3c7 · static read-only analysis · why-not-rust method 2.0",
        "uutils/coreutils 于 0c8a3c7 · 只读静态分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/uutils/coreutils at commit 0c8a3c7, shallow clone, 1,967 tracked files. "
        "Scope: the whole Rust candidate repository, with one utility under src/uu/ as the unit of "
        "decision. The measurement target is the Rust candidate, not the incumbent. GNU coreutils was "
        "not cloned, so no claim is made about its internals, and that limit is why confidence is "
        "MEDIUM rather than HIGH. Sampling: 251,003 lines across 631 .rs files; src/uu/ 118,595 lines "
        "across 855 tracked files in 109 utility directories; src/uucore/ 34,778 lines across 82 files; "
        "tests/ 174,220 lines across 821 tracked paths; 212 .ftl localization files; 275 `unsafe {` "
        "blocks and 4 `unsafe fn` across *.rs; the GNU compatibility harness present as GNUmakefile "
        "with .github/workflows/GnuTests.yml and .github/workflows/GnuComment.yml. README.md:355 is the "
        "'GNU test suite compatibility' heading and links the pass count out to external coverage "
        "documentation, so no in-repository pass count is quoted here. The roughly 500 of 600 figure is "
        "an announcement-time number from the skill's case library, not a current measurement. No "
        "build, test, benchmark or network call was run against the project. Objective: remove the "
        "memory-unsafety class from the default command-line userland without changing the observable "
        "behaviour scripts, Makefiles and installers depend on. User-supplied facts: none. No Amdahl "
        "calculation appears and none should. The objective is resilience and safety, not latency, so "
        "D2 is recorded N/A; converting a line share into a time share to fill it would be a method "
        "error, and the one measured performance fact runs against the migration rather than for it. "
        "Why the selected option is the smallest sufficient step: the module boundary here is a process "
        "boundary. 109 directories sit under src/uu/, of which 108 declare a [[bin]] target, so 108 "
        "shipping utilities are 108 separate binaries with 108 separate behavioural contracts. "
        "Per-utility promotion delivers the same class elimination as the simultaneous default flip, "
        "and it keeps rollback at one utility. External figures keep their URL and regime: the cksum, "
        "base64 and md5sum regressions are press coverage of the Ubuntu 25.10 release "
        "(https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf); Android's unsafe-line share is a "
        "vendor security-blog figure, and a line share rather than a block count. This framework "
        "compares explicit options through four non-compensatory gates. It is a structured decision "
        "protocol, not a statistical predictor.",

        "仓库：github.com/uutils/coreutils，commit 0c8a3c7，浅克隆，1,967 个受版本控制的文件。范围：整个 "
        "Rust 候选仓库，决策单位是 src/uu/ 下的一个工具。测量对象是 Rust 候选实现，不是现任实现。GNU "
        "coreutils 没有克隆，因此不对它的内部作任何断言；正是这个限制让置信度停在 MEDIUM 而不是 HIGH。"
        "采样：631 个 .rs 文件共 251,003 行；src/uu/ 下 109 个工具目录、855 个受控文件、118,595 行；"
        "src/uucore/ 82 个文件、34,778 行；tests/ 821 个受控路径、174,220 行；212 个 .ftl 本地化文件；"
        "*.rs 中 275 个 `unsafe {` 块和 4 个 `unsafe fn`；GNU 兼容测试套件以 GNUmakefile 加 "
        ".github/workflows/GnuTests.yml 和 .github/workflows/GnuComment.yml 的形式存在。README.md:355 是"
        "「GNU test suite compatibility」标题，把通过数链到外部覆盖率文档，因此这里不引用任何仓库内的"
        "通过数。大约 500 / 600 这个数字来自技能自带的案例库，是公告时点的数，不是当前测量值。没有对项目"
        "执行任何构建、测试、基准或网络调用。目标：把内存不安全这一类缺陷从默认命令行 userland 中移除，"
        "同时不改变脚本、Makefile 和安装程序依赖的可观测行为。用户提供的事实：无。报告里没有 Amdahl 计算，"
        "也不该有。目标是韧性与安全，不是延迟，所以 D2 记为 N/A；把行占比换算成时间占比来填这一格属于方法"
        "错误，而唯一一项实测的性能事实，方向是反对迁移而不是支持迁移。为什么推荐方案就是最小充分步骤："
        "这里的模块边界就是进程边界。src/uu/ 下有 109 个目录，其中 108 个声明了 [[bin]] 目标，于是 108 个"
        "出货工具就是 108 个各自独立的二进制、108 份各自独立的行为契约。逐工具晋级带来的类消除，与整套"
        "默认值同时翻转完全一样，同时把回滚控制在一个工具的粒度上。外部数据保留其 URL 与口径：cksum、"
        "base64 和 md5sum 的回退来自对 Ubuntu 25.10 发布的媒体报道"
        "（https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf）；Android 的 unsafe 行占比来自厂商"
        "安全博客，是行占比，不是块计数。这个框架通过四道非补偿性证据门比较明确列出的方案。它是一套结构化"
        "决策协议，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 0c8a3c7 · no build, benchmark or network call",
        "公开仓库 · 在 commit 0c8a3c7 上做静态分析 · 未执行构建、基准测试或网络调用",
    ),
}
