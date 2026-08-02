"""fish-shell/fish-shell — the port that finished, and what it actually bought.

Repository facts were measured read-only on the shallow clone named in
`repository`. The pre-port C++ baseline and the 4.0.0 Rust snapshot come from
source tarballs fetched via `gh api`; history, releases, advisories and author
counts come from the GitHub API.
"""

CASE = {
    "slug": "fish-shell",
    "project_name": "fish-shell/fish-shell",
    "project_desc": (
        "Rust · interactive shell · 103,667 lines of Rust, 0 C++ files, 2 native survivors",
        "Rust · 交互式 shell · 103,667 行 Rust，0 个 C++ 文件，2 个原生文件留了下来",
    ),
    "date": "2026-08-02",
    "archetype": (
        "cli-longtask · interactive shell, forks per job, no network trust boundary",
        "cli-longtask · 交互式 shell，每个 job 都 fork，没有网络信任边界",
    ),

    "scope_word": "MIGRATE",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "STABLE",
    "selected": "rust-full-port",
    "scope_chip": (
        "translate the whole shell to Rust in place, on master, incrementally",
        "在 master 上就地把整个 shell 增量翻译成 Rust",
    ),
    "scope_sub": (
        "the one everybody talks about and almost nobody finishes",
        "所有人都在谈、几乎没人做完的那件事",
    ),

    "why": (
        "fish is the migration that finished. 78,532 lines of C++ and headers at tag 3.6.0; zero C++ "
        "files at HEAD. Deleting the C++ took 338 days and shipping 4.0 took 761, against a plan that "
        "guessed six months. The payoff was never speed, and the project says so itself. It was a "
        "codebase its own contributors would work in: 96 distinct commit authors in the twelve months "
        "before the port, 154 in the twelve months after 4.0.",
        "fish 是那个真做完了的迁移。3.6.0 这个 tag 上有 78,532 行 C++ 和头文件，HEAD 上一个 C++ 文件都没有。"
        "删掉 C++ 用了 338 天，把 4.0 发出去用了 761 天，而当初计划里猜的是半年。买到的东西从来不是速度，项目"
        "自己也这么讲。买到的是一份自己人愿意动手的代码：迁移前十二个月有 96 位不同的提交者，4.0 之后的十二"
        "个月有 154 位。",
    ),
    "trigger": (
        "Stable. The C++ is deleted and the FFI crates are gone, so nothing reopens the scope question. "
        "One promise is still outstanding: concurrent function execution was the reason Rust beat the "
        "alternatives in the project's own comparison, and issue 238 has been open since 2012. If it "
        "never lands, the language choice was justified by something the project never cashed.",
        "结论稳定。C++ 已删，FFI crate 也已移除，范围问题不会再打开。有一笔承诺还挂着：并发函数执行是项目"
        "自己那份语言对比里 Rust 胜出的理由，而 issue 238 从 2012 年开到现在。如果它一直不落地，当初选语言的"
        "那条理由就一直没有兑现。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("17 people ever made 10 or more commits to the C++, across 11 years.",
                           "11 年里，对那份 C++ 提交过 10 次以上的只有 17 个人。"),
         "name": "requirement",
         "evidence": "The gap was contributor supply and a toolchain floor, both named in the project's own RFC at doc_internal/fish-riir-plan.md:5-8. First-party: only 17 people had 10 or more commits to the C++ code in 11 years. The C++ build floor at tag 3.6.0 was a C++11 compiler, CMake 3.5 and ncurses headers. No memory-safety advisory exists in fish's published history, and the RFC does not claim one."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Send and Sync are compiler-checked. C++ has no equivalent.",
                           "Send 和 Sync 由编译器检查，C++ 里没有对等物。"),
         "name": "rust-specific causality",
         "evidence": "The RFC ran the alternatives before the work started and wrote down why each lost: Java and Python on startup and memory, Go on fork(2), and D/Nim/Zig on contributor supply (doc_internal/fish-riir-plan.md:15-17). The Rust-specific mechanism is compiler-checked thread safety: the maintainer had a working C++ threading branch and would not propose it because C++ cannot enforce what crosses a thread boundary (doc_internal/fish-riir-plan.md:67-69)."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("No amount of C++ modernization delivers a different contributor pool.",
                           "把 C++ 现代化到什么程度，都换不来另一批贡献者。"),
         "name": "economics and smallest sufficient option",
         "evidence": "Two cheaper in-stack options existed and are retained: modernize the C++ standard, and ship the C++ threading branch that already worked. Each reaches one stated goal. Neither reaches the goal the RFC put first, because the language itself was the barrier to entry. Cost is not hidden: 338 days to delete the C++, 761 to ship 4.0.0, and 345 days with no release of any kind between 3.7.1 and 4.0.0."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("166 black-box test files predated the port and outlived it.",
                           "166 个黑盒测试文件在迁移之前就在，迁移之后还在。"),
         "name": "delivery and reversibility",
         "evidence": "At tag 3.6.0 the acceptance harness was 130 littlecheck files plus 36 pexpect scripts that drive the fish binary and diff its output; none references an implementation symbol. Work stayed on master with both languages in one binary via forked cxx/autocxx plus corrosion, ordered outside-in from builtins to reader. Rollback was live at every commit until 2024-01-01, when 102ab2c90 removed the C++."},
    ],

    "tiles": [
        (("C++ at the last pre-port tag", "迁移前最后一个 tag 上的 C++"), "78,532", ("lines", "行"),
         ("3.6.0 · 104 .cpp + 105 .h", "3.6.0 · 104 个 .cpp + 105 个 .h")),
        (("C++ files at HEAD", "HEAD 上的 C++ 文件"), "0", ("files", "个"),
         ("9654f5e · the whole point of the exercise", "9654f5e · 整件事的重点就在这里")),
        (("Proposal to C++ deletion", "从提案到删掉 C++"), "338", ("days", "天"),
         ("the plan wrote 'Handwaving, 6 months?'", "计划里写的是「Handwaving, 6 months?」")),
        (("Distinct commit authors, 12 months after 4.0", "4.0 之后 12 个月的不同提交者"), "154",
         ("authors", "位"),
         ("96 in the 12 months before the port", "迁移前 12 个月是 96 位")),
        (("unsafe occurrences at HEAD", "HEAD 上 unsafe 的出现次数"), "287", ("in 218 .rs files", "分布在 218 个 .rs 文件"),
         ("420 at 4.0.0, while the Rust grew 9.5%", "4.0.0 时是 420 次，同期 Rust 代码还多了 9.5%")),
        (("Releases between 3.7.1 and 4.0.0", "3.7.1 到 4.0.0 之间的发布"), "0", ("in 345 days", "345 天里"),
         ("what the project did not do meanwhile", "这段时间项目没干的事")),
    ],

    "options_sub": (
        "Every option is judged against the objective the project wrote down before starting: widen the "
        "contributor pool, lift the C++11/CMake/ncurses floor, and get compiler-checked thread safety "
        "for concurrent functions.",
        "所有方案都对着项目动手前写下的那个目标：扩大贡献者池，抬掉 C++11/CMake/ncurses 这道地板，并为并发"
        "函数拿到编译器检查的线程安全。",
    ),
    "options": [
        {"id": "rust-full-port", "name": ("Translate the whole shell to Rust, in place",
                                          "就地把整个 shell 翻译成 Rust"),
         "implementation": "rust",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("class removed from 78,532 lines; contributor count up 60%",
                              "78,532 行里缺陷类消失；贡献者数量涨 60%"),
         "one_time_cost": "338 days to delete the C++; 761 to ship 4.0.0",
         "recurring_cost": "197 Cargo.lock entries; a Rust toolchain in every distro build",
         "cost_cell": ("338 days to delete C++; 197 lockfile entries after",
                       "338 天删完 C++；此后 197 条 lockfile 条目"),
         "time_to_value": ("first Rust in the proposal PR; user-visible at 2 years",
                           "提案 PR 里就有第一批 Rust；用户看得见要 2 年"),
         "compatibility": "shell behaviour, captured by a pre-existing black-box harness",
         "compat_cell": ("black-box harness · C++ built until 2024-01-01",
                         "黑盒测试兜住 · C++ 一直能编到 2024-01-01"),
         "reversibility": "git revert, at any commit before 102ab2c90",
         "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · the only option that reaches the goal the RFC put first",
                  "推荐 · 唯一打到 RFC 排在第一位那个目标的方案"),
         "reason": "The RFC's first objective was contributor supply, and the language was the barrier. No in-stack change reaches that. Cost overran the plan by 1.9x on code and 4.2x on release, and it was still paid and finished."},
        {"id": "stay-modernize", "name": ("Modernize the C++ in place", "在 C++ 里做现代化"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("lifts the toolchain floor; contributor pool unchanged",
                              "抬掉工具链地板；贡献者池不变"),
         "one_time_cost": "months, incremental", "recurring_cost": "none new",
         "cost_cell": ("months, incremental; nothing new recurring", "数月，可增量做；无新增长期成本"),
         "time_to_value": ("per release", "随版本发布"),
         "compatibility": "native", "compat_cell": ("native · no build-system risk", "原生 · 构建系统无风险"),
         "reversibility": "git revert",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded counterfactual the migration had to beat",
                  "保留 · 迁移必须先赢过的那个已投入对照"),
         "reason": "Reaches the toolchain half of the objective for a fraction of the cost. It leaves the project writing C++, which is the thing the RFC said was driving contributors away."},
        {"id": "stay-concurrent-cpp", "name": ("Ship the C++ concurrency branch as it stands",
                                               "直接把那条 C++ 并发分支发出去"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("delivers issue 238 now; no safety net on thread boundaries",
                              "现在就交付 issue 238；线程边界上没有安全网"),
         "one_time_cost": "weeks; the branch already worked", "recurring_cost": "review burden on every threaded change",
         "cost_cell": ("weeks; permanent review burden", "数周；此后每次改动都要人肉审"),
         "time_to_value": ("one release", "一个发布周期"),
         "compatibility": "changes observable execution semantics",
         "compat_cell": ("semantics change · feature flag", "语义会变 · 用 feature flag 控制"),
         "reversibility": "feature flag",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the smallest option for the goal that is still unmet",
                  "保留 · 针对那个至今未达成目标的最小方案"),
         "reason": "The cheapest path to the concurrency goal, and three and a half years later it is still the only path that has actually been tried. The maintainer's objection was reviewability, not feasibility."},
        {"id": "rust-extract-leaf", "name": ("Port the leaves only, keep the C++ core",
                                             "只把叶子换成 Rust，内核留 C++"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed from the leaves; core untouched",
                              "叶子部分缺陷类消失；内核不动"),
         "one_time_cost": "weeks per component", "recurring_cost": "cxx/autocxx maintained forever",
         "cost_cell": ("weeks per component; permanent FFI tax", "每个组件数周；FFI 税永久留下"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "same harness", "compat_cell": ("same harness · per-component revert", "同一套测试 · 按组件回退"),
         "reversibility": "per component",
         "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · this was the actual state at month three", "保留 · 第三个月时的真实状态就是这个"),
         "reason": "The natural place to stop, and the RFC priced FFI string copying as acceptable only because it was temporary. Stopping here converts that into a permanent tax and reaches none of the three goals."},
        {"id": "native-go", "name": ("Port to Go instead of Rust", "换成 Go，而不是 Rust"),
         "implementation": "external",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("large contributor pool; fork(2) becomes the problem",
                              "贡献者池很大；fork(2) 变成新问题"),
         "one_time_cost": "comparable to the Rust port", "recurring_cost": "a GC in a per-keystroke process",
         "cost_cell": ("comparable one-time; a GC in the shell", "一次性成本相当；shell 里多一个 GC"),
         "time_to_value": ("years", "数年"),
         "compatibility": "job control depends on fork semantics",
         "compat_cell": ("fork semantics at risk · no clean rollback", "fork 语义有风险 · 没有干净的回退"),
         "reversibility": "none", "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · a shell forks for every job", "排除 · shell 每跑一个 job 就 fork 一次"),
         "reason": "fish forks and then does signal, pgroup and tty setup in the child. The RFC excluded Go on exactly that ground, and it also gives up the compiler-checked thread safety that was the tiebreaker."},
        {"id": "adopt-other-shell", "name": ("Point users at a shell already written in Rust",
                                             "让用户改用已经用 Rust 写的 shell"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("nothing for fish; a different shell for the user",
                              "对 fish 没有收益；对用户是另一个 shell"),
         "one_time_cost": "per user", "recurring_cost": "relearning the scripting language",
         "cost_cell": ("per user; a new scripting language", "按用户计；一门新的脚本语言"),
         "time_to_value": ("immediate for one user", "对单个用户是立刻"),
         "compatibility": "not fish; 72,635 lines of share/ scripts do not transfer",
         "compat_cell": ("not fish · share/ does not transfer", "不是 fish · share/ 搬不过去"),
         "reversibility": "switch back", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · answers a different question than the one asked",
                  "排除 · 回答的不是这里问的问题"),
         "reason": "Retained because the method requires an adoption option, and excluded because fish's objective was about fish's maintainers. A user switching shells changes nothing for the project."},
    ],

    "lenses_sub": (
        "Each state is evidence scoped to named options, not a score. The performance lenses sit at "
        "NEUTRAL or N/A because nobody claimed a performance requirement, including the project. The "
        "delivery lenses carry the weight here.",
        "每条状态都绑定到具体方案，不是可以相加的分数。性能相关的几条停在 NEUTRAL 或 N/A，因为没有人主张过"
        "性能需求，项目自己也没有。这里吃重的是交付相关的几条。",
    ),
    "na_note": (
        "One lens is N/A. D2 end-to-end reach: an Amdahl figure needs a performance requirement, and this "
        "migration never had one. D3, D4 and D5 sit at NEUTRAL for a related reason — every retained "
        "option is a native binary with no collector, so no option removes a runtime mechanism the others "
        "keep.",
        "一条记为 N/A。D2 端到端影响面：算 Amdahl 得先有性能需求，这次迁移从来没有。D3、D4、D5 停在 NEUTRAL "
        "是相近的原因——保留下来的方案全是没有 collector 的原生二进制，谁也没法从尾延迟里拿走别人还留着的运行"
        "时机制。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · rust-full-port, stay-modernize", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-full-port", "stay-modernize", "rust-extract-leaf"],
         "claim": ("The unmet requirement was people and toolchain, not CPU time. First-party: 17 people "
                   "made 10 or more commits to the C++ in 11 years. The build floor at 3.6.0 was a C++11 "
                   "compiler, CMake 3.5 and ncurses. Both halves are owned by the project.",
                   "没被满足的需求是人和工具链，不是 CPU 时间。第一方数据：11 年里对那份 C++ 提交过 10 次以上"
                   "的有 17 个人。3.6.0 的构建地板是 C++11 编译器、CMake 3.5、ncurses。这两半都在项目自己手里。"),
         "source": "doc_internal/fish-riir-plan.md:5-8 · README.rst:152 at tag 3.6.0 · https://fishshell.com/blog/rustport/",
         "regime": "the project's own RFC plus a first-party retrospective",
         "caveat": "The toolchain half is also reachable by stay-modernize, so D1 alone does not make this a Rust-specific finding. Only D7 and D9 do that.",
         "change_trigger": "A contributor count that had risen under C++ would have removed the first objective entirely."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("No Amdahl figure appears here. There was never a performance requirement to build "
                   "one from. The 4.0.0 notes open with 'there should be no direct impact on users.' The "
                   "four performance items in that release each carry their own issue number and none is "
                   "attributed to the language.",
                   "这份报告不给 Amdahl 数字，因为从头到尾没有人提出性能需求。4.0.0 的发布说明开头就写"
                   "「there should be no direct impact on users」。那个版本里四条性能改进各自挂着 issue 号，"
                   "没有一条被归给换语言。"),
         "source": "CHANGELOG.rst:727 · CHANGELOG.rst:841, 882, 961, 962",
         "regime": "n/a — no performance target exists",
         "caveat": "Substituting a line-count share for a time share would be a method error, and there is no profile to substitute anyway."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("There is no collector on either side. Neither C++ nor Rust has one, so no option "
                   "removes a runtime mechanism from the tail. The project published its own verdict "
                   "on the outcome: 'usually slightly "
                   "better in terms of time taken, memory use has a slightly higher floor but a lower "
                   "ceiling.' That is parity, stated plainly.",
                   "C++ 和 Rust 都没有 collector，所以没有哪个方案能从尾延迟里拿掉运行时机制。项目自己给过"
                   "结论：'usually slightly better in terms of time taken, memory use has a slightly "
                   "higher floor but a lower ceiling'。这就是打平，说得很直接。"),
         "source": "https://fishshell.com/blog/rustport/ · first-party retrospective",
         "regime": "first-party prose, no published measurement method",
         "caveat": "This is a maintainer's summary, not a benchmark artifact. It is quoted as evidence of what the project claims, not as a measurement.",
         "change_trigger": "A published before/after profile of shell startup and keystroke latency would move this to STRONG in either direction."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "WEAK", "option_ids": [],
         "claim": ("There is no fleet. A shell runs one process per terminal on a developer's own "
                   "machine, so there is nothing to multiply, no instance price, and no utilization "
                   "figure. The first-party memory "
                   "statement cuts both ways: higher floor, lower ceiling.",
                   "shell 是在开发者自己机器上、每个终端一个进程。没有机队可乘，没有实例价格，也没有利用率。"
                   "第一方那句关于内存的说法是两头都有：floor 更高，ceiling 更低。"),
         "source": "https://fishshell.com/blog/rustport/",
         "regime": "n/a — no fleet arithmetic applies",
         "caveat": "A higher memory floor is a regression for someone running hundreds of shells; nobody has measured that case."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Startup matters a lot here. Every new terminal tab pays it. The lens is neutral "
                   "because this constraint did its work earlier: it eliminated Java, Python and the "
                   "scripting family from the RFC's own shortlist. Everything left is a native binary.",
                   "启动在这里很要紧，每开一个终端标签都要付一次。也正因为如此它是中性的：这条约束在 RFC 自己"
                   "的候选名单里筛掉了 Java、Python 和整个脚本语言家族。活下来的方案全是原生二进制。"),
         "source": "doc_internal/fish-riir-plan.md:15 · benchmarks/benchmarks/no_execute.fish",
         "regime": "structural constraint, applied at language-selection time",
         "caveat": "The repository ships a benchmark harness at benchmarks/driver.sh with 15 cases, but no before/after results are committed."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust-full-port", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-full-port", "rust-extract-leaf"],
         "claim": ("fish had no memory-safety crisis. Two published advisories exist and both are logic "
                   "bugs: command-substitution expansion, and a compromised git repository. The port "
                   "removed the memory-unsafety class from 78,532 lines anyway. What replaced it is a "
                   "panic that prints 'crashed, please report a bug' and exits.",
                   "fish 没有内存安全危机。公开的安全公告只有两条，而且都是逻辑问题：命令替换的展开，以及一个"
                   "被污染的 git 仓库。这次迁移还是把 78,532 行里的内存不安全缺陷类拿掉了。取而代之的是一次 "
                   "panic，打印「crashed, please report a bug」然后退出。"),
         "source": "gh api repos/fish-shell/fish-shell/security-advisories · src/panic.rs:39",
         "regime": "structural, at the whole-implementation scope",
         "caveat": "PCRE2 is still C. `string match` runs through pcre2-sys, which compiles the C library with the cc crate (Cargo.lock:982). And 4.0.1 and 4.0.2 each fixed several crashes — Rust changed the failure mode, not the existence of failures.",
         "change_trigger": "A memory-safety advisory in the C++ era would have made this the leading objective instead of a side effect."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · rust-full-port", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-full-port"],
         "claim": ("This is why Rust won the language vote. The maintainer had a working C++ threading "
                   "branch and would not propose it, because C++ cannot check what crosses a thread "
                   "boundary. Send and Sync can. First-party: 'the killer feature of Rust, from "
                   "fish-shell's perspective, is Send and Sync.'",
                   "这是 Rust 在语言投票里胜出的原因。维护者手上有一条能跑的 C++ 线程分支，但一直不肯提出来，"
                   "因为 C++ 检查不了什么东西跨过了线程边界。Send 和 Sync 能。第一方原话：'the killer feature "
                   "of Rust, from fish-shell's perspective, is Send and Sync'。"),
         "source": "doc_internal/fish-riir-plan.md:67-69 · https://fishshell.com/blog/rustport/",
         "regime": "design argument, first-party, from the maintainer who wrote both branches",
         "caveat": "The mechanism is in place and the feature is not. Issue 238 has been open since 2012-07-19, and src/builtins/exit.rs:14 still carries a TODO for concurrent mode. Three and a half years after the proposal, this is the one objective with nothing shipped against it.",
         "change_trigger": "Concurrent function execution landing in a release would move this to STRONG."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "SUPPORTS · rust-full-port", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-full-port"],
         "claim": ("The build floor moved and one dependency disappeared. At 3.6.0: a C++11 compiler, "
                   "CMake 3.5, ncurses headers and libraries. At HEAD: Rust 1.85, CMake 3.15, a C "
                   "compiler for feature detection, and no curses at all. CMakeLists.txt:5 now declares "
                   "`project(fish LANGUAGES C)`.",
                   "构建地板移动了，而且少了一个依赖。3.6.0 那时要：C++11 编译器、CMake 3.5、ncurses 的头和库。"
                   "HEAD 上要：Rust 1.85、CMake 3.15、一个用于特性探测的 C 编译器，curses 完全不需要了。"
                   "CMakeLists.txt:5 现在写的是 `project(fish LANGUAGES C)`。"),
         "source": "README.rst:114-121 at HEAD vs README.rst:150-157 at tag 3.6.0 · CMakeLists.txt:5 · CHANGELOG.rst:193, 976",
         "regime": "static build-manifest comparison across two tagged trees",
         "caveat": "The RFC promised 'After porting the C++, we'll replace CMake' at line 36. Nine .cmake files and CMakeLists.txt are still tracked, and README.rst still calls CMake the recommended path. Distributors traded a C++ toolchain for a Rust one plus 197 Cargo.lock entries.",
         "change_trigger": "Cargo becoming the sole supported build would close the second half of this objective."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · rust-full-port", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-full-port", "native-go"],
         "claim": ("The RFC ran the alternatives before writing any code and recorded why each lost. "
                   "Java and Python: startup and memory. Go: fork. D, Nim and Zig: too few contributors, "
                   "higher risk of irrelevance. That is the comparison G2 needs, done in advance rather "
                   "than reverse-engineered afterwards.",
                   "RFC 在写代码之前就把替代语言过了一遍，并写下每个为什么落选。Java 和 Python：启动和内存。"
                   "Go：fork。D、Nim、Zig：贡献者太少，语言变得无关的风险更高。G2 要的正是这种对比，而且是事先"
                   "做的，不是事后倒推的。"),
         "source": "doc_internal/fish-riir-plan.md:13-18",
         "regime": "the project's own written language selection",
         "caveat": "The contributor half of the argument is a forecast about which language attracts people. It could not be verified in advance, and the 96-to-154 movement afterwards is correlation, not proof.",
         "change_trigger": "A shell-shaped Go project solving the fork problem cleanly would weaken the exclusion of native-go."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "SUPPORTS · rust-full-port, rust-extract-leaf", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG",
         "option_ids": ["rust-full-port", "rust-extract-leaf"],
         "claim": ("A shell's compatibility surface is its observable behaviour, and fish already had it "
                   "captured. At 3.6.0 the harness was 130 littlecheck files plus 36 pexpect scripts "
                   "that run the fish binary and diff its output. None of them names an implementation "
                   "symbol. At HEAD it is 210 and 42.",
                   "shell 的兼容面就是它的可观测行为，而 fish 早就把这部分固定住了。3.6.0 时测试是 130 个 "
                   "littlecheck 文件加 36 个 pexpect 脚本，跑 fish 二进制然后 diff 输出。没有一个引用实现层的"
                   "符号。HEAD 上是 210 和 42。"),
         "source": "tests/checks/ 210 files and tests/pexpects/ 42 files at HEAD; 130 and 36 in the 3.6.0 tarball",
         "regime": "file inventory across two tagged trees",
         "caveat": "fish's other large body of code never entered scope: 72,635 lines of .fish scripts under share/ are data the shell reads at runtime. That is a property of shells, and it is the single biggest structural difference from remacs.",
         "change_trigger": "A harness that asserted on C++ internals would have had to be rebuilt first, and G4 would not have passed on day one."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-full-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full-port"],
         "claim": ("The plan wrote 'Handwaving, 6 months?' The C++ came out 338 days after the proposal "
                   "and 4.0.0 shipped 761 days after it. Between 3.7.1 and 4.0.0 there were 345 days "
                   "with no release of any kind. That is the opportunity cost, and the plan priced none "
                   "of it.",
                   "计划里写的是「Handwaving, 6 months?」。C++ 在提案后 338 天被删掉，4.0.0 在提案后 761 天"
                   "才发出去。3.7.1 到 4.0.0 之间有 345 天，一个版本都没发。这就是机会成本，而计划里一分钱"
                   "也没算。"),
         "source": "gh api commits (102ab2c90 2024-01-01, 1683e720a 2024-01-12) and releases · doc_internal/fish-riir-plan.md:73",
         "regime": "commit and release dates from the GitHub API",
         "caveat": "The 3.7 maintenance branch kept shipping through March 2024, so users were not stranded. The 1.9x code overrun sits inside the Crosslake rewrite dataset's 1.5-2x band, which makes it typical rather than exceptional.",
         "change_trigger": "Nothing reopens this; the cost is spent."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-modernize, stay-concurrent-cpp", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["stay-modernize", "stay-concurrent-cpp"],
         "claim": ("Two in-stack routes were cheaper and available. A newer C++ standard lifts the "
                   "toolchain floor. The threading branch already worked, and shipping it was weeks of "
                   "work. Each reaches one objective. Neither touches the one the RFC listed first.",
                   "栈内有两条更便宜、而且现成的路。换一个更新的 C++ 标准就能抬掉工具链地板。线程分支本来就能"
                   "跑，把它发出去是几周的活。它们各能达成一个目标。RFC 排在第一位的那个，两条都碰不到。"),
         "source": "doc_internal/fish-riir-plan.md:6, 67 · issue 238 open since 2012-07-19",
         "regime": "the RFC's own description of the alternatives it declined",
         "caveat": "The concurrency objective is still unmet under the migration too, which means stay-concurrent-cpp is the only option whose target has been reached by nobody.",
         "change_trigger": "If concurrent mode never ships, this lens becomes the strongest argument that the tiebreaker was never cashed."},
    ],

    "findings": [
        ("rust",
         ("The C++ really is gone", "C++ 真的没了"),
         ("At tag 3.6.0, three weeks before the proposal, fish carried 78,532 lines of C++ and headers "
          "across 209 files. At HEAD the count of .cpp, .cc, .cxx and .hpp files is zero, and no tracked "
          "file contains a namespace, a template, or an include of <string>, <vector> or <memory>. Two "
          "native files survive: a 100-line Objective-C launcher for the macOS .app bundle, and a "
          "284-line C test helper that exists to misbehave at fish on purpose. Neither is in the shell.",
          "在提案前三周的 3.6.0 上，fish 有 78,532 行 C++ 和头文件，分布在 209 个文件里。HEAD 上 .cpp、.cc、"
          ".cxx、.hpp 的文件数是 0，而且没有任何纳管文件里出现 namespace、template，或者 include "
          "<string>/<vector>/<memory>。留下来的原生文件有两个：一个 100 行的 Objective-C 启动器，给 macOS "
          "的 .app 包用；一个 284 行的 C 测试辅助程序，存在的意义就是故意对 fish 使坏。两个都不在 shell 里。"),
         "git ls-files | grep -cE '\\.(cpp|cc|cxx|hpp)$' → 0 · osx/osx_fish_launcher.m · tests/fish_test_helper.c"),
        ("rust",
         ("The interop scaffolding came out six days after the C++",
          "FFI 脚手架在 C++ 之后六天就拆了"),
         ("Commit 102ab2c90 removed the FFI code and the C++ files on 2024-01-01. Commit 29bd6eebd "
          "removed cxx and autocxx on 2024-01-07. The RFC had said so in advance: 'Once the port is done, "
          "we will stop using them.' What remains is a fossil. doc_internal/rust-devel.md still opens "
          "with 'fish is in the process of transitioning from C++ to Rust' and describes a fish-rust/ "
          "directory that no longer exists.",
          "commit 102ab2c90 在 2024-01-01 删掉了 FFI 代码和 C++ 文件。commit 29bd6eebd 在 2024-01-07 删掉了 "
          "cxx 和 autocxx。RFC 事先就写了这句：「Once the port is done, we will stop using them」。留下来的是"
          "一块化石。doc_internal/rust-devel.md 开头还写着「fish is in the process of transitioning from C++ "
          "to Rust」，还在介绍一个已经不存在的 fish-rust/ 目录。"),
         "gh api commits 102ab2c90, 29bd6eebd · doc_internal/rust-devel.md:7 · doc_internal/fish-riir-plan.md:44"),
        ("current",
         ("The plan said six months; deleting the C++ took 338 days and shipping took 761",
          "计划说半年；删 C++ 用了 338 天，发布用了 761 天"),
         ("The RFC's timeline section is one sentence: 'Handwaving, 6 months? Frankly unknown - there's "
          "102 remaining .cpp files of various lengths.' The C++ was deleted 338 days after the proposal "
          "opened. Shipping took 761. In between, 345 days passed with no release of any "
          "kind. Anyone quoting fish as proof that incremental ports are fast should quote the second "
          "number too.",
          "RFC 的时间线只有一句话：「Handwaving, 6 months? Frankly unknown - there's 102 remaining .cpp "
          "files of various lengths」。C++ 在提案打开后 338 天被删掉，4.0.0 在 761 天后发出。中间有 345 天，"
          "一个版本都没发。谁要拿 fish 当「增量迁移很快」的证据，第二个数字也得一起念。"),
         "doc_internal/fish-riir-plan.md:73 · gh api releases: 3.7.1 2024-03-19, 4.0.0 2025-02-27"),
        ("rust",
         ("The test suite predated the port and never changed shape",
          "测试套件在迁移之前就有，形状一直没变"),
         ("This is the part that transfers. fish's acceptance harness at 3.6.0 was 130 littlecheck files "
          "and 36 pexpect scripts, all of which launch the fish binary and compare its output. A language "
          "swap cannot invalidate a test that never looked inside. The harness grew during the port "
          "rather than being rebuilt, and stands at 210 and 42 today. Compare a project whose tests "
          "assert on internal C++ types: that project has to build the harness first.",
          "能搬走的就是这一块。fish 在 3.6.0 时的验收测试是 130 个 littlecheck 文件和 36 个 pexpect 脚本，"
          "全都是起 fish 二进制然后比对输出。一份从不往里看的测试，换语言动不了它。这套测试在迁移期间是长大的，"
          "不是重建的，今天是 210 和 42。对照那些断言内部 C++ 类型的项目：那种项目得先把测试重做一遍。"),
         "tests/checks/ 210 + tests/pexpects/ 42 at HEAD; 130 + 36 in the 3.6.0 tarball"),
        ("unknown",
         ("Concurrent mode, the reason Rust won the vote, has not shipped",
          "Rust 胜出的那条理由，并发模式，还没发"),
         ("The RFC's 'Why Rust' section rests on one thing: Send and Sync would let fish turn on "
          "concurrent function execution, which the maintainer would not do in C++. Issue 238 was opened "
          "2012-07-19 and is still open. src/builtins/exit.rs:14 carries a TODO saying that in concurrent "
          "mode `exit | sleep 1000` may not exit as hoped. The mechanism is in the tree. The feature is "
          "not, three and a half years on.",
          "RFC 的「Why Rust」那一节立在一件事上：Send 和 Sync 能让 fish 打开并发函数执行，而维护者在 C++ 里"
          "不肯做这件事。issue 238 在 2012-07-19 打开，至今还开着。src/builtins/exit.rs:14 有一条 TODO，说"
          "并发模式下 `exit | sleep 1000` 可能不会按预期退出。机制在树里，功能不在，已经三年半了。"),
         "doc_internal/fish-riir-plan.md:67-69 · src/builtins/exit.rs:14 · issue 238, open since 2012-07-19"),
    ],

    "buys": [
        (("A codebase its maintainers will work in", "一份维护者愿意动手的代码"),
         ("17 people cleared 10 commits on the C++ in 11 years. In the twelve months before the "
          "proposal, 96 distinct authors landed commits; in the twelve months after 4.0.0, 154 did. "
          "That is the objective the RFC listed first, and the only one with a number attached.",
          "11 年里，在那份 C++ 上提交过 10 次以上的有 17 个人。提案前十二个月有 96 位不同作者的提交进了树；"
          "4.0.0 之后的十二个月是 154 位。这是 RFC 排第一的目标，也是唯一挂得上数字的那个。")),
        (("The memory-unsafety class, across 78,532 lines, unasked for",
          "78,532 行里的内存不安全缺陷类，本来没人要"),
         ("fish has two published advisories and neither is a memory bug. The class went away anyway. "
          "And the unsafe count is falling, not accumulating: 420 occurrences at 4.0.0, 287 at HEAD, "
          "while the Rust grew 9.5%.",
          "fish 公开的安全公告有两条，都不是内存问题。缺陷类还是走了。而且 unsafe 是在减少，不是在堆积："
          "4.0.0 时 420 次，HEAD 上 287 次，同期 Rust 代码还多了 9.5%。")),
        (("One fewer C dependency to package", "打包时少一个 C 依赖"),
         ("ncurses and the terminfo database are both gone by 4.5.0, and CMakeLists.txt:5 now declares "
          "LANGUAGES C only. Cygwin came back once rustc gained a Cygwin target.",
          "到 4.5.0，ncurses 和 terminfo 数据库都不需要了，CMakeLists.txt:5 现在只声明 LANGUAGES C。"
          "rustc 有了 Cygwin target 之后，Cygwin 支持也回来了。")),
        (("A mechanism for the feature that was blocked", "被卡住的那个功能，机制到位了"),
         ("Send and Sync are compiler-checked, and the maintainer's stated blocker was that C++ offers "
          "nothing equivalent. Whether the feature ships is a separate question, answered below.",
          "Send 和 Sync 由编译器检查，而维护者明说过卡点就是 C++ 没有对等物。功能到底发不发，是另一个问题，"
          "下面回答。")),
    ],
    "nobuys": [
        (("Speed", "速度"),
         ("the project's own retrospective calls it parity: 'usually slightly better in terms of time "
          "taken, memory use has a slightly higher floor but a lower ceiling.' The 4.0.0 notes open by "
          "saying users should notice nothing.",
          "项目自己的回顾说这是打平：'usually slightly better in terms of time taken, memory use has a "
          "slightly higher floor but a lower ceiling'。4.0.0 的发布说明开头就写用户应该察觉不到变化。")),
        (("Concurrent mode itself", "并发模式本身"),
         ("issue 238 has been open since 2012-07-19 and still is. src/builtins/exit.rs:14 has a TODO "
          "for it. The tiebreaker that decided the language has not been cashed.",
          "issue 238 从 2012-07-19 开到现在还开着，src/builtins/exit.rs:14 里为它留着一条 TODO。决定语言的"
          "那条理由还没兑现。")),
        (("Escape from CMake", "从 CMake 里解脱"),
         ("the RFC promised 'After porting the C++, we'll replace CMake.' Nine .cmake files plus "
          "CMakeLists.txt are still tracked, and README.rst still calls CMake the recommended build.",
          "RFC 承诺过「After porting the C++, we'll replace CMake」。九个 .cmake 文件加 CMakeLists.txt "
          "还在版本库里，README.rst 也还把 CMake 称为推荐的构建方式。")),
        (("A crash-free shell", "一个不会崩的 shell"),
         ("4.0.1 and 4.0.2 each fixed several crashes. src/panic.rs:39 prints 'crashed, please report a "
          "bug' and exits. Rust changed the failure mode from undefined behaviour to a controlled abort, "
          "which is worth having and is not the same as no failures.",
          "4.0.1 和 4.0.2 各修了几个崩溃。src/panic.rs:39 打印「crashed, please report a bug」然后退出。"
          "Rust 把失败模式从未定义行为换成了受控中止，这值得有，但跟「不出错」不是一回事。")),
        (("A binary with no C in it", "一个不含 C 的二进制"),
         ("PCRE2 is still C, compiled by pcre2-sys through the cc crate. Every `string match` goes "
          "through it.",
          "PCRE2 还是 C，由 pcre2-sys 通过 cc crate 编译进来。每一次 `string match` 都要走它。")),
    ],

    "precedents": [
        {"name": "remacs · Emacs C → Rust", "outcome": "ABANDONED",
         "body": ("The same strategy, on a target an order of magnitude larger, and it died. remacs "
                  "translated Emacs primitives to Rust in place, module by module, tests green. Its own "
                  "README records the high-water mark: '642 functions in Rust and 823 in C (May 2019)' — "
                  "44% after two and a half years. Last commit April 2021. The README now opens with "
                  "'This project isn't maintained anymore.'",
                  "同一套策略，用在大一个量级的目标上，死了。remacs 就地把 Emacs 的 primitive 一个模块一个"
                  "模块翻译成 Rust，测试保持绿。它自己的 README 记下了最高水位：'642 functions in Rust and "
                  "823 in C (May 2019)'——两年半做到 44%。最后一次提交在 2021 年 4 月。README 现在开头写着"
                  "'This project isn't maintained anymore'。"),
         "match": ("identical delivery pattern: in-place incremental port to Rust of a mature C/C++ "
                   "codebase, on the main line, with an existing test suite",
                   "交付模式完全一样：把成熟的 C/C++ 代码库就地增量移植到 Rust，在主线上做，靠已有测试兜底"),
         "mismatch": ("scope, and it settles the comparison. Emacs' src/*.c is 15,511,455 bytes against fish's "
                      "2,976,090 of C++, and behind it sit 56,553,319 bytes of Elisp that are the "
                      "application. fish's 72,635 lines of share/ scripts are data the shell reads, and "
                      "never entered the port",
                      "范围，而且这是决定性的。Emacs 的 src/*.c 有 15,511,455 字节，fish 的 C++ 是 2,976,090 "
                      "字节，而 Emacs 背后还压着 56,553,319 字节的 Elisp，那才是应用本体。fish 的 72,635 行 "
                      "share/ 脚本是 shell 运行时读的数据，从来没进入迁移范围"),
         "regime": "file inventory via gh api git/trees at each project's master",
         "source_label": "first-party · project README",
         "url": "https://github.com/remacs/remacs"},
        {"name": "Mozilla · Stylo", "outcome": "MIGRATED",
         "body": ("A C++ CSS engine replaced by Rust inside a shipping Firefox, component by component, "
                  "both languages in one binary. Two engineers from late 2015, first pixels April 2016, "
                  "shipped in Firefox 57. Bobby Holley's line is the one fish's RFC could have used: "
                  "'Almost everything successful is incremental in one way or another.'",
                  "一个 C++ CSS 引擎在正在发布的 Firefox 里被 Rust 替掉，一个组件一个组件来，两种语言在同一个"
                  "二进制里。2015 年末两个工程师起手，2016 年 4 月出第一批像素，随 Firefox 57 发布。Bobby "
                  "Holley 那句话，fish 的 RFC 拿去用也合适：'Almost everything successful is incremental in "
                  "one way or another'。"),
         "match": ("in-place incremental C++ to Rust inside a live product, with rollback available at "
                   "every step",
                   "在一个活着的产品里就地把 C++ 增量换成 Rust，每一步都能回退"),
         "mismatch": ("one subsystem, not the whole implementation, and it had a measured performance "
                      "motive — parallel styling that prior C++ attempts had failed to land safely. fish "
                      "claimed no performance benefit at all",
                      "那是一个子系统，不是整个实现，而且它有可测量的性能动机——并行 styling，之前几次 C++ "
                      "尝试都没能安全落地。fish 完全没有主张性能收益"),
         "regime": "shipped in Firefox 57, Nov 2017, first-party",
         "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "curl · the hyper backend", "outcome": "ABANDONED",
         "body": ("Four years, ISRG funding, near-full test-suite parity, dropped at roughly 95%. "
                  "Stenberg named the cause and it was not technical: 'There simply were no users asking "
                  "for it and there were almost no developers interested or knowledgeable enough to work "
                  "on it.' The rustls and quiche backends survived, because they hooked in more cleanly.",
                  "四年，ISRG 出钱，测试套件接近全过，在大约 95% 的位置被砍掉。Stenberg 点明了原因，而且不是"
                  "技术原因：'There simply were no users asking for it and there were almost no developers "
                  "interested or knowledgeable enough to work on it'。rustls 和 quiche 后端活下来了，因为它们"
                  "接得更干净。"),
         "match": ("C to Rust, incremental, in place, with no user demand pulling it and a memory-safety "
                   "rationale nobody had asked for — the same starting position fish had",
                   "C 到 Rust，增量，就地做，没有用户在拉，安全理由也没人要过——fish 的起点是一样的"),
         "mismatch": ("one backend of a library rather than a whole implementation, and the outcome "
                      "inverted: curl could not staff it, while fish's author count rose from 96 to 154",
                      "那是一个库的一个后端，不是整个实现，而结果是反的：curl 招不到人，fish 的作者数从 96 "
                      "涨到 154"),
         "regime": "removed in curl 8.12.0, Feb 2025; drop announced Dec 21, 2024",
         "source_label": "first-party · maintainer blog",
         "url": "https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/"},
        {"name": "uutils coreutils", "outcome": "MIGRATED",
         "body": ("Shipped as Ubuntu 25.10's default with regressions attached: cksum up to 17x slower "
                  "than GNU on large files, base64 slower before it was faster, and md5sum behaviour "
                  "differences that broke Makeself installers. The safety rationale still stands. The "
                  "speed assumption did not.",
                  "作为 Ubuntu 25.10 的默认实现发布，同时带着回归：大文件上 cksum 比 GNU 慢到 17 倍，base64 "
                  "先慢后快，md5sum 的行为差异弄坏了 Makeself 安装包。安全理由依然成立，速度那个假设不成立。"),
         "match": ("C to Rust for a userland tool whose contract is its observable behaviour, with no "
                   "performance case made up front",
                   "把一个用户态工具从 C 换到 Rust，它的契约就是可观测行为，事先也没有立性能理由"),
         "mismatch": ("a reimplementation against a spec rather than a translation of the original "
                      "source. fish translated its own C++ line by line and put fidelity above "
                      "idiomaticity on purpose",
                      "那是照着规格重新实现，不是把原始代码翻译过来。fish 是逐行翻译自己的 C++，而且刻意把"
                      "保真放在地道之前"),
         "regime": "Ubuntu 25.10 default, third-party measurement",
         "source_label": "third-party · trade press measurement",
         "url": "https://www.phoronix.com/news/Ubuntu-Rust-Coreutils-Perf"},
    ],

    "path": [
        {"title": ("Count the surface and check the harness before writing any Rust",
                   "动手写 Rust 之前，先数清面，再看测试"),
         "body": ("Inventory the implementation and inspect what the tests actually assert on. fish had "
                  "78,532 lines of C++ across 209 files, and an acceptance harness of 130 littlecheck "
                  "files plus 36 pexpect scripts that launch the binary and diff its output. That second "
                  "number is the one that decides the project. If the tests assert on internal types, "
                  "build a behavioural harness first or stop here — a port with no black-box acceptance "
                  "gate has no way to know it is still correct. Nothing is written at this step.",
                  "把实现清点一遍，再看测试到底断言了什么。fish 有 78,532 行 C++，分布在 209 个文件里；验收"
                  "测试是 130 个 littlecheck 文件加 36 个 pexpect 脚本，起二进制然后 diff 输出。决定项目命运的"
                  "是第二个数字。如果测试断言的是内部类型，那就先把行为级测试建起来，或者就停在这里——没有黑盒"
                  "验收门的迁移，没有办法知道自己还是对的。这一步不写任何代码。"),
         "owner": "the maintainer proposing the port",
         "cost_range": ("1-2 weeks", "1-2 周"),
         "artifact": "a file and line inventory of the implementation, plus a written finding on whether the existing test suite asserts on observable behaviour or on internal types",
         "acceptance": "the harness runs the shipped binary and compares output only, with no reference to implementation symbols",
         "stop": "stop, or fund a behavioural harness first, if the tests assert on internal types",
         "rollback": "measurement only; no code changes"},
        {"title": ("Port the leaves on the main branch, both languages in one binary",
                   "在主线上先换叶子，两种语言共存于一个二进制"),
         "body": ("Work on master with no long-lived branch, and keep CI green at every commit. Start "
                  "with leaf components and move inward: fish's proposal PR shipped FLOG, the topic "
                  "monitor, wgetopt and builtin_wait, then reached execution in October 2023 and the "
                  "reader in December. Write Rust that resembles the C++ it replaces, because review and "
                  "bisect matter more than idiom at this stage. Accept FFI inefficiency only on the "
                  "understanding that it is temporary. If the bugs start living in the FFI layer rather "
                  "than in the ported code, stop and keep the hybrid. A permanent hybrid beats a stalled "
                  "port. Every commit still builds the old implementation.",
                  "在 master 上做，不开长期分支，每个 commit 都保持 CI 绿。从叶子开始往里走：fish 的提案 PR "
                  "先交了 FLOG、topic monitor、wgetopt 和 builtin_wait，2023 年 10 月做到 execution，12 月做到 "
                  "reader。写出来的 Rust 要像它替掉的那段 C++，这个阶段可审可二分比地道更重要。FFI 的低效可以"
                  "接受，前提是它是临时的。如果 bug 开始长在 FFI 层而不是移植过去的代码里，就停下来保持混合"
                  "状态——那是一个真实的结果，不是失败。每个 commit 都还能编出旧实现。"),
         "owner": "the porting contributors",
         "cost_range": ("months, per component", "数月，按组件计"),
         "artifact": "leaf components in Rust, linked into the existing binary through an FFI layer that is explicitly disposable",
         "acceptance": "the full behavioural harness passes at every commit on the primary platforms",
         "stop": "stop and keep the hybrid if defects concentrate in the FFI layer rather than the ported code",
         "rollback": "git revert per component; the previous implementation still builds"},
        {"title": ("Set the deletion date and hold it", "定下删除日期，然后守住"),
         "body": ("Name the release that removes the old language. Treat that date as a gate. fish put "
                  "it in the RFC as 'in the span of one release' and hit it. Commit 102ab2c90 removed the "
                  "FFI code and the C++ on 2024-01-01; 29bd6eebd removed cxx and autocxx six days later. The "
                  "scaffolding leaves with the old code or it becomes permanent. Budget roughly twice "
                  "what feels right; fish's own estimate was six months against 338 days. Expect a "
                  "release freeze too: 345 days passed between 3.7.1 and 4.0.0 with nothing shipped. If the "
                  "date slips twice, the remaining core is harder than the leaves were and the hybrid is "
                  "the answer.",
                  "点明哪个版本要移除旧语言，并把它当成一道门。fish 在 RFC 里写的是「in the span of one "
                  "release」，也守住了：102ab2c90 在 2024-01-01 删掉 FFI 代码和 C++，29bd6eebd 六天后删掉 cxx "
                  "和 autocxx。脚手架要么跟旧代码一起走，要么就永久留下。预算大约按感觉的两倍来——fish 自己"
                  "估半年，实际 338 天——并且要预料到发布停摆：3.7.1 到 4.0.0 之间 345 天没有任何发布。如果"
                  "日期连滑两次，说明剩下的内核比叶子难得多，答案就是保持混合。"),
         "owner": "the maintainers, collectively",
         "cost_range": ("1 release cycle; budget 2x the estimate", "一个发布周期；预算按估计的 2 倍"),
         "artifact": "a commit that deletes the last file of the old language, followed within one week by removal of the interop crates",
         "acceptance": "the harness passes with the old language absent, and the interop dependencies are gone from the lockfile",
         "stop": "keep the hybrid indefinitely if the deletion date slips twice",
         "rollback": "available at every commit until the deletion lands; after that, none"},
        {"title": ("Ship the feature you chose the language for", "把你为之选语言的那个功能发出去"),
         "body": ("A language chosen for one blocked capability is not settled until that capability "
                  "ships. Set the deadline early. fish chose Rust over Go, Zig and a modernized C++ on "
                  "one argument: "
                  "Send and Sync would make concurrent function execution reviewable. Issue 238 was "
                  "opened in 2012 and is still open, and src/builtins/exit.rs:14 still carries a TODO "
                  "for it. Set a release deadline for the capability at the same time as the port "
                  "deadline. Missing it does not undo the other benefits, which for fish landed. It "
                  "does mean the argument that decided the language was never tested.",
                  "如果选语言的理由是某个被卡住的能力，那这件事在能力发出来之前都没有定论。fish 在 Go、Zig 和"
                  "现代化 C++ 之间选 Rust，靠的是一条论证：Send 和 Sync 能让并发函数执行变得可审。issue 238 "
                  "在 2012 年打开，至今还开着，src/builtins/exit.rs:14 里还留着那条 TODO。给这个能力定一个"
                  "发布期限，和迁移期限一起定。没做到不会抹掉别的收益——fish 拿到的那些是实打实的。但它意味着"
                  "决定语言的那条论证一直没被检验。"),
         "owner": "the maintainer who proposed the port",
         "cost_range": ("1-2 releases after the port", "迁移之后 1-2 个版本"),
         "artifact": "the previously blocked capability, behind a feature flag, in a shipped release",
         "acceptance": "the capability is enabled in a release within two cycles of the port completing",
         "stop": "record the language-selection argument as untested if it has not shipped by then",
         "rollback": "feature flag; the port stands on its other benefits regardless"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("The project never credited Rust with speed. Its own retrospective reports parity, "
                   "and the 4.0.0 notes open by telling users to expect no difference. This report does "
                   "not upgrade that into a performance win.",
                   "项目从没把速度记在 Rust 头上。它自己的回顾说的是打平，4.0.0 的说明开头就叫用户别指望有"
                   "变化。这份报告没有把那句话升级成性能胜利。"),
         "evidence": "CHANGELOG.rst:727 · https://fishshell.com/blog/rustport/"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "PASS",
         "claim": ("The C++ baseline is measured at tag 3.6.0, three weeks before the proposal, not at a "
                   "convenient later point. The .cpp-only figure excluding fish_tests.cpp is 56,983 "
                   "lines, which reconciles with the project's own published '57k'.",
                   "C++ 基线量在 3.6.0 这个 tag 上，也就是提案前三周，不是挑一个后面方便的点。去掉 "
                   "fish_tests.cpp 之后只算 .cpp 是 56,983 行，和项目自己公布的「57k」对得上。"),
         "evidence": "3.6.0 tarball: 64,328 .cpp lines total, 56,983 excluding fish_tests.cpp"},
        {"name": ("Omitted cost", "被省掉的成本"), "state": "HIT",
         "claim": ("The RFC priced neither the schedule overrun nor the release freeze. Six months became "
                   "338 days to delete the C++ and 761 to ship, with 345 days of no releases in between.",
                   "RFC 既没算进度超支，也没算发布停摆。半年变成了 338 天删完 C++、761 天发出去，中间还有 "
                   "345 天一个版本都没发。"),
         "evidence": "D11 · doc_internal/fish-riir-plan.md:73 · gh api releases"},
        {"name": ("Compatibility and dual-run", "兼容与双跑"), "state": "PASS",
         "claim": ("Both languages ran in one binary for eleven months, the acceptance harness was "
                   "black-box and already existed, and the old implementation built at every commit "
                   "until 102ab2c90.",
                   "两种语言在同一个二进制里跑了十一个月，验收测试是黑盒的而且本来就有，旧实现一直到 "
                   "102ab2c90 之前每个 commit 都能编。"),
         "evidence": "D10 · doc_internal/fish-riir-plan.md:28-34 · commit 102ab2c90"},
        {"name": ("Promise not kept", "没兑现的承诺"), "state": "HIT",
         "claim": ("Two of the RFC's own commitments are outstanding. Concurrent mode, the tiebreaker "
                   "that chose Rust, has not shipped. CMake, which the RFC said would be replaced, is "
                   "still the recommended build.",
                   "RFC 自己的两条承诺还挂着。并发模式——选 Rust 的那条决胜理由——没有发出来。CMake——RFC 说"
                   "要替掉的那个——还是推荐的构建方式。"),
         "evidence": "D7, D8 · doc_internal/fish-riir-plan.md:36, 67-69 · issue 238"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("Two in-stack options are retained and priced: modernize the C++ standard, and ship "
                   "the threading branch that already worked. Neither is hypothetical.",
                   "两条栈内方案被保留并计了价：把 C++ 标准现代化，以及把那条本来就能跑的线程分支发出去。"
                   "两条都不是假想。"),
         "evidence": "D12 · options stay-modernize and stay-concurrent-cpp"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying meant 17 people in 11 years stays the number. For a volunteer project that "
                   "is the constraint that eventually ends it, and the report does not treat 18 years of "
                   "shipping C++ as evidence it would keep working.",
                   "不动，就意味着 11 年 17 个人这个数字继续保持。对一个志愿者项目来说，这是最终会把它终结的"
                   "那条约束；报告没有把 18 年一直在发 C++ 当成它还能继续的证据。"),
         "evidence": "D1 · https://fishshell.com/blog/rustport/"},
        {"name": ("Status-quo bias", "现状偏好"), "state": "HIT",
         "claim": ("'It compiles and ships' was true of the C++ throughout. It says nothing about whether "
                   "the next maintainer will show up, which is what the RFC asked about.",
                   "「能编、能发」这句话在整个 C++ 时期都成立。它说不了下一个维护者会不会出现，而 RFC 问的"
                   "正是这件事。"),
         "evidence": "D1 · D9"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report never claims Rust made fish slower or faster. It records the project's own "
                   "parity statement and names the profile that would settle it.",
                   "报告既没说 Rust 让 fish 变慢，也没说变快。它记下项目自己那句打平的表述，并点名了能了结这"
                   "件事的那份 profile。"),
         "evidence": "D3 · gap 1"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The RFC set a deletion target and the project hit it in 338 days. Compare curl's "
                   "hyper backend: four years, no date, abandoned at 95%.",
                   "RFC 定了删除目标，项目在 338 天内做到了。对照 curl 的 hyper 后端：四年，没有日期，在 "
                   "95% 的位置放弃。"),
         "evidence": "doc_internal/fish-riir-plan.md:28 · precedent: curl · the hyper backend"},
    ],

    "gaps": [
        (("A published before-and-after profile of shell startup and keystroke latency",
          "一份公开的 shell 启动与按键延迟的前后对比 profile"),
         ("The parity claim is a maintainer's prose summary, not an artifact. The repository ships a "
          "benchmark harness with 15 cases and commits no results. While that is missing, D3 stays "
          "MODERATE and D4 stays WEAK.",
          "打平这个说法是维护者的文字总结，不是可核查的产物。仓库里有一套 15 个用例的基准脚手架，但没有提交"
          "任何结果。缺着它，D3 停在 MODERATE，D4 停在 WEAK。")),
        (("Causal evidence linking the author count to the language change",
          "把作者数变化和换语言联系起来的因果证据"),
         ("96 to 154 distinct authors across matched twelve-month windows is the only number attached to "
          "the RFC's first objective, and it is correlation. Someone contributing a completion script is "
          "unlikely to care what the shell is written in.",
          "在两个对齐的十二个月窗口里，不同作者从 96 到 154，是 RFC 第一个目标唯一挂得上的数字，而它是相关性。"
          "提交一个补全脚本的人，大概不在意 shell 是用什么写的。")),
        (("Whether CI was actually green at every commit through the port",
          "迁移期间 CI 是否真的每个 commit 都绿"),
         ("The RFC required it and the project asserts it. Run-level workflow history was not checked "
          "here. It is the load-bearing G4 claim, so a reader who cares about the delivery lesson should "
          "verify it rather than take it from this report.",
          "RFC 要求过，项目也这么说。这里没有去查 workflow 的逐次运行记录。这是 G4 里吃重的一条，真在意交付"
          "这条经验的读者应该自己去核，而不是从这份报告里拿。")),
    ],

    "assumptions": [
        "The pre-port C++ baseline is measured at tag 3.6.0 (2023-01-07), three weeks before the proposal PR opened. Tags 3.7.0 and 3.7.1 are a maintenance branch carrying no Rust, so they are not the port's baseline; the 3.7.1 tree confirms this with 104 .cpp files and zero .rs files.",
        "Distinct author counts come from the GitHub commits API `author.login`, falling back to the commit author name where no account is linked. One distinct value is counted as one person, so an author using two identities counts twice.",
        "'unsafe occurrences' counts the word `unsafe` with word boundaries across all tracked .rs files including tests and build.rs. One occurrence sits in a comment. It is a count of occurrences, not of distinct unsafe blocks, and the mix at HEAD is 248 blocks, 17 `unsafe fn` and 16 `unsafe impl`.",
        "The assessment treats doc_internal/fish-riir-plan.md as the RFC and its four stated goals as the requirement, because no separate requirements document exists.",
        "Line counts for tags 3.6.0 and 4.0.0 come from source tarballs fetched through `gh api`; byte-level comparisons against Emacs and remacs come from the git trees API, where sizes are bytes rather than lines and are labelled as such.",
    ],
    "objective": {
        "driver": "maintainability and contributor supply",
        "requirement": "move fish's implementation off C++ to widen the contributor pool, lift the C++11/CMake/ncurses toolchain floor, and obtain compiler-checked thread safety for concurrent function execution",
        "baseline": "78,532 lines of C++ and headers across 209 files at tag 3.6.0; 17 people had made 10 or more commits to that code in 11 years; no memory-safety advisory exists in fish's published history",
        "target": "zero C++ in the shell, tests green at every commit, delivered within one release cycle",
    },
    "repository": {
        "path": "https://github.com/fish-shell/fish-shell",
        "commit": "9654f5e4bd00066e8d0db7fdb66e7b12458f8f4e",
        "scope": "whole repository; the shell implementation is the assessed target",
        "sampling": "shallow clone at 9654f5e, 2,205 tracked files enumerated; src/, crates/, tests/, share/, cmake/ and doc_internal/ measured; the pre-port baseline and the 4.0.0 snapshot from source tarballs fetched via gh api; history, releases, advisories and author counts from the GitHub API; no build, test or benchmark was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "fish-shell/fish-shell at 9654f5e · static read-only analysis · why-not-rust method 2.0",
        "fish-shell/fish-shell @ 9654f5e · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/fish-shell/fish-shell at commit 9654f5e, shallow clone, 2,205 tracked "
        "files. Scope: the whole repository, with the shell implementation as the target. This is a "
        "retrospective assessment of a completed migration, so the gates are run against the decision as "
        "it stood in January 2023 and the outcome is checked against what the project said it would buy. "
        "Sampling: at HEAD, 218 tracked .rs files hold 103,667 lines (89,836 in src/, 13,627 across 21 "
        "workspace crates). Zero files match .cpp, .cc, .cxx or .hpp, and no tracked file contains a "
        "namespace, template, or an include of <string>, <vector> or <memory>. Two native files remain: "
        "osx/osx_fish_launcher.m at 100 lines, the launcher stub for the macOS .app bundle, and "
        "tests/fish_test_helper.c at 284 lines, a dependency-free program that mimics awkward child "
        "processes so fish can test job control against it. At 4.0.0 there were three, including a "
        "182-line src/libc.c that has since gone. Counting bases are stated wherever a comparison "
        "appears and are never mixed. The pre-port C++ baseline is 78,532 lines across 209 files at tag "
        "3.6.0, split 64,328 lines in 104 .cpp files and 14,204 in 105 .h files; excluding the 7,345-line "
        "fish_tests.cpp gives 56,983, which reconciles with the project's own published '57k'. Rust at "
        "tag 4.0.0 was 94,638 lines in 194 files, so the growth to HEAD is 9.5%. Over the same span "
        "`unsafe` occurrences fell from 420 to 287 across 58 of 218 files. The scripting layer was never "
        "in scope: 72,635 lines of .fish under share/ are data the shell reads at runtime, and that is "
        "the structural difference from remacs, where 56,553,319 bytes of Elisp sit behind the C being "
        "ported. Timeline from the GitHub API: PR 9512 opened 2023-01-28; commit 102ab2c90 removed the "
        "FFI code and the C++ on 2024-01-01, 338 days later; 29bd6eebd removed cxx and autocxx on "
        "2024-01-07; 4.0.0 shipped 2025-02-27, 761 days after the proposal, against an RFC estimate of "
        "'Handwaving, 6 months?'. Between 3.7.1 (2024-03-19) and 4.0.0 there were 345 days with no "
        "release. Distinct commit authors: 96 in the twelve months to 2023-01-28, 154 in the twelve "
        "months from 2025-02-27. Objective: taken from doc_internal/fish-riir-plan.md, the project's own "
        "RFC, since no separate requirements document exists. User-supplied facts: none. No Amdahl "
        "calculation appears, because no performance requirement was ever stated and substituting a "
        "line-count share for a time share would be a method error. The decision turns on G1 and G4, "
        "both on directly measured facts; G3 passes on a structural argument, since no in-stack option "
        "changes which language contributors are asked to write. Confidence is MEDIUM rather than HIGH "
        "because the benefit that justified the work is corroborated by a correlational author count, "
        "and because concurrent function execution — the argument that selected Rust over the "
        "alternatives — has still not shipped. This is a structured decision protocol, not a statistical "
        "predictor.",
        "仓库：github.com/fish-shell/fish-shell，commit 9654f5e，shallow clone，2,205 个纳管文件。范围：整个"
        "仓库，评估目标是 shell 实现本体。这是对一次已完成迁移的回溯评估，所以四道门是按 2023 年 1 月那个"
        "时点的决策来跑的，结果则拿项目自己说要买到的东西来对。采样：HEAD 上 218 个纳管 .rs 文件共 103,667 "
        "行（src/ 里 89,836 行，21 个 workspace crate 里 13,627 行）。匹配 .cpp、.cc、.cxx、.hpp 的文件数为 0，"
        "并且没有任何纳管文件里出现 namespace、template，或 include <string>/<vector>/<memory>。留下两个原生"
        "文件：osx/osx_fish_launcher.m，100 行，macOS .app 包的启动壳；tests/fish_test_helper.c，284 行，一个"
        "不依赖 fish 的小程序，专门装成各种别扭的子进程，好让 fish 拿它测作业控制。4.0.0 时还有第三个，182 行"
        "的 src/libc.c，后来也没了。凡是出现对比的地方都写明口径，绝不混用。迁移前的 C++ 基线是 3.6.0 这个 tag "
        "上 209 个文件、78,532 行，其中 104 个 .cpp 共 64,328 行，105 个 .h 共 14,204 行；扣掉 7,345 行的 "
        "fish_tests.cpp 得到 56,983 行，和项目自己公布的「57k」对得上。4.0.0 上的 Rust 是 194 个文件、94,638 "
        "行，到 HEAD 增长 9.5%。同一区间里，`unsafe` 出现次数从 420 降到 287，分布在 218 个文件中的 58 个。"
        "脚本层从来不在范围内：share/ 下 72,635 行 .fish 是 shell 运行时读取的数据，这正是和 remacs 的结构性"
        "差别——remacs 要移植的那些 C 后面压着 56,553,319 字节的 Elisp。时间线取自 GitHub API：PR 9512 在 "
        "2023-01-28 打开；commit 102ab2c90 在 2024-01-01 删掉 FFI 代码和 C++，距提案 338 天；29bd6eebd 在 "
        "2024-01-07 删掉 cxx 和 autocxx；4.0.0 在 2025-02-27 发布，距提案 761 天，而 RFC 的估计是「Handwaving, "
        "6 months?」。3.7.1（2024-03-19）到 4.0.0 之间有 345 天没有任何发布。不同提交作者数：到 2023-01-28 的"
        "十二个月里 96 位，从 2025-02-27 起的十二个月里 154 位。目标：取自 doc_internal/fish-riir-plan.md，也"
        "就是项目自己的 RFC，因为没有单独的需求文档。用户提供的事实：无。本报告没有 Amdahl 计算，因为从头到尾"
        "没有人提出性能需求，而拿代码行数占比顶替时间占比是方法错误。决策落在 G1 和 G4 上，两道门都基于直接"
        "测量的事实；G3 通过靠的是结构性论证——没有任何栈内方案能改变「请贡献者写哪门语言」这件事。置信度给 "
        "MEDIUM 而不是 HIGH，一是支撑这笔投入的收益只有一个相关性的作者数在佐证，二是并发函数执行——那条让 "
        "Rust 赢过其他候选的论证——至今没有发出来。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 9654f5e · baselines from gh api tarballs · no build, benchmark or network call against the target",
        "公开仓库 · 在 commit 9654f5e 上做静态分析 · 基线取自 gh api 下载的源码包 · 没有对目标做构建、基准或网络调用",
    ),
}
