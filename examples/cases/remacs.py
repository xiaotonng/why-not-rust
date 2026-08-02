"""remacs/remacs — the port that ran to the end and still left 309,205 lines of C.

Repository facts were measured read-only on the shallow clone named in
`repository`. History, contributor and pull-request facts come from the GitHub
API, because the clone is `--depth 1`.
"""

CASE = {
    "slug": "remacs",
    "project_name": "remacs/remacs",
    "project_desc": (
        "Rust · in-place port of GNU Emacs 26.2.90 · 30,133 lines of Rust against 309,205 lines of C in src/",
        "Rust · GNU Emacs 26.2.90 的就地移植 · 30,133 行 Rust，对面是 src/ 里 309,205 行 C",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · incremental in-place port of a 40-year-old C core inside a hard fork",
        "原生桌面 GUI · 在硬分叉里对一套四十年历史的 C 内核做渐进式就地移植",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "stay-native-comp",
    "scope_chip": (
        "keep the C core; move the work into natively-compiled Lisp instead",
        "保留 C 内核；把工作挪进原生编译的 Lisp",
    ),
    "scope_sub": (
        "the experiment already ran; it ran out of people before it ran out of C",
        "这个实验已经跑完了；先没的是人，不是 C",
    ),

    "why": (
        "remacs ran this experiment to the end. Four years and four months, 268 contributors, 902 merged "
        "pull requests. What came out is 26,825 lines of converted Emacs behaviour against 309,205 lines "
        "of C still sitting in src/, and five of 126 C files retired. The wall was where the maintainers "
        "said it was: the collector and the loader are C tricks, and Rust holding Lisp objects that a C "
        "collector traces is not memory-safe. 919 unsafe sites in the ported code say the same thing.",
        "remacs 把这个实验做完了。四年四个月，268 个贡献者，902 个合并的 PR。最后的产出是 26,825 行转换过的 "
        "Emacs 行为，对面还站着 src/ 里 309,205 行 C；126 个 C 文件里退役了 5 个。墙就在维护者说的那个位置："
        "收集器和加载器是 C 的把戏，而 Rust 拿着一个由 C 收集器遍历的 Lisp 对象，谈不上内存安全。移植后的代码"
        "里有 919 处 unsafe，说的是同一件事。",
    ),
    "trigger": (
        "Stable. The in-place port reopens only if Rust gains a way to let a foreign collector trace "
        "objects the borrow checker owns. That is a language-level change, not a project decision. "
        "Nothing in the Emacs tree moves it.",
        "结论稳定。就地移植要重开，前提是 Rust 能让一个外部收集器去遍历 borrow checker 所有的对象。那是语言层"
        "面的改动，不是项目层面的决定。Emacs 这棵树里没有任何东西能推动它。",
    ),

    "gates": [
        {"id": "G1", "state": "UNKNOWN", "short": ("Requirement", "需求"),
         "hero_evidence": ("No target was ever named. The README argues tooling and ecosystem.",
                           "从没定过目标。README 讲的是工具链和生态。"),
         "name": "requirement",
         "evidence": "README.md:82-106 'Why Rust?' lists learning curve, tooling, packaging, C interop and compile-time checks. No SLO, no memory-safety incident record, no cost figure, no threshold. A latent safety requirement does exist at the C trust boundary, but remacs never stated it and G2 shows the port could not deliver it."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果"),
         "hero_evidence": ("A C collector traces the Lisp objects Rust holds. The compiler cannot see them.",
                           "Rust 手里的 Lisp 对象由 C 的收集器遍历，编译器看不见它们。"),
         "name": "rust-specific causality",
         "evidence": "Issue #1532, opened by a contributor 2019-08-02: 'we're back to the C world of \"If you don't want memory corruption you have to be really careful, the compiler won't keep you safe\"'. 164 staticpro GC-root registrations live in src/*.c; the ported Rust carries 919 unsafe occurrences across 66 of its 75 files. The mechanism Rust is bought for does not survive inside a C-managed heap."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("Four years, 268 contributors, five C files retired.",
                           "四年，268 个贡献者，退役 5 个 C 文件。"),
         "name": "economics and smallest sufficient option",
         "evidence": "26,825 lines of converted behaviour after 902 merged pull requests, against 309,205 lines of C still in src/*.c. Upstream Emacs reached a comparable goal without a fork: 28.1 shipped native compilation of Lisp on 2022-04-03. Two smaller Rust options meet more of the objective at a fraction of the cost: the dynamic module ABI, and single leaf-file extraction."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("The fork could not track upstream, and the port broke on macOS.",
                           "分叉跟不上上游，移植又在 macOS 上坏了。"),
         "name": "delivery and reversibility",
         "evidence": "Maintainer, issue #1571 2020-04-12: 'we have to update remacs for code by many more people that lands in upstream' and 'It's work that doesn't really pay off'. Another, 2020-04-27: 'We have a mix up in our port blocking usage on current MacOS... It has proven hard to identify exactly what is wrong.' The ported C was deleted rather than gated, so there was no rollback; the reboot branch that tried ifdefs instead stopped on 2020-03-16."},
    ],

    "tiles": [
        (("Emacs behaviour converted", "转换过的 Emacs 行为"), "26,825", ("lines", "行"),
         ("30,133 lines of Rust minus 3,308 of port machinery", "30,133 行 Rust 减去 3,308 行移植脚手架")),
        (("C still standing in src/", "src/ 里还立着的 C"), "309,205", ("lines", "行"),
         ("119 files, unchanged basis: git ls-files 'src/*.c'", "119 个文件，同一口径：git ls-files 'src/*.c'")),
        (("Lisp primitives moved", "搬走的 Lisp primitive"), "666 of 1,414", ("47%", "47%"),
         ("the project's own scoreboard: #[lisp_fn] vs DEFUN", "项目自己的计分板：#[lisp_fn] 对 DEFUN")),
        (("C files the port retired", "移植真正退役的 C 文件"), "5 of 126", ("files", "个"),
         ("four more went with MS-DOS support, not with Rust", "另有 4 个是随 MS-DOS 支持一起走的，不是 Rust 的功劳")),
        (("unsafe in the ported Rust", "移植代码里的 unsafe"), "919", ("occurrences", "处"),
         ("in 66 of 75 files under rust_src/src", "分布在 rust_src/src 的 75 个文件里的 66 个")),
        (("Elapsed before 'not maintained'", "走到「不再维护」用了"), "4 yr 4 mo", ("2016–2021", "2016–2021"),
         ("created 2016-11-22 · README notice 2021-04-07", "2016-11-22 建库 · 2021-04-07 README 公告")),
    ],

    "options_sub": (
        "Every option is judged against one objective: cut the memory-unsafety and maintenance exposure of "
        "Emacs's C core without breaking 1,507,964 lines of Emacs Lisp that depend on the observable "
        "behaviour of its primitives.",
        "所有方案对着同一个目标：降低 Emacs C 内核的内存不安全与维护暴露，同时不破坏那 1,507,964 行依赖 "
        "primitive 可观测行为的 Emacs Lisp。",
    ),
    "options": [
        {"id": "stay-native-comp", "name": ("Keep the C core; native-compile Lisp",
                                           "保留 C 内核，把 Lisp 原生编译"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("shipped upstream 2022-04-03 with no fork",
                              "2022-04-03 已在上游发布，不需要分叉"),
         "one_time_cost": "already paid upstream", "recurring_cost": "libgccjit as an optional build dependency",
         "cost_cell": ("already paid; optional libgccjit", "已经付过；libgccjit 可选"),
         "time_to_value": ("shipped", "已发布"),
         "compatibility": "native", "compat_cell": ("native · configure flag", "原生 · configure 开关"),
         "reversibility": "build flag",
         "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · the goal remacs wanted, reached without a fork",
                  "推荐 · remacs 想要的效果，不分叉也拿到了"),
         "reason": "Emacs 28.1 (2022-04-03) added native compilation of Lisp files, which moves performance-sensitive work out of C into compiled Lisp. It reduces C's role without a fork, without a second toolchain, and without touching primitive semantics."},
        {"id": "rust-module", "name": ("Rust behind the dynamic module ABI", "Rust 藏在动态模块 ABI 后面"),
         "implementation": "rust",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("new functionality in Rust, no core change",
                              "新功能用 Rust 写，内核不动"),
         "one_time_cost": "per module", "recurring_cost": "module maintained outside the Emacs tree",
         "cost_cell": ("per module; maintained outside the tree", "按模块计；在主树之外维护"),
         "time_to_value": ("days per module", "每个模块数天"),
         "compatibility": "the published module ABI",
         "compat_cell": ("stable ABI · unload the module", "ABI 稳定 · 卸掉模块即可"),
         "reversibility": "delete the .so", "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · what remacs's own README now points people to",
                  "保留 · remacs 自己的 README 现在指的就是这条路"),
         "reason": "src/emacs-module.c (1,274 lines) and src/emacs-module.h.in already expose a supported ABI, enabled by default wherever dlopen exists. It adds Rust without a fork, which is the shape the successor project chose."},
        {"id": "rust-leaf-extract", "name": ("Port one leaf C file behind its existing API",
                                            "把一个叶子 C 文件搬到 API 背后"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed in that one file; remacs proved five",
                              "那一个文件里缺陷类消失；remacs 已经证明了 5 个"),
         "one_time_cost": "weeks per file plus a parity harness", "recurring_cost": "a Rust toolchain in every Emacs build",
         "cost_cell": ("weeks per file; Rust in every build", "每个文件数周；每次构建都要 Rust"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "same C symbols, same docstrings",
         "compat_cell": ("same symbols · keep the C behind a flag", "符号不变 · C 用开关留着"),
         "reversibility": "build flag, if the C is kept", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the part of remacs that actually worked",
                  "保留 · remacs 里真正成立的那一部分"),
         "reason": "floatfns.c, marker.c, cmds.c, casetab.c and decompress.c are gone from src/ and live in Rust. The method works on files whose functions do not hold a Lisp object across a collection point. It does not scale to the collector or the loader."},
        {"id": "rust-inplace-port", "name": ("Port the C core to Rust in place, in a fork",
                                            "在分叉里就地把 C 内核移植成 Rust"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("measured: 26,825 lines and 5 files in 4 yr 4 mo",
                              "实测：四年四个月，26,825 行、5 个文件"),
         "one_time_cost": "268 contributors, 902 merged PRs, 4 yr 4 mo", "recurring_cost": "tracking every upstream Emacs commit forever",
         "cost_cell": ("4 yr 4 mo; a permanent merge tax", "四年四个月；永久的合并税"),
         "time_to_value": ("never reached", "没走到"),
         "compatibility": "1,507,964 lines of Emacs Lisp, bug-for-bug",
         "compat_cell": ("all of elisp · C deleted, no rollback", "整个 elisp · C 已删除，无法回滚"),
         "reversibility": "none", "evidence_strength": "STRONG", "disposition": "exclude",
         "note": ("exclude · the experiment ran and is documented",
                  "排除 · 实验跑过了，而且有记录"),
         "reason": "This is the assessed proposal, and remacs is its completed trial. It fails G2 on the collector, G3 on four years of output, and G4 on the merge tax and a macOS breakage nobody could locate."},
        {"id": "adopt-rust-editor", "name": ("Use a Rust editor instead", "干脆换一个 Rust 写的编辑器"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for that user; no Emacs Lisp",
                              "对那个用户缺陷类消失；但没有 Emacs Lisp"),
         "one_time_cost": "per user, relearning", "recurring_cost": "a different package ecosystem",
         "cost_cell": ("per user; a different ecosystem", "按用户计；换一套生态"),
         "time_to_value": ("days per user", "每个用户数天"),
         "compatibility": "none with elisp",
         "compat_cell": ("no elisp · switch back any time", "不兼容 elisp · 随时切回"),
         "reversibility": "switch back", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · a user's decision, not the project's",
                  "保留 · 这是用户的决定，不是项目的决定"),
         "reason": "Meets a single user's safety and performance preferences immediately. It abandons 1,507,964 lines of Emacs Lisp, so it answers a different question than the one the project faces."},
    ],

    "lenses_sub": (
        "These states are scoped to named options and do not add up to a score. Most of them are unusually "
        "strong for this method, because remacs is not a forecast. The experiment finished, and the "
        "maintainers wrote down what happened.",
        "每条状态都绑定到具体方案，不是可以相加的分数。这里的证据强度比这套方法平常拿到的高，因为 remacs 不是"
        "预测。实验做完了，维护者也把过程写下来了。",
    ),
    "na_note": (
        "Two lenses are N/A. D4 fleet footprint: Emacs is one process on one desktop, so there is no fleet "
        "to price. D3 tail latency: no option changes the collector, which stays C in all five.",
        "两条记为 N/A。D4 机队占用：Emacs 是一台桌面上的一个进程，没有机队可算。D3 尾延迟：五个方案都不改收集"
        "器，它在每个方案里都还是 C。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "UNKNOWN · rust-inplace-port", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-inplace-port"],
         "claim": ("The README's case for Rust is learning curve, tooling, packaging, C interop and "
                   "compile-time checks. All five are developer-experience arguments. No SLO appears, no "
                   "vulnerability record, no cost ceiling. Nothing here has a number to beat.",
                   "README 给 Rust 的理由是：学习曲线、工具链、打包、和 C 的互操作、编译期检查。这五条都是开发"
                   "体验层面的论证。没有 SLO，没有漏洞记录，没有成本上限。这里没有一个可以去打的数字。"),
         "source": "README.md:82-106 'Why Rust?' section",
         "regime": "stated project rationale, not a measurement",
         "caveat": "A latent safety requirement does exist: Emacs parses untrusted files, images and TLS streams in C. remacs never named it as the driver, and D6 shows the in-place port could not deliver it.",
         "change_trigger": "The requirement becomes assessable once a threshold is stated: a CVE class count, a startup budget, or a maintenance cost."},
        {"id": "D2", "name": ("Reachable end-to-end impact", "端到端影响面"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("The port advanced by moving DEFUNs, so its reach is bounded by where DEFUNs live. 49 of "
                   "the 119 remaining C files hold none at all, which is 77,047 lines. 82 files hold five "
                   "or fewer: 123,817 lines, 40% of src/. xdisp.c is 33,281 lines and 14 primitives.",
                   "移植的推进方式是搬 DEFUN，所以它能碰到哪里，取决于 DEFUN 在哪里。剩下 119 个 C 文件里有 49 "
                   "个一个 DEFUN 都没有，合计 77,047 行。82 个文件的 DEFUN 不超过 5 个：123,817 行，占 src/ 的 "
                   "40%。xdisp.c 是 33,281 行、14 个 primitive。"),
         "source": "git ls-files 'src/*.c' | xargs grep -c '^DEFUN' · line counts by wc -l",
         "regime": "static structure at commit a684a4c",
         "caveat": "This is a line share, not a time share, and it is not converted into one. No Amdahl figure appears in this report because the proposal never stated a performance objective.",
         "change_trigger": "A porting method that reached non-DEFUN machinery would change this bound. Nobody has proposed one."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Emacs runs a C mark-and-sweep collector. No option on the table replaces it, so "
                   "collector-induced pauses are identical across all five. There is nothing to compare.",
                   "Emacs 跑的是 C 写的 mark-and-sweep 收集器。桌面上没有任何方案要换掉它，所以收集器引起的停顿"
                   "在五个方案里完全一样，没有可比的东西。"),
         "source": "src/alloc.c · 164 staticpro GC-root registrations across src/*.c",
         "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Emacs is one long-lived process on one person's machine. There is no fleet, no "
                   "per-instance cost curve, and no compute bill that a language change would move.",
                   "Emacs 是某个人机器上的一个常驻进程。没有机队，没有单实例成本曲线，也没有一张换语言就能压下"
                   "来的算力账单。"),
         "source": "desktop application, single process", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup & load shape", "启动与加载形态"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("Emacs boots by dumping a pre-loaded image, and on macOS that is src/unexmacosx.c, 1,408 "
                   "lines. Rust had to be bent around it. rust_src/alloc_unexecmacosx exists only to route "
                   "Rust's global allocator through unexec_malloc, and it needs a nightly-only feature to "
                   "do so.",
                   "Emacs 的启动方式是把预加载好的镜像 dump 出来，在 macOS 上就是 src/unexmacosx.c，1,408 行。"
                   "Rust 得绕着它拧。rust_src/alloc_unexecmacosx 存在的唯一目的，就是把 Rust 的全局分配器接到 "
                   "unexec_malloc 上，而这需要一个只有 nightly 才有的特性。"),
         "source": "rust_src/alloc_unexecmacosx/src/lib.rs:1 #![feature(allocator_api)] · src/unexmacosx.c",
         "regime": "structural, at the dump boundary",
         "caveat": "A maintainer described the same problem more broadly in issue #1571: 'Emacs uses some C tricks to make its lisp compilation work and to load faster... Rust's memory model and other bits make this a non-trivial change.'"},
        {"id": "D6", "name": ("Safety & correctness — the collector", "安全与正确性：收集器"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("Ported Rust holds Lisp_Objects. A C collector traces them through 164 staticpro roots "
                   "the borrow checker never sees, so a live object reachable only from Rust can be freed. "
                   "The contributor who found it put it plainly: the compiler will not keep you safe.",
                   "移植后的 Rust 手里拿着 Lisp_Object。C 的收集器通过 164 个 staticpro 根去遍历它们，而 borrow "
                   "checker 从来看不到这些根，于是一个只能从 Rust 到达的活对象是会被回收的。发现这件事的贡献者"
                   "说得很直白：编译器保不住你。"),
         "source": "issue #1532 (2019-08-02, open) · 919 unsafe occurrences in 66 of 75 files under rust_src/src",
         "regime": "first-party maintainer analysis on the target",
         "caveat": "A second contributor went further: 'Garbage collection fundamentally collides with the \"single owner\" concept of Rust.' The mitigation discussed was to ban Rust heap allocation, not to fix the model.",
         "change_trigger": "Rust would need a way to let a foreign collector trace owned objects. That is a language change, not a project decision."},
        {"id": "D6", "name": ("Safety & correctness — clean seams", "安全与正确性：干净的接缝"),
         "label": "SUPPORTS · rust-module, rust-leaf-extract", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-module", "rust-leaf-extract"],
         "claim": ("Where the seam is clean, the benefit is real. Five C files left src/ for Rust and stayed "
                   "gone: floatfns.c, marker.c, cmds.c, casetab.c, decompress.c. Their functions do not hold "
                   "a Lisp object across a collection point. That is the shape that worked.",
                   "接缝干净的地方，收益是实的。五个 C 文件离开 src/ 换成了 Rust，而且没有回来：floatfns.c、"
                   "marker.c、cmds.c、casetab.c、decompress.c。它们的函数不会跨着一次回收持有 Lisp 对象。这就是"
                   "成立的那种形状。"),
         "source": "diff of git ls-files 'src/*.c' against the emacs-26.2 src tree via GitHub API",
         "regime": "static file inventory, two trees compared",
         "caveat": "Four more C files also disappeared: dosfns.c, msdos.c, w16select.c, unexcoff.c. Those went with dropped MS-DOS support, not with Rust. They are not counted as conversions."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-inplace-port"],
         "claim": ("Rust's concurrency story is the one benefit Emacs cannot spend. Elisp semantics assume a "
                   "single thread of execution, and src/thread.c is cooperative by design. Issue #701, "
                   "'What's the plan for multithreading?', was opened in March 2018 and never answered.",
                   "Rust 的并发这条，恰好是 Emacs 花不出去的。Elisp 的语义假定只有一条执行线，src/thread.c 本身"
                   "就是协作式的。issue #701「What's the plan for multithreading?」2018 年 3 月开的，一直没有"
                   "答案。"),
         "source": "src/thread.c (1,029 lines, 15 DEFUN) · issue #701 (2018-03-25, open)",
         "regime": "language semantics plus open issue",
         "caveat": "Breaking the single-thread assumption changes observable elisp behaviour in any language. Rust does not make that decision cheaper."},
        {"id": "D8", "name": ("Distribution & build", "分发与构建"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("The port could not be built on stable Rust. rust-toolchain pins nightly-2020-08-14, and "
                   "the code opens 9 unstable feature gates. Every Emacs packager on every platform would "
                   "have needed that exact nightly. Emacs's own C build needs no such pin.",
                   "这份移植没法用 stable Rust 构建。rust-toolchain 钉的是 nightly-2020-08-14，代码里开了 9 个"
                   "不稳定特性开关。每个平台上的每个 Emacs 打包者都得凑出那一个具体的 nightly。Emacs 自己的 C "
                   "构建不需要这种钉法。"),
         "source": "rust-toolchain · 9 occurrences of #![feature( across tracked .rs files",
         "regime": "build requirement in this commit",
         "caveat": "The module-ABI option avoids this entirely: a Rust module is built by its own author, not by every Emacs distributor."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · rust-module, rust-leaf-extract", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-module", "rust-leaf-extract"],
         "claim": ("The ecosystem argument held up. remacs pulled base64, flate2, md5, sha1, sha2, rand and "
                   "itertools from crates.io, and those crates are what let five C files go. The pull is "
                   "toward leaf functionality, which is where the wins landed.",
                   "生态这条论证站住了。remacs 从 crates.io 拉了 base64、flate2、md5、sha1、sha2、rand、"
                   "itertools，正是这些 crate 让 5 个 C 文件走掉的。这股拉力指向叶子功能，收益也确实落在那里。"),
         "source": "rust_src/Cargo.toml.in dependency list",
         "regime": "declared dependencies in this commit",
         "caveat": "None of these crates helps with the collector, the loader, the display engine or the bytecode interpreter, which is where the remaining C mass sits."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("1,507,964 lines of Emacs Lisp across 1,733 files depend on how these primitives behave, "
                   "docstrings included. A maintainer named the standard in 2023: 'Rewriting the elisp "
                   "engine is going to be fun because you need to be bug compatible.' There is no spec.",
                   "1,733 个文件、1,507,964 行 Emacs Lisp 依赖这些 primitive 的行为，连 docstring 都算在内。"
                   "维护者 2023 年把标准说了出来：'Rewriting the elisp engine is going to be fun because you "
                   "need to be bug compatible.' 而这件事没有规格书。"),
         "source": "git ls-files '*.el' | xargs wc -l · issue #1571 comment 2023-09-16",
         "regime": "static inventory plus maintainer statement",
         "caveat": "The macOS GUI was never touched by the port at all: 51 DEFUNs still sit in Objective-C under src/*.m, across 21,340 lines."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-inplace-port", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-inplace-port"],
         "claim": ("268 contributors and 902 merged pull requests bought 26,825 lines of converted "
                   "behaviour and five retired C files. Then the merge tax closed it: 'we have to update "
                   "remacs for code by many more people that lands in upstream'. Merged PRs went 372, 197, "
                   "15, 0.",
                   "268 个贡献者、902 个合并的 PR，买到 26,825 行转换过的行为和 5 个退役的 C 文件。然后合并税把"
                   "它关掉了：'we have to update remacs for code by many more people that lands in "
                   "upstream'。合并 PR 数是 372、197、15、0。"),
         "source": "GitHub API: contributors, search/issues merged per year · issue #1571 comment 2020-04-12",
         "regime": "GitHub API at 2026-08-02, shallow clone so local git log is unusable",
         "caveat": "The same maintainer added 'It's work that doesn't really pay off.' Nobody in the thread disputed the arithmetic."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-native-comp", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-native-comp", "rust-module"],
         "claim": ("Upstream reached a version of the goal without forking anything. Emacs 28.1 shipped on "
                   "2022-04-03 with native compilation of Lisp files, one year after remacs's README "
                   "declared the port unmaintained. A contributor had predicted exactly that in the same "
                   "thread.",
                   "上游没有分叉任何东西，就拿到了目标的一个版本。Emacs 28.1 在 2022-04-03 发布，带上了 Lisp 文"
                   "件的原生编译；那是 remacs 的 README 宣布移植不再维护之后一年。同一个帖子里已经有贡献者预"
                   "见到了这一点。"),
         "source": "emacs-mirror/emacs tag emacs-28.1 (2022-04-03) · etc/NEWS:21 'Emacs now optionally supports native compilation of Lisp files' · issue #1571 comment 2020-05-02",
         "regime": "upstream release artifact, verified via GitHub API",
         "caveat": "Native compilation is a performance and C-footprint answer, not a memory-safety answer. The safety question at the C trust boundary stays open, which is why the extraction and module options are retained."},
    ],

    "findings": [
        ("rust",
         ("The compiler cannot see the objects the collector frees",
          "收集器要回收的那些对象，编译器看不见"),
         ("A contributor opened issue #1532 in August 2019 after a crash: Rust code was holding a Lisp "
          "object that the C collector could not find, so it got freed while live. His summary was that "
          "they were back in the C world, where the compiler will not keep you safe. 164 staticpro roots "
          "sit in the C. The ported Rust carries 919 unsafe sites. This is the gate the port failed.",
          "2019 年 8 月，一个贡献者在一次崩溃之后开了 issue #1532：Rust 代码持有一个 C 收集器找不到的 Lisp 对"
          "象，于是它在活着的时候被回收了。他的总结是，他们又回到了 C 的世界，编译器保不住你。164 个 staticpro "
          "根在 C 那边。移植出来的 Rust 里有 919 处 unsafe。这就是移植没过的那道门。"),
         "issue #1532 (open) · 919 unsafe in 66 of 75 files under rust_src/src"),
        ("current",
         ("Four years and four months bought five C files",
          "四年四个月，换来 5 个 C 文件"),
         ("Upstream Emacs 26.2 has 126 C files in src/. remacs has 119. Five of the missing ones went to "
          "Rust — floatfns, marker, cmds, casetab, decompress. Four went with MS-DOS support, which is not "
          "a Rust result. Against that, 309,205 lines of C are still in src/, and 26,825 lines of converted "
          "behaviour sit beside them.",
          "上游 Emacs 26.2 的 src/ 里有 126 个 C 文件，remacs 有 119 个。少掉的里面有 5 个是去了 Rust——"
          "floatfns、marker、cmds、casetab、decompress。另外 4 个是随 MS-DOS 支持一起走的，那不算 Rust 的成"
          "果。对面，309,205 行 C 还在 src/ 里，旁边放着 26,825 行转换过的行为。"),
         "git ls-files 'src/*.c' vs emacs-26.2 src tree · 119 files against 126"),
        ("current",
         ("They ported 47% of the primitives and 8% of the code",
          "primitive 搬了 47%，代码只动了 8%"),
         ("The project kept its own scoreboard in the README: functions in Rust versus functions in C. At "
          "the final commit it reads 666 to 748, so 47% of Lisp-callable primitives had moved. The line "
          "count tells the other half of the story. Small primitives are cheap and there are many of them; "
          "xdisp.c is 33,281 lines and holds 14.",
          "项目在 README 里自己记着分：Rust 里多少函数，C 里多少函数。到最后一个 commit 是 666 对 748，也就是 "
          "47% 的可被 Lisp 调用的 primitive 已经搬走了。行数讲的是故事的另一半。小 primitive 便宜，而且数量多；"
          "xdisp.c 有 33,281 行，里面装着 14 个。"),
         "666 #[lisp_fn] in rust_src/src · 748 ^DEFUN in src/*.c · README.md:243"),
        ("current",
         ("The fork could not afford to track upstream",
          "分叉养不起「跟上上游」这件事"),
         ("In April 2020 a maintainer wrote that the project had to keep re-applying remacs on top of code "
          "landing upstream from many more people, and that the work did not pay off. Merged pull requests "
          "went 372 in 2018, 197 in 2019, 15 in 2020, none in 2021. The reboot branch meant to fix the "
          "merge problem stopped in March 2020.",
          "2020 年 4 月，一位维护者写道：项目必须不断把 remacs 重新贴到上游那些由更多人合进来的代码之上，而这"
          "份工作并不划算。合并的 PR 是 2018 年 372 个、2019 年 197 个、2020 年 15 个、2021 年 0 个。为了解决"
          "合并问题而开的那个重启分支，停在 2020 年 3 月。"),
         "issue #1571 comment 2020-04-12 · GitHub API merged-PR counts per year"),
        ("current",
         ("Deleting the C removed the rollback",
          "把 C 删掉，也把回滚删掉了"),
         ("The port replaced C files by deleting them. In April 2020, planning the reboot, a maintainer "
          "described the change of approach: instead of deleting code they would ifdef it, hoping later "
          "merges would be easier. By then the port was blocking use on current macOS and nobody could "
          "locate the cause. That branch's last commit is 2020-03-16.",
          "移植替换 C 文件的方式是删掉它们。2020 年 4 月筹划重启时，一位维护者说明了做法上的变化：不再删代码，"
          "而是用 ifdef 圈起来，希望之后的合并能轻一些。那时移植已经让当前版本的 macOS 用不了，而没有人能定位"
          "原因。那个分支最后一次提交是 2020-03-16。"),
         "issue #1571 comments 2020-04-27 · branch reset-to-emacs-27, last commit 2020-03-16"),
        ("current",
         ("The successor kept the C on purpose",
          "接班的项目是故意把 C 留下的"),
         ("remacs's README now points readers to emacs-ng, and says what changed: that fork is not about "
          "replacing the C code base, but about adding features using Rust's ecosystem. emacs-ng was "
          "created on 2020-08-23, six days after remacs's last code commit. It is still being pushed to in "
          "2026.",
          "remacs 的 README 现在把读者指向 emacs-ng，并且说清了差别：那个分叉不是要替换 C 代码库，而是用 Rust "
          "的生态去加功能。emacs-ng 建于 2020-08-23，比 remacs 最后一次代码提交晚六天。到 2026 年它还在被推"
          "送。"),
         "README.md:3 · GitHub API repos/emacs-ng/emacs-ng created_at, pushed_at"),
    ],

    "buys": [
        (("Leaf files, permanently", "叶子文件，一去不回"),
         ("five C files left src/ and did not come back, because their functions never hold a Lisp object "
          "across a collection point.",
          "五个 C 文件离开了 src/ 并且没有回来，因为它们的函数不会跨着一次回收持有 Lisp 对象。")),
        (("Crates that replace C outright", "能整块替掉 C 的 crate"),
         ("base64, flate2, md5, sha1, sha2 did the work that made those deletions possible. The packaging "
          "argument in the README was correct.",
          "base64、flate2、md5、sha1、sha2 干的活让那些删除成为可能。README 里关于打包的那条论证是对的。")),
        (("A demonstration worth having", "一次值得做的示范"),
         ("a maintainer's own framing: as a proof-of-concept that such a replacement is possible, he called "
          "it a wild success. The report takes that at face value.",
          "维护者自己的说法：作为「这种替换是可能的」这一点的概念验证，他称之为 wild success。报告照原样接受这"
          "个说法。")),
    ],
    "nobuys": [
        (("Memory safety inside a C-collected heap", "在 C 回收的堆里拿内存安全"),
         ("Rust holding a Lisp_Object that 164 staticpro roots and a C mark-and-sweep collector manage is "
          "not protected by the borrow checker.",
          "Rust 手里那个由 164 个 staticpro 根和一个 C mark-and-sweep 收集器管理的 Lisp_Object，borrow "
          "checker 保护不了。")),
        (("The display engine, the collector, the loader", "显示引擎、收集器、加载器"),
         ("49 of the 119 remaining C files hold no primitive at all — 77,047 lines the DEFUN-porting method "
          "cannot reach.",
          "剩下 119 个 C 文件里有 49 个一个 primitive 都没有——77,047 行，搬 DEFUN 这套方法碰不到。")),
        (("Escape from bug-for-bug compatibility", "从「连 bug 一起兼容」里脱身"),
         ("1,507,964 lines of Emacs Lisp depend on observed primitive behaviour, and no specification of "
          "that behaviour exists to build against.",
          "1,507,964 行 Emacs Lisp 依赖 primitive 被观察到的行为，而没有一份关于这些行为的规格书可以照着"
          "实现。")),
        (("Freedom from the merge tax", "从合并税里解脱"),
         ("a fork of a live project pays for every upstream commit forever, in a currency the fork does not "
          "mint.",
          "分叉一个活着的项目，就要为上游的每一次提交永久付费，而付的这种货币分叉自己造不出来。")),
    ],

    "precedents": [
        {"name": "Mozilla · Servo as a Gecko replacement", "outcome": "NEVER SHIPPED",
         "body": ("Holley put the arithmetic on record: a full Gecko replacement 'would probably require "
                  "thousands of engineer-years' while Mozilla 'could only afford a handful of heads'. In "
                  "August 2020 the Servo team was laid off. The components shipped; the replacement never "
                  "did.",
                  "Holley 把账算在了纸面上：完整替换 Gecko 'would probably require thousands of "
                  "engineer-years'，而 Mozilla 'could only afford a handful of heads'。2020 年 8 月，Servo "
                  "团队被裁。组件发布了，整体替换没有。"),
         "match": ("whole-core replacement of a large C/C++ desktop codebase, with funding far below the "
                   "scope; the same month remacs's work stopped",
                   "对一个大型 C/C++ 桌面代码库做整体内核替换，投入远低于范围；停下来的月份和 remacs 相同"),
         "mismatch": ("a funded corporate team with a greenfield engine, not volunteers porting in place "
                      "inside a fork",
                      "那是有预算的公司团队在做全新引擎，不是志愿者在分叉里就地移植"),
         "regime": "browser engine, first-party retrospective", "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Mozilla · Stylo", "outcome": "SHIPPED",
         "body": ("The same organisation, the same codebase, one subsystem: the CSS style system landed in "
                  "Firefox 57 in about two years, with two engineers at the start. Holley's line is the "
                  "lesson remacs's five retired files also teach — almost everything successful is "
                  "incremental in one way or another.",
                  "同一个组织、同一个代码库、只做一个子系统：CSS 样式系统大约两年就进了 Firefox 57，起步时两个"
                  "工程师。Holley 那句话，正是 remacs 那 5 个退役文件也在讲的事——成功的东西几乎都是以某种方式"
                  "渐进来的。"),
         "match": ("the extraction-versus-replacement pair inside one codebase, which is exactly the split "
                   "between remacs's five files and its 309,205 remaining lines",
                   "同一个代码库里「抽取」对「替换」的那一组对照，正好对应 remacs 的 5 个文件和剩下的 309,205 "
                   "行"),
         "mismatch": ("a seam with a parallelism payoff and no foreign garbage collector tracing Rust's "
                      "objects",
                      "那条接缝有并行化的回报，也没有一个外部 GC 去遍历 Rust 的对象"),
         "regime": "shipped in Firefox 57, Nov 2017", "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "curl · the hyper backend", "outcome": "ABANDONED",
         "body": ("Four years, ISRG funding, near-complete test parity, then removal. Stenberg's reason was "
                  "people: 'There simply were no users asking for it and there were almost no developers "
                  "interested or knowledgeable enough to work on it.' The rustls and quiche backends "
                  "survived, because they hooked in more cleanly.",
                  "四年、ISRG 资助、测试基本全过，然后被删掉。Stenberg 给的原因是人：'There simply were no "
                  "users asking for it and there were almost no developers interested or knowledgeable "
                  "enough to work on it.' rustls 和 quiche 那两个后端活下来了，因为它们接得更干净。"),
         "match": ("a technically sound C-to-Rust safety migration that died on staffing at high "
                   "completion, with the cleaner-seam Rust work surviving alongside it",
                   "一次技术上站得住的 C 到 Rust 安全迁移，在完成度很高的时候死在人力上，而接缝更干净的那部分 "
                   "Rust 工作活了下来"),
         "mismatch": ("one backend of a library with a stable API, not a fork tracking a live upstream "
                      "editor",
                      "那是一个 API 稳定的库的一个后端，不是一个要追着活的上游编辑器跑的分叉"),
         "regime": "removed in curl 8.12.0, Feb 2025", "source_label": "first-party · maintainer blog",
         "url": "https://daniel.haxx.se/blog/2024/12/21/dropping-hyper/"},
        {"name": "emacs-ng", "outcome": "ALIVE",
         "body": ("Created 2020-08-23, six days after remacs's last code commit, and still receiving pushes "
                  "in 2026. remacs's own README explains the difference: this fork is not about replacing "
                  "the C code base, but about adding features with Rust's ecosystem. Same community, "
                  "smaller claim, longer life.",
                  "建于 2020-08-23，比 remacs 最后一次代码提交晚六天，到 2026 年还在收到推送。remacs 自己的 "
                  "README 解释了差别：这个分叉不是要替换 C 代码库，而是用 Rust 的生态加功能。同一个社区，更小的"
                  "主张，更长的寿命。"),
         "match": ("the same codebase, the same language, the same contributor pool — the only variable "
                   "changed is the size of the claim",
                   "同一个代码库、同一门语言、同一批贡献者——唯一变的变量是主张的大小"),
         "mismatch": ("its Rust is additive rather than a replacement, so it is not evidence about porting "
                      "the C core at all",
                      "它的 Rust 是加法而不是替换，所以它完全不构成关于「移植 C 内核」的证据"),
         "regime": "GitHub API at 2026-08-02", "source_label": "repository metadata",
         "url": "https://github.com/emacs-ng/emacs-ng"},
    ],

    "path": [
        {"title": ("Write down what you are fixing", "先写清楚你要修的是什么"),
         "body": ("Anyone proposing this again states the requirement with a number before writing Rust. A "
                  "CVE class and its count, a startup budget in milliseconds, a maintenance cost in "
                  "reviewer-hours. remacs skipped this step, and four years later its own thread could not "
                  "agree on whether the project had succeeded. If no threshold can be written, stop here. "
                  "Nothing has been built, so there is nothing to undo.",
                  "谁要再提这件事，先把需求连数字一起写出来，再动 Rust。一个 CVE 类别和它的数量，一份以毫秒计的"
                  "启动预算，一笔以评审工时计的维护成本。remacs 跳过了这一步，四年之后自己的帖子里都没能就"
                  "「项目算不算成功」达成一致。如果写不出阈值，就停在这里。什么都还没造，也就没有什么要撤。"),
         "owner": "whoever proposes the port",
         "cost_range": ("1 week", "1 周"),
         "artifact": "a one-page requirement naming the gap, its current measured value, and the threshold that counts as fixed",
         "acceptance": "the threshold is a number a third party could check against a build",
         "stop": "stop if no threshold can be written; the objective is a preference, not a requirement",
         "rollback": "nothing has been built"},
        {"title": ("Ship it as a module first", "先做成模块发出去"),
         "body": ("Build the thing as a dynamic module against src/emacs-module.h.in and give it to users. "
                  "No fork, no toolchain imposed on distributors, no merge tax. The step passes when real "
                  "people run it on Linux and macOS for a release cycle. If the module ABI cannot express "
                  "what you need, you have learned the seam is wrong before spending four years on it. "
                  "Rolling back is deleting a shared library.",
                  "对着 src/emacs-module.h.in 做成动态模块，发给用户用。不分叉，不给发行版强加工具链，没有合并"
                  "税。通过标准是：有真人在 Linux 和 macOS 上跑满一个发布周期。如果模块 ABI 表达不了你要的东"
                  "西，那你在花掉四年之前就已经知道接缝选错了。回滚就是删掉一个共享库。"),
         "owner": "the module author",
         "cost_range": ("2-6 weeks", "2–6 周"),
         "artifact": "a dynamic module built against src/emacs-module.h.in, distributed to users outside the Emacs tree",
         "acceptance": "users run it on Linux and macOS for one Emacs release cycle without a fork",
         "stop": "if the module ABI cannot carry the feature, the seam is wrong — report that instead of forking",
         "rollback": "delete the shared library"},
        {"title": ("If you must touch the core, take one leaf file and keep the C",
                   "非要动内核，就挑一个叶子文件，并且把 C 留着"),
         "body": ("Pick a C file whose functions never hold a Lisp object across a collection point — the "
                  "shape of floatfns.c and marker.c, which remacs retired and never regretted. Port it "
                  "behind the same symbols and the same docstrings. Keep the C compiled under a build flag "
                  "instead of deleting it, which is the correction remacs's own maintainers reached for on "
                  "the reboot. Acceptance is byte-identical behaviour on the existing test suite.",
                  "挑一个 C 文件，它的函数不会跨着一次回收持有 Lisp 对象——就是 floatfns.c 和 marker.c 那种形"
                  "状，remacs 把它们退役之后从没后悔过。用同样的符号、同样的 docstring 把它移过去。C 用构建开关"
                  "留着继续编，不要删掉，这正是 remacs 维护者在重启时想做的修正。通过标准是：在现有测试套件上行"
                  "为逐字节一致。"),
         "owner": "the porting contributor",
         "cost_range": ("4-8 weeks per file", "每个文件 4–8 周"),
         "artifact": "one C file reimplemented in Rust behind identical symbols, with the C retained under a build flag",
         "acceptance": "byte-identical behaviour on the existing test suite, including docstrings in the DOC file",
         "stop": "stop if the file's functions hold a Lisp object across a collection point; that is issue #1532 territory",
         "rollback": "flip the build flag back to the C implementation"},
        {"title": ("Leave the collector alone until Rust can see it",
                   "在 Rust 能看见收集器之前，别碰它"),
         "body": ("The allocator, the collector, the loader and the display engine stay in C. Issue #1532 "
                  "is open and its answer is not in this repository — Rust would need a way to let a "
                  "foreign collector trace objects the borrow checker owns. Until that exists, porting "
                  "these subsystems produces unsafe Rust with worse tooling than the C it replaced. Revisit "
                  "when the language changes, not when enthusiasm returns.",
                  "分配器、收集器、加载器、显示引擎，留在 C 里。issue #1532 还开着，而答案不在这个仓库里——Rust "
                  "需要一种办法，让外部收集器去遍历 borrow checker 所有的对象。在那之前，把这些子系统移过去，"
                  "得到的是一堆 unsafe 的 Rust，工具链还不如它替掉的 C。等语言变了再回来看，不是等热情回来。"),
         "owner": "nobody, for now",
         "cost_range": ("blocked", "阻塞中"),
         "artifact": "a written answer to issue #1532 that does not rely on banning Rust heap allocation",
         "acceptance": "a foreign collector can trace objects owned by Rust code without unsafe at every call site",
         "stop": "blocked on a Rust language capability; no project decision unblocks it",
         "rollback": "not applicable; no work is authorized"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The safety benefit was attributed to Rust without checking whether it survives inside a "
                   "C-managed heap. It does not. The project found this out in year three.",
                   "安全收益被归给了 Rust，但没有人先检查它在一个由 C 管理的堆里还成不成立。不成立。项目是在第"
                   "三年才发现的。"),
         "evidence": "issue #1532 · G2 FAIL"},
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("Porting DEFUNs cannot reach code that has none. 49 of 119 remaining C files hold zero "
                   "primitives, which is 77,047 lines.",
                   "搬 DEFUN 碰不到没有 DEFUN 的代码。剩下 119 个 C 文件里 49 个一个 primitive 都没有，合计 "
                   "77,047 行。"),
         "evidence": "D2 · grep -c '^DEFUN' across src/*.c"},
        {"name": ("Omitted cost", "被漏算的成本"), "state": "HIT",
         "claim": ("The merge tax was never priced. A fork of a live project pays for every upstream "
                   "commit, and that bill closed the project.",
                   "合并税从来没有被计入。分叉一个活着的项目，要为上游的每一次提交付账，而这张账单把项目关"
                   "掉了。"),
         "evidence": "issue #1571 comment 2020-04-12 · D11"},
        {"name": ("Ownership", "归属"), "state": "HIT",
         "claim": ("268 contributors is a large volunteer pool and it was still not enough. The remaining "
                   "work needed paid specialists on the collector and the bytecode interpreter.",
                   "268 个贡献者已经是很大的志愿者池，依然不够。剩下的活需要在收集器和字节码解释器上有全职投入"
                   "的专家。"),
         "evidence": "issue #1571 comment 2020-04-12 · GitHub API contributor count"},
        {"name": ("Reversibility", "可逆性"), "state": "HIT",
         "claim": ("Ported C was deleted rather than gated, so there was no way back. The reboot branch "
                   "tried ifdefs instead and stopped after five months.",
                   "移植掉的 C 是被删除而不是被开关圈起来的，所以没有退路。重启分支改用 ifdef，五个月后停"
                   "了。"),
         "evidence": "issue #1571 comment 2020-04-27 · branch reset-to-emacs-27"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("Native compilation of Lisp shipped in Emacs 28.1 on 2022-04-03, without a fork. The "
                   "in-stack route was not hypothetical.",
                   "Lisp 的原生编译在 2022-04-03 随 Emacs 28.1 发布，没有分叉。栈内这条路不是假想。"),
         "evidence": "emacs-mirror/emacs tag emacs-28.1 · etc/NEWS:21"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying leaves 309,205 lines of C parsing files, images and TLS streams. That exposure "
                   "is real and this report does not treat Emacs's age as safety.",
                   "不动，就是让 309,205 行 C 继续去解析文件、图像和 TLS 流。这个暴露面是实的，报告没有把 Emacs "
                   "的年纪当成安全。"),
         "evidence": "git ls-files 'src/*.c' | xargs wc -l"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The 51 primitives still in Objective-C under src/*.m, 21,340 lines of macOS GUI, are "
                   "disclosed. The port never touched them.",
                   "src/*.m 里还剩 51 个 primitive、21,340 行 macOS GUI 代码，报告把它披露出来了。移植从没碰过"
                   "它们。"),
         "evidence": "D10 · grep -c '^DEFUN' src/*.m"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report credits what Rust delivered: five C files gone for good, and crates that "
                   "made the deletions possible. The extraction and module options stay retained.",
                   "报告认下了 Rust 交付的东西：5 个 C 文件彻底走掉，以及让这些删除成为可能的那些 crate。抽取和"
                   "模块两个方案继续保留。"),
         "evidence": "D6 second record · D9 · Cargo.toml.in"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The recommendation names the exact trigger that reopens the in-place port, and it is a "
                   "Rust language capability rather than a change of mind.",
                   "推荐里点明了让就地移植重开的确切触发条件，那是 Rust 语言层面的能力，不是谁改主意。"),
         "evidence": "change trigger · issue #1532"},
    ],

    "gaps": [
        (("A build of remacs at this commit on current hardware",
          "在当前硬件上构建这个 commit 的 remacs"),
         ("No build, test or benchmark was run. Every claim here is static structure, maintainer statement, "
          "or repository metadata. A working build would settle whether the macOS breakage is the "
          "collector problem or something else.",
          "没有做过任何构建、测试或基准。这里的每条主张要么是静态结构，要么是维护者的陈述，要么是仓库元数据。"
          "一个能跑起来的构建能确定 macOS 上的问题是收集器那件事还是别的。")),
        (("The size of the generated FFI surface", "生成出来的 FFI 面到底多大"),
         ("rust_src/.gitignore excludes generated/, so the bindgen output that remacs_sys.rs includes is "
          "not in the checkout. The interop surface is therefore larger than the 170 lines that are "
          "visible, by an amount this report cannot state.",
          "rust_src/.gitignore 把 generated/ 排除在外，所以 remacs_sys.rs 里 include 进来的 bindgen 产物不在"
          "检出目录里。互操作面因此比看得见的那 170 行更大，大多少，本报告说不出来。")),
        (("A root-cause classification of Emacs's own advisory history",
          "对 Emacs 自身安全公告做根因分类"),
         ("This would turn D1 from UNKNOWN into a stated requirement, and it would tell the leaf-extraction "
          "option which files to aim at first.",
          "这能把 D1 从 UNKNOWN 变成一条写明的需求，也能告诉叶子抽取方案该先打哪几个文件。")),
    ],

    "assumptions": [
        "The shallow clone at commit a684a4c represents the final state of the project; the README's own 'not maintained' notice is that commit.",
        "One #[lisp_fn] attribute in rust_src/src equals one Lisp-callable primitive, and one line-initial DEFUN in src/*.c equals one primitive still in C. The README uses the same two counts, which is why they are used here.",
        "Port machinery is counted as the 15 files that exist only because the port exists: the proc macro, the bindgen driver, the FFI declaration module, the lisp.h mirror, the test-only mock module, the macro files, the build script, the unexec allocator shim and the hashdir helper. Reclassifying lisp.rs as converted behaviour would move 816 lines.",
        "The five files credited as conversions are those present in the emacs-26.2 src tree and absent from remacs, excluding the four that went with dropped MS-DOS support.",
    ],
    "objective": {
        "driver": "maintainability and latent memory safety of a 40-year-old C core",
        "requirement": "reduce the memory-unsafety and maintenance exposure of Emacs's C core without breaking the 1,507,964 lines of Emacs Lisp that depend on its primitives",
        "baseline": "309,205 lines of C across 119 files in src/, plus 36,970 lines of headers; no stated threshold anywhere in the project",
        "target": "never stated by the project; the README argues tooling, ecosystem and contributor experience",
    },
    "repository": {
        "path": "https://github.com/remacs/remacs",
        "commit": "a684a4c282f98fbe21df551030f1859f52f3ac6d",
        "scope": "the whole fork; the C core in src/ is the assessed target and rust_src/ is the completed experiment",
        "sampling": "shallow clone, 3,847 tracked files enumerated; rust_src/, src/, lisp/ measured; history, contributor, pull-request and successor facts taken from the GitHub API because --depth 1 leaves git log unusable; no build, test or benchmark was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "remacs/remacs at a684a4c · static read-only analysis + GitHub API history · why-not-rust method 2.0",
        "remacs/remacs @ a684a4c · 静态只读分析 + GitHub API 历史 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/remacs/remacs at commit a684a4c282f98fbe21df551030f1859f52f3ac6d, dated "
        "2021-04-07, shallow clone, 3,847 tracked files. The fork's base is GNU Emacs 26.2.90 per "
        "configure.ac. Scope: the C core in src/ is the assessed target; rust_src/ is treated as the "
        "completed trial of the proposal. Sampling and counting basis: 88 tracked .rs files hold 30,133 "
        "lines. Of those, 3,308 lines across 15 files are port machinery — remacs-macros, remacs-bindings, "
        "remacs-util, remacs-lib/docfile.rs and lib.rs, build.rs, and inside rust_src/src the files "
        "remacs_sys.rs, lib.rs, ffi.rs, functions.rs, eval_macros.rs, vector_macros.rs and lisp.rs, plus "
        "alloc_unexecmacosx and lib-src/hashdir. The remaining 26,825 lines are converted Emacs behaviour. "
        "Against that, src/*.c is 309,205 lines across 119 files and src/*.h is 36,970 across 75. Every "
        "Rust-versus-C comparison here uses tracked-file wc -l on both sides, never a whole-tree total "
        "against a subtree. Rust is 1.5% of the 1,997,194 code-extension lines in the tree, counting .rs "
        ".c .h .el .m .java .py .sh; that percentage is reported with its denominator because it is easy to "
        "misread. Primitives: 666 #[lisp_fn] attributes in rust_src/src against 748 line-initial DEFUN in "
        "src/*.c, so 47% of Lisp-callable primitives had moved. Two DEFUN-shaped strings were excluded "
        "after inspection: one inside a comment block in alloc.c and one commented out in xml.c. Nine "
        "#[lisp_fn] matches in build.rs, docfile.rs and attributes.rs are tooling that scans for the "
        "attribute, not primitives, and are excluded. A further 51 primitives remain in Objective-C under "
        "src/*.m. Boundary cost: 919 unsafe occurrences, counted with grep -o rather than grep -c, across "
        "66 of the 75 files in rust_src/src; 164 staticpro GC-root registrations in src/*.c; 9 unstable "
        "feature gates and a rust-toolchain pinned to nightly-2020-08-14. The generated/ directory holding "
        "bindgen output is gitignored, so the full FFI surface could not be measured and is recorded as a "
        "gap. File retirements were established by diffing git ls-files 'src/*.c' against the emacs-26.2 "
        "src tree fetched from the GitHub API: 126 files upstream, 119 here, of which five went to Rust and "
        "four went with dropped MS-DOS support. History facts — created 2016-11-22, merged pull requests of "
        "318, 372, 197, 15 and 0 across 2017 to 2021, 902 merged in total, 268 contributors, last code "
        "commit 2020-08-17, README notice 2021-04-07, reset-to-emacs-27 last touched 2020-03-16 — come from "
        "the GitHub API, because the shallow clone makes git log unusable and the fork carries all of GNU "
        "Emacs's own commit history, which would contaminate any local per-year count. Maintainer "
        "statements are quoted from issues #1532 and #1571 with dates. Objective: no RFC was supplied and "
        "the project never stated a threshold, so D1 and G1 are recorded UNKNOWN rather than filled in. "
        "User-supplied facts: none. No Amdahl calculation appears, because the proposal stated no "
        "performance objective and converting a line share into a time share is a method error. The "
        "decision turns on G2, G3 and G4, all FAIL on measured facts and first-party maintainer statements, "
        "which is why the result is REJECT rather than DEFER-MEASURE despite G1 being UNKNOWN. Confidence "
        "is HIGH because this is an outcome rather than a forecast. No build, test, benchmark or network "
        "call was made against the project itself. This is a structured decision protocol, not a "
        "statistical predictor.",
        "仓库：github.com/remacs/remacs，commit a684a4c282f98fbe21df551030f1859f52f3ac6d，日期 2021-04-07，"
        "shallow clone，3,847 个纳管文件。按 configure.ac，分叉基线是 GNU Emacs 26.2.90。范围：评估对象是 "
        "src/ 里的 C 内核，rust_src/ 被当作这个提案已经跑完的试验。采样与计数口径：88 个纳管 .rs 文件共 30,133 "
        "行。其中 15 个文件、3,308 行是移植脚手架——remacs-macros、remacs-bindings、remacs-util、"
        "remacs-lib/docfile.rs 和 lib.rs、build.rs，以及 rust_src/src 里的 remacs_sys.rs、lib.rs、ffi.rs、"
        "functions.rs、eval_macros.rs、vector_macros.rs、lisp.rs，再加 alloc_unexecmacosx 和 "
        "lib-src/hashdir。剩下 26,825 行是转换过的 Emacs 行为。对面，src/*.c 是 119 个文件 309,205 行，"
        "src/*.h 是 75 个文件 36,970 行。本报告里所有 Rust 对 C 的比较，两边都用纳管文件的 wc -l，不拿整棵树的"
        "总数去比一个子树。Rust 占全树 1,997,194 行代码扩展名（.rs .c .h .el .m .java .py .sh）的 1.5%；这个"
        "百分比连分母一起给出，因为它很容易被读错。Primitive：rust_src/src 里 666 个 #[lisp_fn]，对 src/*.c 里"
        "行首的 748 个 DEFUN，也就是 47% 的可被 Lisp 调用的 primitive 已经搬走。有两处形似 DEFUN 的字符串在人工"
        "检查后排除：一处在 alloc.c 的注释块里，一处在 xml.c 里被注释掉。build.rs、docfile.rs、attributes.rs "
        "里另有 9 处 #[lisp_fn] 匹配，那是扫描这个属性的工具代码，不是 primitive，已排除。src/*.m 里还有 51 个 "
        "primitive 停在 Objective-C。边界成本：919 处 unsafe，用 grep -o 计数而不是 grep -c，分布在 "
        "rust_src/src 的 75 个文件里的 66 个；src/*.c 里 164 处 staticpro GC 根注册；9 个不稳定特性开关，"
        "rust-toolchain 钉在 nightly-2020-08-14。放 bindgen 产物的 generated/ 目录被 gitignore 掉了，完整的 "
        "FFI 面量不出来，作为证据缺口记录在案。文件退役是用 git ls-files 'src/*.c' 和 GitHub API 取回的 "
        "emacs-26.2 src 树做 diff 得到的：上游 126 个文件，这里 119 个，其中 5 个去了 Rust，4 个随 MS-DOS 支持"
        "一起走。历史数据——2016-11-22 建库，2017 到 2021 年合并 PR 分别为 318、372、197、15、0，累计 902，"
        "268 个贡献者，最后一次代码提交 2020-08-17，README 公告 2021-04-07，reset-to-emacs-27 最后一次改动 "
        "2020-03-16——都来自 GitHub API，因为 shallow clone 让 git log 用不了，而且这个分叉带着 GNU Emacs 自己"
        "全部的提交历史，本地按年统计会被污染。维护者的原话引自 issue #1532 和 #1571，都带日期。目标：没有人给"
        "出 RFC，项目自己也从未定过阈值，所以 D1 和 G1 记为 UNKNOWN，不去替它填。用户提供的事实：无。本报告没有 "
        "Amdahl 计算，因为提案没有提出性能目标，而把行数占比换算成时间占比是方法错误。决策落在 G2、G3、G4 上，"
        "这三道门都在实测事实和第一方维护者陈述上失败，所以结论是 REJECT 而不是 DEFER-MEASURE，尽管 G1 是 "
        "UNKNOWN。置信度 HIGH，因为这是一个已经发生的结果，不是预测。没有对项目本身做过任何构建、测试、基准或"
        "网络调用。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit a684a4c · history via GitHub API · no build, benchmark or network call against the project",
        "公开仓库 · 在 commit a684a4c 上做静态分析 · 历史数据来自 GitHub API · 没有对项目做构建、基准或网络调用",
    ),
}
