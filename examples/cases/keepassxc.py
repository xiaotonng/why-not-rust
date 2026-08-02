"""keepassxreboot/keepassxc — Qt is in 476 of 660 files, so a Rust port is a UI rewrite.

Repository facts were measured read-only on the shallow clone named in
`repository`. The 45 `.ts` files in this tree are Qt Linguist translation XML,
not TypeScript; every count below excludes them.
"""

CASE = {
    "slug": "keepassxc",
    "project_name": "keepassxreboot/keepassxc",
    "project_desc": (
        "C++/Qt6 · desktop password manager · 113,863 lines of own src, 16,076 of them security-critical",
        "C++/Qt6 · 桌面密码管理器 · 自有 src 113,863 行，其中 16,076 行属安全关键",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · Qt6 application that parses attacker-supplied files while holding secrets",
        "原生桌面 GUI · Qt6 应用，手里攥着密码，同时解析别人递过来的文件",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "HIGH",
    "robustness": "CONDITIONAL",
    "selected": "stay-fuzz",
    "scope_chip": (
        "keep C++/Qt; point the fuzzer the project already built at the pre-auth parser",
        "留在 C++/Qt；把项目自己已经搭好的 fuzzer 对准预认证解析器",
    ),
    "scope_sub": (
        "stay native; the migration buys a new UI, not a safer parser",
        "继续原生；这场迁移买到的是一套新 UI，不是更安全的解析器",
    ),

    "why": (
        "KeePassXC parses hostile files in C++ while holding secrets. A malicious .kdbx reaches "
        "Kdbx4Reader::readHeaderField before the HMAC is checked, so the exposure is not hypothetical. "
        "Then look at who does the parsing. XML goes to QXmlStreamReader, gzip to zlib, every cipher and "
        "KDF to Botan. KeePassXC's own share of that path is 2,003 lines. Qt appears in 476 of its 660 "
        "source files, so migrating to Rust means building a new UI, which means shipping a different "
        "application.",
        "KeePassXC 用 C++ 解析别人递过来的文件，手里还攥着密码。一个恶意 .kdbx 会先走到 "
        "Kdbx4Reader::readHeaderField，HMAC 校验发生在那之后，所以暴露面不是假想的。再看这条路上究竟是谁"
        "在解析。XML 交给 QXmlStreamReader，gzip 交给 zlib，所有分组密码和 KDF 交给 Botan。KeePassXC 自己"
        "在这条路上只占 2,003 行。Qt 出现在它 660 个源文件中的 476 个，所以迁到 Rust 就得重做一套 UI，"
        "而那等于发布另一个应用。",
    ),
    "trigger": (
        "Stable on the migration question; the Qt counts will not be reinterpreted. Conditional on the "
        "extraction. The project ships an AFL harness aimed at exactly this path. If it finds a "
        "memory-safety defect in the pre-auth header parse or in one of the six importers, "
        "rust-parse-extract becomes the recommendation, and this report was wrong about urgency rather "
        "than about scope.",
        "「整体迁移」这个问题上结论是稳的，Qt 那几个数字不会被重新解读。抽取方案则是有条件的。项目自带一套 "
        "AFL 脚手架，打的正是这条路。如果它在预认证的头部解析或六个导入器里查出内存安全缺陷，推荐结论就换成 "
        "rust-parse-extract；那说明本报告错在紧迫性，不在范围。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("A hostile .kdbx header is parsed before any credential is verified.",
                           "恶意 .kdbx 的头部在任何凭据被验证之前就已经被解析。"),
         "name": "requirement",
         "evidence": "src/format/Kdbx4Reader.cpp:157 reads a file-controlled quint32 length and reads that many bytes; the header HMAC is not compared until line 77 of readDatabaseImpl. Six import formats add 3,705 lines that consume files from other vendors. The safety requirement is named and reachable."},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"),
         "hero_evidence": ("Rust removes the class from the 2,003 lines it would replace.",
                           "它替掉的那 2,003 行里，这个缺陷类会消失。"),
         "name": "rust-specific causality",
         "evidence": "The mechanism is granted for the framing code KeePassXC owns: 2,003 lines on the KDBX read path, including three raw memcpy sites in the block streams. It stops there. QXmlStreamReader parses the decrypted XML, zlib inflates it, and Botan performs every cipher, hash and KDF."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("85.9% of the rewrite budget buys no safety at all.",
                           "重写预算里 85.9% 买不到任何安全收益。"),
         "name": "economics and smallest sufficient option",
         "evidence": "The security-relevant core is 16,076 of 113,863 own src lines, 14.1%. src/gui alone is 50,344, 44.2%. A smaller option is already tooled: utils/fuzz-testing/README.md drives AFL at keepassxc-cli ls with a mutated .kdbx, and src/cli/Utils.cpp:225 carries the __AFL_COMPILER hook it needs."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("476 of 660 files include a Qt header. 72 .ui files. 45 translations.",
                           "660 个文件里 476 个 include 了 Qt 头。72 个 .ui 文件。45 种翻译。"),
         "name": "delivery and reversibility",
         "evidence": "218 distinct Qt headers are included across src/, 194 files declare Q_OBJECT, and 164 class declarations derive from a Qt type. 72 Qt Designer .ui files hold 18,677 lines and 45 Qt Linguist catalogues hold 472,765. No production-grade Rust Qt binding exists, so the migration is a UI replacement with no dual-run and no rollback."},
    ],

    "tiles": [
        (("Security-relevant core", "安全关键内核"), "14.1", ("% of own src", "% 自有 src"),
         ("src/format + crypto + keys + streams · 16,076 of 113,863 lines",
          "src/format + crypto + keys + streams · 16,076 / 113,863 行")),
        (("Files that include a Qt header", "include 了 Qt 头的文件"), "476", ("of 660", "/ 660"),
         ("the migration blocker, counted rather than asserted", "迁移的拦路虎，是数出来的，不是断言的")),
        (("Memory-safety CVEs on record", "有记录的内存安全 CVE"), "0", ("of 6", "/ 6 条"),
         ("NVD records for KeePassXC and KeePassX, 2015–2026",
          "NVD 里 KeePassXC 与 KeePassX 的记录，2015–2026")),
        (("Qt Designer files a rewrite must replace", "重写必须替掉的 Qt Designer 文件"), "72", ("files", "个"),
         ("18,677 lines of .ui XML with no Rust equivalent",
          "18,677 行 .ui XML，Rust 侧没有对应物")),
        (("Translations bound to Qt Linguist", "绑在 Qt Linguist 上的翻译"), "45", ("languages", "种语言"),
         ("472,765 lines of .ts XML — the files that look like TypeScript",
          "472,765 行 .ts XML，就是那些长得像 TypeScript 的文件")),
        (("KDBX bytes KeePassXC frames itself", "KeePassXC 自己拆帧的 KDBX 字节"), "2,003", ("lines", "行"),
         ("everything else on that path is Qt, zlib or Botan",
          "这条路上其余部分是 Qt、zlib 或 Botan")),
    ],

    "options_sub": (
        "One objective judges every option: remove the memory-unsafety class from the code that touches "
        "attacker-supplied bytes, without changing what KeePassXC is or how it reaches its packagers.",
        "所有方案对着同一个目标：把接触攻击者字节的那部分代码里的内存不安全缺陷类去掉，同时不改变 KeePassXC "
        "是什么，也不改变它怎么走到打包者手里。",
    ),
    "options": [
        {"id": "stay-fuzz", "name": ("Fuzz the pre-auth parser in C++", "在 C++ 里 fuzz 预认证解析器"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("aims at the 2,003-line framing path and 3,705 lines of importers",
                              "对准 2,003 行拆帧路径和 3,705 行导入器"),
         "one_time_cost": "weeks; the harness and corpus already exist",
         "recurring_cost": "CI time for a continuous campaign",
         "cost_cell": ("weeks; harness already written", "数周；脚手架已经写好"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "native", "compat_cell": ("native · no format risk", "原生 · 无格式风险"),
         "reversibility": "nothing to roll back",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the project already built this and left it idle",
                  "推荐 · 项目已经把这套东西做好了，只是没跑起来"),
         "reason": "Reaches every line the Rust options would target, at weeks rather than quarters, and it produces the evidence that would authorize an extraction."},
        {"id": "rust-parse-extract",
         "name": ("Rust crate for the KDBX framing layer", "把 KDBX 拆帧层做成 Rust crate"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("class removed in the pre-auth header path", "预认证头部路径里，缺陷类消失"),
         "one_time_cost": "2,003 lines plus a C ABI and a parity harness",
         "recurring_cost": "cargo in every packager's build",
         "cost_cell": ("2,003 lines + ABI; cargo everywhere", "2,003 行 + ABI；到处都要 cargo"),
         "time_to_value": ("months", "数月"),
         "compatibility": "byte-exact KDBX 3.1 and 4.x header handling",
         "compat_cell": ("same internal API · build-flag rollback", "内部 API 不变 · 构建开关回滚"),
         "reversibility": "build flag, if kept dual",
         "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · the one Rust scope with a defensible shape",
                  "保留 · 唯一形状说得通的 Rust 范围"),
         "reason": "Correct target and the right size, but the seam is not clean: 62 of the 91 core files include a Qt header, so the boundary has to be built before the crate can be dropped in."},
        {"id": "rust-core-extract",
         "name": ("Rust core for format, crypto, keys and streams", "format/crypto/keys/streams 整体换 Rust 内核"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("covers 16,076 lines; Botan and Qt still parse and decrypt",
                              "覆盖 16,076 行；解析与解密仍由 Botan 和 Qt 承担"),
         "one_time_cost": "16,076 lines and a new crypto backend decision",
         "recurring_cost": "two crypto stacks until Botan is dropped",
         "cost_cell": ("16,076 lines; two crypto stacks", "16,076 行；两套密码学栈"),
         "time_to_value": ("quarters", "数个季度"),
         "compatibility": "two KDBX generations plus legacy KDB",
         "compat_cell": ("format contract at risk · fixture rollback", "格式契约有风险 · 靠测试夹具回滚"),
         "reversibility": "hard once the format layer moves",
         "evidence_strength": "WEAK", "disposition": "retain",
         "note": ("retain · larger than the exposure it addresses", "保留 · 比它要解决的暴露面更大"),
         "reason": "src/crypto is 1,571 lines of Botan wrapper, so most of this scope re-wraps a vetted library rather than removing unsafe code."},
        {"id": "adopt-rust-kdbx",
         "name": ("Adopt an existing Rust KDBX parser", "直接采用现成的 Rust KDBX 解析器"),
         "implementation": "external",
         "scope": "adopt", "scope_tag": "ADOPT",
         "benefit_interval": ("class removed for parsing, at someone else's maintenance cost",
                              "解析侧缺陷类消失，维护成本落在别人身上"),
         "one_time_cost": "FFI layer plus format-parity validation against 32 fixtures",
         "recurring_cost": "an upstream KeePassXC does not control",
         "cost_cell": ("FFI + parity work; upstream risk", "FFI + 对齐验证；上游风险"),
         "time_to_value": ("months", "数月"),
         "compatibility": "a second implementation of the same format",
         "compat_cell": ("divergence risk · revert the dependency", "有分叉风险 · 撤掉依赖即可"),
         "reversibility": "drop the dependency",
         "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the ecosystem shipped this already", "保留 · 生态里已经有人做出来了"),
         "reason": "The keepass crate exists and is maintained, so this is cheaper than writing a parser; two independent implementations of one database format is the risk it carries."},
        {"id": "rust-core-electron",
         "name": ("Rust core plus a web UI", "Rust 内核 + Web UI"),
         "implementation": "rust",
         "scope": "component", "scope_tag": "PARTIAL",
         "benefit_interval": ("solves cross-platform UI consistency, not memory safety",
                              "解决的是跨平台 UI 一致性，不是内存安全"),
         "one_time_cost": "the whole UI, plus a browser engine in the shipped bundle",
         "recurring_cost": "a rendering engine the project does not own",
         "cost_cell": ("whole UI; new engine to track", "整套 UI；还要跟一个新引擎"),
         "time_to_value": ("years", "数年"),
         "compatibility": "abandons the native look users chose",
         "compat_cell": ("product identity changes · no rollback", "产品身份改变 · 无回滚"),
         "reversibility": "none",
         "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · this is the 1Password 8 shape", "排除 · 这就是 1Password 8 那个形状"),
         "reason": "The published precedent traded a native Mac app for a shared web UI and drew years of public pushback; KeePassXC's users are the people who left over exactly that."},
        {"id": "rust-full-gui",
         "name": ("Rewrite KeePassXC in Rust", "用 Rust 重写 KeePassXC"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("safety on 14.1% of the code; the rest is UI plumbing",
                              "14.1% 的代码拿到安全收益；其余是 UI 管道"),
         "one_time_cost": "113,863 lines, a GUI toolkit choice, and 45 translation catalogues",
         "recurring_cost": "a UI framework with no Qt-equivalent accessibility story",
         "cost_cell": ("113,863 lines; new toolkit", "113,863 行；换工具箱"),
         "time_to_value": ("years", "数年"),
         "compatibility": "Qt6 · 72 .ui files · 45 languages · KDBX contract",
         "compat_cell": ("everything at once · no rollback", "全部一起动 · 无回滚"),
         "reversibility": "none",
         "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · fails G3 and G4 on static counts", "排除 · 在静态计数上过不了 G3 和 G4"),
         "reason": "Qt appears in 476 of 660 files and there is no Rust binding that carries it, so the safety objective arrives attached to a full UI replacement nobody asked for."},
    ],

    "lenses_sub": (
        "Each state is evidence scoped to named options; they do not add up to a score. No performance "
        "claim was made about KeePassXC, so no Amdahl figure appears anywhere in this report.",
        "每条状态都绑到具体方案上，不是可以相加的分数。没有人对 KeePassXC 提出性能主张，所以整份报告里不会出现 "
        "Amdahl 数字。",
    ),
    "na_note": (
        "Two lenses are N/A. D3 tail and runtime: there is no managed runtime, no collector, and no "
        "latency SLO; the one deliberately slow path is Argon2 inside Botan. D4 fleet footprint: this is "
        "a single-user desktop application with no instance count and no price to compute against.",
        "两条记为 N/A。D3 尾延迟与运行时：没有托管运行时，没有 collector，也没有延迟 SLO；唯一故意做慢的是 "
        "Botan 里的 Argon2。D4 机队占用：这是单用户桌面应用，既没有实例数也没有价格可算。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · rust-parse-extract", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-parse-extract"],
         "claim": ("The objective is safety, so ownership means: whose code touches the hostile bytes "
                   "first? KeePassXC's does. Kdbx4Reader reads a file-controlled 32-bit length and reads "
                   "that many bytes before the header HMAC is compared. That surface is owned, small and "
                   "findable.",
                   "目标是安全，所以「归属」问的是：敌意字节最先落到谁的代码里？落到 KeePassXC 自己的代码里。"
                   "Kdbx4Reader 先读一个来自文件的 32 位长度，再按这个长度读字节，之后才比对头部 HMAC。这块面"
                   "是自有的，不大，也找得到。"),
         "source": "src/format/Kdbx4Reader.cpp:157-183 (header field read) vs :77 (HMAC comparison)",
         "regime": "static read of the shipped read path at this commit",
         "caveat": "KDBX 3.1 has no header HMAC at all; Kdbx3Reader.cpp:136 parses header fields and the stream-start-bytes check at :80 happens after decryption.",
         "change_trigger": "A fuzzing finding on this path would move the recommendation to rust-parse-extract."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "DISFAVORS · rust-full-gui, rust-core-extract", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG",
         "option_ids": ["rust-full-gui", "rust-core-extract"],
         "claim": ("Reach here means: which untrusted bytes stop being handled by C or C++? Not the XML, "
                   "which QXmlStreamReader parses. Not the gzip, which zlib inflates through a 622-line "
                   "Qt Solutions wrapper. Not the ciphers or the KDF, which are Botan's. Rewrite all "
                   "113,863 lines and those three stay linked into the same process.",
                   "这里的影响面问的是：哪些不可信字节不再由 C 或 C++ 处理？XML 不算，那是 QXmlStreamReader "
                   "解析的。gzip 也不算，那是 zlib 通过一个 622 行的 Qt Solutions 包装器解压的。分组密码和 "
                   "KDF 也不算，那些是 Botan 的。把 113,863 行全部重写，这三样照旧链进同一个进程。"),
         "source": "src/format/KdbxXmlReader.h:27,107 · src/streams/qtiocompressor.cpp (622 lines) · CMakeLists.txt:478",
         "regime": "static dependency inventory at this commit",
         "caveat": "Replacing Botan and Qt's XML reader as well is conceivable, and is a much larger proposal than the one assessed here."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("No managed runtime, no garbage collector, no latency SLO. The slowest operation is "
                   "Argon2 key derivation, which is slow on purpose and lives in Botan under every "
                   "option.",
                   "没有托管运行时，没有 GC，也没有延迟 SLO。最慢的一步是 Argon2 密钥派生，它是故意慢的，而且"
                   "在每个方案下都住在 Botan 里。"),
         "source": "src/crypto/kdf/Argon2Kdf.cpp:173 · Botan::PasswordHashFamily",
         "regime": "n/a", "caveat": ""},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("One user, one process, one machine. There is no instance count, no utilization figure "
                   "and no unit price, so no cost case can be constructed in either direction.",
                   "一个用户，一个进程，一台机器。没有实例数、没有利用率、没有单价，两个方向都构不出成本论证。"),
         "source": "desktop application, no fleet", "regime": "n/a", "caveat": ""},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("The GUI starts once per session and stays resident; keepassxc-cli is invoked per "
                   "command. Time to unlock is dominated by the KDF, not by process start. No option "
                   "changes either shape.",
                   "GUI 每次会话启动一次然后常驻；keepassxc-cli 是每条命令起一次。解锁耗时主要来自 KDF，不是"
                   "进程启动。没有哪个方案会改变这两种形态。"),
         "source": "src/main.cpp · src/cli (65 files, 4,794 lines)",
         "regime": "shipped invocation model",
         "caveat": "Nobody has published a startup measurement for KeePassXC, and none is needed for a safety decision."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust options", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE",
         "option_ids": ["rust-parse-extract", "rust-core-extract", "rust-full-gui"],
         "claim": ("Three raw memcpy calls sit on the KDBX read path, copying decrypted block data into a "
                   "caller-supplied char* buffer. Each is bounded by an explicit qMin against the buffer "
                   "size. Rust makes that shape impossible rather than merely correct, and 12 memcpy "
                   "occurrences across 113,863 lines is the whole surface.",
                   "KDBX 读路径上有三处裸 memcpy，把解密后的块数据拷进调用方给的 char* 缓冲区。每一处都用显式 "
                   "qMin 对缓冲区大小做了限界。Rust 让这种写法根本不成立，而不只是「这次写对了」；整个仓库 "
                   "113,863 行里 memcpy 一共出现 12 次，这就是全部的面。"),
         "source": "src/streams/HmacBlockStream.cpp:114 · HashedBlockStream.cpp:115 · SymmetricCipherStream.cpp:114",
         "regime": "occurrence count via /usr/bin/grep -o, comments not excluded",
         "caveat": "Six NVD records exist for KeePassXC and KeePassX between 2015 and 2026 and none carries a memory-safety CWE. Absence of found defects is not absence of defects.",
         "change_trigger": "A memory-safety finding in the parse path would raise this to STRONG and authorize rust-parse-extract."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Concurrency is thin and deliberate: 13 QtConcurrent occurrences, 12 QThread, 22 "
                   "QMutex, and no std::thread at all. Qt's signal-slot model already confines "
                   "cross-thread work. Send and Sync would buy less here than they bought fish.",
                   "并发用得又薄又克制：QtConcurrent 出现 13 次，QThread 12 次，QMutex 22 次，std::thread "
                   "一次都没有。Qt 的信号槽模型本来就把跨线程的活儿圈住了。Send 和 Sync 在这里能买到的东西，"
                   "比它们在 fish 那里买到的少。"),
         "source": "occurrence counts over 660 own src files via /usr/bin/grep -o",
         "regime": "static occurrence count at this commit",
         "caveat": "A future decision to parallelize database loading would reopen this lens; nothing in the tree indicates that plan."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "DISFAVORS · rust options", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE",
         "option_ids": ["rust-parse-extract", "rust-core-extract", "rust-full-gui"],
         "claim": ("KeePassXC already builds with CMake, vcpkg, snapcraft and per-distro packaging, and "
                   "INSTALL.md names Snap, AppImage, Flatpak and native as distribution types. Adding "
                   "cargo is a new requirement for every packager. Nothing about distribution is "
                   "currently unmet.",
                   "KeePassXC 现在用 CMake、vcpkg、snapcraft 加各发行版自己的打包脚本构建，INSTALL.md 里把 "
                   "Snap、AppImage、Flatpak、native 列为分发类型。加上 cargo 是给每个打包者新增一条要求。"
                   "分发这块目前没有未满足的约束。"),
         "source": "INSTALL.md:100 · vcpkg.json · snap/snapcraft.yaml · CMakeLists.txt:429-443",
         "regime": "shipped build and packaging configuration",
         "caveat": "A Rust component behind a C ABI is the cheapest version of this cost, which is one reason rust-parse-extract is retained rather than excluded."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · adopt-rust-kdbx", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["adopt-rust-kdbx"],
         "claim": ("A maintained Rust KDBX parser already exists. The keepass crate has 221,728 downloads "
                   "and was updated in July 2026, so nobody needs to write this from scratch. On the UI "
                   "side the ecosystem runs the other way entirely.",
                   "Rust 侧已经有一个在维护的 KDBX 解析器。keepass crate 下载 221,728 次，2026 年 7 月还在"
                   "更新，所以没人需要从零写一遍。UI 那一侧，生态的方向完全相反。"),
         "source": "crates.io API: keepass 0.13.19, 221,728 downloads, updated 2026-07-30",
         "regime": "public registry metadata, retrieved 2026-08-02",
         "caveat": "Two independent implementations of one database format is a correctness risk for a password manager, and download count is not an audit."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "DISFAVORS · rust-full-gui, rust-core-electron", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG",
         "option_ids": ["rust-full-gui", "rust-core-electron"],
         "claim": ("The compatibility surface is not the KDBX format. It is 218 distinct Qt headers, 194 "
                   "files declaring Q_OBJECT, 164 classes deriving from Qt types, 72 .ui layouts and 45 "
                   "Qt Linguist catalogues. QAccessible is in that include list, which is the part no "
                   "Rust toolkit currently answers.",
                   "兼容面不是 KDBX 格式。它是 218 个不同的 Qt 头、194 个声明 Q_OBJECT 的文件、164 个从 Qt "
                   "类型派生的类、72 个 .ui 布局，还有 45 份 Qt Linguist 词条。QAccessible 就在那份 include "
                   "清单里，而这一项目前没有哪个 Rust 工具箱能接。"),
         "source": "660 own src files: 476 with a Qt include, 218 distinct <Q*> headers, 194 Q_OBJECT, 164 Qt-derived classes; 72 .ui files at 18,677 lines",
         "regime": "static API-surface inventory at this commit",
         "caveat": "rust-parse-extract inherits almost none of this surface: only 6 of the 91 core files derive from a Qt type."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-full-gui", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-full-gui"],
         "claim": ("fish shell moved 57k lines of C++ to 75k of Rust in about two years with 200-plus "
                   "authors, and reported performance parity. KeePassXC's own src is 113,863 lines, twice "
                   "that, and 85.9% of it has no safety argument attached. Crosslake's rewrite dataset "
                   "puts typical overrun at 1.5 to 2 times budget and schedule.",
                   "fish shell 用大约两年、200 多位作者，把 5.7 万行 C++ 搬成 7.5 万行 Rust，性能报的是持平。"
                   "KeePassXC 自有 src 是 113,863 行，是它的两倍，其中 85.9% 挂不上任何安全论证。Crosslake "
                   "的重写数据集显示，典型超支和超期都在 1.5 到 2 倍。"),
         "source": "https://fishshell.com/blog/rustport/ · https://crosslaketech.com/how-long-does-a-complete-rewrite-of-a-software-application-take/",
         "regime": "first-party retrospective; consultancy dataset, self-selected sample",
         "caveat": "Neither figure was measured on KeePassXC; both are cited as schedule-realism reference points, not as predictions."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · stay-fuzz", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-fuzz"],
         "claim": ("The in-stack alternative is not hypothetical, and it is not cheap talk either. CodeQL "
                   "security-and-quality runs on cpp for every push to develop and release branches, "
                   "every pull request, and weekly. SonarCloud is configured. An AFL harness aimed at the "
                   ".kdbx load path is written and documented. Tests are 28,849 lines with 32 .kdbx "
                   "fixtures.",
                   "栈内那条路不是假想，也不是嘴上说说。CodeQL 的 security-and-quality 规则集对 cpp 跑在 "
                   "develop 和 release 分支的每次 push、每个 PR，外加每周一次。SonarCloud 配好了。一套对准 "
                   ".kdbx 加载路径的 AFL 脚手架写完并且有文档。测试 28,849 行，带 32 个 .kdbx 夹具。"),
         "source": ".github/workflows/codeql.yml:29 · sonar-project.properties · utils/fuzz-testing/README.md · src/cli/Utils.cpp:225",
         "regime": "current upstream engineering at this commit",
         "caveat": "None of it eliminates the memory-unsafety class; static analysis and fuzzing reduce incidence, and a Rust option would remove the class outright."},
    ],

    "findings": [
        ("unknown",
         ("45 files look like TypeScript and are Qt translation XML",
          "45 个文件长得像 TypeScript，其实是 Qt 翻译 XML"),
         ("Every .ts file in this tree opens with <!DOCTYPE TS><TS version=\"2.1\">. All 45 live under "
          "share/translations, and together they are 472,765 lines. Count them as TypeScript and .ts "
          "becomes 73.3% of the source-code line total. GitHub's Linguist gets this right and reports no "
          "TypeScript; line-counting tools that key on the extension do not. Every figure in this report "
          "excludes them.",
          "这棵树里每个 .ts 文件都以 <!DOCTYPE TS><TS version=\"2.1\"> 开头。45 个全在 share/translations "
          "下面，合计 472,765 行。把它们算成 TypeScript，.ts 就占到源码行数的 73.3%。GitHub 的 Linguist 判"
          "对了，报的是没有 TypeScript；靠扩展名数行的工具判不对。本报告里所有数字都把它们排除在外。"),
         "share/translations/keepassxc_*.ts · 45 files · 472,765 lines"),
        ("current",
         ("The security core is 14.1% of the code", "安全内核占代码的 14.1%"),
         ("src/format, src/crypto, src/keys and src/streams together are 91 files and 16,076 lines. "
          "KeePassXC's own src, excluding the vendored src/thirdparty tree, is 113,863. src/gui alone is "
          "50,344, or 44.2%. A rewrite pitched on memory safety spends most of its budget on dialogs, "
          "models and views.",
          "src/format、src/crypto、src/keys、src/streams 合起来 91 个文件、16,076 行。KeePassXC 自有 src，"
          "扣掉内置的 src/thirdparty，是 113,863 行。仅 src/gui 就有 50,344 行，占 44.2%。一场打着内存安全"
          "旗号的重写，大部分预算花在对话框、model 和 view 上。"),
         "src/format+crypto+keys+streams · 16,076 of 113,863 lines"),
        ("current",
         ("KeePassXC writes no crypto of its own", "KeePassXC 没有自己写任何密码学代码"),
         ("CMakeLists.txt:478 makes Botan a hard requirement, minimum 2.19.1. src/crypto is 1,571 lines "
          "across 14 files, and it is a wrapper: 24 Botan:: call sites cover the ciphers, hashes, RNG and "
          "both KDFs. src/core/Alloc.cpp even routes global operator delete through "
          "Botan::secure_scrub_memory. Rewriting this in Rust replaces glue around a library that was "
          "never KeePassXC's to get wrong.",
          "CMakeLists.txt:478 把 Botan 定为硬依赖，最低 2.19.1。src/crypto 是 14 个文件、1,571 行，而且是层"
          "包装：24 处 Botan:: 调用点覆盖了分组密码、哈希、RNG 和两种 KDF。src/core/Alloc.cpp 甚至把全局 "
          "operator delete 接到 Botan::secure_scrub_memory 上。用 Rust 重写这部分，换掉的是一层胶水，而底下"
          "那个库本来就不是 KeePassXC 能写错的东西。"),
         "CMakeLists.txt:478 · src/crypto (14 files, 1,571 lines) · src/core/Alloc.cpp:47"),
        ("rust",
         ("The pre-auth header parse is the case for Rust", "预认证的头部解析，才是 Rust 的理由所在"),
         ("Kdbx4Reader::readHeaderField reads a 32-bit length straight out of the file, then reads that "
          "many bytes. The header HMAC is not compared until 80 lines earlier in the call graph, inside "
          "readDatabaseImpl. So a hostile .kdbx gets a parser to run with no credential at all. Add the "
          "six importers for Bitwarden, 1Password OpVault, 1PUX, ProtonPass, CSV and legacy KDB, and that "
          "is 3,705 more lines fed by files from other vendors.",
          "Kdbx4Reader::readHeaderField 直接从文件里读一个 32 位长度，然后按这个长度读字节。头部 HMAC 的比对"
          "发生在调用链更靠前的 readDatabaseImpl 里。所以一个恶意 .kdbx 能在完全没有凭据的情况下让解析器跑"
          "起来。再加上 Bitwarden、1Password OpVault、1PUX、ProtonPass、CSV 和旧版 KDB 六个导入器，又是 "
          "3,705 行由别家厂商的文件喂进来的代码。"),
         "src/format/Kdbx4Reader.cpp:157 · six importers, 3,705 lines"),
        ("current",
         ("No memory-safety CVE has been recorded in eleven years",
          "十一年里没有一条内存安全 CVE 记录"),
         ("NVD returns six CVE records for KeePassXC or KeePassX between 2015 and 2026. The CWEs are 200, "
          "863, 316 twice, the 352/353/640 group for the browser extension, and 427 for an OpenSSL "
          "config search path. Not one is a memory-safety class. The CHANGELOG covers 55 releases back to "
          "2012 and names two: an out-of-memory crash on malformed SSH keys, and two heap-use-after-free "
          "crashes in the CLI. Nobody has proven the class is absent. It has not surfaced.",
          "NVD 在 2015 到 2026 年间返回六条 KeePassXC 或 KeePassX 的 CVE 记录。CWE 分别是 200、863、两次 "
          "316、浏览器扩展那组 352/353/640，以及一条关于 OpenSSL 配置搜索路径的 427。没有一条属于内存安全"
          "类。CHANGELOG 覆盖 55 个版本、回溯到 2012 年，里面点到两处：畸形 SSH key 导致的内存耗尽崩溃，以及"
          "CLI 里两个 heap-use-after-free。没人证明这个缺陷类不存在，只是它没有冒出来。"),
         "NVD keywordSearch=keepass · CHANGELOG.md:86, :632"),
    ],

    "buys": [
        (("Class elimination on the pre-auth path", "预认证路径上，这个缺陷类直接消失"),
         ("a Rust framing parser cannot produce a memory-unsafety defect while decoding a hostile .kdbx "
          "header, and that header is parsed before any credential is checked.",
          "用 Rust 写的拆帧解析器，在解码敌意 .kdbx 头部时产不出内存不安全缺陷；而那个头部就是在任何凭据被校"
          "验之前被解析的。")),
        (("A crate that already exists", "一个已经存在的 crate"),
         ("the keepass crate has 221,728 downloads and shipped a release in July 2026, so the extraction "
          "starts from working code rather than a blank file.",
          "keepass crate 下载 221,728 次，2026 年 7 月还发了版本，所以抽取方案是从能跑的代码起步，不是从空文"
          "件起步。")),
        (("Nothing on crypto, and that is fine", "密码学这块什么也买不到，这没问题"),
         ("Botan already owns every cipher, hash, RNG and KDF. src/crypto is 1,571 lines of wrapper, so "
          "there is no unsafe primitive here for Rust to displace.",
          "Botan 已经拿下了所有分组密码、哈希、RNG 和 KDF。src/crypto 是 1,571 行包装层，这里没有不安全的原"
          "语等着 Rust 来替。")),
    ],
    "nobuys": [
        (("A process without C++ in it", "一个不含 C++ 的进程"),
         ("Qt6 and Botan stay linked under every option. QXmlStreamReader still parses the decrypted "
          "database XML and zlib still inflates it.",
          "在任何方案下，Qt6 和 Botan 都还链在里面。解密后的数据库 XML 仍由 QXmlStreamReader 解析，仍由 "
          "zlib 解压。")),
        (("The user interface", "那套用户界面"),
         ("476 of 660 source files include a Qt header and 72 .ui layouts hold 18,677 lines. No Rust "
          "toolkit carries that, so the migration ships a different application.",
          "660 个源文件里 476 个 include 了 Qt 头，72 个 .ui 布局装着 18,677 行。没有哪个 Rust 工具箱接得下"
          "来，所以这场迁移交付的是另一个应用。")),
        (("Freedom from the KDBX contract", "从 KDBX 契约里脱身"),
         ("two format generations plus legacy KDB plus six import formats survive any implementation "
          "change, and a parsing regression in a password manager means silent data loss.",
          "两代格式、旧版 KDB、六种导入格式，在任何实现变更之后都还在；而密码管理器里的解析回归意味着无声的数"
          "据丢失。")),
    ],

    "precedents": [
        {"name": "1Password 8 · Rust core, web UI", "outcome": "MIGRATED",
         "body": ("1Password's own post describes stopping work on the SwiftUI Mac app and extending the "
                  "Electron web UI to cover macOS, with a shared Rust core chosen as a language known "
                  "for \"performance, security, and memory safety\". Mac users pushed back for years "
                  "afterwards, on forums and elsewhere. This is the road KeePassXC has not taken.",
                  "1Password 自己那篇文章写了：停掉 SwiftUI 版 Mac 应用，把 Electron 的 Web UI 扩到 macOS，"
                  "底下用一个共享的 Rust 内核，选它的理由是这门语言以 \"performance, security, and memory "
                  "safety\" 著称。之后好几年，Mac 用户在论坛和别的地方一直在反弹。这条路 KeePassXC 没有走。"),
         "match": ("password manager, native Mac app, Rust core, and the same UI-toolkit decision",
                   "密码管理器、原生 Mac 应用、Rust 内核，面对的是同一个 UI 工具箱决策"),
         "mismatch": ("closed source and unprobeable; their driver was cross-platform consistency and a "
                      "ship date, not memory safety",
                      "闭源，没法探查；他们的动因是跨平台一致性加发布日期，不是内存安全"),
         "regime": "first-party product announcement, August 2021; reaction from public forums",
         "source_label": "first-party blog · reaction third-party",
         "url": "https://1password.com/blog/1password-8-the-story-so-far"},
        {"name": "Mozilla · Stylo vs Servo", "outcome": "EXTRACTED",
         "body": ("The same organisation ran both experiments on one C++ codebase. The CSS engine "
                  "extraction shipped in Firefox 57 after about two years. The whole-engine replacement "
                  "was cancelled and the team laid off. Holley's line is the one to keep: the desire to "
                  "throw everything away tends to be an emotional one.",
                  "同一个组织在同一份 C++ 代码库上跑了两个实验。CSS 引擎的抽取用了大约两年，随 Firefox 57 "
                  "发布。整引擎替换被取消，团队被裁。Holley 那句话值得留着：想把一切扔掉重来，这种冲动往往是"
                  "情绪性的。"),
         "match": ("C++ codebase, memory-safety motive, and the same extract-versus-replace fork",
                   "C++ 代码库、内存安全动机，面对的是同一个「抽取还是替换」的分叉"),
         "mismatch": ("Stylo had a parallel-styling win Rust uniquely enabled; KeePassXC's core has no "
                      "such win, and there is no donor project to ride",
                      "Stylo 有一个只有 Rust 能拿下的并行样式计算收益；KeePassXC 的内核没有这种收益，也没有"
                      "一个可以蹭的捐赠项目"),
         "regime": "first-party retrospective, shipped product",
         "source_label": "first-party · engineering blog",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Google · Android memory-safety program", "outcome": "STAYED",
         "body": ("Android's memory-safety vulnerability share fell from 76% in 2019 to under 20% in "
                  "2025 without a mass rewrite. New code went to Rust; old C and C++ was left to decay. "
                  "Their measured reason: five-year-old code carries 3.4 to 7.4 times lower vulnerability "
                  "density than new code.",
                  "Android 的内存安全漏洞占比从 2019 年的 76% 降到 2025 年的 20% 以下，没有做大规模重写。"
                  "新代码走 Rust，旧的 C 和 C++ 留在原地自然衰减。他们量出来的理由是：五年前的代码，漏洞密度"
                  "比新代码低 3.4 到 7.4 倍。"),
         "match": ("a C++ security-relevant codebase choosing interop over rewrite, and code-age decay "
                   "applies directly to a parse path written in 2018",
                   "一份与安全相关的 C++ 代码库选了互操作而不是重写；代码年龄衰减这条，直接适用于一条 2018 "
                   "年写成的解析路径"),
         "mismatch": ("OS scope at Google headcount; their C and C++ is raw-pointer heavy where "
                      "KeePassXC's parse path is QByteArray-based",
                      "那是操作系统级范围，配 Google 的人力；他们的 C/C++ 裸指针很重，而 KeePassXC 的解析路径"
                      "建在 QByteArray 上"),
         "regime": "first-party vulnerability statistics, 2019-2025",
         "source_label": "first-party · security blog",
         "url": "https://blog.google/security/rust-in-android-move-fast-fix-things/"},
        {"name": "Trifecta · sudo-rs", "outcome": "MIGRATED",
         "body": ("A privilege tool that parses attacker-influenced input was rewritten in Rust and "
                  "became the Ubuntu 25.10 default, with no performance framing anywhere in the "
                  "first-party material. The argument was attack surface, full stop. If KeePassXC's "
                  "pre-auth parser ever produces a finding, this is the shape the answer takes.",
                  "一个解析受攻击者影响输入的提权工具，用 Rust 重写，成了 Ubuntu 25.10 的默认实现，官方材料"
                  "里通篇没有性能话术。论证就是攻击面，没有别的。如果 KeePassXC 的预认证解析器哪天真查出问题，"
                  "答案就长这个样子。"),
         "match": ("the strongest confirming case: untrusted input, security boundary, safety-only "
                   "justification",
                   "最强的正面例证：不可信输入、安全边界、纯安全论证"),
         "mismatch": ("a small setuid CLI with no GUI and no Qt; KeePassXC's equivalent path is 2,003 "
                      "lines inside a 113,863-line Qt application",
                      "那是个小的 setuid CLI，没有 GUI，也没有 Qt；KeePassXC 对应的路径是嵌在 113,863 行 Qt "
                      "应用里的 2,003 行"),
         "regime": "shipped distribution default, first-party",
         "source_label": "first-party · project blog",
         "url": "https://trifectatech.org/blog/memory-safe-sudo-to-become-the-default-in-ubuntu/"},
        {"name": "Zed · GPUI", "outcome": "GREENFIELD",
         "body": ("The flagship Rust desktop application found no existing Rust GUI framework that met "
                  "its bar, so it built one. A 2025 survey of 43 Rust GUI crates reached the same place: "
                  "the overwhelming majority are not production-ready, with accessibility and input "
                  "methods the usual gaps. KeePassXC needs both, in 45 languages.",
                  "那个旗舰级的 Rust 桌面应用，没找到一个达标的现成 Rust GUI 框架，于是自己写了一个。2025 年"
                  "一份对 43 个 Rust GUI crate 的调研走到同一个结论：绝大多数还不能上生产，缺口通常在无障碍"
                  "和输入法。KeePassXC 这两样都要，还要乘以 45 种语言。"),
         "match": ("the G4 question directly: whether a Rust toolkit can carry a real desktop UI today",
                   "直接对上 G4 那个问题：今天有没有 Rust 工具箱能撑起一套真实的桌面 UI"),
         "mismatch": ("Zed is greenfield and venture-funded; KeePassXC is a volunteer project with 72 .ui "
                      "layouts and 472,765 lines of translation catalogue to carry across",
                      "Zed 是有风投的全新项目；KeePassXC 是志愿者项目，还得把 72 个 .ui 布局和 472,765 行"
                      "翻译词条搬过去"),
         "regime": "first-party product claims; third-party ecosystem survey",
         "source_label": "first-party blog · survey third-party",
         "url": "https://zed.dev/blog/videogame"},
    ],

    "path": [
        {"title": ("Run the fuzzer the project already wrote", "把项目自己写好的 fuzzer 跑起来"),
         "body": ("KeePassXC maintainers take utils/fuzz-testing/README.md off the shelf and run it "
                  "continuously in CI instead of by hand. Seed the corpus from the 32 tracked .kdbx "
                  "fixtures, then extend coverage to the six importers, which currently have no harness "
                  "at all. The step passes when the campaign has run one full release cycle over both "
                  "KDBX generations and every import format. A crash in the pre-auth header path goes "
                  "straight to step 3. Nothing ships, so nothing rolls back.",
                  "KeePassXC 维护者把 utils/fuzz-testing/README.md 那套东西从架子上取下来，放进 CI 持续跑，"
                  "不再手动跑。语料用仓库里那 32 个 .kdbx 夹具做种子，然后把覆盖面扩到六个导入器——它们现在"
                  "一个脚手架都没有。通过标准是：这一轮跑满一个完整发布周期，覆盖两代 KDBX 和每一种导入格式。"
                  "预认证头部路径上一旦崩，直接跳到第三步。这一步不发布东西，也就没有东西要回退。"),
         "owner": "KeePassXC maintainers",
         "cost_range": ("2-4 weeks", "2-4 周"),
         "artifact": "a continuous AFL campaign in CI covering both KDBX generations and all six import formats, seeded from the 32 tracked .kdbx fixtures",
         "acceptance": "the campaign runs one full release cycle with the importers covered and every crash triaged",
         "stop": "a crash in the pre-auth header path escalates directly to the Rust extraction step",
         "rollback": "measurement only; no code ships"},
        {"title": ("Say out loud that Qt is the product", "把「Qt 就是产品本身」这句话说出来"),
         "body": ("Before any migration proposal gets review time, someone writes down what replaces "
                  "Qt. Which toolkit renders the 72 .ui layouts. How 45 Qt Linguist catalogues get "
                  "re-plumbed. What answers QAccessible on Windows, macOS and Linux. The step passes when "
                  "that document names a toolkit and a shipping application built on it that has the "
                  "accessibility and input-method coverage KeePassXC has now. No document, no review. "
                  "The current Qt build carries on either way.",
                  "任何迁移提案要拿到评审时间之前，先有人把「拿什么替 Qt」写下来。哪个工具箱来渲染那 72 个 "
                  ".ui 布局。45 份 Qt Linguist 词条怎么重新接线。Windows、macOS、Linux 上谁来接 QAccessible。"
                  "通过标准是：这份文档点出一个工具箱，以及一个基于它发布的应用，其无障碍和输入法覆盖不低于 "
                  "KeePassXC 现在的水平。没有文档就没有评审。不管怎样，现在这套 Qt 构建照旧往前走。"),
         "owner": "whoever proposes the migration",
         "cost_range": ("1 week per review", "每轮评审 1 周"),
         "artifact": "a written UI replacement plan naming a toolkit, a shipping reference application, and the accessibility and translation story",
         "acceptance": "the named toolkit has a shipping application with accessibility and input-method coverage matching the current Qt build",
         "stop": "no migration proposal gets review time without it",
         "rollback": "the current Qt6 build continues unchanged"},
        {"title": ("Extract the framing layer only if the fuzzer says so",
                   "只有 fuzzer 开口，才去抽取拆帧层"),
         "body": ("If step 1 produces a memory-safety finding, the framing layer moves to Rust behind a C "
                  "ABI, starting with the pre-auth header parse and the three block streams. Validate "
                  "against the 32 .kdbx fixtures plus whatever the fuzzer generated, byte for byte, in "
                  "both directions. Keep both implementations behind a build flag for one release. If "
                  "parity fails on any fixture, delete the flag and keep the C++ path. Scope stays at "
                  "2,003 lines; src/gui is never touched.",
                  "如果第一步查出内存安全问题，就把拆帧层挪到 Rust、藏在一个 C ABI 后面，先做预认证头部解析和"
                  "那三条块流。用那 32 个 .kdbx 夹具，加上 fuzzer 生成的样本，双向逐字节校验。两套实现用构建"
                  "开关并存一个版本周期。任何一个夹具对不上，就删掉开关、保留 C++ 那条路。范围就停在 2,003 "
                  "行，src/gui 一行不动。"),
         "owner": "KeePassXC maintainers plus one Rust contributor",
         "cost_range": ("3-6 months", "3-6 个月"),
         "artifact": "a Rust framing crate behind a C ABI covering the pre-auth header parse and the three block streams, with a byte-for-byte parity harness",
         "acceptance": "byte-identical results on all 32 tracked fixtures and the fuzzer corpus, in both read and write directions",
         "stop": "delete the build flag and keep the C++ path if parity fails on any fixture",
         "rollback": "build flag; the C++ implementation stays in tree for one release"},
        {"title": ("Write new importers in the safe language from the start",
                   "新的导入器，一开始就用安全语言写"),
         "body": ("Android's decay finding applies here without much translation: new code carries the "
                  "defects, old code has had them found. KeePassXC adds import formats over time, and the "
                  "six it has are 3,705 lines. The next one gets written against the Rust framing crate "
                  "if step 3 happened, and gets a fuzz target on day one either way. Acceptance is a "
                  "harness merged alongside the parser, not after it. Reverting a new importer costs "
                  "nothing, because nobody depended on it yet.",
                  "Android 那个衰减结论几乎不用转译就能用在这里：缺陷都在新代码里，旧代码的缺陷已经被找出来"
                  "了。KeePassXC 会不断加导入格式，现有六个是 3,705 行。下一个如果第三步发生了，就对着 Rust "
                  "拆帧 crate 写；不管第三步有没有发生，它第一天就要有 fuzz target。验收标准是脚手架跟解析器"
                  "一起合入，不是之后补。撤掉一个新导入器成本为零，因为还没人依赖它。"),
         "owner": "KeePassXC maintainers",
         "cost_range": ("per feature", "按功能计"),
         "artifact": "a project rule that every new import format ships with a fuzz target, and targets the Rust framing crate once it exists",
         "acceptance": "the fuzz harness merges in the same pull request as the parser, not later",
         "stop": "no new import format merges without its harness",
         "rollback": "revert the feature; no existing user depends on a format that just landed"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("The proposal credits Rust with safety over the whole application. The bytes are "
                   "handled by Qt's XML reader, zlib and Botan, and KeePassXC's own share of the KDBX "
                   "read path is 2,003 lines.",
                   "提案把整个应用的安全都记在 Rust 头上。可字节是 Qt 的 XML reader、zlib 和 Botan 在处理，"
                   "KeePassXC 自己在 KDBX 读路径上只占 2,003 行。"),
         "evidence": "D2 · KdbxXmlReader.h:27 · qtiocompressor.cpp · CMakeLists.txt:478"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("A Rust safety claim gets compared against the current build with CodeQL on every "
                   "pull request and an AFL harness in the tree, not against unanalysed C++.",
                   "Rust 的安全主张要跟「每个 PR 都跑 CodeQL、仓库里带 AFL 脚手架」的当前构建比，不是跟一份"
                   "没做过分析的 C++ 比。"),
         "evidence": "D12 · .github/workflows/codeql.yml:29"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("The UI never appears in the proposal's budget. 476 of 660 files include a Qt header, "
                   "72 .ui layouts hold 18,677 lines, and 45 Qt Linguist catalogues hold 472,765.",
                   "提案的预算里从来没出现 UI。660 个文件里 476 个 include 了 Qt 头，72 个 .ui 布局 18,677 "
                   "行，45 份 Qt Linguist 词条 472,765 行。"),
         "evidence": "D10 · G4 evidence"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("Two KDBX generations, legacy KDB and six import formats are named and priced against "
                   "every reimplementation option, including the adoption one.",
                   "两代 KDBX、旧版 KDB 和六种导入格式都点了名，并计入每个重新实现方案的成本，采用现成库那个"
                   "方案也算在内。"),
         "evidence": "D10 · src/format (46 files, 9,622 lines)"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The path requires a written UI replacement plan before any migration proposal gets "
                   "review time, and names what that plan must contain.",
                   "路径要求：任何迁移提案拿到评审时间之前，先有一份书面的 UI 替换计划，并且点明这份计划里必"
                   "须写什么。"),
         "evidence": "reversible path step 2"},
    ],
    "staying_checks": [
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Staying leaves a memory-unsafety class reachable from a file with no credential "
                   "attached. Kdbx4Reader parses a file-controlled length before the header HMAC is "
                   "compared, and KDBX 3.1 has no header HMAC at all.",
                   "不动，就意味着一个内存不安全缺陷类可以由一份不带任何凭据的文件触达。Kdbx4Reader 在比对头部 "
                   "HMAC 之前就按文件给的长度解析，而 KDBX 3.1 根本没有头部 HMAC。"),
         "evidence": "D6 · src/format/Kdbx4Reader.cpp:157 · Kdbx3Reader.cpp:136"},
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("CodeQL security-and-quality on cpp, SonarCloud, an AFL harness with an in-source hook, "
                   "and 28,849 lines of tests with 32 .kdbx fixtures are all in the tree today.",
                   "对 cpp 跑的 CodeQL security-and-quality、SonarCloud、带源码内钩子的 AFL 脚手架，以及 "
                   "28,849 行测试配 32 个 .kdbx 夹具，今天都在仓库里。"),
         "evidence": "D12 · sonar-project.properties · src/cli/Utils.cpp:225"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("The report discloses its own inconvenient counts: 12 memcpy occurrences, 124 "
                   "reinterpret_cast, and 29,484 lines of vendored C and C++ in src/thirdparty that no "
                   "option touches.",
                   "报告把对自己不利的数字也报了：memcpy 出现 12 次，reinterpret_cast 124 次，src/thirdparty "
                   "里 29,484 行第三方 C/C++，没有哪个方案会动它们。"),
         "evidence": "D6 · occurrence counts over 660 own src files"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report does not claim Rust would be slower or worse. It retains three Rust "
                   "options, one of them adoption of an existing crate, and names the trigger that "
                   "promotes the extraction.",
                   "报告没有主张 Rust 会更慢或更差。它保留了三个 Rust 方案，其中一个是采用现成 crate，并点明"
                   "了让抽取方案上位的触发条件。"),
         "evidence": "D9 · options rust-parse-extract, rust-core-extract, adopt-rust-kdbx"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("The selected option carries an explicit escalation rule: a crash in the pre-auth "
                   "header path moves the decision to the Rust extraction, without further debate.",
                   "被选中的方案带一条明确的升级规则：预认证头部路径上出现崩溃，决策直接转到 Rust 抽取，不再"
                   "另行辩论。"),
         "evidence": "reversible path steps 1 and 3"},
    ],

    "gaps": [
        (("A fuzzing result for the pre-auth header path and the six importers",
          "预认证头部路径与六个导入器的 fuzz 结果"),
         ("This is the whole decision. The harness exists and the corpus exists; nobody has published a "
          "campaign result. A finding authorizes rust-parse-extract immediately.",
          "整个决策就压在这上面。脚手架有，语料有，但没有人公开过一轮完整的跑测结果。一旦查出问题，"
          "rust-parse-extract 立刻获得授权。")),
        (("A root-cause classification of the CHANGELOG's 44 crash fixes",
          "对 CHANGELOG 里 44 条崩溃修复做根因分类"),
         ("Two are named as memory-safety issues. The other 42 are described as UI lifecycle problems, "
          "and nobody has checked whether that description holds.",
          "其中两条被点明是内存安全问题。另外 42 条被描述成 UI 生命周期问题，但没有人核对过这个描述是否成"
          "立。")),
        (("A Rust GUI toolkit with KeePassXC's accessibility and translation coverage",
          "一个具备 KeePassXC 无障碍与翻译覆盖度的 Rust GUI 工具箱"),
         ("Without one, G4 stays FAIL for the full migration regardless of what the fuzzer finds. This is "
          "the gap that makes the verdict STAY rather than EXTRACT.",
          "没有这个东西，不管 fuzzer 查出什么，G4 对整体迁移都停在 FAIL。正是这个缺口让结论落在 STAY 而不是 "
          "EXTRACT。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; src/thirdparty is counted as it ships and excluded from own-code percentages.",
        "Occurrence counts come from /usr/bin/grep -o piped to wc -l and count occurrences rather than lines; comments and string literals are not excluded.",
        "The proposal under assessment is the question as posed — should KeePassXC migrate to Rust, primarily for memory safety — since no RFC or issue was supplied.",
        "NVD keyword search is treated as the public CVE record for KeePassXC; a vulnerability fixed without a CVE would not appear in it.",
    ],
    "objective": {
        "driver": "memory safety",
        "requirement": "remove the memory-unsafety class from the code that handles attacker-supplied bytes, without changing the application's identity or its packaging path",
        "baseline": "2,003 lines of own framing code on the KDBX read path plus 3,705 lines of importers; six NVD CVE records since 2015 and none with a memory-safety CWE",
        "target": "class elimination on the pre-auth parse path; no performance target was stated and none is assessed",
    },
    "repository": {
        "path": "https://github.com/keepassxreboot/keepassxc",
        "commit": "205891202f4b995a8c9277cd125498ac76468b15",
        "scope": "the whole application; src/format, src/crypto, src/keys and src/streams are the candidate seam",
        "sampling": "shallow clone; 1,510 tracked files enumerated; 45 .ts Qt Linguist catalogues excluded from every count; src/, tests/ and utils/ measured; no build, test, benchmark or network call was run against the project",
    },
    "user_supplied_facts": [],

    "method_title": (
        "keepassxreboot/keepassxc at 2058912 · static read-only analysis · why-not-rust method 2.0",
        "keepassxreboot/keepassxc @ 2058912 · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/keepassxreboot/keepassxc at commit "
        "205891202f4b995a8c9277cd125498ac76468b15, shallow clone, 1,510 tracked files. Scope: the whole "
        "application, with src/format, src/crypto, src/keys and src/streams as the candidate seam. "
        "Counting basis: this repository is the reason the method demands one. 45 files carry a .ts "
        "extension and total 472,765 lines. All 45 sit under share/translations and every one opens with "
        "<!DOCTYPE TS><TS version=\"2.1\">, which makes them Qt Linguist translation XML. Count them as "
        "TypeScript and .ts becomes 73.3% of the (.ts + C/C++/Objective-C++) line total, which is what "
        "extension-keyed tools report. GitHub's own Linguist gets it right and reports no TypeScript. "
        "Every figure here excludes them. C, C++ and Objective-C++ across the tracked tree: 808 files and "
        "172,146 lines, being 390 .cpp at 114,511, 406 .h at 53,385, 7 .c at 3,469 and 5 .mm at 781. src/ "
        "excluding src/thirdparty is 660 files and 113,863 lines, and that is the denominator for every "
        "percentage in this report. src/thirdparty is 29,484 lines, of which 24,868 are a single zxcvbn "
        "word-list header. src/gui is 282 files and 50,344 lines, 44.2%. The security-relevant core of "
        "src/format, src/crypto, src/keys and src/streams is 91 files and 16,076 lines, 14.1%. tests/ is "
        "127 files and 28,849 lines with 32 tracked .kdbx fixtures. Qt coupling, on the same 660 files: "
        "476 include a Qt header, 218 distinct <Q*> headers are included, 194 files declare Q_OBJECT and "
        "164 class declarations derive from a Qt type; 72 .ui Qt Designer files hold 18,677 lines. "
        "CMakeLists.txt:429-443 requires Qt 6.2.4 or newer with eight components plus DBus on Linux, and "
        "CMakeLists.txt:478 requires Botan 2.19.1 or newer. Occurrence counts use /usr/bin/grep -o piped "
        "to wc -l and count occurrences, not lines; comments are not excluded. memcpy appears 12 times in "
        "the 660 files, three of them on the KDBX read path; reinterpret_cast appears 124 times. Security "
        "history: NVD keyword search returns six CVE records for KeePassXC or KeePassX between 2015 and "
        "2026, carrying CWE-200, CWE-863, CWE-316 twice, CWE-352/353/640 for the browser extension, and "
        "CWE-427; none is a memory-safety class. The repository's GitHub advisory list holds one entry, "
        "CVE-2026-4158. The CHANGELOG spans 55 releases from 2012-05-07 to 2026-03-10, names two "
        "memory-safety-shaped fixes and no CVE. Absence of found defects is not absence of defects, and "
        "D6 is recorded MODERATE rather than WEAK for that reason. Objective: no RFC was supplied, so the "
        "assessment takes the question as posed. User-supplied facts: none. No Amdahl calculation appears, "
        "because no performance claim was made and a line share is not a time share. Nothing in the "
        "scanned repository content attempted to steer this assessment. The decision turns on G3 and G4, "
        "which fail on static counts, while G1 and G2 pass on the pre-auth parse path. Smallest sufficient "
        "step: the selected option reaches every line the Rust options target, using a harness the "
        "project already wrote. This is a structured decision protocol, not a statistical predictor.",
        "仓库：github.com/keepassxreboot/keepassxc，commit 205891202f4b995a8c9277cd125498ac76468b15，"
        "shallow clone，1,510 个纳管文件。范围：整个应用，候选接缝是 src/format、src/crypto、src/keys、"
        "src/streams。计数口径：这个仓库正好说明了为什么方法一定要求先说清口径。45 个文件带 .ts 扩展名，合计 "
        "472,765 行。这 45 个全在 share/translations 下，每个都以 <!DOCTYPE TS><TS version=\"2.1\"> 开头，"
        "也就是 Qt Linguist 的翻译 XML。把它们算成 TypeScript，.ts 就占到（.ts + C/C++/Objective-C++）行数"
        "的 73.3%，这正是按扩展名判断的工具给出的结果。GitHub 自己的 Linguist 判对了，报的是没有 TypeScript。"
        "本文所有数字都把它们排除。全树的 C、C++、Objective-C++：808 个文件、172,146 行，其中 .cpp 390 个共 "
        "114,511 行，.h 406 个共 53,385 行，.c 7 个共 3,469 行，.mm 5 个共 781 行。src/ 扣掉 src/thirdparty "
        "是 660 个文件、113,863 行，本报告每个百分比都以它为分母。src/thirdparty 是 29,484 行，其中 24,868 "
        "行是一个 zxcvbn 词表头文件。src/gui 是 282 个文件、50,344 行，占 44.2%。安全关键内核 src/format + "
        "src/crypto + src/keys + src/streams 是 91 个文件、16,076 行，占 14.1%。tests/ 是 127 个文件、"
        "28,849 行，带 32 个纳管的 .kdbx 夹具。Qt 耦合，同样按这 660 个文件算：476 个 include 了 Qt 头，"
        "被 include 的不同 <Q*> 头有 218 个，194 个文件声明 Q_OBJECT，164 处类声明从 Qt 类型派生；72 个 .ui "
        "Qt Designer 文件共 18,677 行。CMakeLists.txt:429-443 要求 Qt 6.2.4 及以上，八个组件，Linux 上另加 "
        "DBus；CMakeLists.txt:478 要求 Botan 2.19.1 及以上。出现次数用 /usr/bin/grep -o 接 wc -l 统计，数的"
        "是出现次数而不是行数，注释没有剔除。memcpy 在这 660 个文件里出现 12 次，其中三次在 KDBX 读路径上；"
        "reinterpret_cast 出现 124 次。安全历史：NVD 关键词检索在 2015 到 2026 年间返回六条 KeePassXC 或 "
        "KeePassX 的 CVE 记录，CWE 分别是 200、863、两次 316、浏览器扩展的 352/353/640，以及 427；没有一条"
        "属于内存安全类。仓库的 GitHub advisory 列表只有一条，CVE-2026-4158。CHANGELOG 覆盖 55 个版本，从 "
        "2012-05-07 到 2026-03-10，点到两处内存安全形态的修复，没有提到任何 CVE。没找到缺陷不等于没有缺陷，"
        "所以 D6 记的是 MODERATE 而不是 WEAK。目标：没有人给出 RFC，因此按问题原样评估。用户提供的事实：无。"
        "本报告没有 Amdahl 计算，因为没有人提出性能主张，而代码行数占比不能当时间占比用。扫描到的仓库内容里"
        "没有任何试图操纵本次评估的东西。决策落在 G3 和 G4 上，这两道门在静态计数上失败；G1 和 G2 则在预认证"
        "解析路径上通过。最小充分步骤：被选中的方案能覆盖 Rust 方案要打的每一行，而用的是项目自己早就写好的"
        "脚手架。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 2058912 · no build, benchmark or network call against the project",
        "公开仓库 · 在 commit 2058912 上做静态分析 · 没有对项目做构建、基准或网络调用",
    ),
}
