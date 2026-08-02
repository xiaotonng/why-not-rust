"""redis/redis — the event loop everyone wants to rewrite is 516 lines.

Repository facts were measured read-only on the shallow clone named in
`repository`.
"""

CASE = {
    "slug": "redis",
    "project_name": "redis/redis",
    "project_desc": (
        "C · in-memory data store · 209,442 lines of own C, 141,130 lines of vendored C",
        "C · 内存数据存储 · 自有 C 代码 209,442 行，第三方内置 C 代码 141,130 行",
    ),
    "date": "2026-08-01",
    "archetype": (
        "infra-hotpath · network service with a C module ABI and an embedded interpreter",
        "基础设施热路径 · 网络服务，带 C 模块 ABI 和内嵌解释器",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "MEDIUM",
    "robustness": "STABLE",
    "selected": "stay-scoped",
    "scope_chip": (
        "keep the C core; harden the protocol surface in place",
        "保留 C 内核；就地加固协议面",
    ),
    "scope_sub": (
        "keep the store; the rewrite cannot deliver what it promises",
        "留在 C；重写兑现不了它承诺的东西",
    ),

    "why": (
        "Two things get proposed here: make Redis faster, make it memory-safe. Neither survives the "
        "repository. On speed, nobody has published a profile, and the file people picture rewriting is "
        "516 lines. On safety, deps/ carries 141,130 lines of C and headers, and 73,227 of those compile "
        "into the binary — jemalloc, and the Lua interpreter that EVAL is defined by. Rewrite all 209,442 "
        "lines of Redis and that C is still there.",
        "这里一次提两件事：让 Redis 更快，让它内存安全。两条都没能在这个仓库里站住。速度那条，没有人公开过 "
        "profile，而大家心里想重写的那个文件是 516 行。安全那条，deps/ 里有 141,130 行 C 和头文件，其中 "
        "73,227 行会编进二进制——jemalloc，还有 EVAL 语义所依赖的那个 Lua 解释器。把 Redis 自己的 209,442 "
        "行全部重写，这些 C 一行不少。",
    ),
    "trigger": (
        "Stable for the full-rewrite question. The speed half reopens the day someone publishes an "
        "end-to-end profile that splits kernel network time, protocol parsing, command execution and "
        "serialization. Until that exists it is UNKNOWN, not refuted.",
        "对「整体重写」这个问题，结论是稳定的。速度那一半，只要有人公开一份端到端 profile，把内核网络时间、"
        "协议解析、命令执行、序列化四块拆开，它就重新可评估。在那之前它是 UNKNOWN，不是被否证。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("C terminates an untrusted network protocol; that exposure is not in dispute.",
                           "C 直接终结一条不可信的网络协议，这块暴露面没有争议。"),
         "name": "requirement",
         "evidence": "networking.c (6,027 lines) parses RESP from network peers and 459 command definitions dispatch on it. The safety requirement is genuine; the performance requirement is not stated with a measurement."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Rust removes the class from any line it replaces.",
                           "凡是被 Rust 替换的代码行，那个缺陷类就消失。"),
         "name": "rust-specific causality",
         "evidence": "The mechanism is granted for the safety objective. For the performance objective it is UNKNOWN: no public profile locates Redis's time, and 58 lines referencing io_threads show the project already pursued throughput inside C."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("The rewrite cannot deliver a memory-safe Redis.",
                           "这场重写交付不出一个内存安全的 Redis。"),
         "name": "economics and smallest sufficient option",
         "evidence": "73,227 lines of vendored C — jemalloc src/include plus lua/src — compile into the binary after any rewrite of Redis's own code, so the full-migration option does not meet its own objective. Hardening the 6,027-line protocol path is both cheaper and better targeted."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("399 module ABI symbols, 459 commands, one embedded Lua VM.",
                           "399 个模块 ABI 符号，459 条命令，一个内嵌 Lua VM。"),
         "name": "delivery and reversibility",
         "evidence": "src/redismodule.h exports 399 REDISMODULE_API entry points that third-party modules link against, and eval.c holds a lua_State whose observable scripting semantics are part of the contract. No dual-run or rollback plan exists for that surface."},
    ],

    "tiles": [
        (("Event loop", "事件循环"), "516", ("lines", "行"),
         ("src/ae.c — the file the proposal usually pictures", "src/ae.c，提案脑子里想的通常就是这个文件")),
        (("Redis's own C", "Redis 自有 C"), "209,442", ("lines", "行"),
         ("src/ · 218 tracked files", "src/ · 版本库内 218 个文件")),
        (("Vendored C compiled into the binary", "编进二进制的第三方 C"), "73,227", ("lines", "行"),
         ("jemalloc src+include 52,575 + lua/src 20,652", "jemalloc src+include 52,575 行 + lua/src 20,652 行")),
        (("Module ABI entry points", "模块 ABI 入口点"), "399", ("symbols", "个符号"),
         ("src/redismodule.h · third-party link surface", "src/redismodule.h · 第三方链接面")),
        (("Command definitions", "命令定义"), "459", ("commands", "条命令"),
         ("src/commands/*.json · behavioural contract", "src/commands/*.json · 行为契约")),
        (("Public end-to-end profile", "公开的端到端 profile"), "0", ("published", "份"),
         ("why the performance claim is UNKNOWN, not refuted", "速度这一条记为 UNKNOWN 而不是被否证的原因")),
    ],

    "options_sub": (
        "Every option is judged against one objective: cut memory-unsafety exposure on Redis's "
        "network-facing path and raise throughput, without breaking the module ABI or scripting semantics.",
        "所有方案对着同一个目标：降低 Redis 网络侧路径上的内存不安全暴露，并提升吞吐，同时不破坏模块 ABI 和"
        "脚本语义。",
    ),
    "options": [
        {"id": "stay-scoped", "name": ("Harden the protocol path in C", "在 C 里加固协议路径"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("aims at the 6,027-line surface that faces the network",
                              "对准面向网络的那 6,027 行"),
         "one_time_cost": "weeks, scoped", "recurring_cost": "existing fuzz and review effort",
         "cost_cell": ("weeks; existing fuzz budget", "数周；用现有 fuzz 预算"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "native", "compat_cell": ("native · no ABI risk", "原生 · 无 ABI 风险"),
         "reversibility": "git revert",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the only option aimed at where the exposure is",
                  "推荐 · 唯一打在暴露面上的方案"),
         "reason": "Smallest option that reaches the actual trust boundary without touching the module ABI or the embedded interpreter."},
        {"id": "io-threads", "name": ("Continue in-C throughput work", "继续在 C 内做吞吐优化"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("unquantified here; already shipping", "此处未量化；已经在发布中"),
         "one_time_cost": "ongoing upstream work", "recurring_cost": "none new",
         "cost_cell": ("ongoing upstream; none new", "上游持续投入；无新增"),
         "time_to_value": ("per release", "随版本发布"),
         "compatibility": "native", "compat_cell": ("native · config-gated", "原生 · 配置开关控制"),
         "reversibility": "configuration",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded counterfactual any Rust speed claim must beat",
                  "保留 · 任何 Rust 性能主张都要先赢过这个已投入的对照"),
         "reason": "The project already moved I/O off the main thread in C; a Rust proposal must be compared against this, not against single-threaded Redis."},
        {"id": "rust-proto-extract", "name": ("Rust RESP parser behind the C API",
                                              "RESP 解析器换成 Rust，藏在 C API 后面"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed in the network-facing parser", "面向网络的解析器里，这个缺陷类消失"),
         "one_time_cost": "unpriced; parity harness needed", "recurring_cost": "Rust toolchain in every distro build",
         "cost_cell": ("unpriced; Rust in every build", "未定价；每次构建都要 Rust"),
         "time_to_value": ("months", "数月"),
         "compatibility": "byte-exact protocol behaviour",
         "compat_cell": ("same internal API · build-flag rollback", "内部 API 不变 · 用构建开关回滚"),
         "reversibility": "build flag, if kept dual", "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the only Rust scope with a shape you could defend",
                  "保留 · 唯一说得通的 Rust 范围"),
         "reason": "Correct target, but it adds a Rust toolchain requirement to every distribution build for a surface the C hardening option also covers."},
        {"id": "rust-full", "name": ("Rewrite Redis in Rust", "用 Rust 重写 Redis"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("misses memory safety; throughput unquantified", "拿不到内存安全；吞吐未量化"),
         "one_time_cost": "209,442 lines plus a scripting story", "recurring_cost": "399-symbol ABI compatibility forever",
         "cost_cell": ("209,442 lines; permanent ABI debt", "209,442 行；永久的 ABI 负债"),
         "time_to_value": ("years", "数年"),
         "compatibility": "module ABI + 459 commands + Lua semantics",
         "compat_cell": ("whole ABI + scripting · no rollback", "整套 ABI + 脚本 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails its own objective at G3", "排除 · 在 G3 上没达成自己设的目标"),
         "reason": "The vendored allocator and Lua interpreter remain C, so the result is not a memory-safe Redis; and no profile supports the throughput half."},
        {"id": "adopt-rust-store", "name": ("Adopt a Rust-implemented store", "改用 Rust 实现的存储"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for the adopter's deployment", "对采用方的那套部署，缺陷类消失"),
         "one_time_cost": "per deployment migration", "recurring_cost": "different operational surface",
         "cost_cell": ("per deployment; new ops surface", "按部署计；新的运维面"),
         "time_to_value": ("weeks per deployment", "每套部署数周"),
         "compatibility": "RESP-compatible, not module-compatible",
         "compat_cell": ("protocol only · restore from backup", "只兼容协议 · 从备份恢复"),
         "reversibility": "switch back", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · an operator's call, not the project's", "保留 · 这是运维方的决定，不是项目的决定"),
         "reason": "Meets the objective for a specific deployment that does not use modules or Lua; it does not address Redis's own surface."},
    ],

    "lenses_sub": (
        "Each state is evidence scoped to named options. They do not add up to a score. The performance "
        "lenses sit at UNKNOWN because no public profile exists, and argument moves them in neither "
        "direction.",
        "每条状态都绑定到具体方案，不是可以相加的分数。性能相关的几条停在 UNKNOWN，因为公开的 profile 不存在；"
        "靠辩论推不动它们，往哪边都推不动。",
    ),
    "na_note": (
        "Two lenses are N/A. D5 startup shape: Redis is a daemon started once per host. D8 distribution: "
        "the current C build already satisfies every constraint there is.",
        "两条记为 N/A。D5 启动形态：Redis 是每台机器只起一次的常驻进程。D8 分发：现在的 C 构建已经满足了所有"
        "约束。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "UNKNOWN · rust-full", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-full", "rust-proto-extract"],
         "claim": ("On the performance objective, nobody has located Redis's end-to-end time. No public "
                   "profile splits kernel networking, protocol parsing, command execution and "
                   "serialization. The owned share is unmeasured.",
                   "性能目标这边，没有人定位过 Redis 的端到端时间。公开资料里没有一份 profile 把内核网络、"
                   "协议解析、命令执行、序列化拆开。自有代码占多少，没量过。"),
         "source": "no published end-to-end Redis profile",
         "regime": "n/a — the measurement is absent",
         "caveat": "Recorded UNKNOWN rather than assumed either way; the structural note is that src/ae.c, the event loop, is 516 lines.",
         "change_trigger": "A published profile splitting those four components would make the performance claim assessable."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-full", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-full"],
         "claim": ("No Amdahl figure appears here. Without D1's time share there is no f worth defending. "
                   "Substituting a line share for a time share is a method error.",
                   "这里不给 Amdahl 数字。没有 D1 的时间占比，就没有站得住的 f。拿代码行数占比顶替时间占比是"
                   "方法错误。"),
         "source": "D1 is UNKNOWN", "regime": "n/a",
         "caveat": "The full-rewrite option therefore carries no benefit interval for throughput."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Redis has no managed runtime and no collector. No option removes a GC or JIT mechanism "
                   "from the tail, because there is none to remove. Allocator behaviour is shared: every "
                   "option keeps jemalloc.",
                   "Redis 没有托管运行时，也没有 collector。没有哪个方案能从尾延迟里拿走 GC 或 JIT，因为本来"
                   "就没有。分配器行为对所有方案一样：每个方案都继续用 jemalloc。"),
         "source": "deps/jemalloc src+include · 52,575 lines of C linked by all options",
         "regime": "shipped allocator choice",
         "caveat": "Allocator-induced tail effects would be identical across options unless the allocator itself changed."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "UNKNOWN · rust-full", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-full"],
         "claim": ("Per-instance memory is dominated by stored data and allocator behaviour, not by the "
                   "implementation language. No measurement separates them for Redis.",
                   "单实例内存主要由存储的数据和分配器行为决定，不是由实现语言决定。Redis 这边没有任何测量把"
                   "这几项分开。"),
         "source": "no published footprint decomposition",
         "regime": "n/a", "caveat": "A cost case would need instance count, utilization and price, none of which are in evidence here."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Redis is a long-lived daemon. Startup time is RDB/AOF load time, which tracks data "
                   "volume rather than language.",
                   "Redis 是常驻进程。启动时间就是 RDB/AOF 的加载时间，跟数据量走，不跟语言走。"),
         "source": "persistence load path", "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-proto-extract", "rust-full", "adopt-rust-store"],
         "claim": ("Redis parses an untrusted wire protocol in C, and it runs user-supplied Lua. Replace "
                   "the parsing code in Rust and the memory-unsafety class leaves that code.",
                   "Redis 用 C 解析不可信的线上协议，还执行用户提交的 Lua。把解析代码换成 Rust，那段代码里的"
                   "内存不安全缺陷类就消失。"),
         "source": "src/networking.c (6,027 lines) · src/eval.c lua_State",
         "regime": "structural, at the network boundary",
         "caveat": "Scripting sandbox escapes and logic defects are not memory-safety issues and survive the language change."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Single-threaded command execution is a correctness invariant Redis chose on purpose. "
                   "Rust does not lift it. The project already added I/O threading in C.",
                   "单线程执行命令是 Redis 有意选定的正确性不变量，Rust 解除不了它。而且项目已经在 C 里"
                   "加上了 I/O 线程。"),
         "source": "58 lines referencing io_threads in src/",
         "regime": "existing concurrency design",
         "caveat": "Any option that parallelizes command execution changes observable semantics, regardless of language."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("Redis ships as a self-contained native binary with no runtime dependency. Nothing "
                   "about distribution is unmet.",
                   "Redis 以自包含的原生二进制发布，没有运行时依赖。分发上没有未满足的约束。"),
         "source": "static C build", "regime": "n/a",
         "caveat": "Adding Rust would introduce a new build requirement for distributors rather than removing one."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "NEUTRAL · rust-full, adopt-rust-store", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["rust-full", "adopt-rust-store"],
         "claim": ("RESP-compatible stores exist in Rust and in other languages. None of them reproduces "
                   "the 399-symbol module ABI. Ecosystem availability does not argue for rewriting Redis "
                   "itself.",
                   "Rust 和别的语言里都有兼容 RESP 的存储。没有一个复刻了那 399 个符号的模块 ABI。生态里有"
                   "替代品，构不成重写 Redis 本身的理由。"),
         "source": "src/redismodule.h · 399 REDISMODULE_API entry points",
         "regime": "module compatibility surface",
         "caveat": "Deployments that use neither modules nor Lua face a much smaller compatibility surface."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": ("The compatibility surface is 399 exported module entry points, 459 command "
                   "definitions, and the observable semantics of an embedded Lua interpreter. That last "
                   "one includes error messages and type coercions scripts depend on.",
                   "兼容面是 399 个导出的模块入口点、459 条命令定义，加上一个内嵌 Lua 解释器的可观测语义。"
                   "最后这项包括脚本依赖的错误消息和类型转换。"),
         "source": "src/redismodule.h (1,951 lines) · src/commands/*.json (459 files) · src/eval.c",
         "regime": "static contract inventory in this commit",
         "caveat": "A protocol-parser extraction inherits almost none of this surface, and is retained for that reason."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": ("Rewrite Redis's own 209,442 lines of C and headers. 73,227 lines of vendored "
                   "allocator and interpreter C still compile into the same binary. The migration pays a "
                   "full rewrite's cost, and the safety objective it was bought for stays unmet.",
                   "把 Redis 自己那 209,442 行 C 和头文件重写完，仍有 73,227 行第三方分配器和解释器的 C 编进"
                   "同一个二进制。这笔迁移付的是完整重写的钱，而它要买的那个安全目标没拿到。"),
         "source": "deps/ 141,130 lines of C and headers across 8 projects; 73,227 in the compiled jemalloc and Lua trees",
         "regime": "static dependency inventory in this commit",
         "caveat": "Replacing jemalloc and Lua too is conceivable, and would change allocator behaviour and scripting semantics — a different and larger proposal."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-scoped, io-threads", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["stay-scoped", "io-threads"],
         "claim": ("Two in-stack alternatives are funded and shipping: protocol hardening in C, and I/O "
                   "threading already merged upstream. A Rust proposal has to beat both on one "
                   "measurement. That measurement does not exist yet.",
                   "栈内有两条已经投入并在发布的路线：在 C 里加固协议，以及已经合并进上游的 I/O 线程。Rust "
                   "提案要在同一份测量上赢过这两条。那份测量目前还不存在。"),
         "source": "58 lines referencing io_threads · existing fuzz and review practice",
         "regime": "current upstream engineering",
         "caveat": "Neither eliminates the memory-unsafety class; they reduce incidence and raise throughput within C."},
    ],

    "findings": [
        ("current",
         ("The event loop is 516 lines", "事件循环 516 行"),
         ("src/ae.c is the file most 'rewrite Redis in Rust' proposals have in mind. It is 516 lines. "
          "Whatever the performance story turns out to be, it is not concentrated there. Nobody has "
          "published a profile saying where it is.",
          "大多数「用 Rust 重写 Redis」的提案，脑子里想的是 src/ae.c。它 516 行。性能故事最后无论长什么样，"
          "都不会集中在这里。至于集中在哪里，没有人公开过 profile。"),
         "src/ae.c · 516 lines"),
        ("current",
         ("A Rust rewrite still compiles 73,227 lines of C into the binary",
          "重写完，仍有 73,227 行 C 编进二进制"),
         ("deps/ vendors 141,130 lines of C and headers across eight projects. Two of those trees build "
          "into redis-server: jemalloc's src and include at 52,575 lines, and lua/src at 20,652. That is "
          "73,227, against Redis's own 209,442 on the same counting basis. Rewriting Redis leaves every "
          "one of them in place. A memory-safe Redis is not on offer here.",
          "deps/ 里内置了八个项目、141,130 行 C 和头文件。其中两棵树会编进 redis-server：jemalloc 的 src 和 "
          "include，52,575 行；lua/src，20,652 行。合计 73,227 行，对照 Redis 自己在同一口径下的 209,442 行。"
          "重写 Redis 一行都动不到它们。一个内存安全的 Redis，这里买不到。"),
         "deps/jemalloc/{src,include} · deps/lua/src · matched .c/.h basis"),
        ("current",
         ("EVAL's semantics are an embedded C interpreter", "EVAL 的语义就是那个内嵌的 C 解释器"),
         ("src/eval.c holds a lua_State. src/script_lua.h registers the Redis API into it. Scripting "
          "compatibility is the observable behaviour of one specific interpreter, so there is no spec to "
          "re-implement against.",
          "src/eval.c 里持有一个 lua_State，src/script_lua.h 把 Redis API 注册进去。脚本兼容性是某一个具体"
          "解释器的可观测行为，没有一份规格可以照着重新实现。"),
         "src/eval.c:60 · src/script_lua.h:48"),
        ("current",
         ("399 module entry points are a link-time contract", "399 个模块入口点是链接期契约"),
         ("src/redismodule.h exports 399 REDISMODULE_API entry points. Third-party modules compile "
          "against them. A reimplementation owes all 399, on top of 459 command definitions.",
          "src/redismodule.h 导出 399 个 REDISMODULE_API 入口点，第三方模块就是对着它们编译的。重新实现要"
          "还上这 399 个，外加 459 条命令定义。"),
         "src/redismodule.h · 1,951 lines"),
        ("unknown",
         ("The performance claim is unmeasured, not refuted", "速度这一条是没量过，不是被否证"),
         ("No public end-to-end profile separates kernel network time, protocol parsing, command "
          "execution and serialization for Redis. D1 and D2 are recorded UNKNOWN. This report names the "
          "profile that would settle them. It does not assert that the language cannot help.",
          "没有一份公开的端到端 profile 把 Redis 的内核网络时间、协议解析、命令执行、序列化分开。D1 和 D2 "
          "记为 UNKNOWN。报告点名了能了结它们的那份 profile，没有断言换语言帮不上忙。"),
         "no published end-to-end profile"),
    ],

    "buys": [
        (("Class elimination wherever it lands", "它落到哪一段，哪一段就没有这个缺陷类"),
         ("a Rust protocol parser cannot produce a memory-unsafety defect while decoding RESP from a "
          "hostile peer.",
          "用 Rust 写的协议解析器，在解码敌意对端发来的 RESP 时产不出内存不安全缺陷。")),
        (("A small scope you could defend", "一个说得过去的小范围"),
         ("the network-facing parser is a seam that already exists. If a Rust option ever gets funded "
          "here, that is the one with a shape.",
          "面向网络的解析器本来就是一条现成的接缝。如果这里真要投一个 Rust 方案，那就是唯一有形状的那个。")),
        (("Nothing on throughput, on this evidence", "吞吐这一项，按现有证据什么也买不到"),
         ("the performance case is recorded UNKNOWN, and the report names the profile that would settle "
          "it.",
          "性能这条记为 UNKNOWN，报告里点名了能了结它的那份 profile。")),
    ],
    "nobuys": [
        (("A memory-safe Redis", "一个内存安全的 Redis"),
         ("73,227 lines of vendored allocator and interpreter C still compile into the binary after any "
          "rewrite of Redis's own code.",
          "不管把 Redis 自己的代码怎么重写，73,227 行第三方分配器和解释器的 C 照样编进二进制。")),
        (("Relief from the module ABI", "从模块 ABI 里解脱"),
         ("399 exported entry points and 459 command definitions survive every implementation change.",
          "399 个导出入口点和 459 条命令定义，在任何实现变更之后都还在。")),
        (("Freedom from the single-threaded invariant", "摆脱单线程不变量"),
         ("serialized command execution is a correctness decision. Parallelize it and the semantics "
          "change, in any language.",
          "串行执行命令是一个正确性决定。把它并行化就会改变语义，换什么语言都一样。")),
    ],

    "precedents": [
        {"name": "Grab · counter service", "outcome": "MIGRATED",
         "body": ("A Go service rewritten in Rust went from 20 cores to 4.5 at 1,000 QPS. p99 latency "
                  "came out 'similar (or perhaps even slightly worse)'. The team's own conclusion: "
                  "rewriting solely for performance is unlikely to yield significant benefits.",
                  "一个 Go 服务用 Rust 重写后，在 1,000 QPS 下核数从 20 降到 4.5。p99 延迟的结果是 "
                  "'similar (or perhaps even slightly worse)'。团队自己的结论：只为性能而重写，不太可能带来"
                  "显著收益。"),
         "match": ("high-QPS network service; the shape a language-swap performance result actually takes",
                   "高 QPS 网络服务；换语言得到的性能结果通常就长这样"),
         "mismatch": ("Go source with a GC, not C; and a service with no module ABI and no embedded "
                      "interpreter",
                      "源语言是带 GC 的 Go，不是 C；那个服务也没有模块 ABI，没有内嵌解释器"),
         "regime": "1,000 QPS steady state, first-party", "source_label": "first-party · engineering blog",
         "url": "https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust"},
        {"name": "Cloudflare · Pingora", "outcome": "MIGRATED",
         "body": ("A C/Lua edge proxy replaced in Rust cut CPU ~70% and memory ~67%. The team said "
                  "plainly where that came from: a new connection-sharing architecture, not code that "
                  "runs faster.",
                  "一个 C/Lua 的边缘代理换成 Rust 后，CPU 降约 70%，内存降约 67%。团队明说了收益来自哪里："
                  "新的连接共享架构，不是代码跑得更快。"),
         "match": ("C plus embedded Lua, at network scale, with a safety motive behind it",
                   "同样是 C 加内嵌 Lua，同样在网络规模上，背后同样有安全动机"),
         "mismatch": ("a proxy with no third-party module ABI, and the win is explicitly architectural",
                      "那是个没有第三方模块 ABI 的代理，而且收益被明确归给了架构"),
         "regime": ">1T requests/day, first-party", "source_label": "first-party · engineering blog",
         "url": "https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/"},
        {"name": "Twitch · Go ballast → GOMEMLIMIT", "outcome": "STAYED",
         "body": ("A runtime-level tuning change fixed tail latency on their busiest service. A runtime "
                  "flag later made the trick unnecessary. Where in-stack tuning is not exhausted, a "
                  "runtime question stays open. It is not yet an argument for migrating.",
                  "一次运行时层面的调参修好了他们最忙那个服务的尾延迟，后来一个运行时开关让这个技巧变得多余。"
                  "栈内调优没走完的时候，运行时的问题只是悬着，还构不成迁移的理由。"),
         "match": ("the discipline of exhausting in-stack options before blaming the language",
                   "在把问题归给语言之前，先把栈内选项走完的纪律"),
         "mismatch": ("a GC'd runtime problem; Redis has no collector to tune",
                      "那是带 GC 的运行时问题；Redis 没有 collector 可调"),
         "regime": "production tail latency, first-party", "source_label": "first-party · engineering blog",
         "url": "https://blog.twitch.tv/en/2019/04/10/go-memory-ballast-how-i-learnt-to-stop-worrying-and-love-the-heap/"},
        {"name": "Notion · WASM SQLite caching", "outcome": "STAYED",
         "body": ("Changing where the data lived improved user-perceived speed by 20–50%. The language "
                  "that processed it never changed. When the time is in I/O and round-trips, a language "
                  "swap is aimed at the wrong layer.",
                  "把数据换个地方放，用户感知速度提升了 20–50%，处理数据的语言一行没换。时间花在 I/O 和往返"
                  "上的时候，换语言打的是错误的层。"),
         "match": ("the wrong-layer test that Redis's unmeasured performance claim has not passed",
                   "「打错层」这道题，Redis 那个没量过的性能主张还没过"),
         "mismatch": ("a client application, not a server hot path",
                      "那是客户端应用，不是服务端热路径"),
         "regime": "first-party product measurements", "source_label": "first-party · engineering blog",
         "url": "https://www.notion.com/blog/how-we-sped-up-notion-in-the-browser-with-wasm-sqlite"},
    ],

    "path": [
        {"title": ("Publish the profile before the proposal", "先出 profile，再谈提案"),
         "body": ("Whoever proposes the rewrite publishes the profile first. State the QPS and payload "
                  "mix, then split measured wall-clock into kernel network time, protocol parsing, "
                  "command execution and reply serialization. The four shares must sum to the "
                  "wall-clock, on a harness a third party can re-run. If Redis's own code is not a large "
                  "share of it, stop the performance track — the profile has answered the question. No "
                  "code moves here.",
                  "提出重写的人先把 profile 发出来。写清 QPS 和负载配比，再把实测墙钟时间拆成内核网络、协议"
                  "解析、命令执行、回复序列化四块。四块之和要对得上墙钟，测量脚手架要能被第三方复跑。如果 "
                  "Redis 自己的代码占不了多少，性能这条线就停——profile 已经把问题回答了。这一步不动代码。"),
         "owner": "whoever proposes the rewrite",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "an end-to-end profile at a stated QPS and payload mix, splitting kernel network time, protocol parsing, command execution and reply serialization",
         "acceptance": "the four shares sum to the measured wall-clock and the harness is reproducible by a third party",
         "stop": "stop the performance track if Redis's own code is not a material share — that is the answer",
         "rollback": "measurement only; no code changes"},
        {"title": ("Harden the protocol path in C", "在 C 里加固协议路径"),
         "body": ("Redis maintainers fuzz the RESP parsing path, review its bounds handling, and land "
                  "whatever fixes come out. The step passes when the corpus covers the parser's "
                  "documented input space and one release cycle goes by with no new findings. If "
                  "findings keep landing in the same code, escalate to the Rust extraction option. "
                  "Backing out is a git revert. The ABI is never touched.",
                  "Redis 维护者对 RESP 解析路径做定向 fuzz 和边界审查，把查出来的问题修掉。通过标准是：语料"
                  "覆盖解析器文档化的输入空间，并且整整一个发布周期没有新发现。如果同一段代码反复出问题，就"
                  "升级到 Rust 抽取方案。回退就是一次 git revert，ABI 全程不动。"),
         "owner": "Redis maintainers",
         "cost_range": ("3–6 weeks", "3–6 周"),
         "artifact": "targeted fuzzing and bounds review of the RESP parsing path, with findings and fixes",
         "acceptance": "the fuzzing corpus covers the parser's documented input space with no new findings for one release cycle",
         "stop": "escalate to the Rust extraction option if findings keep recurring in the same code",
         "rollback": "git revert; the ABI is untouched"},
        {"title": ("Compare against in-C throughput work, not against 2015 Redis",
                   "要比的是 C 里已经做完的吞吐工作，不是 2015 年的 Redis"),
         "body": ("The proposer benchmarks the current build with I/O threading enabled. That "
                  "configuration is the baseline. Any Rust candidate is then measured against it on "
                  "identical hardware and payloads. If the candidate does not beat the tuned C baseline, "
                  "stop. Only a configuration moved, so there is nothing to undo.",
                  "提案人用开启 I/O 线程的当前构建跑一遍基准。这个配置就是基线。任何 Rust 候选都要在相同硬件、"
                  "相同负载下跟它比。赢不过调优后的 C 基线，就停。这一步只改了一项配置，没有什么要撤销的。"),
         "owner": "the proposer",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "a benchmark of the current build with I/O threading enabled as the baseline for any Rust claim",
         "acceptance": "the Rust candidate is measured against that configuration on identical hardware and payloads",
         "stop": "stop if the candidate does not beat the tuned C baseline",
         "rollback": "configuration change only"},
        {"title": ("Re-open only with the ABI answered", "ABI 有了交代，才谈重开"),
         "body": ("Redis maintainers write the plan for the 399-symbol module ABI and for Lua scripting "
                  "semantics under any reimplementation. The plan names which modules break, which "
                  "scripting behaviours break, and who owns that decision. No migration proposal "
                  "proceeds without it. Until one exists, the current C implementation continues "
                  "unchanged.",
                  "Redis 维护者写出一份计划：在任何重新实现之下，399 个符号的模块 ABI 和 Lua 脚本语义怎么办。"
                  "计划要点名哪些模块会坏、哪些脚本行为会变，以及这个决定归谁。没有这份计划，迁移提案一律不"
                  "往下走。在它出现之前，现在的 C 实现原样继续。"),
         "owner": "Redis maintainers",
         "cost_range": ("1 week per review", "每轮评审 1 周"),
         "artifact": "a written plan for the 399-symbol module ABI and Lua scripting semantics under any reimplementation",
         "acceptance": "the plan states which modules and which scripting behaviours would break, and who owns that decision",
         "stop": "no migration proposal proceeds without it",
         "rollback": "the current C implementation continues unchanged"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("No profile locates Redis's time, so the performance claim has no reach argument to "
                   "make. The report records UNKNOWN instead of filling the gap with an estimate.",
                   "没有 profile 定位 Redis 的时间去向，性能主张就拿不出影响面的论证。报告记 UNKNOWN，没有拿"
                   "估算把缺口填上。"),
         "evidence": "D1, D2 UNKNOWN"},
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The proposal bundles a safety objective with a throughput objective. Only the safety "
                   "mechanism is established. The report keeps the two apart.",
                   "提案把安全目标和吞吐目标捆在一起。只有安全那条的机制是成立的。报告把两者分开处理。"),
         "evidence": "G2 evidence · D6 vs D1"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("Any Rust throughput claim gets compared against the current build with I/O "
                   "threading, not against older single-threaded Redis.",
                   "任何 Rust 吞吐主张都要跟开启 I/O 线程的当前构建比，不是跟更早的单线程 Redis 比。"),
         "evidence": "58 lines referencing io_threads in src/"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("The 399-symbol module ABI, 459 command definitions and Lua semantics are named and "
                   "priced against the full-migration option.",
                   "399 个符号的模块 ABI、459 条命令定义和 Lua 语义都被点名，并计入整体迁移方案的成本。"),
         "evidence": "D10 · src/redismodule.h, src/commands/"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("Before any migration proposal proceeds, the report requires a written plan for the "
                   "ABI and for scripting semantics.",
                   "任何迁移提案往下走之前，报告都要求先有一份关于 ABI 和脚本语义的书面计划。"),
         "evidence": "reversible path step 4"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("Protocol hardening and in-C I/O threading are both shipping work, not hypothetical "
                   "optimizations.",
                   "协议加固和 C 内的 I/O 线程都是已经在发的工作，不是假想中的优化。"),
         "evidence": "D12 · 58 lines referencing io_threads"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying leaves the memory-unsafety class reachable in the 6,027-line network-facing "
                   "parser. The report says so. Redis's maturity is not counted here as safety.",
                   "不动，就意味着那 6,027 行面向网络的解析器里，内存不安全缺陷类依然可达。报告把这句写出来"
                   "了，没有把 Redis 的成熟度当成安全。"),
         "evidence": "D6 · src/networking.c"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The vendored C is disclosed as part of the attack surface. It is also the reason the "
                   "full rewrite fails its own objective.",
                   "第三方 C 被当作攻击面的一部分披露出来，没有藏。它同时也是整体重写达不成自身目标的原因。"),
         "evidence": "D11 · deps/ 141,130 lines of C and headers, 73,227 of them compiled"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report never claims Rust would be slower. It records the throughput question as "
                   "unmeasured and names the profile that settles it.",
                   "报告没有主张 Rust 会更慢。它把吞吐这个问题记为未测量，并点名了能了结它的那份 profile。"),
         "evidence": "D1 change trigger"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The hardening option carries an explicit escalation rule: recurring findings in the "
                   "same code move the decision to the Rust extraction option.",
                   "加固方案带一条明确的升级规则：同一段代码反复出问题，决策就转到 Rust 抽取方案。"),
         "evidence": "reversible path step 2"},
    ],

    "gaps": [
        (("End-to-end Redis profile at a stated QPS and payload mix",
          "端到端 Redis profile，含明确的 QPS 和负载配比"),
         ("This settles the performance half. While it is missing, D1 and D2 stay UNKNOWN and no "
          "throughput claim can be authorized in any language.",
          "它能了结性能那一半。缺着的时候，D1 和 D2 停在 UNKNOWN，任何语言的吞吐主张都授权不了。")),
        (("Root-cause classification of Redis's advisory history",
          "对 Redis 历史安全公告做根因分类"),
         ("Would tell the hardening work where to aim, and would strengthen or weaken the "
          "protocol-parser extraction option.",
          "它能告诉加固工作往哪里打，也会让协议解析器抽取方案的理由变强或变弱。")),
        (("A written plan for the module ABI and Lua semantics",
          "一份关于模块 ABI 和 Lua 语义的书面计划"),
         ("Without it, G4 stays FAIL for every reimplementation option regardless of what the profile "
          "shows.",
          "没有它，不管 profile 显示什么，G4 对每个重新实现的方案都停在 FAIL。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; vendored deps/ are counted as they ship.",
        "Module ABI symbol count comes from REDISMODULE_API occurrences in src/redismodule.h and is read as one entry point per occurrence.",
        "The proposal under assessment is the commonly stated one — rewrite Redis in Rust for speed and memory safety — since no specific RFC was supplied.",
    ],
    "objective": {
        "driver": "mixed safety and performance",
        "requirement": "reduce memory-unsafety exposure on Redis's network-facing path and improve throughput, without breaking the module ABI or scripting semantics",
        "baseline": "6,027 lines of C parse RESP from untrusted peers; no public end-to-end throughput profile exists",
        "target": "class elimination on the network-facing path; throughput target unstated by the proposal",
    },
    "repository": {
        "path": "https://github.com/redis/redis",
        "commit": "3acc0c49cf5ad2af9425d333e62728342dd6159b",
        "scope": "whole repository; src/networking.c and the RESP path are the candidate seam",
        "sampling": "shallow clone; 1,858 tracked files enumerated; src/, deps/, src/commands/ and tests/ measured; no profiling or benchmark was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "redis/redis at 3acc0c4 · static read-only analysis · why-not-rust method 2.0",
        "redis/redis @ 3acc0c4 · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/redis/redis at commit 3acc0c4, shallow clone, 1,858 tracked files. "
        "Scope: the whole repository, with the RESP parsing path as the candidate seam. Sampling: src/ "
        "is 209,442 lines of C and headers across 218 files. deps/ is 141,130 lines of C and headers "
        "across 508 files in eight vendored projects; of those, the jemalloc src/include and lua/src "
        "trees that actually compile are 73,227. Every own-versus-vendored comparison in this report "
        "uses that matched .c/.h basis, never whole-tree totals. src/ae.c is 516 lines; src/networking.c "
        "is 6,027. src/redismodule.h is 1,951 lines and carries 402 REDISMODULE_API occurrences, of "
        "which 399 are function-pointer entry points (the other three are the APIVER define and the "
        "include guard), corroborated independently by 399 REDISMODULE_GET_API occurrences. There are "
        "459 command definition files, and tests/ is 113,836 lines. No build, test, benchmark or "
        "network call was run against the project. Objective: no specific RFC was supplied, so the "
        "assessment takes the commonly stated proposal — reduce memory-unsafety exposure and improve "
        "throughput by rewriting Redis in Rust. User-supplied facts: none. No Amdahl calculation "
        "appears. D1 is UNKNOWN "
        "because no public end-to-end profile exists, and without a time share there is no defensible "
        "f. The performance half of the proposal is therefore recorded UNKNOWN rather than refuted. The "
        "decision turns on G3 and G4, which fail on measured facts about the vendored C and the module "
        "ABI. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/redis/redis，commit 3acc0c4，shallow clone，1,858 个纳管文件。范围：整个仓库，候选"
        "接缝是 RESP 解析路径。采样：src/ 是 209,442 行 C 和头文件，分布在 218 个文件里。deps/ 是 141,130 行 "
        "C 和头文件，分布在八个第三方项目的 508 个文件里；其中真正参与编译的 jemalloc src/include 与 lua/src "
        "两棵树合计 73,227 行。本报告里所有「自有 vs 第三方」的对比都用这个对齐的 .c/.h 口径，不用整棵树的"
        "总数。src/ae.c 516 行；src/networking.c 6,027 行。src/redismodule.h 1,951 行，其中 REDISMODULE_API "
        "出现 402 次，399 次是函数指针入口点（另外三次是 APIVER 宏和 include guard），并由 399 次 "
        "REDISMODULE_GET_API 出现独立佐证。命令定义文件 459 个，tests/ 113,836 行。没有对项目做过任何构建、"
        "测试、基准或网络调用。目标：没有人给出具体的 RFC，因此按通常被提出的那个提案评估——用 Rust 重写 "
        "Redis，以降低内存不安全暴露并提升吞吐。用户提供的事实：无。本报告没有 Amdahl 计算。D1 是 UNKNOWN，因为不"
        "存在公开的端到端 profile；没有时间占比就没有站得住的 f。所以提案里性能那一半记为 UNKNOWN，不是被"
        "否证。决策落在 G3 和 G4 上，这两道门是在关于第三方 C 和模块 ABI 的实测事实上失败的。这是一套结构化"
        "决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 3acc0c4 · no build, benchmark or network call",
        "公开仓库 · 在 commit 3acc0c4 上做静态分析 · 没有构建、基准或网络调用",
    ),
}
