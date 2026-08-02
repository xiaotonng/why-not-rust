"""spacedriveapp/spacedrive — 95.5% of the index is one phase that opens each file six times.

Repository facts were measured read-only on the shallow clone named in
`repository`. Commit, release and author history came from the GitHub REST API.
"""

CASE = {
    "slug": "spacedrive",
    "project_name": "spacedriveapp/spacedrive",
    "project_desc": (
        "Rust + React/Tauri · cross-device file manager · 240,726 lines of Rust, 48,279 of TSX",
        "Rust + React/Tauri · 跨设备文件管理器 · Rust 240,726 行，TSX 48,279 行",
    ),
    "date": "2026-08-02",
    "archetype": (
        "native-desktop-gui · Rust engine under a webview UI, with a P2P sync subsystem",
        "原生桌面 GUI · webview 界面下面一个 Rust 引擎，外加一套 P2P 同步子系统",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "stay-rust-cut-scope",
    "scope_chip": (
        "keep the Rust core; defer the distributed-systems scope",
        "保留 Rust 内核；把分布式那一摊往后放",
    ),
    "scope_sub": (
        "Rust stays. The feature scope does not.",
        "Rust 留着，功能范围留不住。",
    ),

    "why": (
        "A file manager spends its time on three things: filesystem I/O, thumbnail decode, database "
        "queries. Spacedrive has 240,726 lines of Rust. Its own committed benchmark puts content "
        "identification at 95.5% of index wall clock on 100,000 files. That phase costs 13.4 ms per file "
        "and reads at most 58 KB of each one. The cost is six File::open calls per file, awaited in "
        "sequence. No language fixes that.",
        "文件管理器的时间花在三处：文件系统 I/O、缩略图解码、数据库查询。Spacedrive 有 240,726 行 Rust。它自己"
        "提交进仓库的基准说，在 100,000 个文件上，content identification 占索引墙钟时间的 95.5%。这一段每个文件"
        "耗 13.4 ms，而每个文件最多只读 58 KB。代价是每个文件六次 File::open，一个接一个 await。换语言解决不了"
        "这个。",
    ),
    "trigger": (
        "Two things reopen this. First, a Deep-mode profile that splits thumbnail wall clock between "
        "Spacedrive's own pipeline and the ffmpeg-sys, libheif and pdfium calls it makes. No such "
        "benchmark exists, so the thumbnail half of G2 is UNKNOWN rather than refuted. Second, one "
        "non-prerelease release shipping the sync subsystem. That would move G3 from FAIL to arguable.",
        "两件事能让这个结论重开。第一，一份 Deep 模式的 profile，把缩略图的墙钟时间拆成 Spacedrive 自己的流水线"
        "和它调用 ffmpeg-sys、libheif、pdfium 的部分。这样的基准现在不存在，所以 G2 里缩略图那一半是 UNKNOWN，"
        "不是被否证。第二，发一个带 sync 子系统、且不带 prerelease 标记的版本。那能把 G3 从 FAIL 变成可以争论。",
    ),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("One core has to run on five platforms, a server and a CLI.",
                           "同一个内核要跑在五个平台、一台服务器和一个 CLI 上。"),
         "name": "requirement",
         "evidence": "One Cargo workspace builds apps/tauri for desktop, apps/server, apps/cli at 9,808 lines, and apps/mobile/modules/sd-mobile-core for iOS and Android, alongside packages/swift-client. That distribution requirement is real and it is what Rust actually serves. The performance requirement is stated three ways and measured once: docs/overview/history.mdx:242 claims 8,500 files/second with no hardware or configuration, docs/core/indexing.mdx:388 claims ~1K files/sec for Content mode, and core/benchmarks/results records 74.58 files/s."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果"),
         "hero_evidence": ("The three hot paths are C libraries and one bad I/O loop.",
                           "三条热路径：一边是 C 库，一边是一个写坏的 I/O 循环。"),
         "name": "rust-specific causality",
         "evidence": "Thumbnail decode goes to ffmpeg-sys-next 7.1.3, libheif-sys 2.2.1+1.17.6, pdfium-render 0.8.27 and libwebp-sys 0.9.6. The advertised ~55ms search is SQLite FTS5, created in core/src/infra/db/migration/m20250120_000001_create_fts5_search_index.rs. Filesystem I/O is where Spacedrive's own Rust runs, and its dominant phase costs 13.4 ms per file to read at most 58 KB, because core/src/volume/backend/local.rs:133 opens the file on every one of six ranged reads. Rust is load-bearing for distribution. It is not load-bearing for any of the three."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("36,463 lines of P2P and sync, and no 1.0 in four years ten months.",
                           "36,463 行 P2P 与 sync，四年十个月没有 1.0。"),
         "name": "economics and smallest sufficient option",
         "evidence": "core/src/service/{network,sync,file_sync,sidecar_sync} plus core/src/infra/sync plus core/src/ops/{network,sync,file_sync} come to 36,463 lines, 18.5% of core/. Device pairing alone is 2,629 lines and the sync peer is 3,038. The repository was created 2021-09-27. Across 28 releases the highest without the prerelease bit is 0.4.3, published 2025-03-24; the two 2.0.0 releases are both marked prerelease. The smaller option keeps every line of Rust and puts that subsystem behind a flag."},
        {"id": "G4", "state": "UNKNOWN", "short": ("Delivery", "交付"),
         "hero_evidence": ("858 commits in 2025Q4, 36 in the last four months.",
                           "2025Q4 有 858 个 commit，最近四个月一共 36 个。"),
         "name": "delivery and reversibility",
         "evidence": "Commits on main: 858 in 2025Q4, 344 in 2026Q1, then 35 in April, 0 in May, 0 in June, 1 in July. Of 1,504 commits in the last twelve months, 1,256 carry a single author name. The repository is not archived and the newest commit is dated 2026-07-28, so stalled is supported by the evidence and abandoned is not. Capacity existed eight months ago. Whether it exists now cannot be read off the repository, which is why this gate is UNKNOWN and not FAIL."},
    ],

    "tiles": [
        (("Content identification", "content identification"), "95.5", ("% of index wall clock", "占索引墙钟时间"),
         ("shape_large · 100,000 files · Apple M3 Max", "shape_large · 100,000 个文件 · Apple M3 Max")),
        (("Cost per file in that phase", "该阶段每文件耗时"), "13.4", ("ms", "ms"),
         ("74.58 files/s · six File::open per file", "74.58 files/s · 每个文件六次 File::open")),
        (("Read throughput there, upper bound", "该阶段读取吞吐的上界"), "7.6", ("MB/s", "MB/s"),
         ("≤102,400 B per file × 100,000 ÷ 1,340.8 s", "每文件 ≤102,400 B × 100,000 ÷ 1,340.8 s")),
        (("Ceiling from optimizing traversal", "优化目录遍历能拿到的上限"), "1.047", ("× end-to-end", "× 端到端"),
         ("share 0.045; the docs ask for 13.4×", "占比 0.045；文档要的是 13.4×")),
        (("P2P and sync machinery", "P2P 与 sync 那一摊"), "36,463", ("lines of Rust", "行 Rust"),
         ("18.5% of core/ · highest non-prerelease is 0.4.3", "占 core/ 的 18.5% · 不带 prerelease 的最高版本是 0.4.3")),
        (("Commits, April to July 2026", "2026 年 4 月至 7 月的 commit"), "36", ("on main", "在 main 上"),
         ("against 858 in 2025Q4", "对照 2025Q4 的 858")),
    ],

    "options_sub": (
        "Every option is judged against one objective: index and browse a user's files fast on five "
        "platforms, and get a release out without the prerelease bit on it.",
        "所有方案对着同一个目标：在五个平台上把用户的文件索引好、浏览得快，并且发出一个不带 prerelease 标记的"
        "版本。",
    ),
    "options": [
        {"id": "stay-rust-cut-scope", "name": ("Keep the Rust core, defer P2P and sync",
                                               "保留 Rust 内核，推迟 P2P 与 sync"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("takes 36,463 lines off the 1.0 critical path",
                              "把 36,463 行从 1.0 的关键路径上挪走"),
         "one_time_cost": "feature-flagging one subsystem", "recurring_cost": "the flagged code still needs to compile",
         "cost_cell": ("weeks; one feature flag", "数周；一个 feature flag"),
         "time_to_value": ("weeks", "数周"),
         "compatibility": "no language change; the sync schema stays on disk",
         "compat_cell": ("no language change · flag rollback", "不换语言 · 用 flag 回滚"),
         "reversibility": "flip the flag back on",
         "evidence_strength": "MODERATE", "disposition": "selected",
         "note": ("recommended · the smallest step that gets a 1.0 out the door",
                  "推荐 · 能把 1.0 送出门的最小一步"),
         "reason": "Keeps the whole Rust engine, including the parts the evidence credits, and removes the one subsystem whose predecessor the team's own retrospective blames for V1."},
        {"id": "fix-io-loop", "name": ("Open each file once in the sampled hash",
                                       "抽样哈希里每个文件只 open 一次"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("aims at 95.5% of index wall clock", "打在占索引墙钟 95.5% 的那一段上"),
         "one_time_cost": "days", "recurring_cost": "none",
         "cost_cell": ("days; no new dependency", "数天；不加新依赖"),
         "time_to_value": ("days", "数天"),
         "compatibility": "hash output unchanged",
         "compat_cell": ("same hash bytes · git revert", "哈希字节不变 · git revert"),
         "reversibility": "git revert",
         "evidence_strength": "STRONG", "disposition": "retain",
         "note": ("retain · the counterfactual any performance claim has to beat first",
                  "保留 · 任何性能主张要先赢过这个对照"),
         "reason": "Six File::open calls per file, awaited in sequence, sit inside the phase that is 95.5% of the measured wall clock. One handle and six seeks is the cheapest change on the board."},
        {"id": "stay-full-scope", "name": ("Carry on at the current scope", "按现在的范围继续"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("the product as pitched, if it ships", "如果发得出来，就是宣传里那个产品"),
         "one_time_cost": "already spent", "recurring_cost": "240,726 lines against one active author",
         "cost_cell": ("sunk; 240,726 lines, one author", "已投入；240,726 行，一个活跃作者"),
         "time_to_value": ("unbounded on this evidence", "按现有证据说不出来"),
         "compatibility": "n/a — this is the status quo",
         "compat_cell": ("status quo · nothing to roll back", "现状 · 没什么要回滚"),
         "reversibility": "n/a",
         "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · fails G3 on measured delivery history", "排除 · 在实测交付史上过不了 G3"),
         "reason": "Four years ten months, 28 releases, the highest non-prerelease still 0.4.3, and 36 commits in the last four months. The scope has outrun the delivery capacity the repository can show."},
        {"id": "rust-native-ui", "name": ("Replace the webview UI with Rust GPUI",
                                          "把 webview 界面换成 Rust GPUI"),
         "implementation": "rust",
         "scope": "component", "scope_tag": "PARTIAL",
         "benefit_interval": ("unmeasured; no frame-time or input-latency data exists",
                              "没量过；没有帧时间或输入延迟数据"),
         "one_time_cost": "39,926 lines of TSX to re-implement", "recurring_cost": "a GUI framework the project does not own",
         "cost_cell": ("39,926 TSX lines; new UI stack", "39,926 行 TSX；一套新的 UI 栈"),
         "time_to_value": ("quarters", "以季度计"),
         "compatibility": "the whole visible product surface",
         "compat_cell": ("full UI rewrite · no partial rollback", "整个界面重写 · 无法部分回滚"),
         "reversibility": "keep both shells, at double cost",
         "evidence_strength": "UNKNOWN", "disposition": "retain",
         "note": ("retain · the one place more Rust could touch what users call fast",
                  "保留 · 「多用一点 Rust」唯一可能影响用户口中「快」的地方"),
         "reason": "apps/gpui-photo-grid exists at 322 lines and is commented out of the workspace members list. The idea is live and entirely unmeasured, so it stays UNKNOWN rather than excluded."},
        {"id": "swift-core-mac", "name": ("Swift core, Apple platforms only", "Swift 内核，只做 Apple 平台"),
         "implementation": "non-rust-native",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("same C decoders, same SQLite, one fewer toolchain",
                              "同样的 C 解码器，同样的 SQLite，少一套工具链"),
         "one_time_cost": "197,230 lines of core/ re-implemented", "recurring_cost": "no Windows, Linux or Android story",
         "cost_cell": ("197,230 lines; three platforms lost", "197,230 行；丢三个平台"),
         "time_to_value": ("years", "以年计"),
         "compatibility": "abandons the non-Apple targets in the workspace",
         "compat_cell": ("Apple only · no rollback", "只剩 Apple · 无回滚"),
         "reversibility": "none",
         "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · the workspace already targets Windows, Linux and Android",
                  "排除 · workspace 已经在做 Windows、Linux、Android"),
         "reason": "The strongest non-Rust native alternative on macOS. It fails the requirement the repository actually states, because apps/mobile, apps/server and the Windows build are in the tree."},
        {"id": "ts-node-core", "name": ("TypeScript core calling the same C libraries",
                                        "TypeScript 内核，调同一批 C 库"),
         "implementation": "external",
         "scope": "full", "scope_tag": "MIGRATE",
         "benefit_interval": ("hot paths unchanged; hiring and iteration get easier",
                              "热路径不变；招人和迭代变容易"),
         "one_time_cost": "197,230 lines of core/ re-implemented", "recurring_cost": "a runtime shipped to every device",
         "cost_cell": ("197,230 lines; runtime in the bundle", "197,230 行；包里带运行时"),
         "time_to_value": ("years", "以年计"),
         "compatibility": "loses the single native binary and the mobile cores",
         "compat_cell": ("no single binary · no rollback", "没有单一二进制 · 无回滚"),
         "reversibility": "none",
         "evidence_strength": "MODERATE", "disposition": "exclude",
         "note": ("exclude · the resident daemon and the single binary are the part Rust does buy",
                  "排除 · 常驻进程和单一二进制恰好是 Rust 真买到的东西"),
         "reason": "Prisma made this exact move and got 3.4x by deleting a chatty boundary. Spacedrive's boundary is not chatty, and its distribution requirement is the one thing Rust is measured to serve."},
    ],
    "lenses_sub": (
        "Each state is evidence tied to named options, not a score to add up. The performance lenses lean "
        "on one artifact: the benchmark results the project committed itself. Where it has published no "
        "measurement, the lens says UNKNOWN.",
        "每条状态都绑在具体方案上，不是可以相加的分数。性能几条主要靠一份材料：项目自己提交进仓库的基准结果。"
        "凡是它没量过的地方，这条就记 UNKNOWN。",
    ),
    "na_note": (
        "One lens is N/A. D4 fleet footprint: Spacedrive runs on the user's own machine. There is no "
        "instance count and no price per hour, so there is no fleet cost to compare.",
        "一条记为 N/A。D4 机队占用：Spacedrive 跑在用户自己的机器上。没有实例数，也没有小时单价，没有可比的"
        "机队成本。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · fix-io-loop", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["fix-io-loop", "stay-rust-cut-scope"],
         "claim": ("Spacedrive owns the hot path, and the project measured it. On its own 100,000-file "
                   "recipe, a discovery-only index finishes in 60.15 s. Turn content identification on "
                   "and the same tree takes 1,340.8 s. So 95.5% of the work sits in one phase of "
                   "Spacedrive's own code.",
                   "热路径确实归 Spacedrive 自己，而且项目自己量过。在它自己那份 100,000 文件的 recipe 上，只做"
                   "discovery 的索引 60.15 s 跑完。打开 content identification，同一棵树要 1,340.8 s。也就是说"
                   "95.5% 的工作压在 Spacedrive 自有代码的一个阶段里。"),
         "source": "core/benchmarks/results/shape_large-{indexing_discovery,content_identification}-ssd.json",
         "regime": "shape_large recipe, Apple M3 Max, 16 physical cores, 48 GB, internal SSD",
         "caveat": "The same ratio holds on the smaller recipes: 2.0% for 5,000 files and 2.8% for 20,000. The benchmark tree is generated sparse, so these are optimistic durations.",
         "change_trigger": "A run on a tree with real bytes would move the absolute times; the share would move against Spacedrive's own code, not for it."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "DISFAVORS · stay-full-scope", "css": "current",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["stay-full-scope"],
         "claim": ("Directory traversal is 4.5% of a full Content-mode index. Make it ten times faster "
                   "and the index gets 1.042× faster; make it infinitely fast and the ceiling is 1.047×. "
                   "The project's own docs ask for 13.4× over its own measurement. The gap does not live "
                   "in the traversal code.",
                   "目录遍历占完整 Content 模式索引的 4.5%。把它快十倍，整体快 1.042×；快到无穷，上限是 "
                   "1.047×。而项目自己的文档要求比自己的实测快 13.4×。这个差距不在遍历代码里。"),
         "source": "share 0.045 from the two committed shape_large runs; target 13.4 = ~1K files/sec at docs/core/indexing.mdx:388 over 74.58 files/s measured",
         "regime": "Amdahl on measured wall clock, same host and recipe",
         "caveat": "The kernel speedup of 10 is generous for code that already uses a work-stealing parallel walker on half the cores.",
         "change_trigger": "If a profile relocated the time into traversal, the share and the ceiling both change."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "UNKNOWN · rust-native-ui", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-native-ui"],
         "claim": ("The explorer a user actually looks at is 39,926 lines of TSX in a system webview. "
                   "Nobody has published a frame time or an input latency for it. Whatever the Rust core "
                   "does about garbage collection, it does not reach the surface where people decide "
                   "whether an app feels fast.",
                   "用户真正看着的那个 explorer 是 39,926 行 TSX，跑在系统 webview 里。没有人公开过它的帧时间"
                   "或输入延迟。Rust 内核在 GC 上做了什么，都到不了用户判断「这个 app 快不快」的那一层。"),
         "source": "packages/interface · 191 .tsx files, 39,926 lines; 77 .ts files, 6,837 lines",
         "regime": "n/a — the measurement is absent",
         "caveat": "Tauri's own maintainers have said WebKitGTK on Linux is getting worse each release; on Windows WebView2 is Chromium. Neither is Spacedrive's code.",
         "change_trigger": "A frame-time and input-latency measurement of the explorer grid would make the GPUI option assessable."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "STRONG", "option_ids": [],
         "claim": ("This is a desktop app. It runs on hardware the user already paid for, so there is no "
                   "instance count, no utilization and no hourly price to compare across options.",
                   "这是个桌面应用，跑在用户已经买下的硬件上。没有实例数、没有利用率、没有小时单价，方案之间"
                   "没有可比的机队成本。"),
         "source": "apps/tauri · apps/mobile · desktop and mobile targets",
         "regime": "n/a",
         "caveat": "apps/server exists for self-hosting, but no deployment or cost data is published for it."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "SUPPORTS · stay-rust-cut-scope", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["stay-rust-cut-scope", "stay-full-scope"],
         "claim": ("Two native binaries come out of core/: spacedrive and sd-daemon. A desktop file "
                   "manager gets launched and killed all day, and there is no runtime to boot first. "
                   "That property is worth something and it is the kind of thing Rust gives you for "
                   "free.",
                   "core/ 产出两个原生二进制：spacedrive 和 sd-daemon。桌面文件管理器一天里被开开关关很多次，"
                   "而它前面没有运行时要先起来。这个性质有价值，而且是 Rust 顺手就给的。"),
         "source": "core/Cargo.toml [[bin]] spacedrive, sd-daemon · core/src/bin (4 files, 698 lines)",
         "regime": "structural, from the manifest",
         "caveat": "No cold-start number is published. The ~150MB-for-1M-files figure in docs has no artifact behind it either."},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "NEUTRAL · all options", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Rust removes memory-unsafety from 240,726 lines, and that is a real property. It is "
                   "not a distinctive one here. Swift is memory-safe, TypeScript is memory-safe, and the "
                   "code that parses hostile image and video bytes is C under every option.",
                   "Rust 让 240,726 行代码没有内存不安全问题，这是实在的性质，但在这里不是差异化的性质。"
                   "Swift 内存安全，TypeScript 内存安全，而真正去解析可疑图片和视频字节的那部分，每个方案下都是 C。"),
         "source": "220 unsafe occurrences across 39 .rs files; 109 of them in crates/ffmpeg (2,672 lines)",
         "regime": "occurrence count from grep -o, not line count; comments not excluded",
         "caveat": "crates/ffmpeg is a hand-written FFI wrapper around ffmpeg-sys-next, so the densest unsafe in the tree sits exactly at the untrusted-input boundary."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "SUPPORTS · stay-rust-cut-scope", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["stay-rust-cut-scope"],
         "claim": ("The indexer uses a work-stealing walker on half the available cores and a "
                   "memory-mapped arena for the ephemeral index, 3,623 lines of it. Doing that in a "
                   "language with real threads and no collector is easier. The property is genuine.",
                   "索引器用 work-stealing walker 跑在一半的核上，临时索引用内存映射 arena，那部分 3,623 行。"
                   "在一个有真线程、没有 collector 的语言里做这些确实更省事。这个性质是实的。"),
         "source": "core/src/ops/indexing/ephemeral/ (arena.rs, index.rs, writer.rs, snapshot.rs) · docs/core/indexing.mdx:395",
         "regime": "structural, from the implementation",
         "caveat": "It did not prevent the defect that dominates the measurement: content_identity.rs awaits six separate read_range calls per file and local.rs:133 opens the file inside each one.",
         "change_trigger": "Fixing that loop is the test of whether the concurrency design is as good as the structure suggests."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "SUPPORTS · stay-rust-cut-scope", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-rust-cut-scope", "stay-full-scope"],
         "claim": ("One workspace ships a desktop app, a headless server, a 9,808-line CLI, and iOS and "
                   "Android cores. This is the requirement Rust is measurably serving. Swift does not "
                   "reach Windows or Android, and a Node core does not produce a single native binary "
                   "for five targets.",
                   "一个 workspace 出桌面应用、无头服务端、9,808 行的 CLI，以及 iOS 和 Android 内核。这才是 "
                   "Rust 在这里确实兑现的需求。Swift 到不了 Windows 和 Android，Node 内核也给不出面向五个目标的"
                   "单一原生二进制。"),
         "source": "Cargo.toml members: apps/server, apps/cli, apps/tauri/src-tauri, apps/mobile/modules/sd-mobile-core/core, core, crates/*",
         "regime": "workspace manifest at this commit",
         "caveat": "packages/swift-client (10 .swift files) and packages/ts-client are generated by specta from the Rust types, so the binding surface is a maintenance cost as well as a benefit."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "DISFAVORS · stay-full-scope", "css": "current",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["stay-full-scope", "stay-rust-cut-scope"],
         "claim": ("The team's own retrospective names the bill. They wrote prisma-client-rust and rspc "
                   "because Rust had neither, then could not maintain either. Prisma's Rust engine was "
                   "deprecated under them. libp2p was replaced by Iroh. This is what a thin ecosystem "
                   "costs, and it is priced in years.",
                   "账单是团队自己写下来的。他们写了 prisma-client-rust 和 rspc，因为 Rust 两样都没有，然后两样"
                   "都维护不下去。Prisma 的 Rust engine 在他们脚下被弃用。libp2p 后来换成了 Iroh。生态薄就是这个"
                   "价钱，而且是按年算的。"),
         "source": "docs/overview/history.mdx:82-92 — \"The team built prisma-client-rust and rspc out of necessity, then couldn't maintain them\"",
         "regime": "first-party retrospective committed to the repository",
         "caveat": "They also wrote crates/task-system, 4,835 lines of their own scheduler on top of tokio. The pattern the retrospective warns about is still in the tree.",
         "change_trigger": "sea-orm and iroh are both maintained by others; if they hold, this lens weakens over time."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "NEUTRAL · all options", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE",
         "option_ids": ["stay-rust-cut-scope", "stay-full-scope", "fix-io-loop", "rust-native-ui",
                        "swift-core-mac", "ts-node-core"],
         "claim": ("Every option links the same C. Cargo.lock resolves 1,272 crates, 51 of them -sys "
                   "bindings: SQLite, FFmpeg, libheif, libwebp, zstd, whisper.cpp. A Swift core would "
                   "call the same FFmpeg. So would a Node core. The decode boundary is a constant, not a "
                   "variable.",
                   "每个方案链接的是同一批 C。Cargo.lock 解出 1,272 个 crate，其中 51 个是 -sys 绑定：SQLite、"
                   "FFmpeg、libheif、libwebp、zstd、whisper.cpp。Swift 内核会调同一个 FFmpeg，Node 内核也一样。"
                   "解码边界是常量，不是变量。"),
         "source": "Cargo.lock · libsqlite3-sys 0.30.1, ffmpeg-sys-next 7.1.3, libheif-sys 2.2.1+1.17.6, libwebp-sys 0.9.6, whisper-rs-sys 0.14.1, pdfium-render 0.8.27",
         "regime": "static dependency inventory at this commit",
         "caveat": "pdfium-render points at a spacedriveapp fork pinned to rev 983f8d8, so one of the decoders is already a maintained-by-us dependency."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · stay-full-scope", "css": "current",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["stay-full-scope"],
         "claim": ("240,726 lines of Rust, 36,463 of them distributed systems, and 1,256 of the last "
                   "1,504 commits from one author name. 28 releases in four years ten months and none "
                   "non-prerelease is still 0.4.3. core/src/service/watcher_old carries 5,559 lines kept for "
                   "reference and not compiled.",
                   "240,726 行 Rust，其中 36,463 行是分布式系统，最近 1,504 个 commit 里 1,256 个来自同一个"
                   "作者名。四年十个月 28 个发布，不带 prerelease 的最高版本还是 0.4.3。core/src/service/watcher_old 里留着 5,559 "
                   "行，注释说是留作参考、不参与编译。"),
         "source": "gh api repos/spacedriveapp/spacedrive/{commits,releases} · core/src/service/mod.rs:22",
         "regime": "GitHub REST API, commits on main branch, and file counts at this commit",
         "caveat": "The engineering discipline is not in question: 63 test files and 30,959 lines in core/tests, 711 test attributes repo-wide, and committed benchmark artifacts. This is a capacity finding, not a quality one.",
         "change_trigger": "A non-prerelease release, or a second sustained contributor, moves this lens."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · fix-io-loop", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["fix-io-loop"],
         "claim": ("There is an in-stack change worth days that aims at 95.5% of the measured wall clock. "
                   "Hold one file handle instead of opening six times per file. Any argument that "
                   "Spacedrive needs a different language for speed has to beat that first, and nobody "
                   "has tried it.",
                   "栈内有一个几天的改动，正对着实测墙钟的 95.5%：一个文件句柄拿着用，别每个文件开六次。任何"
                   "「Spacedrive 换语言才能快」的说法都要先赢过它，而这件事还没有人做过。"),
         "source": "core/src/domain/content_identity.rs:224,235,247 · core/src/volume/backend/local.rs:133",
         "regime": "code reading against the committed benchmark",
         "caveat": "The gain is not quantified here, because that would require running the benchmark and this analysis is read-only."},
    ],

    "findings": [
        ("current",
         ("95.5% of the index is one phase that opens each file six times",
          "索引的 95.5% 压在一个阶段上，而它每个文件开六次"),
         ("Spacedrive committed its own benchmark results. On 100,000 files, an Apple M3 Max with 16 "
          "physical cores, a discovery-only index takes 60.15 s. With content identification on, the "
          "same tree takes 1,340.8 s. That is 13.4 ms per file. content_identity.rs hashes files above "
          "100 KB by sampling 8 KB plus four 10 KB blocks plus 8 KB, so it reads at most 58 KB of each "
          "one, and it gets those six ranges through six calls to read_range. local.rs:133 opens the "
          "file inside every call.",
          "Spacedrive 把自己的基准结果提交进了仓库。100,000 个文件，Apple M3 Max、16 个物理核，只做 discovery "
          "的索引 60.15 s；打开 content identification，同一棵树 1,340.8 s。合到每个文件 13.4 ms。"
          "content_identity.rs 对 100 KB 以上的文件用抽样：8 KB 加四个 10 KB 块加 8 KB，所以每个文件最多读 58 "
          "KB，而这六段是通过六次 read_range 拿的。local.rs:133 在每一次调用里都重新 open 一遍文件。"),
         "core/src/domain/content_identity.rs:213-251 · core/src/volume/backend/local.rs:133"),
        ("current",
         ("The thumbnail path is FFmpeg, libheif, PDFium and libwebp",
          "缩略图那条路是 FFmpeg、libheif、PDFium、libwebp"),
         ("crates/ffmpeg is 2,672 lines of Rust over ffmpeg-sys-next 7.1.3, and 109 of the repository's "
          "220 unsafe occurrences are in it. crates/images pulls libheif-sys for HEIF and a pinned fork "
          "of pdfium-render for PDF. Encoding goes out through libwebp-sys. Rust holds the pointers and "
          "checks the error codes. The decoders are C and C++, and they would be in any language.",
          "crates/ffmpeg 是 2,672 行 Rust，架在 ffmpeg-sys-next 7.1.3 上；全仓库 220 处 unsafe 里有 109 处在"
          "它里面。crates/images 为 HEIF 拉 libheif-sys，为 PDF 拉一个钉住版本的 pdfium-render fork。编码走 "
          "libwebp-sys 出去。Rust 负责持指针、查错误码。解码器是 C 和 C++，换任何语言它们都在。"),
         "crates/ffmpeg/Cargo.toml · crates/images/Cargo.toml · Cargo.lock"),
        ("current",
         ("Search is SQLite's C full-text extension", "搜索是 SQLite 的 C 全文扩展"),
         ("The headline is a ~55ms search over a million entries. The implementation is an FTS5 virtual "
          "table, created by a migration whose own comment says \"high-performance full-text search\". "
          "FTS5 ships inside SQLite, reached through libsqlite3-sys 0.30.1. Spacedrive writes the query. "
          "SQLite answers it.",
          "宣传语是「百万条目 ~55ms 搜索」。实现是一个 FTS5 虚拟表，建表 migration 自己的注释写着 "
          "\"high-performance full-text search\"。FTS5 在 SQLite 里，经 libsqlite3-sys 0.30.1 到达。"
          "Spacedrive 写查询，SQLite 回答。"),
         "core/src/infra/db/migration/m20250120_000001_create_fts5_search_index.rs:3"),
        ("current",
         ("36,463 lines of P2P and sync, and 0.4.3 is still the highest stable tag",
          "36,463 行 P2P 与 sync，而最高的稳定标签还是 0.4.3"),
         ("Device pairing is 2,629 lines. The sync peer is 3,038. P2P file transfer is 2,015. Add the "
          "network and sync trees under core/src/service, core/src/infra and core/src/ops and it comes "
          "to 36,463 lines, 18.5% of core/. The repository opened on 2021-09-27. Twenty-eight releases "
          "later, the newest is v2.0.0-alpha.2 from 2026-02-07, and it carries the prerelease bit.",
          "设备配对 2,629 行，sync peer 3,038 行，P2P 文件传输 2,015 行。把 core/src/service、core/src/infra、"
          "core/src/ops 下的 network 和 sync 几棵树加起来是 36,463 行，占 core/ 的 18.5%。仓库 2021-09-27 建的。"
          "二十八个发布之后，最新的是 2026-02-07 的 v2.0.0-alpha.2，带着 prerelease 标记。"),
         "core/src/service/network/protocol/pairing/mod.rs:2629 lines · gh api repos/spacedriveapp/spacedrive/releases"),
        ("current",
         ("The team wrote its own ORM client and its own RPC layer, then could not maintain them",
          "团队自己写了 ORM 客户端和 RPC 层，然后维护不下去"),
         ("The retrospective is in the repository and it is blunt. Prisma's Rust client engine was "
          "deprecated, \"leaving the project on an unmaintained fork with no migration path\". libp2p was "
          "\"fundamentally broken\". And the line that matters most: the team built prisma-client-rust "
          "and rspc \"out of necessity, then couldn't maintain them\". Neither existed in Rust. Both "
          "became debt.",
          "回顾就在仓库里，写得很直接。Prisma 的 Rust client engine 被弃用，\"leaving the project on an "
          "unmaintained fork with no migration path\"。libp2p 是 \"fundamentally broken\"。而最要紧的一句："
          "团队写 prisma-client-rust 和 rspc 是 \"out of necessity, then couldn't maintain them\"。这两样 Rust "
          "里都没有，后来都变成了负债。"),
         "docs/overview/history.mdx:82-92"),
        ("unknown",
         ("Nobody has benchmarked the thumbnail path", "缩略图那条路没有人量过"),
         ("core/benchmarks/results holds three scenarios: indexing-discovery, aggregation, "
          "content-identification. There is no media or thumbnail scenario, on any shape, on either "
          "disk. Deep mode is the configuration that triggers thumbnail generation, and its cost is "
          "unmeasured. This is why the thumbnail half of G2 reads UNKNOWN and not FAIL.",
          "core/benchmarks/results 里有三个场景：indexing-discovery、aggregation、content-identification。"
          "没有 media 或 thumbnail 场景，任何 shape、任何盘都没有。触发缩略图生成的是 Deep 模式，而它的开销"
          "没被量过。所以 G2 里缩略图那一半写的是 UNKNOWN，不是 FAIL。"),
         "core/benchmarks/results/ · 18 result files, 3 scenarios, none for media"),
    ],

    "buys": [
        (("One core on five platforms, with no runtime", "一个内核，五个平台，不带运行时"),
         ("one workspace builds the Tauri desktop app, a headless server, a 9,808-line CLI, and the iOS "
          "and Android cores. This is the requirement the repository actually demonstrates.",
          "一个 workspace 出 Tauri 桌面应用、无头服务端、9,808 行的 CLI，以及 iOS 和 Android 内核。这是仓库真正"
          "证明了的需求。")),
        (("A daemon that can hold a large resident index", "一个装得下大索引的常驻进程"),
         ("sd-daemon keeps a memory-mapped arena index, 3,623 lines of it. Real threads, no collector "
          "walking a million entries.",
          "sd-daemon 里是内存映射的 arena 索引，3,623 行。真线程，没有 collector 去爬一百万条目。")),
        (("Memory safety across 240,726 lines", "240,726 行代码的内存安全"),
         ("real, though 220 unsafe occurrences sit in 39 files and the image decoders stay C. Swift and "
          "TypeScript would also be memory-safe.",
          "这是实的，尽管 39 个文件里有 220 处 unsafe，而图像解码器还是 C。Swift 和 TypeScript 也一样内存安全。")),
    ],
    "nobuys": [
        (("Faster indexing", "更快的索引"),
         ("content identification is 95.5% of index wall clock and costs 13.4 ms per file to read at most "
          "58 KB. Six File::open calls per file is not a language problem.",
          "content identification 占索引墙钟的 95.5%，每个文件 13.4 ms，只为读最多 58 KB。每文件六次 "
          "File::open，这不是语言问题。")),
        (("Faster thumbnails", "更快的缩略图"),
         ("FFmpeg, libheif, PDFium and libwebp do the decoding. No benchmark for that path exists either "
          "way.",
          "解码是 FFmpeg、libheif、PDFium、libwebp 做的。而且这条路上根本没有基准。")),
        (("Faster search", "更快的搜索"),
         ("the ~55ms figure is an FTS5 virtual table. That is SQLite, written in C.",
          "那个 ~55ms 是 FTS5 虚拟表。那是 SQLite，用 C 写的。")),
        (("A UI that feels native", "原生手感的界面"),
         ("the explorer is 39,926 lines of TSX in a system webview. The core's language never touches "
          "that frame.",
          "explorer 是 39,926 行 TSX，跑在系统 webview 里。内核用什么语言，碰不到那一帧。")),
    ],

    "precedents": [
        {"name": "Zed · GPUI", "outcome": "SHIPPED",
         "body": ("A Rust desktop editor with its own GPU UI framework shipped, and shipped fast: "
                  "third-party numbers put it around 58ms end-to-end against VS Code's 97ms. The catch "
                  "is in how they got there. No Rust GUI framework met the bar, so they wrote one.",
                  "一个 Rust 桌面编辑器，带自己的 GPU UI 框架，发出来了，而且够快：第三方数据大概是端到端 58ms "
                  "对 VS Code 的 97ms。代价在于他们怎么走到那一步——没有现成的 Rust GUI 框架够用，于是自己写了"
                  "一个。"),
         "match": ("a Mac-first Rust desktop app where perceived speed is the product",
                   "同样是 Mac 优先的 Rust 桌面应用，同样把感知速度当产品"),
         "mismatch": ("Zed owns its render path; Spacedrive's UI is 39,926 lines of TSX in a webview, and "
                      "its gpui experiment is 322 lines commented out of the workspace",
                      "Zed 自己掌着渲染路径；Spacedrive 的界面是 webview 里 39,926 行 TSX，它的 gpui 实验是 322 "
                      "行，还被注释出了 workspace"),
         "regime": "third-party unaudited editor latency measurements", "source_label": "third-party · unaudited",
         "url": "https://zed.dev/blog/videogame"},
        {"name": "Prisma · Rust query engine removed", "outcome": "REVERSED",
         "body": ("Prisma deleted its Rust query engine and got faster: findMany on 25k rows went from "
                  "185ms to 55ms. Their diagnosis was the boundary, not the language. This is the same "
                  "Prisma whose Rust engine deprecation the Spacedrive retrospective names as a cause of "
                  "V1's collapse.",
                  "Prisma 把自己的 Rust query engine 删了，然后变快了：25k 行的 findMany 从 185ms 到 55ms。他们的"
                  "诊断是边界的问题，不是语言的问题。而 Spacedrive 的回顾里，把 V1 崩掉的原因之一记成了这同一个 "
                  "Prisma 的 Rust engine 被弃用。"),
         "match": ("the exact dependency Spacedrive built on and then got stranded by",
                   "Spacedrive 当年就架在这个依赖上，后来被它甩在半路"),
         "mismatch": ("Prisma's boundary was crossed per query from JavaScript; Spacedrive's core is the "
                      "process, not a callee",
                      "Prisma 的边界是每次查询从 JavaScript 穿过去；Spacedrive 的内核就是进程本身，不是被调用方"),
         "regime": "first-party benchmarks, Prisma 6.16 GA", "source_label": "first-party · engineering blog",
         "url": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm"},
        {"name": "Linear · sync engine", "outcome": "STAYED",
         "body": ("Local-first sync with sub-50ms page loads and working offline, built in TypeScript "
                  "against a local object graph. The hard part was the design of the sync protocol. The "
                  "language was never the lever.",
                  "本地优先的同步，页面加载 50ms 以内，离线可用，用 TypeScript 架在一张本地对象图上。难的是同步"
                  "协议怎么设计，语言从来不是那个杠杆。"),
         "match": ("local-first sync as a product feature, which is what Spacedrive's 36,463 lines are for",
                   "把本地优先同步当产品特性，Spacedrive 那 36,463 行就是干这个的"),
         "mismatch": ("Linear syncs a SaaS object graph through a server; Spacedrive is leaderless P2P "
                      "across user devices with pairing and NAT traversal",
                      "Linear 是通过服务端同步一张 SaaS 对象图；Spacedrive 是用户设备之间无主的 P2P，还要配对和"
                      "NAT 穿透"),
         "regime": "first-party product measurements", "source_label": "first-party · engineering blog",
         "url": "https://linear.app/now/scaling-the-linear-sync-engine"},
        {"name": "Mozilla · Servo as a Gecko replacement", "outcome": "CANCELLED",
         "body": ("A full engine replacement was priced at thousands of engineer-years against a handful "
                  "of heads. The team was laid off in 2020. What shipped was the extraction: Stylo and "
                  "WebRender went into Firefox, and the replacement goal did not.",
                  "整个引擎的替换被算成几千人年，而手上只有几个人。2020 年团队被裁。真正发出去的是抽出来的部分："
                  "Stylo 和 WebRender 进了 Firefox，替换这个目标没有。"),
         "match": ("scope economics against available heads, and R&D that was still worth doing",
                   "范围经济性对上手里的人头，而那些研发本身仍然值得做"),
         "mismatch": ("Mozilla had a shipping product to fall back on; Spacedrive's V1 was retired and V2 "
                      "is the only thing there is",
                      "Mozilla 还有一个在发的产品可以退守；Spacedrive 的 V1 已经退役，V2 是唯一的东西"),
         "regime": "first-party account and public record", "source_label": "first-party · blog + public record",
         "url": "https://bholley.net/blog/2017/stylo.html"},
        {"name": "Fixie · Rust at a startup", "outcome": "CAUTIONARY",
         "body": ("A CEO and ex-Google systems researcher wrote it plainly: \"Rust is awesome, for "
                  "certain things. But think twice before picking it up for a startup that needs to move "
                  "fast.\" His specific complaint was that Rust makes roughing out new features hard.",
                  "一位 CEO、前 Google 系统研究员写得很直白：\"Rust is awesome, for certain things. But think "
                  "twice before picking it up for a startup that needs to move fast.\" 他具体的抱怨是，Rust 让"
                  "新功能的粗胚很难打。"),
         "match": ("a VC-funded startup pre-product-market-fit, which is where Spacedrive spent 2022-2025",
                   "拿了 VC、还没找到 PMF 的创业公司，Spacedrive 2022 到 2025 就在这个位置"),
         "mismatch": ("one account about a backend CRUD product; Spacedrive's requirement does include "
                      "five native targets",
                      "那是关于一个后端 CRUD 产品的单一叙述；Spacedrive 的需求里确实包含五个原生目标"),
         "regime": "first-party velocity account, n=1", "source_label": "first-party · essay",
         "url": "https://mdwdotla.medium.com/using-rust-at-a-startup-a-cautionary-tale-42ab823d9454"},
    ],
    "path": [
        {"title": ("Open the file once", "文件只 open 一次"),
         "body": ("Whoever owns core/src/domain and core/src/volume holds a single File handle across the "
                  "six ranged reads in the sampled hash, instead of opening the file inside each one. "
                  "Then re-run shape_large content-identification on the same recipe and the same host. "
                  "The step passes when the recorded files/s rises and the hash output is byte-identical "
                  "for the same tree. If wall clock does not move, publish the flame graph: the time is "
                  "somewhere else and this report is wrong about where. Backing out is a git revert, and "
                  "the hash algorithm is never touched.",
                  "core/src/domain 和 core/src/volume 的负责人，在抽样哈希的六次范围读之间只拿一个 File 句柄，"
                  "别在每次读里重新 open。然后在同一份 recipe、同一台机器上重跑 shape_large 的 "
                  "content-identification。通过标准是：记录下来的 files/s 上升，且同一棵树的哈希输出逐字节不变。"
                  "如果墙钟没动，就把 flame graph 发出来——时间在别处，这份报告猜错了位置。回退就是一次 git "
                  "revert，哈希算法全程不动。"),
         "owner": "whoever owns core/src/domain and core/src/volume",
         "cost_range": ("days", "数天"),
         "artifact": "a re-run of shape_large content-identification on the committed recipe, with one File handle per file instead of six opens",
         "acceptance": "recorded files/s rises and the hash output is byte-identical for the same tree",
         "stop": "if wall clock does not move, publish the flame graph — the time is elsewhere and this report is wrong about where",
         "rollback": "git revert; the hash algorithm is untouched"},
        {"title": ("Benchmark Deep mode before saying anything about media",
                   "先给 Deep 模式做基准，再谈媒体"),
         "body": ("Whoever wants to argue about thumbnail performance adds a Deep-mode scenario to "
                  "core/benchmarks and splits its wall clock two ways: time inside Spacedrive's own "
                  "pipeline, and time inside ffmpeg-sys, libheif and pdfium. The two shares have to sum "
                  "to the measured wall clock on a recipe someone else can regenerate. If most of it is "
                  "inside the C libraries, the media performance track closes and nobody spends another "
                  "week on it. This step moves no product code.",
                  "想争论缩略图性能的人，先在 core/benchmarks 里加一个 Deep 模式场景，把它的墙钟时间拆成两块："
                  "在 Spacedrive 自己流水线里的时间，和在 ffmpeg-sys、libheif、pdfium 里的时间。两块之和要对得上"
                  "实测墙钟，recipe 要能被别人重新生成。如果大部分在 C 库里，媒体性能这条线就关掉，没人再花一周"
                  "在上面。这一步不动产品代码。"),
         "owner": "whoever proposes media performance work",
         "cost_range": ("1-2 weeks", "1–2 周"),
         "artifact": "a Deep-mode benchmark scenario splitting wall clock between Spacedrive's pipeline and time inside ffmpeg-sys, libheif and pdfium",
         "acceptance": "the two shares sum to measured wall clock on a recipe a third party can regenerate",
         "stop": "close the media performance track if most of the time is inside the C libraries",
         "rollback": "measurement only; no product code changes"},
        {"title": ("Put the sync subsystem behind a flag and ship a 1.0",
                   "把 sync 子系统放到 flag 后面，发一个 1.0"),
         "body": ("The maintainer feature-gates core/src/service/network and core/src/service/sync so the "
                  "default build excludes them, then publishes a release without the prerelease bit. "
                  "36,463 lines come off the 1.0 critical path and stay in the tree. The step passes when "
                  "that release exists and the gated code still compiles under its flag. If the flag "
                  "cannot be cut without breaking the on-disk schema, say so in writing and re-price the "
                  "subsystem as core rather than optional. Flipping the flag back on is the rollback.",
                  "维护者给 core/src/service/network 和 core/src/service/sync 加 feature gate，让默认构建不含"
                  "它们，然后发一个不带 prerelease 标记的版本。36,463 行离开 1.0 的关键路径，但留在树里。通过标准"
                  "是：那个版本存在，且被 gate 的代码在自己的 flag 下仍能编过。如果这个 flag 切不出来、不破坏磁盘"
                  "上的 schema 就切不动，那就写下来，把这个子系统重新定价成核心而不是可选。回滚就是把 flag 打开。"),
         "owner": "the maintainer",
         "cost_range": ("weeks", "数周"),
         "artifact": "a release without the prerelease bit whose default build excludes core/src/service/{network,sync}",
         "acceptance": "the release is published and the gated code still compiles under its feature flag",
         "stop": "if the flag cannot be cut without breaking the on-disk schema, re-price the subsystem as core and say so in writing",
         "rollback": "flip the feature flag back on"},
        {"title": ("Attach a regime to every published number, or delete it",
                   "每个公开数字都配上工况，否则删掉"),
         "body": ("Whoever maintains docs/ puts hardware, configuration and recipe next to every files/s "
                  "and millisecond figure, or removes the figure. Today history.mdx:242 says 8,500 "
                  "files/second with no hardware named, indexing.mdx:388 says ~1K files/sec for Content "
                  "mode, and the committed benchmark says 74.58. That is a 13.4x spread inside one "
                  "repository. The step passes when no performance figure in docs/ lacks a regime and "
                  "none contradicts core/benchmarks/results. Deleting an unsupported number is the "
                  "preferred outcome, and it is documentation-only either way.",
                  "docs/ 的维护者给每个 files/s 和毫秒数字配上硬件、配置和 recipe，配不上就删掉。现在 "
                  "history.mdx:242 写 8,500 files/second，没说硬件；indexing.mdx:388 写 Content 模式 ~1K "
                  "files/sec；而提交进来的基准写 74.58。同一个仓库里 13.4 倍的落差。通过标准是：docs/ 里没有一个"
                  "性能数字缺工况，也没有一个和 core/benchmarks/results 相矛盾。删掉没有依据的数字是更好的结果，"
                  "而且这一步只动文档。"),
         "owner": "whoever maintains docs/",
         "cost_range": ("days", "数天"),
         "artifact": "hardware, configuration and recipe attached to every files/s and millisecond figure in docs/, or the figure removed",
         "acceptance": "no performance figure in docs/ lacks a regime and none contradicts core/benchmarks/results",
         "stop": "delete rather than defend any figure with no artifact behind it",
         "rollback": "documentation only"},
    ],

    "migration_checks": [
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("Of the four performance numbers the project advertises, search belongs to SQLite "
                   "FTS5, transfer belongs to Iroh, and the memory figure has no artifact. The one that "
                   "is Spacedrive's own is 13.4x off Spacedrive's own benchmark.",
                   "项目宣传的四个性能数字里，搜索归 SQLite FTS5，传输归 Iroh，内存那个没有依据。唯一属于 "
                   "Spacedrive 自己的那个，和 Spacedrive 自己的基准差 13.4 倍。"),
         "evidence": "docs/overview/history.mdx:240-245 vs core/benchmarks/results"},
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("Traversal is 4.5% of a Content-mode index, so the ceiling from optimizing it is "
                   "1.047x. The documentation asks for 13.4x. The reach argument is not available.",
                   "遍历占 Content 模式索引的 4.5%，优化它的上限是 1.047×。文档要 13.4×。影响面这条论证根本"
                   "拿不出来。"),
         "evidence": "D2 · Amdahl share 0.045, ceiling 1.047x, target 13.4x"},
        {"name": ("Baseline and regime", "基线与工况"), "state": "HIT",
         "claim": ("The one committed benchmark tree is generated sparse: an 8 KB header, four 10 KB "
                   "samples, an 8 KB footer, then set_len. Real disks return real blocks. So 13.4 ms per "
                   "file is the optimistic figure, not the pessimistic one.",
                   "唯一提交进来的基准目录树是稀疏生成的：8 KB 头、四个 10 KB 采样、8 KB 尾，然后 set_len。真实"
                   "磁盘返回真实块。所以每个文件 13.4 ms 是乐观值，不是悲观值。"),
         "evidence": "core/benchmarks/src/generator/filesystem.rs:94-135 · recipes/shape_large.yaml"},
        {"name": ("Omitted cost", "被漏掉的成本"), "state": "HIT",
         "claim": ("prisma-client-rust, rspc and a 4,835-line task system were all written because Rust "
                   "lacked them. Two became unmaintainable and the retrospective says so. That cost "
                   "belongs in the price of the language, not outside it.",
                   "prisma-client-rust、rspc，还有 4,835 行的 task system，都是因为 Rust 里没有才自己写的。"
                   "其中两个后来维护不下去，回顾里写了。这笔钱要算进语言的价格里，不能挂在外面。"),
         "evidence": "docs/overview/history.mdx:82-92 · crates/task-system"},
        {"name": ("Delivery ownership", "交付归属"), "state": "HIT",
         "claim": ("1,256 of the last 1,504 commits on main carry a single author name, and 87 more come "
                   "from an agent account. A 240,726-line codebase with one active author is a capacity "
                   "fact, whatever the language.",
                   "main 上最近 1,504 个 commit 里，1,256 个来自同一个作者名，另有 87 个来自一个 agent 账号。"
                   "240,726 行代码只有一个活跃作者，这是产能事实，跟语言无关。"),
         "evidence": "gh api repos/spacedriveapp/spacedrive/commits?since=2025-08-01"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("A days-long in-stack change aims at 95.5% of the measured wall clock: hold one file "
                   "handle instead of opening six times per file. Nobody has tried it yet.",
                   "一个几天的栈内改动，正对着实测墙钟的 95.5%：拿一个文件句柄用，别每个文件开六次。这件事还"
                   "没有人做过。"),
         "evidence": "D12 · content_identity.rs:224,235,247 · local.rs:133"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Cutting the sync subsystem out of 1.0 costs the product its headline feature. That is "
                   "a real loss and the report does not pretend otherwise. It is priced against a "
                   "four-year-ten-month record whose highest non-prerelease tag is still 0.4.3.",
                   "把 sync 子系统从 1.0 里砍出去，产品就少了最响的那个卖点。这是实在的损失，报告不假装它不"
                   "存在。它的对价是四年十个月里，不带 prerelease 的最高标签还停在 0.4.3。"),
         "evidence": "G3 · 36,463 lines · gh api releases, 28 releases, highest non-prerelease 0.4.3"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report credits the distribution win at G1 and D8 and keeps the scope word at "
                   "STAY. It never claims Rust was the wrong language for this product.",
                   "报告在 G1 和 D8 上认下分发这个收益，范围词保持 STAY。它没有说 Rust 是这个产品的错误选择。"),
         "evidence": "D8 · Cargo.toml workspace members across five targets"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "PASS",
         "claim": ("220 unsafe occurrences across 39 files and 51 -sys crates are disclosed, and the "
                   "decode boundary is priced as identical under every option including the non-Rust "
                   "ones.",
                   "39 个文件里 220 处 unsafe、51 个 -sys crate，都披露了；解码边界在每个方案下都按同一个成本"
                   "计，包括非 Rust 的那几个。"),
         "evidence": "D6, D10 · Cargo.lock 1,272 crates, 51 -sys"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("Step one carries its own falsifier. If holding one file handle does not move wall "
                   "clock, the flame graph gets published and this report was wrong about where the time "
                   "is.",
                   "第一步自带否证条件。如果拿一个句柄不改变墙钟，就把 flame graph 发出来，说明这份报告猜错了"
                   "时间的位置。"),
         "evidence": "reversible path step 1"},
    ],

    "gaps": [
        (("A Deep-mode benchmark for the thumbnail path", "缩略图路径的 Deep 模式基准"),
         ("Three scenarios are committed and none covers media. While that holds, the thumbnail half of "
          "G2 is UNKNOWN and no claim about media performance can be authorized in either direction.",
          "提交进来的是三个场景，没有一个覆盖媒体。这种状态下，G2 里缩略图那一半是 UNKNOWN，关于媒体性能的主张"
          "两个方向都授权不了。")),
        (("Frame time and input latency for the explorer UI", "explorer 界面的帧时间与输入延迟"),
         ("39,926 lines of TSX in a system webview decide what users call fast. Until someone measures "
          "it, the GPUI option stays UNKNOWN rather than excluded.",
          "系统 webview 里 39,926 行 TSX，决定了用户口中的「快」。在有人量它之前，GPUI 那个方案停在 UNKNOWN，"
          "不是被排除。")),
        (("A benchmark on a tree with real bytes", "在真实字节的目录树上跑一次基准"),
         ("The committed recipe writes sparse files, so 13.4 ms per file is measured against holes. Real "
          "blocks would raise the absolute cost and shrink the traversal share further.",
          "提交的 recipe 写的是稀疏文件，所以每文件 13.4 ms 是对着空洞测出来的。真实块会把绝对开销抬上去，把"
          "遍历那部分的占比压得更小。")),
        (("Whether the delivery capacity of 2025Q4 still exists", "2025Q4 那种交付产能是否还在"),
         ("858 commits in one quarter is real capacity, eight months ago. 36 commits in four months is "
          "real too. G4 stays UNKNOWN because the repository cannot settle which one describes now.",
          "一个季度 858 个 commit 是实在的产能，但那是八个月前。四个月 36 个 commit 也是实在的。G4 停在 UNKNOWN，"
          "因为仓库判不出哪一个描述的是现在。")),
    ],

    "assumptions": [
        "The shallow clone at 6dfeccf2113039e35f2ce735f945e70dc3e4ea45 represents the shipped tree, and the JSON and CSV files under core/benchmarks/results are read as the project's own measurements of its own code.",
        "The read-volume upper bound assumes no file can produce a read larger than MINIMUM_FILE_SIZE, which follows from content_identity.rs:180-186: files at or below 102,400 bytes are read whole and larger files are sampled at roughly 57,344 bytes.",
        "Author names 'Jamie Pine' and 'James Pine' are treated as one person, since the GitHub login is jamiepine and the benchmark host path is /Users/jamespine. The 1,256-of-1,504 figure uses 'Jamie Pine' alone, so the conclusion does not depend on that reading.",
        "No migration RFC was supplied, so the proposal assessed is the one the repository states about itself: a Rust core for a cross-device file manager at the scope currently on main.",
        "Commit counts come from the GitHub commits endpoint restricted to sha=main, so work living only on unmerged branches is not counted.",
    ],
    "objective": {
        "driver": "mixed performance, distribution and scope economics",
        "requirement": "index and browse a user's own files fast across macOS, Windows, Linux, iOS and Android, and publish a release without the prerelease bit",
        "baseline": "committed benchmark: 1,662.5 files/s discovery and 74.58 files/s content identification on 100,000 files, Apple M3 Max, internal SSD; the highest non-prerelease release is 0.4.3 from 2025-03-24, and the two 2.0.0 releases are prereleases",
        "target": "docs/core/indexing.mdx:388 states ~1K files/sec for Content mode; no other threshold in the repository carries a stated regime",
    },
    "repository": {
        "path": "https://github.com/spacedriveapp/spacedrive",
        "commit": "6dfeccf2113039e35f2ce735f945e70dc3e4ea45",
        "scope": "whole repository; core/ is the assessed engine, packages/interface is the assessed UI surface, and core/src/service/{network,sync} is the subsystem under scope review",
        "sampling": "shallow clone; 2,919 tracked files enumerated; core/, crates/, apps/, packages/, adapters/, docs/ and core/benchmarks/results measured; commit, release and author history from the GitHub REST API; no build, test or benchmark was run against the project",
    },
    "user_supplied_facts": [],
    "analysis_mode": "public-repository static analysis plus the GitHub REST API for commit, release and author history; no build, benchmark, or execution of the target",

    "amdahl": {
        "share": 0.045,
        "kernel_speedup": 10.0,
        "boundary": 0.0,
        "target": 13.4,
        "note": "share 0.045 is 60.15 s discovery-only against 1,340.8 s with content identification, shape_large on internal SSD, same host and recipe; kernel_speedup 10 is generous for code that already runs a work-stealing parallel walker; target 13.4 is the ~1K files/sec at docs/core/indexing.mdx:388 divided by the measured 74.58 files/s",
    },

    "method_title": (
        "spacedriveapp/spacedrive at 6dfeccf · static read-only analysis · why-not-rust method 2.0",
        "spacedriveapp/spacedrive @ 6dfeccf · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/spacedriveapp/spacedrive at commit "
        "6dfeccf2113039e35f2ce735f945e70dc3e4ea45, shallow clone, 2,919 tracked files. Scope: the whole "
        "repository, with core/ as the assessed engine and core/src/service/{network,sync} as the "
        "subsystem under scope review. Sampling: 240,726 lines of Rust across 1,166 files, of which "
        "core/ is 197,230 across 901, crates/ 24,099 across 153, apps/ 16,084 across 74, extensions/ "
        "1,293 and xtask/ 2,020. The UI is 48,279 lines of .tsx across 252 files and 23,674 of .ts "
        "across 153; the .ts files were checked and are TypeScript, not translation XML. 3,211 lines of "
        "Swift across 17 files, and 2,801 lines of Python across the 11 adapters under adapters/. Line "
        "counts are raw lines from `git ls-files -z <glob> | xargs -0 cat | wc -l`; comments and blanks "
        "are included and no vendored tree exists in this repository. The 36,463-line P2P and sync "
        "figure is core/src/service/{network,sync,file_sync,sidecar_sync} plus core/src/infra/sync plus "
        "core/src/ops/{network,sync,file_sync}, on the same raw-line basis as the 197,230 it is compared "
        "against; adding core/src/device and core/src/ops/{devices,redundancy} would make it 38,137. "
        "Unsafe counts are occurrences from `grep -o '\\bunsafe\\b'`, not matching lines, and comments "
        "were not excluded: 220 occurrences in 39 files, 109 of them in crates/ffmpeg. Performance "
        "evidence comes from artifacts the project committed itself under core/benchmarks/results: 18 "
        "JSON files across three scenarios and two disks, plus whitepaper_metrics.csv. The two runs this "
        "report turns on are shape_large on internal SSD, Apple M3 Max, 16 physical cores, 48 GB, 100,000 files and "
        "16,507 directories: discovery-only total_s 60.15, content-identification total_s 1,340.8. The "
        "GB/s column in that CSV is total logical file size divided by duration, not bytes read; "
        "content_identity.rs reads at most 102,400 bytes per file, so the true read rate in that phase "
        "is at most 7.6 MB/s, about 1,160 times lower than the 8.86 GB/s the CSV reports. The benchmark "
        "tree is generated sparse, which makes those durations optimistic rather than pessimistic. "
        "Amdahl inputs: share 0.045 (60.15 / 1,340.8), kernel_speedup 10, boundary 0, target 13.4 "
        "(~1K files/sec at docs/core/indexing.mdx:388 over 74.58 measured), giving 1.042x end-to-end and "
        "a 1.047x ceiling. Commit, release and author history came from the GitHub REST API on the main "
        "branch: `gh api \"repos/spacedriveapp/spacedrive/commits?sha=main&since=...&until=...\"` with "
        "per-quarter windows, and `gh api repos/spacedriveapp/spacedrive/releases`. No build, test, "
        "benchmark or execution of the app was performed, and nothing was written inside the clone. "
        "Objective: no migration RFC was supplied, so the assessment takes the proposal the repository "
        "states about itself. User-supplied facts: none. G4 is UNKNOWN rather than FAIL because 858 "
        "commits landed in 2025Q4 and the repository is not archived; the decision turns on G2 and G3, "
        "which fail on measured artifacts the project published. This is a structured decision protocol, "
        "not a statistical predictor.",
        "仓库：github.com/spacedriveapp/spacedrive，commit 6dfeccf2113039e35f2ce735f945e70dc3e4ea45，"
        "shallow clone，2,919 个纳管文件。范围：整个仓库，被评估的引擎是 core/，被审视范围的子系统是 "
        "core/src/service/{network,sync}。采样：Rust 240,726 行、1,166 个文件，其中 core/ 197,230 行 901 个文件，"
        "crates/ 24,099 行 153 个文件，apps/ 16,084 行 74 个文件，extensions/ 1,293 行，xtask/ 2,020 行。界面是 "
        "252 个 .tsx 文件 48,279 行、153 个 .ts 文件 23,674 行；.ts 文件逐一确认过是 TypeScript，不是翻译用的 "
        "XML。Swift 17 个文件 3,211 行，adapters/ 下 11 个适配器共 2,801 行 Python。行数是 "
        "`git ls-files -z <glob> | xargs -0 cat | wc -l` 的原始行数，含注释和空行；这个仓库里没有内置的第三方"
        "源码树。36,463 行的 P2P 与 sync 口径是 core/src/service/{network,sync,file_sync,sidecar_sync} 加 "
        "core/src/infra/sync 加 core/src/ops/{network,sync,file_sync}，和用来对比的 197,230 行同一个原始行口径；"
        "如果再算上 core/src/device 和 core/src/ops/{devices,redundancy}，是 38,137 行。unsafe 是 "
        "`grep -o '\\bunsafe\\b'` 的出现次数，不是匹配行数，也没有剔除注释：39 个文件里 220 次，其中 109 次在 "
        "crates/ffmpeg。性能证据来自项目自己提交进 core/benchmarks/results 的材料：三个场景、两种盘，共 18 个 "
        "JSON，加一份 whitepaper_metrics.csv。决定性的一对是内置 SSD 上的 shape_large：Apple M3 Max、16 个物理"
        "核、48 GB，100,000 个文件、16,507 个目录，只做 discovery 的 total_s 是 60.15，做 content-identification "
        "的 total_s 是 1,340.8。那份 CSV 里的 GB/s 列是文件逻辑总大小除以时长，不是实际读取字节；"
        "content_identity.rs 每个文件最多读 102,400 字节，所以这一阶段真实读取速率最高 7.6 MB/s，比 CSV 写的 "
        "8.86 GB/s 低大约 1,160 倍。基准目录树是稀疏生成的，所以这些时长是偏乐观而不是偏悲观。Amdahl 输入："
        "share 0.045（60.15 / 1,340.8）、kernel_speedup 10、boundary 0、target 13.4"
        "（docs/core/indexing.mdx:388 的 ~1K files/sec 除以实测 74.58），得到端到端 1.042×、上限 1.047×。"
        "commit、release 和作者历史来自 GitHub REST API 的 main 分支："
        "`gh api \"repos/spacedriveapp/spacedrive/commits?sha=main&since=...&until=...\"` 按季度取窗口，以及 "
        "`gh api repos/spacedriveapp/spacedrive/releases`。没有做任何构建、测试、基准，也没有运行这个应用，"
        "clone 里没有写入任何东西。目标：没有人给出迁移 RFC，因此按仓库自己陈述的方案评估。用户提供的事实：无。"
        "G4 记 UNKNOWN 而不是 FAIL，因为 2025Q4 有 858 个 commit 落地，而且仓库没有归档；决策落在 G2 和 G3 上，"
        "这两道门是在项目自己公布的实测材料上失败的。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit 6dfeccf · history from the GitHub REST API · no build, benchmark or execution of the app",
        "公开仓库 · 在 commit 6dfeccf 上做静态分析 · 历史来自 GitHub REST API · 没有构建、基准，也没有运行这个应用",
    ),
}
