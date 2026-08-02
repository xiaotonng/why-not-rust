"""FFmpeg/FFmpeg — 2,021,868 lines, and the report authorizes rewriting 3.6% of them.

Repository facts were measured read-only on the shallow clone named in
`repository`.
"""

CASE = {
    "slug": "ffmpeg",
    "project_name": "FFmpeg/FFmpeg",
    "project_desc": (
        "C + assembly · media framework · 1,827,590 lines of C/headers plus 194,278 lines of hand-written asm",
        "C + 汇编 · 媒体框架 · C 与头文件 1,827,590 行，另有手写汇编 194,278 行",
    ),
    "date": "2026-08-01",
    "archetype": (
        "security-parser · table-driven module framework with hand-tuned SIMD",
        "安全解析器 · 表驱动模块框架，配手工调优的 SIMD",
    ),

    "scope_word": "PARTIAL",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "rust-demux-partial",
    "scope_chip": (
        "the container demux/parse layer only, behind the existing module interface",
        "只做容器 demux/parse 层，走现有模块接口",
    ),
    "scope_sub": (
        "replace the layer attacker bytes reach first",
        "替换攻击者字节最先抵达的那一层",
    ),

    "why": (
        "Hostile bytes hit the container demux and bitstream parse layer first. That layer is 72,465 lines "
        "across 210 files, 3.6% of a 2,021,868-line tree, and it already sits behind a table-driven interface "
        "hosting 368 independent demuxer modules. Requirement and seam line up. The other 96% is excluded for "
        "one reason: 194,278 lines of it are hand-written assembly that carries the throughput and no part of "
        "the safety objective, and a rewrite inherits none of it.",

        "攻击者的字节最先落在容器 demux 与 bitstream parse 层。这一层 72,465 行，分布在 210 个文件里，占 "
        "2,021,868 行代码树的 3.6%，而且早就位于一个表驱动接口之后，接口上挂着 368 个互相独立的 demuxer 模块。"
        "需求和接缝对得上。剩下的 96% 被排除只有一个理由：其中 194,278 行是手写汇编，扛的是吞吐量，"
        "不承担安全目标的任何部分，重写一行也继承不到。",
    ),
    "trigger": (
        "Conditional. Re-open if a demuxer replacement cannot reach bit-exact output parity on the FATE corpus, "
        "if the per-module boundary adds measurable decode overhead, or if no maintainer commits to the Rust "
        "modules. With this many modules, an unowned subsystem rots fast.",

        "有条件。出现下面任何一种情况就重开：替换后的 demuxer 在 FATE 语料上达不到逐位一致的输出；"
        "按模块划分的边界带来可测的解码开销；没有 maintainer 认领这些 Rust 模块。模块这么多，无人认领的子系统烂得很快。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("368 demuxer modules parse attacker-supplied containers in C.",
                           "368 个 demuxer 模块用 C 解析攻击者提供的容器。"),
         "name": "requirement",
         "evidence": "FFmpeg's inputs are untrusted media files by definition; the project runs a dedicated security list and publishes a CVE ledger, and states it is 'currently receiving a very large number of reports'."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Container/bitstream parsing in C is the canonical Rust safety case.",
                           "用 C 做容器/bitstream 解析，正是 Rust 安全论证的标准场景。"),
         "name": "rust-specific causality",
         "evidence": "The safety delta follows from replacing manual-lifetime C at the point untrusted bytes are first interpreted; no algorithm, format or architecture change is needed to obtain it."},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"),
         "hero_evidence": ("3.6% of the codebase, versus 100%, with no additional safety benefit.",
                           "3.6% 对 100%，后者不带来额外的安全收益。"),
         "name": "economics and smallest sufficient option",
         "evidence": "The demux/parse layer is 72,465 lines across 210 files. Extending the scope to the 999,497-line codec layer adds cost without moving the objective, and requires re-creating 194,278 lines of hand-written assembly."},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"),
         "hero_evidence": ("Table-driven module ABI plus a bit-exact regression corpus.",
                           "表驱动的模块 ABI，加一套逐位一致的回归语料。"),
         "name": "delivery and reversibility",
         "evidence": "Demuxers register through the AVInputFormat/FFInputFormat struct, so a Rust module is selectable per format and removable per module; the project's own FATE suite provides bit-exact acceptance. Precedent exists: Mozilla ships a Rust MP4 metadata parser behind a C API in Firefox."},
    ],

    "tiles": [
        (("Total code measured", "测得的代码总量"), "2,021,868", ("lines", "行"),
         ("C 1,567,523 + headers 260,067 + asm 194,278", "C 1,567,523 + 头文件 260,067 + 汇编 194,278")),
        (("Authorized scope", "授权范围"), "72,465", ("lines", "行"),
         ("demux 59,433 + bitstream parsers 13,032 · 210 files · 3.6%",
          "demux 59,433 + bitstream parser 13,032 · 210 个文件 · 3.6%")),
        (("Excluded: hand-written asm", "排除项：手写汇编"), "194,278", ("lines", "行"),
         (".asm and .S · a rewrite inherits none of it", ".asm 与 .S · 重写一行也继承不到")),
        (("Demuxer modules behind one struct", "挂在同一个 struct 后的 demuxer 模块"), "368", ("modules", "个模块"),
         ("libavformat/allformats.c registrations", "libavformat/allformats.c 里的注册项")),
        (("Decoder modules (out of scope)", "decoder 模块（范围外）"), "604", ("modules", "个模块"),
         ("libavcodec/allcodecs.c registrations", "libavcodec/allcodecs.c 里的注册项")),
        (("Codec layer left alone", "不动的编解码层"), "999,497", ("lines", "行"),
         ("libavcodec .c+.h · 55% of C and headers", "libavcodec 的 .c+.h · 占 C 与头文件的 55%")),
    ],

    "options_sub": (
        "Same objective for every option: eliminate the memory-unsafety class at the point FFmpeg first "
        "interprets attacker-controlled bytes, without changing decode output or losing SIMD throughput.",

        "每个方案的目标都一样：在 FFmpeg 首次解释攻击者控制的字节的地方消除内存不安全这一整类缺陷，"
        "同时不改变解码输出，也不损失 SIMD 吞吐。",
    ),
    "options": [
        {"id": "c-fuzz", "name": ("Fuzz and harden the C demuxers", "对 C demuxer 做模糊测试和加固"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("reduces incidence, class stays reachable", "降低发生率，整类缺陷仍然可达"),
         "one_time_cost": "none new", "recurring_cost": "existing fuzzing and triage effort",
         "cost_cell": ("none new; existing triage load", "无新增；现有的分诊负担"),
         "time_to_value": ("already running", "已经在跑"),
         "compatibility": "native", "compat_cell": ("native · no risk", "原生 · 无风险"), "reversibility": "n/a",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the funded baseline, and it stays after the Rust modules land",
                  "保留 · 有预算的基线，Rust 模块上线后继续保留"),
         "reason": "Necessary regardless; it lowers incidence but cannot remove the class from 72,465 lines of C."},
        {"id": "sandbox", "name": ("Sandbox the whole framework in the host", "在宿主里把整个框架沙箱化"),
         "implementation": "non-rust-native",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("contains the class rather than removing it", "把这类缺陷关住，而不是移除"),
         "one_time_cost": "host-side, per application", "recurring_cost": "process/IPC boundary per stream",
         "cost_cell": ("host-side; IPC per stream", "宿主侧；每路流一次 IPC"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "unchanged decode behaviour",
         "compat_cell": ("unchanged framework · trivial rollback", "框架不变 · 回滚很轻"),
         "reversibility": "remove the sandbox", "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · what most large consumers actually do, and it composes with the Rust option",
                  "保留 · 大型使用方实际就这么做，而且能和 Rust 方案叠加"),
         "reason": "Strong containment with no upstream change; does not eliminate the class, and every consumer pays it separately."},
        {"id": "rust-demux-partial", "name": ("Rust demux/parse modules", "Rust 写的 demux/parse 模块"),
         "implementation": "rust",
         "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("class eliminated in the layer attacker bytes reach first",
                              "在攻击者字节最先抵达的那一层消除整类缺陷"),
         "one_time_cost": "per module; highest-exposure formats first", "recurring_cost": "Rust in the build; module maintainers",
         "cost_cell": ("per module; Rust toolchain + owners", "按模块计价；Rust 工具链 + 模块负责人"),
         "time_to_value": ("one format", "一个格式的工期"),
         "compatibility": "bit-exact output required",
         "compat_cell": ("same module ABI · per-format rollback", "沿用同一模块 ABI · 按格式回滚"),
         "reversibility": "unregister the module", "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · smallest scope that removes the class where it matters",
                  "推荐 · 在要紧的位置移除这类缺陷的最小范围"),
         "reason": "Coarse existing seam, per-module rollback, bit-exact acceptance corpus, and a shipped precedent in another large native media stack."},
        {"id": "rust-full", "name": ("Rewrite FFmpeg in Rust", "用 Rust 重写 FFmpeg"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("no additional safety benefit over the demux layer", "相比只做 demux 层，没有额外的安全收益"),
         "one_time_cost": "re-create 194,278 lines of asm and 604 decoders", "recurring_cost": "two toolchains on every platform",
         "cost_cell": ("re-create asm + 604 decoders", "重造汇编 + 604 个 decoder"),
         "time_to_value": ("years", "数年"),
         "compatibility": "bit-exactness across 972 modules",
         "compat_cell": ("whole framework · no rollback", "整个框架 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G3; the excluded 96% carries no part of the objective",
                  "排除 · G3 不过；被排除的 96% 不承担目标的任何部分"),
         "reason": "Adds the entire codec and SIMD surface to a safety objective that lives in the demux layer, and no public profile exists to support the performance half of the proposal."},
        {"id": "adopt-rust-media", "name": ("Consumers adopt Rust media crates", "使用方改用 Rust 媒体 crate"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for the formats the crate covers", "crate 覆盖到的格式上，这类缺陷被移除"),
         "one_time_cost": "per consumer", "recurring_cost": "far narrower format and codec coverage",
         "cost_cell": ("per consumer; narrow format coverage", "按使用方计价；格式覆盖窄"),
         "time_to_value": ("days per project", "每个项目数天"),
         "compatibility": "different API and coverage",
         "compat_cell": ("different API · caller-side rollback", "API 不同 · 在调用方回滚"),
         "reversibility": "caller-side", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · works where the format set is small and known", "保留 · 格式集合小且已知时可行"),
         "reason": "Viable for applications handling a handful of formats; no crate approaches FFmpeg's 368-demuxer, 604-decoder coverage."},
    ],

    "lenses_sub": (
        "States are evidence scoped to named options. They do not add up to a score. The performance half of "
        "the usual proposal is recorded as UNKNOWN rather than argued, because no public FFmpeg profile exists.",

        "每个状态都是绑定到具体方案的证据，不能相加成分数。常见提案里性能那一半记为 UNKNOWN，不拿来论证："
        "没有公开的 FFmpeg 性能剖析。",
    ),
    "na_note": (
        "N/A lenses: D4 fleet footprint and D5 startup shape do not bear on this objective. FFmpeg is invoked "
        "as a library or a batch process inside the caller's own deployment.",

        "N/A 维度：D4 机群规模和 D5 启动形态与本目标无关。FFmpeg 是在调用方自己的部署里以库或批处理进程的形式被调用的。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"), "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-demux-partial", "rust-full", "adopt-rust-media"],
         "claim": ("368 demuxer modules and 68 bitstream parsers own the first interpretation of "
                   "attacker-controlled container data, in 72,465 lines of C.",
                   "368 个 demuxer 模块和 68 个 bitstream parser 负责第一次解释攻击者控制的容器数据，共 72,465 行 C。"),
         "source": "libavformat/*dec.c and *demux*.c (142 files) · libavcodec/*_parser.c (68 files)",
         "regime": "static structure of the shipped framework",
         "caveat": "Structural exposure at the entry point; the project's CVE ledger is not published with per-component attribution."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响"), "label": "UNKNOWN · rust-full", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-full"],
         "claim": ("The performance half of a full-rewrite proposal cannot be evaluated. No public FFmpeg "
                   "profile gives the time share of the C that a Rust port would replace, and a line share "
                   "is not a time share.",
                   "全量重写提案里性能那一半无法评估。没有公开的 FFmpeg 剖析给出 Rust 移植要替换的那部分 C 占多少时间，"
                   "而行数占比不等于时间占比。"),
         "source": "no public end-to-end decode profile",
         "regime": "n/a — the measurement is absent",
         "caveat": "Recorded as UNKNOWN rather than estimated. The safety objective does not require this number; a performance claim would.",
         "change_trigger": "A published decode profile separating asm kernels from C control flow would make the performance claim assessable."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("No managed runtime or collector exists, so there is no runtime mechanism in any tail to remove.",
                   "没有托管运行时，也没有回收器，尾部里没有可以拿掉的运行时机制。"),
         "source": "C framework, no GC", "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机群规模"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("FFmpeg runs inside the caller's process or batch job; this decision changes no fleet density.",
                   "FFmpeg 跑在调用方的进程或批处理作业里；这个决策不改变任何机群密度。"),
         "source": "library and CLI invocation model", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"), "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("Transcode jobs are long-lived relative to process start; startup is not a stated constraint.",
                   "相对于进程启动，转码作业是长时任务；启动时间不在已声明的约束里。"),
         "source": "no startup requirement asserted", "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"), "label": "SUPPORTS · rust-demux-partial", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-demux-partial", "rust-full"],
         "claim": ("The demux/parse layer interprets length fields, offsets and indices supplied by the file; "
                   "replacing it in Rust removes that class by construction at the exact boundary.",
                   "demux/parse 层解释的是文件给出的长度字段、偏移量和索引；用 Rust 替换它，就在这条边界上从构造上消除了这类缺陷。"),
         "source": "libavformat demuxer read_header/read_packet implementations",
         "regime": "structural, at the trust boundary",
         "caveat": "Logic defects, format-confusion and resource-exhaustion bugs survive the language change."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"), "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Frame- and slice-level threading already exists in the C implementation; no option is "
                   "blocked by the language on this axis.",
                   "C 实现里已经有帧级和 slice 级线程；在这条轴上没有方案被语言卡住。"),
         "source": "libavcodec/pthread_frame.c · pthread_slice.c",
         "regime": "existing threading model",
         "caveat": "A Rust module must interoperate with the existing threading contract rather than replace it."},
        {"id": "D8", "name": ("Distribution", "分发"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-full"],
         "claim": ("FFmpeg builds across an unusually wide platform and architecture matrix, including targets "
                   "carried mainly by their C toolchain and per-architecture assembly.",
                   "FFmpeg 要在一个异常宽的平台与架构矩阵上构建，其中一些目标主要靠各自的 C 工具链和按架构写的汇编撑着。"),
         "source": "libavcodec/{x86,aarch64,arm,ppc,riscv,loongarch,mips}/ subtrees",
         "regime": "supported architecture inventory",
         "caveat": "One optional Rust module is a much smaller distribution change than a full rewrite."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"), "label": "SUPPORTS · rust-demux-partial", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-demux-partial", "adopt-rust-media"],
         "claim": ("Rust container parsers exist and one is shipped inside a major C/C++ media stack behind a "
                   "C API, so the integration shape is demonstrated rather than theoretical.",
                   "Rust 的容器解析器是存在的，其中一个已经带着 C API 发布在一个主流 C/C++ 媒体栈里，集成形态有实物可看。"),
         "source": "https://github.com/mozilla/mp4parse-rust — mp4parse plus mp4parse_capi, shipped into mozilla-central",
         "regime": "third-party project, shipped as a pinned revision in Firefox",
         "caveat": "It parses track metadata, not the full demux path, and covers one container family."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"), "label": "SUPPORTS · rust-demux-partial", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["rust-demux-partial"],
         "claim": ("Demuxers register through a struct-shaped module interface, so the boundary is one "
                   "registration per format with packets crossing in bulk — not a per-sample FFI call.",
                   "demuxer 通过一个 struct 形态的模块接口注册，边界就是每个格式注册一次，packet 成批穿过，"
                   "不是每个 sample 调一次 FFI。"),
         "source": "libavformat/avformat.h:565 typedef struct AVInputFormat · 368 registered demuxers",
         "regime": "existing internal module ABI",
         "caveat": "Bit-exact output parity is required, and boundary cost per packet must be measured rather than assumed negligible."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"), "label": "DISFAVORS · rust-full", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full"],
         "claim": ("A full rewrite must re-create 194,278 lines of hand-written assembly and 604 decoder "
                   "modules, none of which serve the safety objective; the per-module option prices only the "
                   "formats it replaces.",
                   "全量重写必须重造 194,278 行手写汇编和 604 个 decoder 模块，它们都不服务于安全目标；"
                   "按模块推进的方案只为自己替换掉的那些格式付钱。"),
         "source": "*.asm and *.S (420 files, 194,278 lines) · 604 registered decoders",
         "regime": "static inventory in this commit",
         "caveat": "Assembly could in principle be kept via FFI, which is exactly what makes the full rewrite's benefit case empty rather than merely expensive."},
        {"id": "D12", "name": ("Counterfactual", "反事实"), "label": "SUPPORTS · c-fuzz, sandbox", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["c-fuzz", "sandbox"],
         "claim": ("Two funded alternatives already operate: continuous fuzzing with an active triage pipeline, "
                   "and host-side sandboxing by large consumers. The Rust option composes with both rather than "
                   "replacing them.",
                   "已经有两条有预算的替代路线在跑：带活跃分诊流程的持续模糊测试，以及大型使用方在宿主侧做的沙箱。"
                   "Rust 方案和这两条叠加，不取代它们。"),
         "source": "https://ffmpeg.org/security.html — project security process and CVE ledger",
         "regime": "current project practice",
         "caveat": "The security page notes a very large report volume and explicitly flags a spike in AI-generated false positives, which is triage load rather than defect evidence."},
    ],

    "findings": [
        ("rust", ("The attack surface is 3.6% of the codebase", "攻击面只占代码库的 3.6%"),
         ("Container demux is 59,433 lines across 142 files. The bitstream parsers add 13,032 across 68 more. "
          "Total: 72,465 lines, 3.6% of the tree. Attacker-controlled bytes get interpreted there first. "
          "Framework-wide proposals target something about twenty-eight times bigger.",

          "容器 demux 是 142 个文件、59,433 行。bitstream parser 再加 68 个文件、13,032 行。合计 72,465 行，"
          "占代码树的 3.6%。攻击者控制的字节最先在这里被解释。而面向整个框架的提案，瞄准的体量大约是它的二十八倍。"),
         "libavformat/*dec.c, *demux*.c · libavcodec/*_parser.c"),
        ("current", ("194,278 lines of hand-written assembly are the reason not to widen",
                     "不该扩大范围的理由：194,278 行手写汇编"),
         ("FFmpeg's throughput lives in .asm and .S files spread over seven architecture subtrees. A Rust "
          "rewrite inherits none of it. Either you keep that assembly over FFI or you write it again. Both add "
          "cost, and the safety objective is already satisfied by 3.6% of the tree.",

          "FFmpeg 的吞吐量在 .asm 和 .S 里，散布在七个架构子树中。Rust 重写一行也继承不到。要么用 FFI 把这些汇编留着，"
          "要么重新写一遍。两条路都加成本，而安全目标靠代码树的 3.6% 就已经满足。"),
         "420 asm files · libavcodec's x86, aarch64 and arm subtrees are 147,380 lines with their C wrappers"),
        ("rust", ("The seam is already a module table", "接缝已经是一张模块表"),
         ("Demuxers register as struct instances. There are 368. A Rust demuxer is one more registration: "
          "selectable per format, removable per format. Packets cross in bulk, not one sample at a time.",

          "demuxer 以 struct 实例的形式注册，一共 368 个。一个 Rust demuxer 就是多一条注册记录：按格式启用，按格式移除。"
          "packet 成批穿过，不是一个 sample 过一次。"),
         "libavformat/avformat.h:565 · 300 ff_*_demuxer definitions"),
        ("rust", ("The integration shape has shipped elsewhere", "这种集成形态别处已经上线了"),
         ("Mozilla maintains a Rust ISO-BMFF parser with a C API wrapper, and ships pinned revisions of it into "
          "Firefox. The project describes it as a pure-Rust replacement for the metadata parser the browser "
          "needs. Same language pair. Same boundary shape, same kind of host.",

          "Mozilla 维护一个带 C API 包装的 Rust ISO-BMFF 解析器，并以固定 revision 的方式发进 Firefox。"
          "项目自己的说法是：这是浏览器所需元数据解析器的纯 Rust 替代。语言组合相同。边界形态相同，宿主类型也相同。"),
         "github.com/mozilla/mp4parse-rust · mp4parse + mp4parse_capi"),
        ("unknown", ("The performance half of the proposal is unmeasurable today", "提案里性能那一半，今天量不出来"),
         ("No public FFmpeg profile separates time in SIMD kernels from time in C control flow. Without that "
          "split, a speedup claim is arithmetic on line counts. D2 stays UNKNOWN. The full-rewrite option "
          "carries no benefit interval as a result.",

          "没有公开的 FFmpeg 剖析把 SIMD kernel 的时间和 C 控制流的时间分开。缺了这一刀，任何加速比都只是拿行数做算术。"
          "D2 保持 UNKNOWN。全量重写方案因此没有收益区间。"),
         "no public end-to-end decode profile"),
    ],

    "buys": [
        (("Class elimination at the entry point", "在入口处消除整类缺陷"),
         ("a Rust demuxer cannot produce a memory-unsafety defect while interpreting the length fields and "
          "offsets a hostile file supplies.",
          "Rust 写的 demuxer 在解释恶意文件给出的长度字段和偏移量时，产生不了内存不安全缺陷。")),
        (("Per-format blast radius", "爆炸半径收敛到单个格式"),
         ("the module table means one format can be replaced, shipped, and unregistered independently of the "
          "other 367.",
          "有模块表在，一个格式可以独立于另外 367 个被替换、发布、下架。")),
        (("A parity harness that already exists", "对齐用的验收台已经有了"),
         ("FFmpeg's own bit-exact regression suite answers 'did the output change' before release, which keeps "
          "this option cheap to try.",
          "FFmpeg 自带的逐位一致回归套件能在发布前回答「输出变了没有」，这让这个方案试起来很便宜。")),
    ],
    "nobuys": [
        (("Any throughput improvement", "任何吞吐提升"),
         ("the speed is in 194,278 lines of hand-written assembly; a Rust demuxer neither helps nor is meant to.",
          "速度在那 194,278 行手写汇编里；Rust demuxer 帮不上忙，也不打算帮。")),
        (("Safety for the codec layer", "编解码层的安全性"),
         ("999,497 lines of libavcodec stay in C; this scope does not reach them and the report does not "
          "pretend otherwise.",
          "libavcodec 的 999,497 行继续留在 C；本范围够不到那里，报告也不假装够得到。")),
        (("Freedom from logic bugs", "摆脱逻辑缺陷"),
         ("format confusion, integer semantics and resource exhaustion survive the language change and still "
          "need fuzzing.",
          "格式混淆、整数语义、资源耗尽都能挺过换语言，仍然要靠模糊测试。")),
    ],

    "precedents": [
        {"name": "Mozilla · mp4parse-rust", "outcome": "PARTIAL SHIPPED",
         "body": ("A Rust ISO-BMFF parser with a C API wrapper lives as a standalone crate. Firefox ships "
                  "pinned revisions of it, in place of the metadata parser the browser relied on before.",
                  "一个带 C API 包装的 Rust ISO-BMFF 解析器以独立 crate 的形式维护。Firefox 以固定 revision 的方式引入，"
                  "取代浏览器原先依赖的元数据解析器。"),
         "match": ("same language pair, same container-parsing boundary, C API in a large native media stack",
                   "语言组合相同，容器解析的边界相同，同样是大型原生媒体栈里的 C API"),
         "mismatch": ("track metadata only, one container family, and a browser's threat model rather than a "
                      "general transcoder",
                      "只做 track 元数据，只覆盖一个容器家族，威胁模型是浏览器的，不是通用转码器的"),
         "regime": "shipped revision in mozilla-central", "source_label": "first-party · project README",
         "url": "https://github.com/mozilla/mp4parse-rust"},
        {"name": "Mozilla · Stylo", "outcome": "PARTIAL SHIPPED",
         "body": ("One subsystem with a clean interface got replaced in Rust inside a large C++ codebase, and "
                  "shipped in about two years. The same organisation's whole-engine replacement was cancelled.",
                  "在一个大型 C++ 代码库里，一个接口干净的子系统被 Rust 替换，大约两年上线。"
                  "同一家机构的整引擎替换则被取消。"),
         "match": ("component-scoped replacement inside a large native codebase with an existing internal interface",
                   "在已有内部接口的大型原生代码库里做组件级替换"),
         "mismatch": ("CSS styling had a parallelism benefit; this scope claims safety only",
                      "CSS 样式计算有并行化收益；本范围只主张安全性"),
         "regime": "shipped in Firefox 57", "source_label": "first-party · engineer account",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Google · Android memory-safety program", "outcome": "INCREMENTAL",
         "body": ("Memory safety's share of Android vulnerabilities fell from 76% to below 20%. Mass rewriting "
                  "was explicitly not the method. New code was made safe and old C/C++ was left to age out. "
                  "Their data puts vulnerability density in older code 3.4–7.4× below new code.",
                  "内存安全类缺陷在 Android 漏洞中的占比从 76% 降到 20% 以下。大规模重写被明确排除在做法之外。"
                  "路线是让新代码安全，让旧的 C/C++ 自然老化。他们的数据显示，旧代码的漏洞密度比新代码低 3.4–7.4×。"),
         "match": ("same requirement class and the same 'scope the replacement' conclusion",
                   "需求类别相同，结论同样是「把替换范围划小」"),
         "mismatch": ("OS-wide programme; figures are C/C++-relative rather than component-attributed",
                      "那是操作系统级的计划；数字相对的是 C/C++ 整体，没有按组件归因"),
         "regime": "2019–2025 vulnerability share", "source_label": "first-party · vendor security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
        {"name": "Mozilla · Servo as Gecko replacement", "outcome": "CANCELLED",
         "body": ("The whole-engine replacement was costed at thousands of engineer-years against a handful of "
                  "funded positions. It was cancelled. The component extractions shipped.",
                  "整引擎替换的估算是数千人年，对面只有为数不多的带薪岗位。项目被取消。真正上线的是拆出来的组件。"),
         "match": ("the outcome the excluded full-rewrite option is heading toward at 2,021,868 lines",
                   "被排除的全量重写方案在 2,021,868 行的体量下，正走向同样的结局"),
         "mismatch": ("a browser engine, and Servo had a research budget FFmpeg does not",
                      "对象是浏览器引擎，而且 Servo 有 FFmpeg 没有的研究预算"),
         "regime": "2012–2020 programme outcome", "source_label": "first-party · engineer account",
         "url": "https://en.wikipedia.org/wiki/Servo_(software)"},
    ],

    "path": [
        {"title": ("Pick the format by exposure, not by taste", "按暴露面挑格式，不按口味"),
         "body": ("FFmpeg's security contacts rank the container formats by attacker reachability and by how "
                  "often each one shows up in reports, then name the first target. The ranking has to come out "
                  "of the project's own CVE ledger and fuzzing findings, not out of opinion. If no format "
                  "stands out, stop: sandboxing alone is the better answer. Only documentation changes here.",

                  "FFmpeg 的安全联系人按攻击者可达性和历史报告量给容器格式排序，并点名第一个目标。"
                  "排序必须来自项目自己的 CVE 记录和模糊测试结果，不能靠印象。如果没有哪个格式明显更突出，就停："
                  "单靠沙箱是更好的答案。这一步只动文档。"),
         "owner": "FFmpeg security contacts",
         "cost_range": ("1–2 weeks", "1–2 周"),
         "artifact": "a ranking of container formats by attacker reachability and historical report volume, with the chosen first target named",
         "acceptance": "the ranking is derived from the project's own CVE ledger and fuzzing findings, not from opinion",
         "stop": "stop if no format shows materially higher exposure than the others — then sandboxing alone is the better answer",
         "rollback": "documentation only"},
        {"title": ("Measure the module boundary before writing the module", "先量接缝，再写模块"),
         "body": ("Two engineers who know both C and Rust register a null Rust demuxer through the existing "
                  "struct interface, then time it against the C equivalent on the same inputs. Passing means "
                  "boundary overhead sits inside noise under the project's own timing methodology, with the "
                  "measurement published. Visible per-packet crossing cost means stop — the seam is wrong even "
                  "though the objective is right. Rollback is one deletion. Nothing was registered by default.",

                  "两位同时熟悉 C 和 Rust 的工程师，用现有的 struct 接口注册一个空的 Rust demuxer，"
                  "在同一批输入上和 C 版本对时。通过的标准是：按项目自己的计时方法，边界开销落在噪声以内，并公开测量结果。"
                  "逐 packet 的穿越成本只要看得见，就停——接缝错了，哪怕目标是对的。回滚只是删掉这个模块。默认本来就没注册它。"),
         "owner": "two engineers with C and Rust experience",
         "cost_range": ("2 weeks", "2 周"),
         "artifact": "a null Rust demuxer registered through the existing struct interface, measured against its C equivalent on the same inputs",
         "acceptance": "boundary overhead is within noise on the project's own timing methodology, with the measurement published",
         "stop": "stop if per-packet crossing cost is material; the seam would then be wrong even though the objective is right",
         "rollback": "delete the null module; nothing is registered by default"},
        {"title": ("Ship one Rust demuxer behind a build flag", "先用编译开关放出一个 Rust demuxer"),
         "body": ("The Rust module maintainers implement the chosen format in Rust, disabled by default, with a "
                  "differential-fuzzing harness pointed at the C demuxer. Three things have to hold: bit-exact "
                  "output on the project's regression corpus, identical accept/reject decisions under "
                  "differential fuzzing, and no measured decode regression. At twelve weeks without "
                  "bit-exactness, stop and publish the divergences. Rollback unregisters the module. The C "
                  "demuxer stays the default for that format.",

                  "Rust 模块维护者用 Rust 实现选定的格式，默认关闭，并配一套对着 C demuxer 跑的差分模糊测试。"
                  "三条必须同时成立：在项目回归语料上输出逐位一致；差分模糊测试下接受/拒绝的判断完全相同；"
                  "解码没有可测的退化。到第十二周仍然做不到逐位一致，就停下来，把差异公布出去。回滚就是取消注册。"
                  "那个格式的默认实现仍然是 C demuxer。"),
         "owner": "the Rust module maintainers",
         "cost_range": ("8–12 weeks", "8–12 周"),
         "artifact": "a Rust implementation of the chosen format with a differential-fuzzing harness against the C demuxer, disabled by default",
         "acceptance": "bit-exact output on the project's regression corpus, identical accept/reject decisions under differential fuzzing, and no measured decode regression",
         "stop": "stop at twelve weeks if bit-exactness is unreached; publish the divergences",
         "rollback": "unregister the module; the C demuxer remains the default for that format"},
        {"title": ("Name owners before adding the second module", "加第二个模块之前，先把人定下来"),
         "body": ("Before a second module lands, FFmpeg maintainers name at least two committed reviewers for "
                  "the Rust subsystem and write down what happens to unowned modules. No Rust module is enabled "
                  "by default without two people who can review and release changes to it. If ownership lapses, "
                  "disable them. An unmaintained parser is worse than none. The C demuxers never left, and they "
                  "become the default again.",

                  "在第二个模块进来之前，FFmpeg maintainer 要为这个 Rust 子系统点名至少两位承诺投入的评审人，"
                  "并把无人认领模块的处理写成明文政策。没有两个人能评审并发布改动的 Rust 模块，不许默认开启。"
                  "归属一旦断了，就关掉。没人维护的解析器比没有更糟。C demuxer 一直都在，会重新变回默认。"),
         "owner": "FFmpeg maintainers",
         "cost_range": ("ongoing", "持续"),
         "artifact": "at least two committed reviewers for the Rust subsystem and a documented policy for unowned modules",
         "acceptance": "no Rust module is enabled by default without two people who can review and release changes to it",
         "stop": "if ownership lapses, disable the Rust modules by default rather than shipping unmaintained parsers",
         "rollback": "the C demuxers are still present and become the default again"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响"), "state": "PASS",
         "claim": ("No performance benefit is claimed for the selected option, and the full-rewrite option's "
                   "performance case is recorded UNKNOWN rather than estimated from line counts.",
                   "选定方案不主张任何性能收益；全量重写方案的性能论证记为 UNKNOWN，没有拿行数去估。"),
         "evidence": "D2 UNKNOWN"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("The safety delta is attributed to the language property at the demux boundary only; no "
                   "architecture or format change is credited to Rust.",
                   "安全收益只归因于 demux 边界上的语言属性；没有把任何架构或格式改动算到 Rust 头上。"),
         "evidence": "D6 record"},
        {"name": ("Baseline and regime", "基线与口径"), "state": "HIT",
         "claim": ("Format selection currently rests on structural exposure, because the project's CVE ledger "
                   "is not published with per-component attribution.",
                   "格式的挑选目前靠结构性暴露面，因为项目的 CVE 记录没有按组件归因公布。"),
         "evidence": "D1 caveat · ffmpeg.org/security.html"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "HIT",
         "claim": ("Per-packet boundary cost has not been measured yet. The path spends two weeks on a null "
                   "module before anyone writes a real one.",
                   "逐 packet 的边界成本还没有测过。所以路径里先花两周做一个空模块，然后才动真的。"),
         "evidence": "D10 caveat · reversible path step 2"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The path blocks the second Rust module on two named reviewers and defines what happens if "
                   "ownership lapses.",
                   "路径把第二个 Rust 模块卡在「两位具名评审人」上，并规定了归属断掉时怎么办。"),
         "evidence": "reversible path step 4"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有预算的反事实"), "state": "PASS",
         "claim": ("Fuzzing with active triage and host-side sandboxing are both recorded as options that stay "
                   "in place after the Rust modules land.",
                   "带活跃分诊的模糊测试和宿主侧沙箱都被记为方案，并且在 Rust 模块上线之后继续保留。"),
         "evidence": "D12 · c-fuzz, sandbox"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying entirely in C leaves the memory-unsafety class reachable in the 72,465 lines that "
                   "interpret hostile files first.",
                   "完全留在 C，就是让内存不安全这一整类缺陷在最先解释恶意文件的那 72,465 行里保持可达。"),
         "evidence": "D1 · G1 PASS"},
        {"name": ("Unsafe-surface omission", "遗漏不安全面"), "state": "PASS",
         "claim": ("The report names the demux/parse surface explicitly rather than treating FFmpeg's maturity "
                   "as a substitute for safety.",
                   "报告明确点出 demux/parse 这块面，没有拿 FFmpeg 的成熟度当安全性的替代品。"),
         "evidence": "D1 and D6 records"},
        {"name": ("Native-advantage denial", "否认 Rust 侧已有战绩"), "state": "PASS",
         "claim": ("A shipped Rust container parser inside another large native media stack is cited as working "
                   "evidence, not dismissed as a toy.",
                   "另一个大型原生媒体栈里已经上线的 Rust 容器解析器，被当作可用证据引用，没有当玩具打发掉。"),
         "evidence": "D9 · github.com/mozilla/mp4parse-rust"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The authorized scope is bounded at the demux layer with explicit acceptance thresholds, so "
                   "this is neither an open-ended rewrite nor an open-ended 'fuzz forever'.",
                   "授权范围止于 demux 层，并带明确的验收阈值：既不是没有边界的重写，也不是没有边界的「一直 fuzz 下去」。"),
         "evidence": "selected option scope · reversible path steps 2–3"},
    ],

    "gaps": [
        (("Per-component attribution of FFmpeg's CVE ledger", "FFmpeg CVE 记录的按组件归因"),
         ("Format selection currently rests on structural exposure. With attribution, step 1 gets a defensible "
          "first target; without it, the first module may be the wrong one.",
          "格式挑选目前靠结构性暴露面。有了归因，第 1 步就能给出站得住的首个目标；没有的话，第一个模块可能选错。")),
        (("Measured per-packet boundary cost at the module interface", "模块接口上逐 packet 边界成本的实测"),
         ("If crossing cost is material, the seam is wrong even though the objective is right, and the option "
          "reverts to sandboxing plus fuzzing.",
          "如果穿越成本大到要紧，接缝就是错的，哪怕目标是对的，方案会退回沙箱加模糊测试。")),
        (("End-to-end decode profile separating asm from C", "把汇编和 C 分开的端到端解码剖析"),
         ("Absent this, the performance half of any full-rewrite proposal stays UNKNOWN and that option keeps "
          "an empty benefit interval.",
          "没有它，任何全量重写提案里性能那一半都保持 UNKNOWN，那个方案的收益区间也一直是空的。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; module counts come from registration-symbol matches in tracked sources.",
        "FFmpeg's bit-exact regression corpus is available to the implementing team as the acceptance harness.",
        "No performance requirement is attached to the selected option; if one appears, D2 must be recomputed from a real profile.",
    ],
    "objective": {
        "driver": "safety",
        "requirement": "eliminate the memory-unsafety class at the point FFmpeg first interprets attacker-controlled bytes, without changing decode output or losing SIMD throughput",
        "baseline": "72,465 lines of C — 59,433 across 368 demuxer modules plus 13,032 across 68 bitstream parsers — interpret hostile input first",
        "target": "class elimination in the demux/parse layer with bit-exact output parity",
    },
    "repository": {
        "path": "https://github.com/FFmpeg/FFmpeg",
        "commit": "946272b79a325e9bce613b260e50e4e4fe7f3159",
        "scope": "whole repository; the libavformat demux/parse layer is the selected component",
        "sampling": "shallow clone; 10,511 tracked files enumerated; libavcodec, libavformat, libavfilter, libavutil, libswscale, libswresample and architecture subtrees measured; FATE media fixtures not downloaded",
    },
    "user_supplied_facts": [],

    "method_title": (
        "FFmpeg/FFmpeg at 946272b · static read-only analysis · why-not-rust method 2.0",
        "FFmpeg/FFmpeg @ 946272b · 只读静态分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/FFmpeg/FFmpeg at commit 946272b, shallow clone, 10,511 tracked files. Scope: "
        "the whole repository, with the libavformat demux/parse layer as the selected component. Sampling: "
        "1,567,523 lines of C, 260,067 of headers, 110,661 in .S and 83,617 in .asm files, for 2,021,868 lines "
        "total; libavcodec 999,497; libavformat 272,807, of which 59,433 across 142 files are demux. Module "
        "counts come from the registration tables: 368 extern const FFInputFormat demuxer declarations in "
        "libavformat/allformats.c, and 604 extern const FFCodec decoder declarations in libavcodec/allcodecs.c. "
        "Per-directory figures count .c and .h together; the 1,567,523 figure is .c only, and each lens states "
        "which. The authorized scope is 59,433 lines of libavformat demux plus 13,032 lines of libavcodec "
        "bitstream parsers, 72,465 in total across 210 files. No build, test, benchmark or network call was run "
        "against the project. Objective: eliminate the memory-unsafety class at the point FFmpeg first "
        "interprets attacker-controlled bytes, without changing decode output or losing SIMD throughput. "
        "User-supplied facts: none. D2 is recorded UNKNOWN, not estimated. No public profile separates time in "
        "SIMD kernels from time in C control flow, and converting the 3.6% line share into a speedup would be a "
        "method error. The full-rewrite option therefore carries no benefit interval instead of a favourable "
        "one. This is a structured decision protocol, not a statistical predictor.",

        "仓库：github.com/FFmpeg/FFmpeg，commit 946272b，浅克隆，10,511 个纳入版本管理的文件。范围：整个仓库，"
        "选定组件是 libavformat 的 demux/parse 层。采样：C 1,567,523 行，头文件 260,067 行，.S 文件 110,661 行，"
        ".asm 文件 83,617 行，合计 2,021,868 行；libavcodec 999,497 行；libavformat 272,807 行，其中 142 个文件、"
        "59,433 行属于 demux。模块数量取自注册表：libavformat/allformats.c 中 368 条 extern const FFInputFormat "
        "demuxer 声明，libavcodec/allcodecs.c 中 604 条 extern const FFCodec decoder 声明。按目录统计的数字把 .c 和 "
        ".h 一起计入；1,567,523 这个数字只算 .c，每个维度都会写明用的是哪一种。授权范围是 libavformat demux 的 "
        "59,433 行，加 libavcodec bitstream parser 的 13,032 行，合计 72,465 行，分布在 210 个文件中。"
        "没有对该项目执行任何构建、测试、基准或网络调用。目标：在 FFmpeg 首次解释攻击者控制的字节的地方消除"
        "内存不安全这一整类缺陷，同时不改变解码输出，也不损失 SIMD 吞吐。用户提供的事实：无。D2 记为 UNKNOWN，"
        "不做估算：没有公开剖析把 SIMD kernel 的时间与 C 控制流的时间分开，把 3.6% 的行数占比换算成加速比属于方法错误。"
        "全量重写方案因此没有收益区间，而不是拿到一个好看的区间。这是一套结构化的决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 946272b · no build, benchmark or network call",
        "公开仓库 · 在 commit 946272b 上做静态分析 · 无构建、无基准、无网络调用",
    ),
}
