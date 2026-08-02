"""sqlite/sqlite — the case where gates 1 and 2 pass and the rewrite still loses.

Repository facts were measured read-only on the shallow clone named in
`repository`. Published figures keep their URL and regime.
"""

CASE = {
    "slug": "sqlite",
    "project_name": "sqlite/sqlite",
    "project_desc": (
        "C · embedded SQL engine · 182,029 lines of core C, 1,021,321 lines of in-repo tests",
        "C · 嵌入式 SQL 引擎 · 核心 C 代码 182,029 行，仓库内测试 1,021,321 行",
    ),
    "date": "2026-08-01",
    "archetype": (
        "security-parser · embedded library with a 2050 compatibility promise",
        "安全解析器 · 承诺兼容到 2050 年的嵌入式库",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "stay-verified",
    "scope_chip": (
        "keep the C core; consumers who want Rust adopt an existing Rust engine",
        "保留 C 内核；想要 Rust 的使用方去采用现成的 Rust 引擎",
    ),
    "scope_sub": (
        "keep the C engine; the verification programme is what actually ships",
        "保留 C 引擎；真正交付出去的是那套验证体系",
    ),

    "why": (
        "Gates 1 and 2 pass. SQLite is C that parses untrusted SQL and untrusted database files, and "
        "Rust would remove that defect class from any line it replaced. Gates 3 and 4 fail. Behind "
        "those 182,029 lines of C sit 100% branch and MC/DC coverage and 590 times as much test "
        "material as source. There is also a written promise: the C API and on-disk format stay "
        "backwards compatible through 2050. That is the asset. A rewrite inherits the source and none "
        "of it.",
        "G1 与 G2 通过。SQLite 用 C 解析不受信任的 SQL 和不受信任的数据库文件，Rust 换掉哪一行，就在那一行"
        "消灭这类缺陷。G3 与 G4 不通过。这 182,029 行 C 背后，是 100% 分支与 MC/DC 覆盖，以及 590 倍于源码"
        "的测试材料。还有一份书面承诺：C API 与磁盘格式向后兼容到 2050 年。资产就是这些东西。重写继承得到源码，"
        "这些一样都拿不到。",
    ),
    "trigger": (
        "Stable. This flips only when a Rust engine shows equivalent verification: 100% MC/DC on its "
        "own core, plus byte-identical on-disk behaviour. Even then the question for consumers is "
        "whether to adopt it. The SQLite project still would not be rewriting anything.",
        "判断稳定。只有当某个 Rust 引擎拿出对等的验证证据——自己内核上 100% MC/DC，加上字节级一致的磁盘"
        "行为——这个结论才会翻。就算那天到了，使用方要决定的也只是采不采用。SQLite 项目仍然不必重写任何东西。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS",
         "short": ("Requirement", "需求"),
         "hero_evidence": (
             "C parses untrusted SQL text and untrusted database files.",
             "C 代码解析不受信任的 SQL 文本和不受信任的数据库文件。"),
         "name": "requirement",
         "evidence": "The engine's input is attacker-reachable in both directions; the project runs a dedicated fuzzer (dbsqlfuzz) at roughly one billion mutations per day, which is direct evidence the surface produces findings."},
        {"id": "G2", "state": "PASS",
         "short": ("Causality", "因果"),
         "hero_evidence": (
             "C→Rust removes the memory-unsafety class by construction.",
             "C→Rust 从构造上消除内存不安全这一类缺陷。"),
         "name": "rust-specific causality",
         "evidence": "No redesign, algorithm or storage-format change is needed to obtain the safety delta; it follows from replacing manual-lifetime C."},
        {"id": "G3", "state": "FAIL",
         "short": ("Economics", "经济性"),
         "hero_evidence": (
             "92,053.1 KSLOC of tests carry the reliability, and they do not port.",
             "可靠性靠的是 92,053.1 KSLOC 测试代码，这部分搬不过去。"),
         "name": "economics and smallest sufficient option",
         "evidence": "SQLite reports 155.8 KSLOC of library code against 92,053.1 KSLOC of test code and scripts — a 590× ratio — plus 100% branch and MC/DC coverage from a proprietary harness. A rewrite starts that investment at zero, and consumers who want a Rust engine can already adopt one."},
        {"id": "G4", "state": "FAIL",
         "short": ("Delivery", "交付"),
         "hero_evidence": (
             "A written promise of C-API and on-disk compatibility through 2050.",
             "C API 与磁盘格式兼容的书面承诺，一直到 2050 年。"),
         "name": "delivery and reversibility",
         "evidence": "The project promises to keep the C API and on-disk format fully backwards compatible and plans support through 2050. There is no dual-run or rollback story for re-implementing that promise across the installed base."},
    ],

    "tiles": [
        (("Test code per line of source", "每行源码对应的测试代码"), "590", ("×", "×"),
         ("sqlite.org/testing.html · 155.8 vs 92,053.1 KSLOC",
          "sqlite.org/testing.html · 155.8 对 92,053.1 KSLOC")),
        (("Branch and MC/DC coverage", "分支与 MC/DC 覆盖率"), "100", ("%", "%"),
         ("TH3 harness on the core, measured with gcov", "TH3 在内核上运行，用 gcov 测量")),
        (("In-repo test material", "仓库内的测试材料"), "1,021,321", ("lines", "行"),
         ("test/ · 1,294 tracked files, this commit", "test/ · 本次提交，1,294 个受控文件")),
        (("Core C measured here", "此处测得的核心 C"), "182,029", ("lines", "行"),
         ("src/ excluding test harness · 102 files", "src/ 排除测试脚手架 · 102 个文件")),
        (("Compatibility horizon", "兼容承诺的期限"), "2050", ("year", "年"),
         ("written C-API and on-disk format promise", "C API 与磁盘格式的书面承诺")),
        (("Rust engine already shipped", "已经在跑的 Rust 引擎"), "23.6k", ("stars", "stars"),
         ("tursodatabase/turso · ground-up rewrite, pre-1.0", "tursodatabase/turso · 从零重写，pre-1.0")),
    ],

    "options_sub": (
        "Every option answers the same objective: remove the memory-unsafety class from SQL and "
        "database-file parsing without weakening the assurance level SQLite currently ships.",
        "每个方案对的都是同一个目标：在不削弱 SQLite 现有保证水平的前提下，从 SQL 与数据库文件解析中消除"
        "内存不安全这一类缺陷。",
    ),
    "options": [
        {"id": "stay-verified",
         "name": ("Keep C + the verification programme", "保留 C 与那套验证体系"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("class remains possible, incidence held very low", "缺陷类仍然可能出现，发生率压得很低"),
         "one_time_cost": "none", "recurring_cost": "the existing test and fuzz investment",
         "cost_cell": ("none new; existing test + fuzz budget", "无新增；沿用现有测试与 fuzz 预算"),
         "time_to_value": ("in effect today", "今天已经生效"),
         "compatibility": "native",
         "compat_cell": ("native · nothing to roll back", "原生 · 没有东西需要回滚"),
         "reversibility": "n/a", "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · the assurance is the product", "推荐 · 保证水平本身就是产品"),
         "reason": "Only option that preserves 100% MC/DC coverage and the 2050 compatibility promise."},
        {"id": "adopt-rust-engine",
         "name": ("Consumers adopt a Rust engine", "使用方改用 Rust 引擎"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for that consumer", "这一缺陷类在该使用方处消失"),
         "one_time_cost": "per consumer integration", "recurring_cost": "tracks a pre-1.0 project",
         "cost_cell": ("per consumer; pre-1.0 dependency", "每个使用方各付各的；依赖一个 pre-1.0 项目"),
         "time_to_value": ("days per project", "每个项目几天"),
         "compatibility": "self-declared, not yet complete",
         "compat_cell": ("SQLite-compatible · caller-side rollback", "SQLite 兼容 · 调用方侧可回滚"),
         "reversibility": "swap the dependency back", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the answer for callers who want Rust", "保留 · 想要 Rust 的调用方该走这条"),
         "reason": "Meets the objective for an individual application without asking SQLite to rewrite anything."},
        {"id": "rust-parser-extract",
         "name": ("Rust tokenizer/parser behind the C API", "C API 背后换成 Rust 词法/语法分析器"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed in one front-end component", "一个前端组件内消除这一缺陷类"),
         "one_time_cost": "rebuild coverage for the component", "recurring_cost": "second toolchain in every build",
         "cost_cell": ("coverage rebuild; second toolchain everywhere", "覆盖率要重建；处处多一条工具链"),
         "time_to_value": ("months", "数月"),
         "compatibility": "must match legacy quirks exactly",
         "compat_cell": ("byte-exact parse behaviour · hard rollback", "解析行为要字节级一致 · 回滚困难"),
         "reversibility": "build flag, if kept dual", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the only Rust scope worth re-examining later", "保留 · 以后唯一值得再看一眼的 Rust 范围"),
         "reason": "Plausible in shape, but it forfeits MC/DC coverage for the replaced component and adds a Rust toolchain to a project whose portability claim is 'any platform with a C compiler'."},
        {"id": "rust-full",
         "name": ("Rewrite SQLite in Rust", "用 Rust 重写 SQLite"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("class removed; assurance level unproven", "缺陷类消除；保证水平未经证明"),
         "one_time_cost": "the entire verification programme, again", "recurring_cost": "compatibility obligation to 2050",
         "cost_cell": ("re-earn 92,053.1 KSLOC of tests; 2050 obligation", "92,053.1 KSLOC 测试重新挣一遍；还背着 2050 义务"),
         "time_to_value": ("years", "数年"),
         "compatibility": "C API + on-disk format + legacy quirks",
         "compat_cell": ("whole promise · no rollback", "整份承诺 · 无法回滚"),
         "reversibility": "none at the installed base", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G3 and G4", "排除 · G3、G4 不通过"),
         "reason": "The cost is the asset. An independent team has been building exactly this for 18,966 commits and still lists full SQLite compatibility as a prerequisite for its 1.0."},
        {"id": "sandbox",
         "name": ("Sandbox the engine in the host", "在宿主里把引擎沙箱化"),
         "implementation": "non-rust-native",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("contains the class instead of removing it", "把这一缺陷类圈住，没有消除"),
         "one_time_cost": "host-side, per application", "recurring_cost": "process or wasm boundary",
         "cost_cell": ("host-side; boundary overhead", "宿主侧付出；有边界开销"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "unchanged SQL and format",
         "compat_cell": ("unchanged engine · trivial rollback", "引擎不动 · 回滚很容易"),
         "reversibility": "remove the sandbox", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · caller-side mitigation the report must present", "保留 · 调用方侧的缓解手段，报告必须列出"),
         "reason": "For applications opening untrusted database files, isolation addresses the same exposure without touching the engine."},
    ],

    "lenses_sub": (
        "States are option-scoped evidence. They do not add up. Repository line counts come from the "
        "commit named in the methodology; published ratios keep their source and date.",
        "每条状态都是针对某个方案的证据。它们不能相加。仓库行数来自方法一节写明的提交；引用的比值保留其"
        "来源与日期。",
    ),
    "na_note": (
        "Three lenses are N/A: D3 tail latency, D4 fleet footprint, D5 startup shape. The engine links "
        "into the caller's process and carries no runtime of its own. None of them bears on memory safety.",
        "三个维度记为 N/A：D3 尾延迟、D4 机队占用、D5 启动形态。引擎链进调用方进程，自己没有运行时。这三条"
        "都够不着内存安全。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"), "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-parser-extract", "rust-full", "adopt-rust-engine"],
         "claim": (
             "SQLite parses untrusted SQL text and untrusted database files in C. The project funds a "
             "dedicated database-file fuzzer against exactly that surface.",
             "SQLite 用 C 解析不受信任的 SQL 文本和不受信任的数据库文件。项目专门出钱养了一个针对这块面的"
             "数据库文件 fuzzer。"),
         "source": "src/tokenize.c · src/btree.c · dbsqlfuzz, ~1e9 mutations/day (sqlite.org/testing.html)",
         "regime": "project testing programme, 2023 figures onward",
         "caveat": "Exposure is structural; the advisory history is not broken down by root cause on the testing page."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": (
             "This decision asserts no performance requirement. No Amdahl calculation is performed, "
             "because the only way to produce one here would be to invent it from line counts.",
             "这个决策没有提出任何性能要求。因此不做 Amdahl 计算——真要做，只能拿行数硬凑一个出来。"),
         "source": "objective is safety, not latency", "regime": "n/a",
         "caveat": "Line share is not time share; substituting one for the other would be a method error."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": (
             "There is no managed runtime or collector in the engine, so no runtime mechanism exists in "
             "any tail to remove.",
             "引擎里没有托管运行时，也没有回收器，尾部就没有可以拿掉的运行时机制。"),
         "source": "C library, no GC", "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": (
             "The engine runs inside the caller's process; this decision changes no fleet density.",
             "引擎跑在调用方进程里，这个决策不改变任何机队密度。"),
         "source": "embedded linkage model", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": (
             "Library initialization is not a stated constraint for any consumer in this decision.",
             "这个决策里没有任何使用方把库的初始化列为约束。"),
         "source": "no startup requirement asserted", "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"), "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-parser-extract", "rust-full", "adopt-rust-engine"],
         "claim": (
             "Replacing manual-lifetime C removes the memory-unsafety class from whatever it replaces. "
             "That much is causal. No benchmark needed.",
             "把手工管理生命周期的 C 换掉，换掉多少，就在多少代码里消除内存不安全这一类缺陷。这一步是因果关系。"
             "不需要跑基准。"),
         "source": "language property, applied at the scope of each option",
         "regime": "structural", "caveat": "It says nothing about logic, isolation or storage-corruption defects, which dominate SQLite's own testing effort."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": (
             "Concurrency is governed by file locking and WAL semantics that every option must reproduce "
             "identically; no option is better placed to encode them.",
             "并发由文件锁和 WAL 语义决定，每个方案都得原样复现；没有哪个方案在表达这些语义上更占优。"),
         "source": "src/pager.c · src/os_unix.c locking model",
         "regime": "storage concurrency contract",
         "caveat": "A Rust rewrite would have to match the same externally observable locking behaviour, not a nicer one."},
        {"id": "D8", "name": ("Distribution", "分发"), "label": "DISFAVORS · rust options", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-parser-extract", "rust-full"],
         "claim": (
             "SQLite's portability claim is that it runs on any platform with an 8-bit byte, 32/64-bit "
             "two's-complement integers and a C compiler. A Rust component narrows that set.",
             "SQLite 的可移植性主张是：只要平台有 8-bit byte、32/64-bit 二进制补码整数和一个 C 编译器，"
             "它就能跑。加一个 Rust 组件，这个集合就变小。"),
         "source": "https://www.sqlite.org/lts.html — \"Cross-platform Code\"",
         "regime": "stated long-term support design constraint",
         "caveat": "Rust's target list is large and growing; it is still a strict subset of 'has a C compiler'."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"), "label": "SUPPORTS · adopt-rust-engine", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-engine"],
         "claim": (
             "A ground-up Rust engine already exists: SQLite dialect, on-disk format and C-API "
             "compatibility, 23.6k stars, reported production use. Consumers who want Rust do not need "
             "SQLite to change.",
             "从零写的 Rust 引擎已经有了：SQLite 方言、磁盘格式、C API 都对上，23.6k stars，也有生产使用的"
             "报告。想要 Rust 的使用方，不需要 SQLite 改任何东西。"),
         "source": "https://github.com/tursodatabase/turso — repository README",
         "regime": "third-party project self-description, pre-1.0",
         "caveat": "Its own README states compatibility is \"not at 100% yet\" and that full compatibility is a prerequisite for 1.0."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": (
             "The compatibility surface has three parts: the C API, the byte-level on-disk format, and "
             "legacy behavioural quirks. All three are promised backwards compatible.",
             "兼容面有三块：C API、字节级磁盘格式，以及历史遗留的行为怪癖。三块都写进了向后兼容的承诺。"),
         "source": "https://www.sqlite.org/lts.html — API and on-disk format promise",
         "regime": "written project commitment",
         "caveat": "A component extraction inherits a smaller share of this surface, which is why it is retained and the full rewrite is not."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": (
             "The verification programme is the majority of the project's cost: 92,053.1 KSLOC of test "
             "material, 100% branch and MC/DC coverage, and roughly one billion daily fuzz mutations. "
             "None of it transfers to a new implementation.",
             "验证体系占了项目成本的大头：92,053.1 KSLOC 测试材料、100% 分支与 MC/DC 覆盖、每天约十亿次 "
             "fuzz 变异。换一套实现，这些一样都带不走。"),
         "source": "https://www.sqlite.org/testing.html · in-repo test/ measured at 1,021,321 lines",
         "regime": "first-party testing disclosure plus this commit's tree",
         "caveat": "The 590× ratio counts generated and parameterized test material, which inflates raw line comparisons; the coverage claim does not depend on it."},
        {"id": "D12", "name": ("Counterfactual", "反事实对照"), "label": "SUPPORTS · stay-verified, sandbox", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-verified", "sandbox"],
         "claim": (
             "The current-stack answer is funded and already running at unusual intensity. Callers "
             "exposed to untrusted database files can isolate the engine without any language change.",
             "现有技术栈这条路已经有人出钱，而且强度很不寻常。要面对不受信任数据库文件的调用方，不换语言"
             "也能把引擎隔离起来。"),
         "source": "dbsqlfuzz + TH3 + 51,445 TCL cases (sqlite.org/testing.html); host-side sandboxing",
         "regime": "existing practice plus standard host isolation",
         "caveat": "Sandboxing contains rather than eliminates the class, and carries its own boundary cost."},
    ],

    "findings": [
        ("current",
         ("The asset is the verification, not the source", "资产是那套验证体系，不是源码"),
         ("SQLite reports 155.8 KSLOC of library code against 92,053.1 KSLOC of test code and scripts, "
          "with 100% branch and MC/DC coverage on the core. A rewrite copies the design. The assurance "
          "programme restarts at zero.",
          "SQLite 公布的数字是 155.8 KSLOC 库代码，对 92,053.1 KSLOC 测试代码与脚本，内核上分支与 MC/DC "
          "覆盖率 100%。重写能抄走设计。保证体系要从零重来。"),
         "sqlite.org/testing.html · 590× ratio, 2023 figures onward"),
        ("current",
         ("This commit alone carries 1,021,321 lines of tests", "光这一个提交就带着 1,021,321 行测试"),
         ("Exclude the proprietary MC/DC harness and the public tree still ships 5.6 lines of test "
          "material for every line of core C. That ratio is what a rewrite proposal has to price. None has.",
          "把闭源的 MC/DC 脚手架排除在外，公开代码树里每一行核心 C 仍然配着 5.6 行测试材料。这个比值是重写"
          "提案必须先报价的东西。目前没有一份报过。"),
         "test/ · 1,294 tracked files vs src/ 182,029 lines"),
        ("current",
         ("The 2050 promise is in writing", "2050 年那份承诺是白纸黑字"),
         ("The project promises the C API and on-disk format stay fully backwards compatible, and plans "
          "support through 2050. Re-implementing that promise has no rollback. The installed base is "
          "already holding the files.",
          "项目承诺 C API 与磁盘格式保持完全向后兼容，并计划支持到 2050 年。重新实现这份承诺没有回滚路径。"
          "文件已经在装机量手里了。"),
         "sqlite.org/lts.html · API and on-disk format commitment"),
        ("rust",
         ("The Rust version already exists, and says what it still lacks", "Rust 版本已经存在，也说了自己还差什么"),
         ("A ground-up Rust engine with dialect, format and C-API compatibility has 23.6k stars and "
          "reports production deployments. Its own README says compatibility is not yet complete. "
          "Completing it is a prerequisite for 1.0. That is the adoption path for callers who want Rust.",
          "有一个从零写起的 Rust 引擎，方言、格式、C API 都对齐，23.6k stars，也有生产部署的报告。它自己的 "
          "README 写着兼容性还没做完。做完是 1.0 的前置条件。想要 Rust 的调用方，走的就是这条采用路径。"),
         "github.com/tursodatabase/turso · 18,966 commits, pre-1.0"),
        ("rust",
         ("The safety requirement here holds up", "这里的安全需求是站得住的"),
         ("SQLite parses untrusted SQL and untrusted database files in C, and funds a fuzzer at roughly "
          "one billion mutations per day against that surface. Gates 1 and 2 pass. The rewrite loses on "
          "gates 3 and 4, not on the premise.",
          "SQLite 用 C 解析不受信任的 SQL 和不受信任的数据库文件，并出钱在这块面上跑每天约十亿次变异的 "
          "fuzzer。G1 与 G2 通过。重写栽在 G3 和 G4 上，前提本身没问题。"),
         "src/tokenize.c · src/btree.c · dbsqlfuzz"),
    ],

    "buys": [
        (("Class elimination in whatever it replaces", "换到哪里，哪里就没有这一类缺陷"),
         ("any Rust component stops being able to produce a memory-unsafety defect in its own code.",
          "Rust 组件在自己这段代码里，不再可能产出内存不安全缺陷。")),
        (("A viable path for callers", "调用方有一条走得通的路"),
         ("an application that needs a memory-safe embedded engine can adopt one today without SQLite changing.",
          "需要内存安全嵌入式引擎的应用，今天就能采用一个，SQLite 不用改。")),
        (("A defensible future extraction", "将来抽一块出来，说得过去"),
         ("if a Rust front-end component ever reaches equivalent coverage, the tokenizer/parser is the seam with the smallest compatibility share.",
          "如果哪天某个 Rust 前端组件做到对等覆盖率，词法/语法分析器是兼容面占比最小的那道缝。")),
    ],
    "nobuys": [
        (("Any of the existing assurance", "现有的保证水平，一点也买不到"),
         ("100% MC/DC coverage, 51,445 TCL cases and roughly one billion daily fuzz mutations, all published at sqlite.org/testing.html. Those attach to the current implementation, not to the language.",
          "100% MC/DC 覆盖、51,445 个 TCL 用例、每天约十亿次 fuzz 变异，数字都公布在 sqlite.org/testing.html。它们长在当前这份实现上，跟语言无关。")),
        (("Freedom from the compatibility promise", "从兼容承诺里脱身"),
         ("the C API, the byte-level format and the legacy quirks are the contract; a rewrite owes all of it, forever.",
          "C API、字节级格式、历史怪癖，这些就是合同。重写全都要背，一直背下去。")),
        (("Protection from the defect classes that dominate here", "挡住这里真正占多数的缺陷类"),
         ("logic, isolation and storage-corruption bugs are what the testing programme mostly hunts, and Rust does not remove them.",
          "测试体系主要在抓逻辑、隔离和存储损坏这三类 bug，Rust 不消除它们。")),
    ],

    "precedents": [
        {"name": "tursodatabase/turso", "outcome": "GREENFIELD",
         "body": (
             "An independent team is rewriting SQLite in Rust from scratch rather than forking it. "
             "18,966 commits, with reported production users. Full SQLite compatibility is the stated "
             "prerequisite for 1.0. It is not there yet.",
             "一支独立团队在用 Rust 从零重写 SQLite，而不是 fork。18,966 个提交，有生产用户的报告。完整的 "
             "SQLite 兼容是它自己写明的 1.0 前置条件。目前还没做到。"),
         "match": ("identical target, identical language pair, explicit compatibility goal",
                   "目标相同，语言对相同，兼容目标也写明了"),
         "mismatch": ("a new project choosing its own reliability bar, not the SQLite project accepting a migration",
                      "这是一个新项目自己定可靠性标准，而非 SQLite 项目接受了一次迁移"),
         "regime": "third-party self-description, pre-1.0", "source_label": "third-party · project README",
         "url": "https://github.com/tursodatabase/turso"},
        {"name": "jaq vs jq", "outcome": "ADOPTED",
         "body": (
             "A Rust reimplementation of a widely used C tool arrived from outside the original project, "
             "carrying its own test suite and audits. The original's maintainers had nothing to do.",
             "一个广泛使用的 C 工具，它的 Rust 重实现是从原项目外面冒出来的，自带测试套件和审计。原项目的"
             "维护者什么都不用做。"),
         "match": ("the ecosystem shipping the Rust option instead of the incumbent rewriting",
                   "由生态提供 Rust 选项，原项目自己不动手"),
         "mismatch": ("jq's compatibility surface is a CLI, not a byte-level storage format promised to 2050",
                      "jq 的兼容面是一个 CLI，不是承诺到 2050 年的字节级存储格式"),
         "regime": "author-run benchmarks, drop-in \"in most cases\"", "source_label": "third-party · project README",
         "url": "https://github.com/01mf02/jaq"},
        {"name": "Mozilla · Servo as Gecko replacement", "outcome": "CANCELLED",
         "body": (
             "A whole-engine replacement was estimated at thousands of engineer-years, against a team of "
             "a handful. It was cancelled. The component extractions shipped instead.",
             "整机引擎替换的估算是几千工程师年，而团队只有几个人。项目被取消。最后交付的是拆出来的那几个"
             "组件。"),
         "match": ("replacement scope defeated by the size of the existing verified implementation",
                   "替换范围被现有已验证实现的体量拖垮"),
         "mismatch": ("a browser engine with far more churn than a storage format designed to be frozen",
                      "浏览器引擎的变动远多于一个设计上就要冻结的存储格式"),
         "regime": "2012–2020 programme outcome", "source_label": "first-party · engineer account",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "AWS · S3 ShardStore", "outcome": "MIGRATED",
         "body": (
             "A storage node was rewritten in Rust. The correctness claim came with roughly nine months "
             "of dedicated formal-methods work: executable reference models, property tests, Loom. That "
             "work caught 16 issues before production.",
             "一个存储节点用 Rust 重写。正确性的说法背后是大约九个月专门的形式化方法工作：可执行参考模型、"
             "性质测试、Loom。这些工作在上生产前抓出 16 个问题。"),
         "match": ("shows what assurance a storage rewrite actually costs",
                   "说明存储系统重写要为保证水平付出多少"),
         "mismatch": ("40,000 lines with a private interface, not 182,029 lines under a public 2050 promise",
                      "那是 40,000 行、私有接口；这里是 182,029 行，压着一份到 2050 年的公开承诺"),
         "regime": "SOSP'21 paper", "source_label": "first-party · peer-reviewed paper",
         "url": "https://www.cs.utexas.edu/~bornholt/papers/shardstore-sosp21.pdf"},
    ],

    "path": [
        {"title": ("Say what the requirement actually is", "先把需求说清楚"),
         "body": (
             "The proposer writes down which exposure is unacceptable: untrusted SQL, untrusted database "
             "files, or a specific deployment's threat model. The statement passes only if it names a "
             "concrete scenario the current assurance programme does not cover. If the answer is 'C is "
             "unsafe in general', stop here. That is not a requirement. No codebase has changed yet.",
             "提出重写的人写下一份说明：哪一种暴露不能接受——不受信任的 SQL、不受信任的数据库文件，还是某个"
             "具体部署的威胁模型。这份说明必须点名一个当前保证体系覆盖不到的具体场景，否则不算过。如果答案"
             "是「C 总体上不安全」，到此为止。那不是需求。此时任何代码库都还没动过。"),
         "owner": "the proposer",
         "cost_range": ("1 day", "1 天"),
         "artifact": "a written statement of which exposure is unacceptable: untrusted SQL, untrusted database files, or a specific deployment's threat model",
         "acceptance": "the statement names a concrete scenario the current assurance programme does not cover",
         "stop": "stop here if the answer is 'C is unsafe in general' — that is not a requirement",
         "rollback": "no change to any codebase"},
        {"title": ("Contain the exposure at the caller", "先在调用方把暴露圈住"),
         "body": (
             "The application team runs the engine inside a process or wasm sandbox on the untrusted-file "
             "paths, and measures the boundary cost. It passes when untrusted files are opened only "
             "inside the sandbox and the overhead fits the application's budget. If the boundary cost "
             "blows that budget, stop and go back to comparing options. Rolling back is easy. Delete the "
             "sandbox; the engine was never modified.",
             "应用团队把引擎放进进程沙箱或 wasm 沙箱，专门跑处理不受信任文件的那条路径，并测量边界开销。"
             "通过的标准是：不受信任的文件只在沙箱里打开，开销在应用预算之内。开销超预算就停下来，回到方案"
             "对比。回滚很轻。删掉沙箱就行，引擎从头到尾没改过。"),
         "owner": "the application team",
         "cost_range": ("1–3 weeks", "1–3 周"),
         "artifact": "the engine running in a process or wasm sandbox for untrusted-file paths, with the boundary cost measured",
         "acceptance": "untrusted files are opened only inside the sandbox, and the measured overhead is acceptable to the application",
         "stop": "stop if the boundary cost exceeds the application's budget; escalate to option comparison again",
         "rollback": "remove the sandbox; the engine is unmodified"},
        {"title": ("Evaluate the existing Rust engine on your own workload", "拿自己的负载去试现成的 Rust 引擎"),
         "body": (
             "Same team, different question. Point the Rust engine at the application's own schemas, "
             "queries and existing database files, then write up what matched. Acceptance is byte-level "
             "format compatibility and query-result parity across that corpus, with the gaps documented. "
             "Any parity failure that touches data integrity ends the evaluation. Reverting is a "
             "dependency change. The database files are unchanged by design.",
             "还是应用团队，换一个问题。把 Rust 引擎接到应用自己的 schema、查询和现有数据库文件上，再把对"
             "得上的部分写成报告。验收看两条：这份语料上的字节级格式兼容，以及查询结果一致；差异逐条记录"
             "在案。只要有一处不一致碰到数据完整性，评估就结束。回退只是换回依赖。数据库文件按设计本来就"
             "不变。"),
         "owner": "the application team",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "a compatibility and correctness report against the application's real schemas, queries and existing database files",
         "acceptance": "byte-level format compatibility and query-result parity on the application's own corpus, with a documented gap list",
         "stop": "stop if any parity failure touches data integrity",
         "rollback": "revert the dependency; database files are unchanged by design"},
        {"title": ("Re-open the engine decision only on verification evidence", "再提这个决策，只看验证证据"),
         "body": (
             "Whoever proposes a rewrite next brings a comparison of assurance level, not of language: "
             "coverage measured the same way, fuzzing intensity, format-compatibility evidence. Nothing "
             "counts until the challenger publishes MC/DC-equivalent coverage on its own core and "
             "byte-identical on-disk behaviour. Without that evidence, no proposal proceeds. The C "
             "engine and its testing programme continue either way.",
             "下一个提重写的人，带来的材料要比保证水平，别比语言：用同样方法测出的覆盖率、fuzz 强度、格式"
             "兼容的证据。挑战者不在自己内核上公布与 MC/DC 对等的覆盖率、不给出字节级一致的磁盘行为，就都"
             "不算数。拿不出这些证据，提案就不往下走。无论如何，C 引擎和它的测试体系照常运行。"),
         "owner": "whoever proposes a rewrite next",
         "cost_range": ("1 day per review", "每次评审 1 天"),
         "artifact": "a comparison of assurance level — coverage measured the same way, fuzzing intensity, format-compatibility evidence — rather than a comparison of language",
         "acceptance": "the challenger publishes MC/DC-equivalent coverage on its own core and byte-identical on-disk behaviour",
         "stop": "no rewrite proposal proceeds without that evidence",
         "rollback": "the C engine and its testing programme continue unchanged"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响面"), "state": "PASS",
         "claim": (
             "No performance claim is made. D2 is left N/A rather than filled with a line-share standing "
             "in for a time-share.",
             "报告没有提出性能主张。D2 保持 N/A，没有拿行数占比冒充时间占比去填。"),
         "evidence": "D2 record"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": (
             "The safety delta is attributed to the language property alone, at the scope of each option, "
             "with no redesign credited to Rust.",
             "安全收益只归因于语言属性本身，按每个方案各自的范围计算，没有把任何重新设计算到 Rust 头上。"),
         "evidence": "D6 record"},
        {"name": ("Baseline and regime", "基线与口径"), "state": "HIT",
         "claim": (
             "The 590× ratio counts generated and parameterized test material, so raw line comparisons "
             "overstate the gap. The coverage claim is the load-bearing one.",
             "590× 这个比值把生成的和参数化的测试材料都算了进去，按原始行数比会夸大差距。真正承重的是覆盖率"
             "那一条。"),
         "evidence": "sqlite.org/testing.html"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": (
             "The compatibility surface is stated in full: the C API, the byte-level on-disk format, and "
             "legacy quirks. An API alone would understate it.",
             "兼容面是完整列出来的：C API、字节级磁盘格式、历史怪癖。只说 API 会低估它。"),
         "evidence": "sqlite.org/lts.html"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": (
             "The report names the missing artifact: MC/DC-equivalent coverage on a challenger core. It "
             "does not assert that a rewrite is impossible.",
             "报告点名了缺的那份材料：挑战者内核上与 MC/DC 对等的覆盖率。它没有断言重写不可能。"),
         "evidence": "reversible path step 4"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有钱在投的反事实对照"), "state": "PASS",
         "claim": (
             "TH3, 51,445 TCL cases and a billion daily fuzz mutations are already funded and running. "
             "The staying option is not a hypothetical.",
             "TH3、51,445 个 TCL 用例、每天十亿次 fuzz 变异，都已经在花钱、在跑。「不动」这个方案不是假设。"),
         "evidence": "sqlite.org/testing.html"},
        {"name": ("Cost of inaction", "不作为的代价"), "state": "HIT",
         "claim": (
             "Staying in C keeps the memory-unsafety class reachable in code that parses attacker-supplied "
             "SQL and database files. Testing intensity lowers incidence, not possibility.",
             "继续用 C，就意味着在解析攻击者提供的 SQL 和数据库文件的代码里，内存不安全这一类缺陷始终可达。"
             "测试强度降低的是发生率，不是可能性。"),
         "evidence": "D1 and D6 records"},
        {"name": ("Unsafe-surface omission", "遗漏不安全面"), "state": "PASS",
         "claim": (
             "The report grants gates 1 and 2 to the Rust options rather than hiding the unsafe surface "
             "behind the project's reputation.",
             "报告把 G1 和 G2 判给了 Rust 方案，没有拿项目声誉去挡住那块不安全面。"),
         "evidence": "G1 and G2 states"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": (
             "The existing Rust engine is recorded as a retained option for consumers, with its own stated "
             "pre-1.0 caveats.",
             "现成的 Rust 引擎被记为使用方可用的保留方案，并附上它自己声明的 pre-1.0 保留条件。"),
         "evidence": "D9 · github.com/tursodatabase/turso"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": (
             "The decision has a named reopening condition: published MC/DC-equivalent coverage and "
             "byte-identical format behaviour. This is not a permanent veto.",
             "这个决策写明了重启条件：公布与 MC/DC 对等的覆盖率，以及字节级一致的格式行为。它不是永久否决。"),
         "evidence": "change trigger"},
    ],

    "gaps": [
        (("Root-cause classification of SQLite's advisory history", "SQLite 历史安全公告的根因分类"),
         ("Without it, the share of past defects Rust would have eliminated by construction stays an "
          "argument rather than a measurement. It would move G1's strength. The G3 and G4 failures stand.",
          "没有这份分类，Rust 本可以从构造上消除掉多少历史缺陷，就只是个说法，不是测量结果。它会影响 G1 的"
          "证据强度。G3 和 G4 的失败照旧。")),
        (("Assurance level of any Rust challenger", "任何 Rust 挑战者的保证水平"),
         ("If a Rust engine publishes MC/DC-equivalent coverage on its own core and byte-identical "
          "on-disk behaviour, the adoption option strengthens for consumers. The extraction option "
          "becomes re-examinable.",
          "如果某个 Rust 引擎公布了自己内核上与 MC/DC 对等的覆盖率，以及字节级一致的磁盘行为，采用方案对"
          "使用方就更有说服力。抽取方案也值得重新看一遍。")),
        (("Cost of rebuilding coverage for one extracted component", "为抽出来的单个组件重建覆盖率要多少钱"),
         ("Unpriced. Until someone estimates it, the tokenizer/parser extraction stays "
          "retained-but-unselected rather than recommended.",
          "没人报过价。在有人估出来之前，词法/语法分析器的抽取方案只能保留待议，进不了推荐。")),
    ],

    "assumptions": [
        "The published 155.8 KSLOC / 92,053.1 KSLOC figures describe a 2023-onward release and are used as a ratio, not as this commit's exact counts.",
        "The shallow clone at the named commit represents the shipped public tree; the proprietary TH3 harness is not in it and was not inspected.",
        "No performance or footprint requirement is attached to this decision.",
    ],
    "objective": {
        "driver": "safety",
        "requirement": "remove the memory-unsafety class from SQL and database-file parsing without weakening the assurance level SQLite currently ships",
        "baseline": "182,029 lines of core C under 100% branch and MC/DC coverage with roughly 1e9 daily fuzz mutations",
        "target": "equal-or-better assurance, with the C API and on-disk format promise intact",
    },
    "repository": {
        "path": "https://github.com/sqlite/sqlite",
        "commit": "f034d515b4208e1c9325271aef3dc4901f24e216",
        "scope": "whole repository; the core engine in src/ is the migration candidate",
        "sampling": "shallow clone; 2,221 tracked files enumerated; src/, test/ and ext/ measured; the proprietary TH3 harness is not part of this repository",
    },
    "user_supplied_facts": [],

    "method_title": (
        "sqlite/sqlite at f034d51 · static read-only analysis · why-not-rust method 2.0",
        "sqlite/sqlite @ f034d51 · 只读静态分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/sqlite/sqlite at commit f034d51, shallow clone, 2,221 tracked files. "
        "Scope: the whole repository, with the core engine in src/ as the migration candidate. Sampling: "
        "tracked files only. src/ holds 47 test-harness files (44 .c translation units plus 3 headers); "
        "the 102 files left after excluding them carry 182,029 lines of core C. test/ carries 1,021,321 "
        "lines across 1,294 files, and ext/ carries 326,793. No build, test, benchmark or network call "
        "was run against the project. The proprietary TH3 harness behind the 100% MC/DC figure is not in "
        "this repository. That number and the 590× test-to-source ratio come from sqlite.org/testing.html "
        "and carry its 2023-onward release regime. Objective: remove the memory-unsafety class from SQL "
        "and database-file parsing without weakening the assurance level SQLite currently ships. "
        "User-supplied facts: none. No Amdahl calculation appears, because no performance requirement is "
        "asserted; treating a line share as a time share would be a method error, so D2 is recorded N/A. "
        "Gates 1 and 2 pass, gates 3 and 4 fail. The gates are non-compensatory, so a safety requirement "
        "that clears G1 and G2 still does not survive an option whose cost is the project's own assurance "
        "programme. The framework is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/sqlite/sqlite，提交 f034d51，浅克隆，2,221 个受控文件。范围：整个仓库，其中 src/ "
        "里的核心引擎是迁移候选。采样：只统计受控文件。src/ 里有 47 个测试脚手架文件（44 个 .c 编译单元加 "
        "3 个头文件）；排除之后剩下的 102 个文件是 182,029 行核心 C。test/ 是 1,294 个文件、1,021,321 行，"
        "ext/ 是 326,793 行。没有对项目执行任何构建、测试、基准或网络调用。产出 100% MC/DC 这个数字的闭源 "
        "TH3 脚手架不在本仓库里。那个数字和 590× 的测试源码比来自 sqlite.org/testing.html，口径是它 2023 年"
        "起的发布版本。目标：在不削弱 SQLite 现有保证水平的前提下，从 SQL 与数据库文件解析中消除内存不安全"
        "这一类缺陷。用户提供的事实：无。报告里没有 Amdahl 计算，因为没有提出性能要求；把行数占比当成时间"
        "占比是方法错误，所以 D2 记为 N/A。G1、G2 通过，G3、G4 不通过。四道门不可互相补偿，所以一个已经过了 "
        "G1 和 G2 的安全需求，仍然扛不住一个代价等于项目自身保证体系的方案。这套框架是结构化的决策协议，"
        "不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit f034d51 · no build, benchmark or network call",
        "公开仓库 · 在提交 f034d51 上做静态分析 · 无构建、无基准、无网络调用",
    ),
}
