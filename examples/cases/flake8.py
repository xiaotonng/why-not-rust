"""PyCQA/flake8 — a real 10x gap, and the rewrite is still the wrong move.

Repository facts were measured read-only on the shallow clone named in
`repository`. The Amdahl figures are produced by the skill's own calculator.
"""

CASE = {
    "slug": "flake8",
    "project_name": "PyCQA/flake8",
    "project_desc": ("Python · lint orchestrator · 4,741 lines of source across 33 files",
                     "Python · lint 编排器 · 33 个文件共 4,741 行源码"),
    "date": "2026-08-01",
    "archetype": ("cli-quick · plugin host that delegates all checking to three separate packages",
                  "cli-quick · 插件宿主，检查工作全部交给三个独立的包"),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "STABLE",
    "selected": "adopt-rust-linter",
    "scope_chip": ("keep flake8 as a plugin host; teams that need speed adopt the Rust linter",
                   "flake8 继续做插件宿主；需要速度的团队去用那个 Rust linter"),
    "scope_sub": ("the rewrite already happened, and it was not yours",
                  "重写已经发生过了，只是不由你来做"),

    "why": (
        "Gates 1 and 2 pass. Adopters report one to three orders of magnitude against Python "
        "linters, and the published mechanism holds up. Gate 3 is where it stops. flake8's own "
        "source is 4,741 lines; the checking happens in three packages it declares as "
        "dependencies, and the product is a plugin entry-point table. Give the orchestrator a "
        "generous 30% of lint wall-clock and make it infinitely fast: the ceiling is 1.43×, so a "
        "10× target is impossible at that scope. The Rust linter that meets the target already "
        "shipped, and adopting it costs no rewrite.",
        "G1 和 G2 通过。采用方报告的加速是一到三个数量级，公开的机制解释也站得住。卡住的是 G3。"
        "flake8 自己的源码 4,741 行；真正做检查的是它声明的三个依赖包，它卖的东西是一张插件 "
        "entry-point 表。就算给编排器 30% 的 lint 墙钟时间（已经很宽松），再让它快到无穷，天花板"
        "也只有 1.43×，10× 的目标在这个范围内不可能达成。满足这个目标的 Rust linter 已经发布了，"
        "采用它不需要重写。",
    ),
    "trigger": (
        "Stable. One thing would move it: a team whose blocking requirement is flake8's plugin "
        "ecosystem specifically. Even then a Rust rewrite of flake8 is still not the answer, "
        "because a native binary cannot host Python plugins without embedding an interpreter.",
        "结论稳定。只有一种情况会改变它：某个团队的阻塞需求恰好就是 flake8 的插件生态。就算那样，"
        "答案也不是把 flake8 用 Rust 重写——原生二进制没法在不内嵌解释器的前提下托管 Python 插件。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS",
         "short": ("Requirement", "需求"),
         "hero_evidence": ("Reported gains of 150–1000× against Python linters.",
                           "对 Python linter 报告出的加速是 150–1000×。"),
         "name": "requirement",
         "evidence": "Adopters report 2.5 min → 0.4 s against four-core-parallel pylint and roughly 150–200× against flake8; per-save invocation makes the gap felt on every keystroke cycle."},
        {"id": "G2", "state": "PASS",
         "short": ("Causality", "因果"),
         "hero_evidence": ("Native start, parse-once and GIL-free parallelism all hold up.",
                           "原生启动、一次解析、无 GIL 并行，这三条都成立。"),
         "name": "rust-specific causality",
         "evidence": "The published decomposition names reading and parsing each file exactly once for all rules, native execution with no interpreter cold start, file-level parallelism without the GIL, and caching. A large share is architectural rather than language-specific, which the report keeps separate."},
        {"id": "G3", "state": "FAIL",
         "short": ("Economics", "经济性"),
         "hero_evidence": ("Adoption meets the target at zero rewrite cost; the ceiling is 1.43×.",
                           "采用现成工具就能达标，重写成本为零；重写路线的天花板是 1.43×。"),
         "name": "economics and smallest sufficient option",
         "evidence": "A Rust linter already exists and lints CPython in under 500 ms. Rewriting flake8's 4,741-line orchestrator is capped at a 1.43× ceiling under a generous 30% share assumption, computed with scripts/decision_math.py."},
        {"id": "G4", "state": "FAIL",
         "short": ("Delivery", "交付"),
         "hero_evidence": ("A native binary cannot host Python plugins.",
                           "原生二进制托管不了 Python 插件。"),
         "name": "delivery and reversibility",
         "evidence": "flake8's product is the flake8.extension entry-point table plus delegation to pycodestyle, pyflakes and mccabe. A Rust reimplementation either drops third-party Python plugins or embeds an interpreter and re-acquires the cost it was rewritten to escape."},
    ],

    "tiles": [
        (("flake8's own source", "flake8 自己的源码"), "4,741", ("lines", "行"),
         ("src/ · 33 files — the whole orchestrator", "src/ · 33 个文件，整个编排器")),
        (("Dependencies doing the checking", "真正做检查的依赖"), "3", ("packages", "个包"),
         ("pycodestyle, pyflakes, mccabe — all Python", "pycodestyle、pyflakes、mccabe，全是 Python")),
        (("Amdahl ceiling at 30% share", "30% 份额下的 Amdahl 天花板"), "1.43", "×",
         ("decision_math.py · share=.30, kernel=∞, b=0", "decision_math.py · share=.30, kernel=∞, b=0")),
        (("Target the ceiling rules out", "被天花板排除的目标"), "10", "×",
         ("physically impossible at orchestrator scope", "在编排器这个范围内物理上不可能")),
        (("Rust linter already shipped", "已经发布的 Rust linter"), "<500", "ms",
         ("lints CPython · adoption cost, not rewrite cost", "lint 完 CPython · 只有采用成本，没有重写成本")),
        (("Reported adopter gain", "采用方报告的加速"), "150–1000", "×",
         ("vs flake8 and 4-core pylint · adopter-reported", "对比 flake8 与 4 核 pylint · 采用方自述")),
    ],

    "options_sub": (
        "Same objective for every option. Cut Python lint wall-clock by roughly an order of "
        "magnitude, for per-save and for CI, without losing the checks a team relies on.",
        "所有方案对着同一个目标。把 Python lint 的墙钟时间压掉约一个数量级，保存时触发和 CI 两种调用"
        "都算，同时不丢掉团队依赖的检查项。",
    ),
    "options": [
        {"id": "adopt-rust-linter",
         "name": ("Adopt the existing Rust linter", "直接采用已有的 Rust linter"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("reported 150–1000× on adopter workloads", "采用方负载上报告 150–1000×"),
         "one_time_cost": "days of rule mapping per project", "recurring_cost": "tracks a fast-moving tool",
         "cost_cell": ("days of rule mapping; fast-moving dep", "几天做规则映射；依赖迭代很快"),
         "time_to_value": ("same day", "当天"),
         "compatibility": "rule coverage is close, not identical",
         "compat_cell": ("rule-code mapping · revert the config", "规则码映射 · 改回配置即可"),
         "reversibility": "put flake8 back in the config", "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · meets the target today, at no rewrite cost",
                  "推荐 · 今天就能达标，且没有重写成本"),
         "reason": "Cheapest option that meets the stated target; the rewrite the requirement implies has already been done by someone else."},
        {"id": "py-optimize",
         "name": ("Optimize flake8 and its checkers in Python", "在 Python 里优化 flake8 和它的 checker"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("unmeasured; precedent suggests ~3× is reachable", "未实测；先例显示 ~3× 可达"),
         "one_time_cost": "weeks of funded profiling", "recurring_cost": "none new",
         "cost_cell": ("weeks of profiling; none recurring", "数周的 profiling；无新增长期成本"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "native",
         "compat_cell": ("native · git revert", "原生兼容 · git revert"),
         "reversibility": "git revert",
         "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · a comparable project reached ~3× this way", "保留 · 同型项目走这条路拿到过 ~3×"),
         "reason": "Genuinely undertried — Prettier found ~3× by profiling alone — but ~3× does not meet a 10× target."},
        {"id": "stay-plugins",
         "name": ("Keep flake8 for its plugin ecosystem", "为插件生态留下 flake8"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("no speed benefit; preserves checks nothing else has",
                              "没有速度收益；保住别处没有的检查项"),
         "one_time_cost": "none", "recurring_cost": "the current lint time",
         "cost_cell": ("none; current lint time", "无；继续承担当前的 lint 时间"),
         "time_to_value": ("in effect today", "今天就生效"),
         "compatibility": "native",
         "compat_cell": ("native · nothing to change", "原生兼容 · 什么都不用改"),
         "reversibility": "n/a", "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · correct whenever a required plugin has no equivalent",
                  "保留 · 只要某个必需插件找不到替代，这就是对的答案"),
         "reason": "For a team whose blocking need is a specific Python plugin, this is the right answer and speed is not the objective."},
        {"id": "rust-rewrite-flake8",
         "name": ("Rewrite flake8 in Rust", "用 Rust 重写 flake8"),
         "implementation": "rust",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("capped at 1.43× under a generous share assumption",
                              "在宽松的份额假设下也封顶 1.43×"),
         "one_time_cost": "4,741 lines plus a plugin story", "recurring_cost": "a second implementation of an existing tool",
         "cost_cell": ("4,741 lines; duplicate an existing tool", "4,741 行；重复造一个已有的工具"),
         "time_to_value": ("months", "数月"),
         "compatibility": "entry-point plugin API cannot survive",
         "compat_cell": ("loses Python plugins · no rollback", "丢掉 Python 插件 · 无回滚"),
         "reversibility": "poor", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · impossible threshold and an unshippable plugin story",
                  "排除 · 目标阈值不可能，插件方案也交付不了"),
         "reason": "Fails on the Amdahl ceiling and on the plugin contract simultaneously; the checkers it delegates to stay in Python."},
        {"id": "rust-checker-extract",
         "name": ("Rust parser behind the Python API", "Python API 背后放一个 Rust parser"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("unmeasured; boundary cost unpriced", "未实测；边界成本没有定价"),
         "one_time_cost": "PyO3 boundary plus AST parity", "recurring_cost": "wheels for every platform",
         "cost_cell": ("PyO3 boundary; wheels everywhere", "PyO3 边界；每个平台都要出 wheel"),
         "time_to_value": ("months", "数月"),
         "compatibility": "AST must match CPython's exactly",
         "compat_cell": ("AST parity · pip rollback", "AST 必须对齐 · pip 回滚"),
         "reversibility": "pin the previous release", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the shape that worked elsewhere, aimed at the wrong project",
                  "保留 · 这个形态在别处成功过，但对错了项目"),
         "reason": "This is the pydantic-core pattern and it is sound in general, but here it would rebuild the tool that already exists, and per-node PyO3 crossings cost roughly 20–40 ns each."},
    ],

    "amdahl": {
        "share": 0.30,
        "kernel_speedup": float("inf"),
        "boundary": 0.0,
        "target": 10.0,
        "note": (
            "Generous upper bound on flake8's own orchestration share of lint wall-clock, with an "
            "infinitely fast replacement and no boundary cost. Ceiling 1.4285714285714286x; the 10x "
            "target is physically impossible at this scope. The 30% share is an explicit assumption, "
            "not a measurement.",
            "对 flake8 自身编排环节占 lint 墙钟时间的份额取一个宽松上界，替换件速度设为无穷，边界成本"
            "设为零。天花板 1.4285714285714286x；10x 目标在这个范围内物理上不可能。30% 这个份额是显式"
            "假设，不是实测。",
        ),
    },

    "lenses_sub": (
        "States are option-scoped evidence, not additive points. The Amdahl figures come from "
        "scripts/decision_math.py with the inputs disclosed in the methodology.",
        "每个状态都绑定到具体方案，不是可以相加的分数。Amdahl 数字来自 scripts/decision_math.py，"
        "输入在方法一节里列明。",
    ),
    "na_note": (
        "Two lenses are N/A. D4 fleet footprint and D6 safety carry no part of this objective: "
        "linting runs on developer machines and CI, and Python is memory-safe at application scope "
        "with no compiled extension declared. The only native call in the tree is a stdlib ctypes "
        "hop into kernel32 for Windows console colour.",
        "两个维度判 N/A。D4 机群占用和 D6 安全性与本目标无关：lint 跑在开发机和 CI 上，Python 在应用"
        "层是内存安全的，仓库也没有声明任何编译扩展。整棵树里唯一的原生调用，是标准库 ctypes 为 "
        "Windows 控制台颜色跳一次 kernel32。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · native options", "css": "neutral",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-linter", "rust-rewrite-flake8", "rust-checker-extract"],
         "claim": ("The gap is adopter-reported and large: 2.5 min → 0.4 s against four-core-parallel "
                   "pylint, and roughly 150–200× against flake8 on another team's codebase.",
                   "差距由采用方报告，量级不小：对四核并行的 pylint 是 2.5 min → 0.4 s，在另一个团队的"
                   "代码库上对 flake8 约 150–200×。"),
         "source": "https://github.com/astral-sh/ruff — adopter reports",
         "regime": "adopter-reported, self-selected success stories",
         "caveat": "These are third-party reports of a competing tool, not measurements of flake8 taken here; the direction is solid, the multiplier is not transferable."},
        {"id": "D2", "name": ("End-to-end reach", "端到端可达性"),
         "label": "DISFAVORS · rust-rewrite-flake8", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-rewrite-flake8"],
         "claim": ("Grant flake8's own code a generous 30% share of lint wall-clock and make it "
                   "infinitely fast. The ceiling is 1.43×. A 10× target is physically impossible at "
                   "orchestrator scope.",
                   "给 flake8 自己的代码 30% 的 lint 墙钟份额，这已经很宽松，再让它无限快。天花板是 "
                   "1.43×。10× 的目标在编排器这个范围内物理上不可能。"),
         "source": "scripts/decision_math.py · share=.30, kernel=inf, boundary=0, target=10",
         "regime": "explicit upper-bound assumption, not a measured profile",
         "caveat": "If the true share were even higher than 30%, the argument would only need re-running; the checking work still lives in three separate Python packages."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("A batch linter has no tail-latency SLO; CPython's collector is not implicated in "
                   "any stated requirement.",
                   "批处理式的 linter 没有尾延迟 SLO；已声明的需求里也没有一条牵涉 CPython 的垃圾回收。"),
         "source": "batch CLI invocation model", "regime": "invocation shape", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机群占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Linting runs on developer machines and CI runners; no fleet-density objective or "
                   "break-even is stated.",
                   "lint 跑在开发机和 CI runner 上；没有提出任何机群密度目标，也没有回本测算。"),
         "source": "developer and CI invocation", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "SUPPORTS · native options", "css": "neutral",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-linter", "rust-rewrite-flake8"],
         "claim": ("Per-save invocation puts interpreter cold start on the critical path every time, "
                   "and a native binary removes it. This favours any native tool, not Rust specifically.",
                   "保存即触发的调用方式，把解释器冷启动放进了每一次的关键路径，原生二进制可以去掉它。"
                   "这一条对任何原生工具都成立，不是 Rust 独有。"),
         "source": "https://notes.crmarsh.com/python-tooling-could-be-much-much-faster",
         "regime": "first-party decomposition by the competing tool's author",
         "caveat": "Startup is one of several named factors; the account attributes a large share to parse-once architecture instead."},
        {"id": "D6", "name": ("Safety & correctness", "安全性与正确性"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Python is memory-safe at application scope and this codebase declares no native or "
                   "FFI surface, so no memory-safety delta exists to claim.",
                   "Python 在应用层是内存安全的，这个代码库也没有声明任何原生或 FFI 界面，所以没有可以"
                   "主张的内存安全差值。"),
         "source": "pure-Python package; setup.cfg declares three Python dependencies",
         "regime": "n/a", "caveat": ""},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · adopt-rust-linter", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-linter"],
         "claim": ("File-level linting is embarrassingly parallel and the GIL constrains in-process "
                   "Python parallelism; a native tool captures that directly.",
                   "按文件 lint 是天然可并行的，而 GIL 限制了进程内的 Python 并行；原生工具可以直接吃到"
                   "这一块。"),
         "source": "https://notes.crmarsh.com/python-tooling-could-be-much-much-faster",
         "regime": "first-party architectural account",
         "caveat": "Python can parallelize with processes; the comparison then shifts to per-process interpreter startup and memory."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Both the Python package and the native binary install through ordinary package "
                   "managers; no distribution constraint is unmet.",
                   "Python 包和原生二进制都能用常规包管理器装；没有哪条分发约束没被满足。"),
         "source": "pip-installable package · prebuilt native binaries",
         "regime": "packaging inventory", "caveat": ""},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · adopt-rust-linter", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["adopt-rust-linter"],
         "claim": ("The Rust linter this requirement implies already exists, is maintained, and lints "
                   "CPython in under 500 ms. Adoption is the option; building it again is not.",
                   "这个需求指向的那个 Rust linter 已经存在、有人维护，lint 完 CPython 用不到 500 ms。"
                   "可选项是采用它，不是再造一个。"),
         "source": "https://github.com/astral-sh/ruff",
         "regime": "shipped third-party tool",
         "caveat": "Rule coverage overlaps flake8's ecosystem but is not identical; the mapping is the adopter's real cost."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-checker-extract", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-checker-extract"],
         "claim": ("An extraction would cross the Python boundary per AST node or per check rather than "
                   "in bulk, and PyO3 calls cost roughly 20–40 ns each against the raw C API.",
                   "抽取方案会按 AST 节点或按检查项逐次跨越 Python 边界，而不是批量跨越；相对裸 C API，"
                   "每次 PyO3 调用约 20–40 ns。"),
         "source": "https://github.com/PyO3/pyo3/issues/3827",
         "regime": "measured per-call overhead in the binding layer",
         "caveat": "Batching and zero-copy designs reduce this; doing so means redesigning the plugin contract, which is the product."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-rewrite-flake8", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-rewrite-flake8"],
         "claim": ("flake8's value is its plugin contract: an entry-point table mapping rule prefixes to "
                   "checkers, plus delegation to three Python packages. A native binary cannot host "
                   "Python plugins without embedding an interpreter.",
                   "flake8 的价值就是它的插件契约：一张把规则前缀映射到 checker 的 entry-point 表，加上"
                   "对三个 Python 包的委派。原生二进制不内嵌解释器就托管不了 Python 插件。"),
         "source": "setup.cfg:40 [options.entry_points] · install_requires mccabe, pycodestyle, pyflakes",
         "regime": "packaging metadata in this commit",
         "caveat": "A Rust tool can reimplement popular plugins' rules natively — which is what the existing one did, and why adoption rather than rewriting is the option."},
        {"id": "D12", "name": ("Counterfactual", "反事实对照"),
         "label": "SUPPORTS · py-optimize, adopt-rust-linter", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["py-optimize", "adopt-rust-linter"],
         "claim": ("Two non-rewrite options are live: profiling the current stack, where a comparable "
                   "project found roughly 3× with no language change, and adopting the existing native "
                   "tool, which meets the target today.",
                   "两条不重写的路都还活着：一是给现有栈做 profiling，同型项目没换语言就拿到过约 3×；"
                   "二是采用现成的原生工具，今天就能达标。"),
         "source": "https://prettier.io/blog/2023/11/30/cli-deep-dive · https://github.com/astral-sh/ruff",
         "regime": "first-party reproduced result plus shipped tool",
         "caveat": "~3× is real and still short of a 10× target; the two options are complementary, not alternatives."},
    ],

    "findings": [
        ("current",
         ("flake8's own source is 4,741 lines", "flake8 自己的源码是 4,741 行"),
         ("The whole orchestrator is 33 files. It declares mccabe, pycodestyle and pyflakes as "
          "dependencies, and those three separate packages do the actual checking. What flake8 adds "
          "is a plugin table mapping rule prefixes to them. Rewrite flake8 and you have not rewritten "
          "the linting.",
          "整个编排器 33 个文件。它把 mccabe、pycodestyle、pyflakes 声明为依赖，真正做检查的就是这三个"
          "独立的包。flake8 自己加上去的，是一张把规则前缀映射到它们的插件表。重写 flake8，并没有重写 "
          "lint 本身。"),
         "src/ 4,741 lines · setup.cfg install_requires"),
        ("current",
         ("The plugin entry-point table is the product", "插件 entry-point 表就是产品本身"),
         ("setup.cfg registers flake8.extension entries pointing at the pyflakes and pycodestyle "
          "adapters, plus a report-formatter table. Third-party plugins register the same way. That "
          "contract is what a native binary cannot carry.",
          "setup.cfg 注册了指向 pyflakes 和 pycodestyle 适配器的 flake8.extension 条目，还有一张报告"
          "格式化表。第三方插件走的是同一条注册路径。原生二进制搬不动的，正是这份契约。"),
         "setup.cfg:40 [options.entry_points]"),
        ("unknown",
         ("A 10× target is physically impossible at this scope", "10× 的目标在这个范围内物理上不可能"),
         ("Give flake8's own code a generous 30% of lint wall-clock, make it infinitely fast, charge "
          "nothing for the boundary: the ceiling is 1.43×. The calculator returns 'target physically "
          "IMPOSSIBLE'. In this method that string is a rendering-time error condition, not a figure "
          "of speech.",
          "给 flake8 自己的代码 30% 的 lint 墙钟时间，速度设为无穷，边界成本记零：天花板 1.43×。计算器"
          "返回的是 'target physically IMPOSSIBLE'。在这套方法里，这个字符串是渲染期的错误条件，不是"
          "修辞。"),
         "decision_math.py amdahl --share .30 --kernel-speedup inf --target 10"),
        ("rust",
         ("The slowness is not in dispute", "慢这件事没有争议"),
         ("Adopters report 2.5 min → 0.4 s against four-core-parallel pylint and roughly 150–200× "
          "against flake8. Gate 1 passes. Nothing here defends the incumbent on speed. The cheapest "
          "option that meets the requirement happens to be adoption, and that is the whole of the "
          "argument.",
          "采用方报告：对四核并行的 pylint 是 2.5 min → 0.4 s，对 flake8 约 150–200×。G1 通过。这里"
          "没有替现状辩护的意思。只是满足需求的最便宜方案恰好是采用现成工具，整个论证就这么多。"),
         "github.com/astral-sh/ruff · adopter reports"),
        ("current",
         ("Nobody has profiled the current stack", "现有这套栈还没人做过 profiling"),
         ("A comparable formatter found roughly 3× by profiling, caching and IPC fixes with no "
          "language change, days after a Rust competitor claimed its speed bounty. So the staying "
          "case has homework. Profile first. Then read the result: 3× still misses 10×.",
          "同型的一个 formatter 靠 profiling、缓存和 IPC 修复拿到约 3×，一行语言都没换，时间就在某个 "
          "Rust 竞品领走速度赏金之后几天。所以「不动」这一方也有作业要交。先做 profiling。然后照结果"
          "说话：3× 仍然够不到 10×。"),
         "prettier.io/blog/2023/11/30/cli-deep-dive"),
    ],

    "buys": [
        (("Order-of-magnitude lint time, by adoption", "一个数量级的 lint 时间，靠采用就能拿到"),
         ("the native tool exists, is maintained, and lints CPython in under 500 ms — the benefit is "
          "available without writing Rust.",
          "那个原生工具已经存在、有人维护，lint 完 CPython 不到 500 ms——这份收益不需要你写一行 Rust。")),
        (("No interpreter cold start per invocation", "每次调用不再付解释器冷启动"),
         ("worth having for per-save workflows, and obtained by any native tool, not by Rust "
          "specifically.",
          "对保存即 lint 的工作流值得要；任何原生工具都能给，不是 Rust 独有。")),
        (("File-level parallelism without the GIL", "绕开 GIL 的文件级并行"),
         ("a large part of the published attribution, alongside parse-once architecture — and "
          "parse-once is not a language property.",
          "公开归因里占很大一块，另一块是一次解析的架构——而一次解析不是语言属性。")),
    ],
    "nobuys": [
        (("A faster flake8", "更快的 flake8"),
         ("the orchestrator is 4,741 lines and the checking happens in three Python packages; a 10× "
          "target is above the physical ceiling at that scope.",
          "编排器 4,741 行，检查工作在三个 Python 包里；10× 的目标高过这个范围的物理天花板。")),
        (("The plugin ecosystem", "插件生态"),
         ("entry-point-registered Python plugins cannot run inside a native binary without an embedded "
          "interpreter.",
          "用 entry-point 注册的 Python 插件，没有内嵌解释器就跑不进原生二进制。")),
        (("Memory safety", "内存安全"),
         ("Python is memory-safe at application scope and this codebase declares no FFI surface.",
          "Python 在应用层已经是内存安全的，这个代码库也没有声明 FFI 界面。")),
    ],

    "precedents": [
        {"name": "Astral · ruff", "outcome": "ADOPTED",
         "body": ("A Rust linter displaced the Python linter federation from outside it. "
                  "Adopter-reported gains ran far above vendor claims. Its author's decomposition "
                  "credits four things: reading and parsing each file once for all rules, native "
                  "execution, GIL-free parallelism, and caching.",
                  "一个 Rust linter 从外部把 Python linter 联盟顶掉了。采用方报告的加速远高于厂商自己"
                  "的说法。作者本人的拆解把功劳给了四件事：每个文件只读取和解析一次供所有规则使用、"
                  "原生执行、无 GIL 并行、缓存。"),
         "match": ("identical objective, identical tool category, and it already exists",
                   "目标一致，工具品类一致，而且它已经存在"),
         "mismatch": ("not a migration by flake8's maintainers; a separate tool with its own rule set",
                      "这不是 flake8 维护者做的迁移，是另一个工具，有自己的规则集"),
         "regime": "adopter-reported and first-party figures", "source_label": "third-party · project and adopter reports",
         "url": "https://github.com/astral-sh/ruff"},
        {"name": "pydantic · pydantic-core", "outcome": "EXTRACT",
         "body": ("A Rust validation core sat behind an unchanged Python API and captured native "
                  "value at a coarse seam. The kernel gain was reported at roughly 17× on a "
                  "representative model. End-to-end application gains landed around 2–3×.",
                  "一个 Rust 校验核心放在不变的 Python API 后面，在粗粒度的接缝上吃到了原生收益。"
                  "代表性模型上内核加速报告约 17×。应用端到端落在 2–3×。"),
         "match": ("the extraction pattern the rust-checker-extract option would follow",
                   "rust-checker-extract 这个方案要走的就是这种抽取形态"),
         "mismatch": ("pydantic owned its hot kernel; flake8 delegates checking to three separate packages",
                      "pydantic 自己拥有热点内核；flake8 把检查委派给三个独立的包"),
         "regime": "vendor benchmark plus user-reported app figures", "source_label": "first-party · vendor article",
         "url": "https://pydantic.dev/articles/pydantic-v2"},
        {"name": "Prettier · pure-JavaScript CLI rework", "outcome": "STAYED",
         "body": ("Roughly 3× from profiling, caching and IPC fixes, with no language change. The "
                  "baseline had simply never been optimized. Announced days after a Rust competitor "
                  "claimed the speed bounty.",
                  "靠 profiling、缓存和 IPC 修复拿到约 3×，语言一行没动。基线此前根本没被优化过。发布"
                  "时间就在某个 Rust 竞品领走速度赏金之后几天。"),
         "match": ("the in-stack counterfactual that must be priced before any rewrite",
                   "任何重写之前都必须先定价的栈内反事实"),
         "mismatch": ("a formatter with its own hot path, not a thin orchestrator over three packages",
                      "那是一个有自己热点路径的 formatter，不是压在三个包之上的薄编排器"),
         "regime": "reproduced 29 s → 9 s", "source_label": "first-party · project blog",
         "url": "https://prettier.io/blog/2023/11/30/cli-deep-dive"},
        {"name": "jaq vs jq", "outcome": "ADOPTED",
         "body": ("A Rust reimplementation of a widely used tool arrived from outside the original "
                  "project. The incumbent's maintainers wrote no Rust. Users who wanted the Rust "
                  "version installed it.",
                  "一个被广泛使用的工具，它的 Rust 重实现是从原项目外部冒出来的。原项目维护者一行 Rust "
                  "都没写。想要 Rust 版本的用户，自己装上就是了。"),
         "match": ("the same 'the ecosystem already shipped it' shape as this decision",
                   "和本次决策同一种形态：生态里已经有人把它做出来了"),
         "mismatch": ("jq has no plugin entry-point ecosystem to preserve",
                      "jq 没有需要保住的插件 entry-point 生态"),
         "regime": "author-run benchmarks", "source_label": "third-party · project README",
         "url": "https://github.com/01mf02/jaq"},
    ],

    "path": [
        {"title": ("Measure your own lint time before choosing", "先量自己的 lint 时间，再谈选型"),
         "body": ("The adopting team times its own lint configuration on its own repository, split per "
                  "tool and per invocation mode — per-save against CI. The number has to name which "
                  "mode hurts and by how much. If neither mode misses a threshold the team cares "
                  "about, stop here. Nothing changed, so nothing to undo.",
                  "采用方团队在自己的仓库上给现有 lint 配置计时，按工具拆，按调用方式拆——保存时触发和 "
                  "CI 分开。结果必须能指出是哪一种调用方式在疼、疼多少。如果两种方式都没有越过团队在意"
                  "的阈值，就到此为止。这一步什么都没改，也就没有东西要回滚。"),
         "owner": "the adopting team",
         "cost_range": ("1 day", "1 天"),
         "artifact": "wall-clock for the current lint configuration on the real repository, split per tool and per invocation mode (per-save versus CI)",
         "acceptance": "the measurement identifies which invocation mode actually hurts and by how much",
         "stop": "stop if neither mode misses a threshold the team cares about",
         "rollback": "measurement only"},
        {"title": ("Map your rules to the native tool", "把规则对到原生工具上"),
         "body": ("Same team, one table: every rule in the current flake8 plugin set against the native "
                  "linter's codes, with the unmapped ones written down rather than glossed. Each "
                  "enforced rule ends up either mapped or dropped on purpose, in writing. If an "
                  "unmapped rule turns out to be a hard requirement, keep flake8 and stop; that is a "
                  "legitimate outcome. Rollback is a configuration revert.",
                  "同一个团队，一张表：把现有 flake8 插件集里的每条规则对到原生 linter 的规则码上，映射"
                  "不上的写清楚，不要含糊过去。团队强制执行的每条规则，最后要么有映射，要么是白纸黑字"
                  "有意放弃。如果某条映射不上的规则是硬需求，那就留下 flake8，到此为止；这是一个正当"
                  "结果。回滚就是把配置改回去。"),
         "owner": "the adopting team",
         "cost_range": ("2–5 days", "2–5 天"),
         "artifact": "a rule-by-rule mapping from the current flake8 plugin set to the native linter's codes, with the unmapped rules listed explicitly",
         "acceptance": "every rule the team enforces is either mapped or consciously dropped, in writing",
         "stop": "stop and keep flake8 if an unmapped rule is a hard requirement — that is a legitimate outcome",
         "rollback": "revert the configuration; nothing else changed"},
        {"title": ("Run both in parallel for one cycle", "两个 linter 并行跑一个周期"),
         "body": ("Both linters run in CI for a cycle, with the native one non-blocking, and someone "
                  "diffs the findings. Each diff line gets an explanation. A silent drop with no "
                  "explanation stops the switch. Pulling the native linter out of CI restores the old "
                  "world exactly, because flake8 never stopped being the gate.",
                  "两个 linter 在 CI 里并行跑一个周期，原生的那个设为非阻塞，然后有人去 diff 两边的发现。"
                  "diff 的每一行都要有解释。任何一处没有解释的静默丢失，都足以叫停切换。把原生 linter 从 "
                  "CI 里撤掉就完全回到原样，因为 flake8 从头到尾都还是那道闸。"),
         "owner": "the adopting team",
         "cost_range": ("1 week", "1 周"),
         "artifact": "both linters in CI, with the native one non-blocking, and a diff of findings",
         "acceptance": "the finding diff is explained line by line, with no unexplained silent drops",
         "stop": "stop the switch on any unexplained divergence",
         "rollback": "remove the native linter from CI; flake8 remains the gate"},
        {"title": ("If flake8 must stay, profile it instead of rewriting it",
                   "如果 flake8 必须留下，就去 profile，不要重写"),
         "body": ("A flake8 contributor profiles the orchestrator together with its three checkers and "
                  "reports the top contributors with their measured shares. Two outcomes. Either "
                  "enough of the time sits inside flake8's own code, which reopens D2 with "
                  "measurements instead of a 30% assumption. Or it sits in the checkers, which is "
                  "where the structure says it is, and the Rust track closes. Nothing ships either way.",
                  "一位 flake8 贡献者把编排器和它的三个 checker 一起做 CPU profile，报告排在前面的贡献者"
                  "及其实测份额。两种结局。一种是有足够多的时间落在 flake8 自己的代码里，那就用实测数据"
                  "而不是 30% 的假设重开 D2。另一种是时间落在 checker 里，也就是结构本来指向的地方，"
                  "Rust 这条线就此关闭。两种结局都不上线任何东西。"),
         "owner": "a flake8 contributor",
         "cost_range": ("1–3 weeks", "1–3 周"),
         "artifact": "a CPU profile of the orchestrator and its three checkers, with the top contributors and their measured shares",
         "acceptance": "the profile either finds a material share in flake8's own code — reopening D2 with real inputs — or shows it is in the checkers",
         "stop": "stop the Rust track entirely if the time is in the checkers, which is where the structure says it is",
         "rollback": "measurement only"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端可达性"), "state": "HIT",
         "claim": ("The rewrite option's ceiling is 1.43× under a generous share assumption, so the 10× "
                   "target is above the physical ceiling at orchestrator scope.",
                   "在宽松的份额假设下，重写方案的天花板是 1.43×，10× 的目标高过编排器范围内的物理"
                   "天花板。"),
         "evidence": "decision_math.py · share=.30, kernel=inf, target=10"},
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("A large share of the reported speedup is parse-once architecture, not language; the "
                   "report separates the two rather than crediting all of it to Rust.",
                   "报告出的加速里有很大一块来自一次解析的架构，不来自语言；本报告把两者分开算，没有把"
                   "功劳全记在 Rust 头上。"),
         "evidence": "D5, D7 · notes.crmarsh.com decomposition"},
        {"name": ("Baseline and regime", "基线与测量口径"), "state": "HIT",
         "claim": ("The 150–1000× figures are adopter-reported for a competing tool on their own "
                   "codebases, not measurements of flake8 taken here.",
                   "150–1000× 这组数字，是采用方在自己代码库上对一个竞品工具的报告，不是这里对 flake8 "
                   "的实测。"),
         "evidence": "D1 caveat"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("The extraction option is priced with per-call PyO3 overhead of roughly 20–40 ns, and "
                   "the rewrite option with the loss of the Python plugin contract.",
                   "抽取方案按每次调用约 20–40 ns 的 PyO3 开销定价，重写方案按丢失 Python 插件契约定价。"),
         "evidence": "D10, D11"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The report notes that a Rust flake8 would duplicate a maintained tool, and asks who "
                   "would maintain the second one.",
                   "报告指出 Rust 版 flake8 会和一个有人维护的工具重复，并追问第二份实现由谁来维护。"),
         "evidence": "rust-rewrite-flake8 reason"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有预算的反事实对照"), "state": "HIT",
         "claim": ("In-stack profiling has not been done for flake8, and a comparable project found "
                   "roughly 3× that way — so the staying case is currently asserted rather than "
                   "measured.",
                   "flake8 没有做过栈内 profiling，而同型项目靠这条路拿到过约 3×——所以「不动」这一方"
                   "目前是断言，不是实测。"),
         "evidence": "D12 · reversible path step 4"},
        {"name": ("Target shortfall", "目标缺口"), "state": "HIT",
         "claim": ("Even the precedent-supported ~3× from Python-side optimization does not meet a 10× "
                   "target; the report states both facts together.",
                   "就算拿到先例支持的 ~3×，Python 侧优化也够不到 10× 的目标；报告把这两件事放在一起说。"),
         "evidence": "py-optimize benefit interval"},
        {"name": ("Cost of inaction", "不作为的代价"), "state": "PASS",
         "claim": ("The report grants the requirement and names the per-save cost rather than treating "
                   "slow linting as acceptable.",
                   "报告承认这个需求成立，并点名保存时触发的那部分代价，没有把慢当成可以接受。"),
         "evidence": "G1 PASS · D5"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("Native startup and GIL-free parallelism are recorded as advantages, and the selected "
                   "option is the one that captures them.",
                   "原生启动和无 GIL 并行都被记为优势，而被选中的方案正是能吃到这两点的那个。"),
         "evidence": "D5, D7, D9"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The path ends in a decision: adopt after a parallel-run cycle, or keep flake8 "
                   "because a specific plugin is a hard requirement.",
                   "路径终点是一个决定：并行跑一个周期之后采用，或者因为某个具体插件是硬需求而留下 "
                   "flake8。"),
         "evidence": "reversible path steps 2–3"},
    ],

    "gaps": [
        (("A profile of flake8's own orchestration share", "flake8 自身编排份额的 profile"),
         ("The 30% figure is a generous assumption, not a measurement. An actual profile would either "
          "reopen D2 with defensible inputs or confirm the time sits in the three checker packages.",
          "30% 是一个宽松的假设，不是实测。真跑一次 profile，要么用站得住的输入重开 D2，要么确认时间"
          "就在那三个 checker 包里。")),
        (("Rule-coverage mapping for the adopting team", "采用方团队的规则覆盖映射"),
         ("Adoption's actual cost is which rules do not map. Until that list exists, the selected "
          "option's compatibility risk is unquantified for any specific project.",
          "采用的真实成本在于哪些规则映射不过去。这份清单出来之前，对任何具体项目来说，所选方案的兼容"
          "风险都没有量化。")),
        (("An independent benchmark of flake8 versus the native linter",
          "flake8 与原生 linter 的独立基准测试"),
         ("Current figures are adopter-reported for the competing tool. An independent same-corpus "
          "comparison would firm up D1's strength.",
          "现在这些数字来自采用方对竞品工具的报告。一次同语料的独立对比可以坐实 D1 的证据强度。")),
    ],

    "assumptions": [
        "flake8's own orchestration share of lint wall-clock is at most 30% — an explicit upper bound chosen to be generous to the rewrite option, not a measurement.",
        "The shallow clone at the named commit represents the shipped package; dependency versions are read from setup.cfg as declared.",
        "The competing tool's reported multipliers are third-party adopter figures and are used directionally, never transferred as a predicted result.",
    ],
    "objective": {
        "driver": "performance",
        "requirement": "cut Python lint wall-clock by roughly an order of magnitude for per-save and CI invocation, without losing the checks a team relies on",
        "baseline": "flake8 orchestrating pycodestyle, pyflakes and mccabe in CPython",
        "target": "approximately 10x end-to-end, from the adopter-reported gap",
    },
    "repository": {
        "path": "https://github.com/PyCQA/flake8",
        "commit": "01b972636056a0ed581db62e260ef8df1ce470de",
        "scope": "whole repository; the orchestrator in src/ is the migration candidate",
        "sampling": "shallow clone; src/ (4,741 lines, 33 files), tests/ (4,802 lines) and setup.cfg measured; the three checker dependencies are separate packages and were not cloned",
    },
    "user_supplied_facts": [],

    "method_title": ("PyCQA/flake8 at 01b9726 · static read-only analysis · why-not-rust method 2.0",
                     "PyCQA/flake8 @ 01b9726 · 只读静态分析 · why-not-rust method 2.0"),
    "method_body": (
        "Repository: github.com/PyCQA/flake8 at commit 01b9726, shallow clone. Scope: the whole "
        "repository, with the orchestrator in src/ as the migration candidate. Sampling: 4,741 lines "
        "across 33 files in src/, 4,802 lines of tests, and packaging metadata from setup.cfg. "
        "install_requires names mccabe, pycodestyle and pyflakes; [options.entry_points] at "
        "setup.cfg:40 declares the flake8.extension and flake8.report tables. The three checker "
        "packages are separate distributions and were not cloned or measured. No build, test, "
        "benchmark or network call was run against the project. Objective: cut Python lint wall-clock "
        "by roughly an order of magnitude. User-supplied facts: none. Amdahl inputs: share=0.30, "
        "kernel speedup=infinite, boundary=0, target=10 → end-to-end 1.4285714285714286x, "
        "infinite-kernel ceiling 1.4285714285714286x, target physically IMPOSSIBLE. The 30% share is "
        "an explicit upper-bound assumption chosen to favour the rewrite option; it is not a profile. "
        "Gates 1 and 2 pass, gates 3 and 4 fail. So a performance requirement that clears the first "
        "two gates still yields REJECT: the cheapest option that meets it is adopting a tool that "
        "already exists. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/PyCQA/flake8，commit 01b9726，shallow clone。范围：整个仓库，其中 src/ 里的"
        "编排器是迁移候选。取样：src/ 下 33 个文件共 4,741 行，测试 4,802 行，以及 setup.cfg 里的打包"
        "元数据。install_requires 列出 mccabe、pycodestyle、pyflakes；setup.cfg:40 的 "
        "[options.entry_points] 声明了 flake8.extension 和 flake8.report 两张表。三个 checker 包是"
        "独立的发行物，没有克隆，也没有测量。没有对项目执行任何构建、测试、基准或网络调用。目标：把 "
        "Python lint 的墙钟时间压掉约一个数量级。用户提供的事实：无。Amdahl 输入：share=0.30, kernel "
        "speedup=infinite, boundary=0, target=10 → end-to-end 1.4285714285714286x, infinite-kernel "
        "ceiling 1.4285714285714286x, target physically IMPOSSIBLE。30% 这个份额是为了照顾重写方案而"
        "显式选取的上界，不是 profile 结果。G1、G2 通过，G3、G4 未通过。所以一个能过前两道门的性能"
        "需求，最终仍然是 REJECT：满足它的最便宜方案，是采用一个已经存在的工具。这是一套结构化决策"
        "协议，不是统计预测器。",
    ),
    "footer": ("public repository · static analysis at commit 01b9726 · no build, benchmark or network call",
               "公开仓库 · 在 commit 01b9726 上做静态分析 · 无构建、无基准、无网络调用"),
}
