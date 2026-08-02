"""bitwarden/clients — the desktop app took the smallest sufficient option in 2022.

Repository facts were measured read-only on the shallow clone named in
`repository`. History facts come from the GitHub REST API because the clone is
depth-1.
"""

CASE = {
    "slug": "bitwarden-desktop",
    "project_name": "bitwarden/clients · apps/desktop",
    "project_desc": (
        "Electron + Angular · 32,549 lines of the desktop app's own TypeScript, 28,301 lines of Rust",
        "Electron + Angular · 桌面端自有 TypeScript 32,549 行，Rust 28,301 行",
    ),
    "date": "2026-08-02",
    "archetype": (
        "electron-desktop · password manager with a napi Rust module and a uniffi Swift extension",
        "Electron 桌面端 · 密码管理器，带 napi Rust 模块和 uniffi Swift 扩展",
    ),

    "scope_word": "STAY",
    "auth": "REJECT",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "stay-split",
    "scope_chip": (
        "keep the Electron UI; keep growing the Rust module at the OS seam",
        "界面留在 Electron；Rust 模块继续在 OS 接缝上长",
    ),
    "scope_sub": (
        "the split it already has is the answer",
        "它现在这套拆分方式就是答案",
    ),

    "why": (
        "Bitwarden already put Rust where it pays. 28,301 lines of it in 13 workspace crates under "
        "apps/desktop/desktop_native, reached through 38 functions in a generated 491-line .d.ts, "
        "called by 15 files that all live in the Electron main process. The proposal on the table is "
        "to carry on into the UI. It does not survive its own security argument. The vault crypto is "
        "already Rust, and the decrypted user key still crosses IPC into the renderer's V8 heap — a "
        "Rust UI relocates that heap rather than emptying it.",
        "Bitwarden 早就把 Rust 放在了它值钱的位置。apps/desktop/desktop_native 下 13 个 workspace crate、"
        "28,301 行，"
        "对外通过一份生成的 491 行 .d.ts 里的 38 个函数，调用它的 15 个文件全在 Electron 主进程。桌面上的"
        "提案是继续往界面里推。这条提案过不了它自己的安全论证。金库加解密已经是 Rust，而解密后的 user key "
        "照样跨 IPC 进到渲染进程的 V8 堆里——换成 Rust 界面只是把这个堆搬个地方，不是把它清空。",
    ),
    "trigger": (
        "One thing reopens the scope. If Bitwarden rules that a decrypted user key must never enter "
        "the renderer's V8 heap, the answer becomes EXTRACT: grow secure_memory and move the unlock "
        "path behind it. A UI rewrite is still not the shape. Frame time, RSS and startup stay "
        "UNKNOWN because nobody has published a measurement for this app.",
        "有一件事能让范围重开。如果 Bitwarden 定下「解密后的 user key 绝不能进渲染进程 V8 堆」，答案就变成 "
        "EXTRACT：把 secure_memory 做厚，把解锁路径搬到它后面。界面重写仍然不是这个形状。帧时间、RSS、启动"
        "时间都停在 UNKNOWN，因为没有人公开过这个应用的测量。",
    ),

    # G1–G4 are graded against the Rust-expansion proposal under review — replacing the
    # Electron/Angular UI (rust-native-gui) or the Electron shell (tauri-shell) — not against
    # the status quo. The existing OS-seam module is not what is being authorized here.
    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"),
         "hero_evidence": ("A decrypted user key sits in the renderer's V8 heap while unlocked.",
                           "金库解锁期间，解密后的 user key 就在渲染进程的 V8 堆里。"),
         "name": "requirement",
         "evidence": "One gap is real and structural. On macOS the biometric key is read out of the Keychain and sent over IPC, and renderer-biometrics.service.ts:87 rebuilds it as a SymmetricCryptoKey inside the Angular process. The other half of the proposal — that the app should be faster or feel more native — names no measurable target anywhere in the repository or in public."},
        {"id": "G2", "state": "FAIL", "short": ("Causality", "因果"),
         "hero_evidence": ("A Rust UI relocates that heap; it does not empty it.",
                           "Rust 界面只是把那个堆搬个地方，清空不了。"),
         "name": "rust-specific causality",
         "evidence": "PureCrypto.symmetric_decrypt_string already runs Rust as WASM and hands back a JavaScript string, so plaintext in the UI process is not a property of the UI language. The second stated benefit is that the app should feel like a Mac app, which is a UI-framework property: uniffi and 569 lines of shipped Swift already serve that path with no Rust in the UI at all."},
        {"id": "G3", "state": "FAIL", "short": ("Economics", "经济性"),
         "hero_evidence": ("Weeks of secure_memory work beats rewriting 32,549 lines.",
                           "把 secure_memory 补几周，胜过重写 32,549 行。"),
         "name": "economics and smallest sufficient option",
         "evidence": "A far cheaper option meets the same target. secure_memory already holds keys outside ordinary heap on Windows and Linux; giving it a macOS backend and moving the unlock path behind it is weeks of work behind a feature flag. The rewrite costs 32,549 lines of desktop TypeScript plus whatever it consumes of 247,757 shared lines, for a benefit interval nobody has quantified."},
        {"id": "G4", "state": "FAIL", "short": ("Delivery", "交付"),
         "hero_evidence": ("No dual-run: the UI sits on a library three clients share.",
                           "没有双跑方案：界面坐在三个客户端共用的库上。"),
         "name": "delivery and reversibility",
         "evidence": "There is no rollback story for a UI rewrite here. libs/ is 247,757 non-spec lines that the browser extension, web vault and CLI also import, at 874 @bitwarden/common import statements in the desktop app alone. The shipped distribution matrix would be re-earned as well: 7 Rust target triples, a universal macOS build, a sandboxed Mac App Store package, snap, flatpak and three Windows architectures."},
    ],

    "tiles": [
        (("Rust in the desktop app", "桌面端里的 Rust"), "28,301", ("lines", "行"),
         ("13 workspace crates in apps/desktop/desktop_native · 100% of the repo's Rust",
          "apps/desktop/desktop_native 里 13 个 workspace crate · 全仓库 Rust 的 100%")),
        (("The whole FFI surface", "整个 FFI 面"), "38", ("functions", "个函数"),
         ("napi/index.d.ts · 491 lines · 15 namespaces", "napi/index.d.ts · 491 行 · 15 个命名空间")),
        (("The desktop app's own TypeScript", "桌面端自有 TypeScript"), "32,549", ("lines", "行"),
         ("apps/desktop/src · 238 files · 4.2% of the monorepo's TS",
          "apps/desktop/src · 238 个文件 · 整个 monorepo TS 的 4.2%")),
        (("Runtime callers of the Rust module", "运行时调用 Rust 模块的文件"), "15", ("files", "个"),
         ("every one of them in the Electron main process", "全部位于 Electron 主进程")),
        (("Rust that never compiles on a Mac", "在 Mac 上根本不编译的 Rust"), "7,851", ("lines", "行"),
         ("win_webauthn + windows_plugin_authenticator + process_isolation",
          "win_webauthn + windows_plugin_authenticator + process_isolation")),
        (("TypeScript files calling the Rust SDK", "调用 Rust SDK 的 TypeScript 文件"), "285", ("files", "个"),
         ("@bitwarden/sdk-internal · Rust delivered as WASM",
          "@bitwarden/sdk-internal · Rust 以 WASM 交付")),
    ],

    "options_sub": (
        "Every option is judged against one objective. Reach the macOS APIs a vault needs, and keep "
        "secret handling as tight as the platform allows. Leave the shared TypeScript alone; the "
        "browser extension, web vault and CLI import it too.",
        "所有方案对着同一个目标。拿到金库需要的 macOS API，把密钥处理收紧到平台允许的程度。共享的那套 "
        "TypeScript 不要动，浏览器扩展、Web 端和 CLI 都在 import 它。",
    ),
    "options": [
        {"id": "stay-split", "name": ("Keep Electron UI + Rust at the OS seam", "界面留 Electron，Rust 守 OS 接缝"),
         "implementation": "current",
         "scope": "stay", "scope_tag": "STAY",
         "benefit_interval": ("OS access met today; secret handling as tight as the platform allows",
                              "OS 访问已经拿到；密钥处理已收到平台允许的程度"),
         "one_time_cost": "none; already shipped", "recurring_cost": "two toolchains in CI, seven Rust target triples",
         "cost_cell": ("already paid; two toolchains in CI", "已经付过了；CI 里两条工具链"),
         "time_to_value": ("shipping since 2022", "2022 年起已在发布"),
         "compatibility": "native", "compat_cell": ("native · per-crate rollback", "原生 · 按 crate 回滚"),
         "reversibility": "drop a crate; the UI never notices",
         "evidence_strength": "STRONG", "disposition": "selected",
         "note": ("recommended · the smallest option that meets the requirement, taken in 2022",
                  "推荐 · 满足需求的最小方案，2022 年就选了"),
         "reason": "Rust sits exactly where OS APIs and cross-host code sharing demand it, and nowhere else. The UI keeps the shared library three other clients depend on."},
        {"id": "rust-secure-memory", "name": ("Move the unlock path behind secure_memory",
                                              "把解锁路径搬到 secure_memory 后面"),
         "implementation": "rust",
         "scope": "extract", "scope_tag": "EXTRACT",
         "benefit_interval": ("the one gap this report found: a decrypted user key in the V8 heap",
                              "本报告找到的唯一缺口：V8 堆里的解密 user key"),
         "one_time_cost": "weeks; a macOS backend for secure_memory does not exist yet",
         "recurring_cost": "one more IPC contract to review each release",
         "cost_cell": ("weeks; needs a macOS backend", "数周；需要一个 macOS 后端"),
         "time_to_value": ("one release cycle", "一个发布周期"),
         "compatibility": "IPC-shaped; no UI change",
         "compat_cell": ("IPC only · feature-flag rollback", "只动 IPC · 用 feature flag 回滚"),
         "reversibility": "feature flag", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · where the next Rust investment belongs, if the key must leave V8",
                  "保留 · 如果 key 必须离开 V8，下一笔 Rust 投入该落在这里"),
         "reason": "Targets the actual exposure rather than the language of the UI. secure_memory already exists with Windows and Linux backends; macOS falls back to mlock, which the code itself calls weaker."},
        {"id": "swift-native-mac", "name": ("Native Swift/AppKit Mac UI on the Rust core",
                                            "在 Rust 内核上做原生 Swift/AppKit Mac 界面"),
         "implementation": "non-rust-native",
         "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("answers the actual Mac complaint; buys nothing for memory safety",
                              "回应 Mac 用户真正的抱怨；内存安全上一分不涨"),
         "one_time_cost": "a second Mac client; two UIs to keep at feature parity",
         "recurring_cost": "Mac-only feature lag, forever",
         "cost_cell": ("a second Mac client; permanent parity debt", "多一个 Mac 客户端；长期的功能对齐负债"),
         "time_to_value": ("quarters", "以季度计"),
         "compatibility": "Rust core unchanged; UI parity is the risk",
         "compat_cell": ("core unchanged · ship both, drop one", "内核不动 · 两个都发，再砍一个"),
         "reversibility": "keep the Electron build", "evidence_strength": "MODERATE", "disposition": "retain",
         "note": ("retain · the native answer that is not a Rust answer", "保留 · 「原生」的答案，但不是 Rust 的答案"),
         "reason": "The complaint Mac users make is that the app is not native. uniffi already generates Swift bindings from autofill_provider, and 569 lines of Swift already ship in the credential-provider extension. Naming this keeps the native claim separate from the Rust claim."},
        {"id": "tauri-shell", "name": ("Swap Electron for a Rust shell on the system webview",
                                       "把 Electron 换成 Rust 外壳 + 系统 webview"),
         "implementation": "rust",
         "scope": "partial", "scope_tag": "PARTIAL",
         "benefit_interval": ("smaller installer; the rendering engine becomes someone else's",
                              "安装包更小；渲染引擎变成别人的"),
         "one_time_cost": "rewrite the main process and preload; requalify three platforms",
         "recurring_cost": "a webview matrix you do not control",
         "cost_cell": ("main process rewrite; 3 platforms requalified", "重写主进程；三个平台重新验证"),
         "time_to_value": ("quarters", "以季度计"),
         "compatibility": "WKWebView on macOS, WebKitGTK on Linux, WebView2 on Windows",
         "compat_cell": ("3 engines instead of 1 · hard to reverse", "1 个引擎变 3 个 · 很难回退"),
         "reversibility": "low", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · trades one Chromium for three engines you cannot patch",
                  "排除 · 用一个 Chromium 换三个你补不了的引擎"),
         "reason": "The Rust part is the shell, not the product surface. Tauri's own maintainers documented the Linux WebKitGTK problem, and on Windows WebView2 is Chromium anyway. For a vault, an engine you cannot pin is a security regression, not a win."},
        {"id": "rust-native-gui", "name": ("Rewrite the UI in a Rust GUI toolkit", "用 Rust GUI 框架重写界面"),
         "implementation": "rust", "scope": "full",
         "scope_tag": "MIGRATE",
         "benefit_interval": ("no measured benefit on any lens; loses the shared library",
                              "任何维度都没有实测收益；还丢掉共享库"),
         "one_time_cost": "32,549 lines of desktop TypeScript plus whatever it uses from 247,757 shared lines",
         "recurring_cost": "a11y, IME and platform matrix owned in-house",
         "cost_cell": ("32,549 + a share of 247,757 lines", "32,549 行，外加共享层 247,757 行里的一部分"),
         "time_to_value": ("years", "以年计"),
         "compatibility": "breaks code sharing with three other clients",
         "compat_cell": ("forks the shared layer · no rollback", "分叉共享层 · 无回滚"),
         "reversibility": "none", "evidence_strength": "WEAK", "disposition": "exclude",
         "note": ("exclude · pays for a rewrite and the threat model does not move",
                  "排除 · 付一次重写的钱，威胁模型不挪动"),
         "reason": "The vault crypto is already Rust and the decrypted key already lands in a heap the UI process owns. Moving that heap from V8 to Rust changes which process leaks it, not whether. Meanwhile the shared TypeScript layer serves three other clients."},
    ],

    "lenses_sub": (
        "Each state is evidence about named options, not a score to add up. The performance and "
        "footprint lenses sit at UNKNOWN because no measurement of this app exists in public, and no "
        "amount of argument moves them.",
        "每条状态都绑在具体方案上，不是能相加的分数。性能和占用那几条停在 UNKNOWN，因为公开资料里没有这个应用"
        "的任何测量，靠辩论推不动。",
    ),
    "na_note": (
        "One lens is N/A. D5 startup shape: the app registers autostart and lives in the tray, so it "
        "boots once per login and stays resident.",
        "一条记为 N/A。D5 启动形态：这个应用注册开机自启并常驻托盘，每次登录只启动一次然后一直在。",
    ),
    "lenses": [
        {"id": "D1", "name": ("Requirement & ownership", "需求与归属"),
         "label": "SUPPORTS · stay-split", "css": "current",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-split"],
         "claim": ("The unmet requirement was never speed. It was reaching the macOS Keychain, Touch "
                   "ID, an SSH agent socket, the clipboard and process hardening from inside "
                   "Electron. 15 main-process files do that through Rust, and no file in the "
                   "renderer calls the module at runtime.",
                   "从来没有满足不了的性能需求。缺的是在 Electron 里面拿到 macOS Keychain、Touch ID、"
                   "SSH agent socket、剪贴板和进程加固。15 个主进程文件通过 Rust 做这件事，渲染进程没有任何"
                   "文件在运行时调它。"),
         "source": "15 non-spec files import @bitwarden/desktop-napi as a value; 4 more use import type only",
         "regime": "static import graph at this commit",
         "caveat": "apps/desktop/src/autofill/services/desktop-autofill.service.ts is an Angular renderer service that imports the namespace without `type`, but every use of it is a type position; its runtime calls go through the preload IPC bridge.",
         "change_trigger": "A published frame-time or RSS profile would add a second, currently absent, requirement to weigh."},
        {"id": "D2", "name": ("End-to-end reach", "端到端影响面"),
         "label": "UNKNOWN · rust-native-gui, tauri-shell", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-native-gui", "tauri-shell"],
         "claim": ("No Amdahl figure appears here, and that is deliberate. There is no published "
                   "profile of this app splitting Chromium compositing, Angular change detection, "
                   "network sync and crypto. Substituting the line share for a time share would be a "
                   "method error.",
                   "这里不给 Amdahl 数字，是故意的。没有公开 profile 把这个应用的 Chromium 合成、Angular 变更"
                   "检测、网络同步和加解密拆开。拿代码行数占比顶替时间占比是方法错误。"),
         "source": "no published end-to-end profile of the Bitwarden desktop app",
         "regime": "n/a — the measurement is absent",
         "caveat": "The UI-rewrite options therefore carry no benefit interval for speed; they are excluded on other lenses, not on a speed calculation."},
        {"id": "D3", "name": ("Tail & runtime", "尾延迟与运行时"),
         "label": "UNKNOWN · rust-native-gui", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["rust-native-gui"],
         "claim": ("A V8 heap and a Chromium compositor are both in the loop, so a GC-pause story is "
                   "plausible on paper. Nobody has traced one. The repository shows the opposite "
                   "concern: backgroundThrottling is switched off so the window keeps updating, which "
                   "is a responsiveness decision, not a collector one.",
                   "V8 堆和 Chromium 合成器都在链路里，纸面上 GC 停顿的故事讲得通。但没有人做过 trace。仓库里"
                   "反映的是另一头的顾虑：backgroundThrottling 被关掉，让窗口持续更新——这是响应性的决定，"
                   "不是 collector 的决定。"),
         "source": "apps/desktop/src/main/window.main.ts:410 backgroundThrottling: false",
         "regime": "shipped webPreferences at this commit",
         "caveat": "Recorded UNKNOWN rather than assumed either way. A jank trace on a large vault would make this assessable."},
        {"id": "D4", "name": ("Fleet footprint", "机队占用"),
         "label": "UNKNOWN · tauri-shell, rust-native-gui", "css": "unknown",
         "state": "UNKNOWN", "strength": "UNKNOWN", "option_ids": ["tauri-shell", "rust-native-gui"],
         "claim": ("Desktop RAM is not a fleet cost, and no Bitwarden measurement exists. The only "
                   "numbers on the table are third-party and N=1: one macOS comparison put a Tauri "
                   "app at ~172 MB against ~409 MB for Electron after six windows, written by a "
                   "Tauri user.",
                   "桌面端内存不构成机队成本，而且 Bitwarden 自己没有测量。桌面上唯一的数字是第三方的、N=1 的："
                   "一份 macOS 对比里，开六个窗口后 Tauri 应用约 172 MB，Electron 约 409 MB，作者本人用 Tauri。"),
         "source": "https://www.gethopp.app/blog/tauri-vs-electron (2025, N=1, author uses Tauri)",
         "regime": "third-party macOS single-machine comparison of other apps",
         "caveat": "On Windows, WebView2 is Chromium, so the same comparison collapses once shared pages are counted. Neither number was measured on Bitwarden."},
        {"id": "D5", "name": ("Startup shape", "启动形态"),
         "label": "N/A", "css": "neutral",
         "state": "N/A", "strength": "MODERATE", "option_ids": [],
         "claim": ("The app registers autostart and lives in the tray. It boots once per login and "
                   "stays resident, so startup cost is amortized over a work day rather than paid per "
                   "invocation.",
                   "这个应用注册开机自启并常驻托盘。每次登录启动一次然后一直在，启动开销摊在一整天里，不是"
                   "每次调用都付。"),
         "source": "apps/desktop/desktop_native/napi/src/autostart.rs · src/main/tray.main.ts",
         "regime": "n/a", "caveat": ""},
        {"id": "D6", "name": ("Safety & correctness", "安全与正确性"),
         "label": "SUPPORTS · rust-secure-memory", "css": "rust",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-secure-memory"],
         "claim": ("One exposure survives the current design. The main process reads the biometric "
                   "key out of the Keychain and sends it over IPC, where the renderer rebuilds it as "
                   "a SymmetricCryptoKey. A decrypted user key therefore lives in the V8 heap while "
                   "the vault is unlocked.",
                   "现在这套设计下还剩一处暴露。主进程从 Keychain 读出生物识别密钥，通过 IPC 发出去，渲染进程"
                   "把它重建成 SymmetricCryptoKey。所以金库解锁期间，解密后的 user key 就在 V8 堆里。"),
         "source": "apps/desktop/src/key-management/biometrics/renderer-biometrics.service.ts:87 · os-biometrics-mac.service.ts:50 · published audits indexed at bitwarden.com/help/is-bitwarden-audited/",
         "regime": "structural, on the unlock path",
         "caveat": "Two mitigations already ship: contextIsolation with nodeIntegration off, and a process reload on lock that discards the renderer's memory. The first of those was itself an audit fix — Cure53's 2023 desktop assessment raised BWN-08-013 and the Critical BWN-08-014, an RCE chain that existed because the main BrowserWindow ran with nodeIntegration on and contextIsolation off. Rust does not make this class go away by itself either: Cure53's 2024 SDK finding BWN-11-006 was a master password left in freed memory, fixed by adding a zeroing global allocator. secure_memory exists for exactly this problem and has no macOS backend beyond mlock."},
        {"id": "D7", "name": ("Concurrency & invariants", "并发与不变量"),
         "label": "NEUTRAL · all", "css": "neutral",
         "state": "NEUTRAL", "strength": "MODERATE", "option_ids": [],
         "claim": ("Process isolation is already the concurrency model. Main, renderer and preload are "
                   "separate OS processes with an explicit IPC contract, and the Rust side runs its "
                   "own tokio work behind napi. No race incident appears in the repository.",
                   "进程隔离本来就是这里的并发模型。主进程、渲染进程、preload 是三个独立 OS 进程，之间有明确的 "
                   "IPC 契约，Rust 那边在 napi 后面跑自己的 tokio。仓库里没有竞态事故的记录。"),
         "source": "apps/desktop/tsconfig.main.json · tsconfig.renderer.json · tsconfig.preload.json",
         "regime": "shipped build configuration",
         "caveat": "The IPC contract is hand-written and therefore hand-checked; that is a review burden in any implementation language."},
        {"id": "D8", "name": ("Distribution", "分发"),
         "label": "DISFAVORS · rust-native-gui, tauri-shell", "css": "rust",
         "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["rust-native-gui", "tauri-shell"],
         "claim": ("The distribution matrix is already large and already met. build.js maps 7 Rust "
                   "target triples; electron-builder produces a universal macOS build, a sandboxed "
                   "Mac App Store package, snap, flatpak and three Windows architectures. A new UI "
                   "stack re-earns every one of those.",
                   "分发矩阵已经很大，而且已经满足了。build.js 映射 7 个 Rust 目标三元组；electron-builder 产出 "
                   "macOS universal 包、沙箱化的 Mac App Store 包、snap、flatpak 和三种 Windows 架构。换一套 "
                   "UI 栈，这些要重新挣一遍。"),
         "source": "apps/desktop/desktop_native/build.js:9-15 · apps/desktop/package.json pack:* scripts",
         "regime": "static build configuration at this commit",
         "caveat": "A 2025 survey of 43 Rust GUI crates found the overwhelming majority not production-ready on accessibility and IME; that cost lands in D11, not here."},
        {"id": "D9", "name": ("Ecosystem & alternatives", "生态与替代品"),
         "label": "SUPPORTS · stay-split", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["stay-split"],
         "claim": ("The crates that make this work are ordinary, maintained ecosystem pieces: "
                   "security-framework for Keychain, napi 3.x for the addon, uniffi for Swift, "
                   "interprocess for IPC, ssh-key and rsa for the agent. All 13 crates pin exact "
                   "versions and the workspace denies unwrap_used.",
                   "让这套东西成立的 crate 都是普通的、有人维护的生态件：Keychain 用 security-framework，插件用 "
                   "napi 3.x，Swift 用 uniffi，IPC 用 interprocess，agent 用 ssh-key 和 rsa。13 个 crate 全部"
                   "锁死精确版本，workspace 层面 deny unwrap_used。"),
         "source": "apps/desktop/desktop_native/Cargo.toml · clippy.toml · deny.toml",
         "regime": "manifest inventory at this commit",
         "caveat": "The Rust GUI half of the ecosystem is a different story and is priced against the rewrite options at D8 and D11."},
        {"id": "D10", "name": ("Boundary & compatibility", "边界与兼容"),
         "label": "SUPPORTS · stay-split, rust-secure-memory", "css": "rust",
         "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["stay-split", "rust-secure-memory"],
         "claim": ("The seam is small and coarse. 491 generated lines of .d.ts, 15 namespaces, 38 "
                   "exported functions, 27 exported types. Calls happen per user action: unlock, read "
                   "the clipboard, sign an SSH request. Nothing fires per item or per frame.",
                   "接缝小而粗。生成的 .d.ts 491 行，15 个命名空间，38 个导出函数，27 个导出类型。调用按"
                   "用户动作发生：解锁、读剪贴板、签一次 SSH 请求。没有任何调用是按条目或按帧触发的。"),
         "source": "apps/desktop/desktop_native/napi/index.d.ts · 491 lines · 38 `export function` declarations",
         "regime": "static interface inventory at this commit",
         "caveat": "The seam is not free, and a published audit priced one edge of it. IOActive 2024 finding BITSR24-02 sits in desktop_native/core/src/ssh_agent/unix.rs, and Bitwarden's own resolution note reads: 'If the SSH agent spawned thread encounters errors there is no way for the TypeScript implementation to see this error.' A second boundary is excluded from the count above: uniffi generates Swift bindings for the macOS credential-provider extension from the same autofill_provider crate."},
        {"id": "D11", "name": ("Delivery economics", "交付经济性"),
         "label": "DISFAVORS · rust-native-gui", "css": "rust",
         "state": "DISFAVORS", "strength": "STRONG", "option_ids": ["rust-native-gui"],
         "claim": ("The desktop app is 32,549 lines of its own TypeScript sitting on 247,757 non-spec "
                   "lines in libs/. That shared layer is what the browser extension, web vault and CLI "
                   "also import — 874 import statements from @bitwarden/common in the desktop app "
                   "alone. A UI rewrite forks it or reimplements it.",
                   "桌面端自有 TypeScript 32,549 行，坐在 libs/ 的 247,757 行非测试代码上。这层共享代码同时"
                   "被浏览器扩展、Web 端和 CLI import——单是桌面端就有 874 条 @bitwarden/common 的 import。"
                   "界面重写要么分叉它，要么重新实现它。"),
         "source": "apps/desktop/src 32,549 lines / 238 files · libs/ 247,757 non-spec lines / 2,757 files",
         "regime": "matched .ts basis, spec files excluded from the libs figure",
         "caveat": "The 780,391-line whole-repo TypeScript total is not the rewrite cost and is not used as one here; it includes three other clients."},
        {"id": "D12", "name": ("Counterfactual", "对照方案"),
         "label": "SUPPORTS · swift-native-mac", "css": "current",
         "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["swift-native-mac"],
         "claim": ("If the complaint is that the app does not feel like a Mac app, the answer in this "
                   "repository is Swift, not Rust. autofill_provider already builds a "
                   "BitwardenMacosProviderFFI.xcframework through uniffi, and 569 lines of Swift "
                   "already ship as the credential-provider extension.",
                   "如果抱怨的是「不像 Mac 应用」，这个仓库里给出的答案是 Swift，不是 Rust。autofill_provider "
                   "已经通过 uniffi 产出 BitwardenMacosProviderFFI.xcframework，569 行 Swift 已经作为凭据"
                   "提供方扩展在发布。"),
         "source": "apps/desktop/desktop_native/autofill_provider/build.sh · apps/desktop/macos/autofill-extension/CredentialProviderViewController.swift (569 lines)",
         "regime": "shipped build script and source at this commit",
         "caveat": "A second Mac UI means permanent feature-parity work; this is retained as the counterfactual the native claim has to beat, not recommended."},
    ],

    "findings": [
        ("current",
         ("The whole Rust boundary is 38 functions", "整个 Rust 边界是 38 个函数"),
         ("napi/index.d.ts is generated, 491 lines long, and declares 15 namespaces with 38 exported "
          "functions and 27 exported types. That is the whole contract. Fifteen TypeScript files call "
          "into it at runtime, every one in the Electron main process. Compare a boundary you cannot "
          "walk away from: Redis exports 399 module ABI entry points.",
          "napi/index.d.ts 是生成的，491 行，声明 15 个命名空间、38 个导出函数、27 个导出类型。契约就这么多。"
          "运行时调它的有 15 个 TypeScript 文件，全在 Electron 主进程。对比一个走不掉的边界：Redis 导出 399 "
          "个模块 ABI 入口点。"),
         "apps/desktop/desktop_native/napi/index.d.ts · 491 lines · 38 `export function`"),
        ("unknown",
         ("The decrypted user key does reach the renderer", "解密后的 user key 确实会进渲染进程"),
         ("On macOS the biometric key is stored in the Keychain as base64, read back by the Rust "
          "passwords namespace, and sent over IPC. renderer-biometrics.service.ts rebuilds it: "
          "\"Objects received over IPC lose their prototype, so they must be recreated.\" So a "
          "decrypted user key sits in V8 while the vault is unlocked. Two mitigations ship. "
          "contextIsolation is on with nodeIntegration off, and locking triggers a process reload "
          "that throws the renderer's memory away.",
          "在 macOS 上，生物识别密钥以 base64 存进 Keychain，由 Rust 的 passwords 命名空间读回来，然后经 IPC "
          "发出去。renderer-biometrics.service.ts 把它重建："
          "\"Objects received over IPC lose their prototype, so they must be recreated.\" "
          "所以金库解锁期间，解密后的 user key 就待在 V8 里。缓解手段有两项，都已经在发。contextIsolation 开着、"
          "nodeIntegration 关着；锁定时会做一次 process reload，把渲染进程内存扔掉。"),
         "apps/desktop/src/key-management/biometrics/renderer-biometrics.service.ts:87,91-92"),
        ("current",
         ("The vault crypto is already Rust", "金库加解密已经是 Rust"),
         ("encrypt.service.implementation.ts does not implement AES. It calls "
          "PureCrypto.symmetric_decrypt_string from @bitwarden/sdk-internal, which is Rust compiled "
          "to WASM — the sdk-internal repository is 7.27 MB of Rust against 65 KB of TypeScript by "
          "GitHub's own byte count. 285 TypeScript files import it. desktop_native pins the same "
          "bitwarden-crypto crate natively.",
          "encrypt.service.implementation.ts 里没有 AES 实现。它调 @bitwarden/sdk-internal 的 "
          "PureCrypto.symmetric_decrypt_string，那是 Rust 编成的 WASM——按 GitHub 自己的字节统计，"
          "sdk-internal 仓库是 7.27 MB Rust 对 65 KB TypeScript。285 个 TypeScript 文件 import 它。"
          "desktop_native 在原生侧锁的是同一个 bitwarden-crypto crate。"),
         "libs/common/src/key-management/crypto/services/encrypt.service.implementation.ts:49"),
        ("current",
         ("On a Mac, the Rust module is thinner than on Windows", "在 Mac 上，Rust 模块比 Windows 上薄"),
         ("7,851 of the 28,301 Rust lines are gated out of a macOS build by a crate-level cfg: "
          "win_webauthn (6,086), windows_plugin_authenticator (1,717) and process_isolation (48). The "
          "biometric crate has windows.rs and linux.rs. There is no macos.rs. secure_memory carries "
          "DPAPI, keyctl and memfd_secret backends; on macOS it falls back to mlock, which its own "
          "doc comment calls weaker. Touch ID comes from Electron's systemPreferences, not from Rust.",
          "28,301 行 Rust 里有 7,851 行被 crate 级 cfg 挡在 macOS 构建之外：win_webauthn（6,086）、"
          "windows_plugin_authenticator（1,717）、process_isolation（48）。biometric crate 有 windows.rs 和 "
          "linux.rs。没有 macos.rs。secure_memory 带 DPAPI、keyctl、memfd_secret 三种后端；在 macOS 上退回 "
          "mlock，它自己的文档注释说这个更弱。Touch ID 来自 Electron 的 systemPreferences，不是 Rust。"),
         "win_webauthn/src/lib.rs:7 · secure_memory/src/secure_key/mlock.rs:8-9 · os-biometrics-mac.service.ts:37"),
        ("current",
         ("Rust arrived in 2022 as a keytar replacement", "Rust 是 2022 年作为 keytar 替代品进来的"),
         ("bitwarden/desktop PR #1379, merged 2022-04-05: +1,806 / -336 across 37 files. Its own "
          "objective paragraph says npm modules and Electron lacked functionality, and that the "
          "choice was between C++ and Rust. It shipped \"a drop-in replacement of the keytar module "
          "rewritten in rust\". The repository was created in 2016. Four years of Electron came "
          "first, then one module.",
          "bitwarden/desktop PR #1379，2022-04-05 合并：37 个文件，+1,806 / -336。它自己的 objective 段落写"
          "着 npm 模块和 Electron 缺功能，选择是在 C++ 和 Rust 之间。它交付的是 \"a drop-in replacement of "
          "the keytar module rewritten in rust\"。仓库 2016 年建的。先有四年 Electron，然后才有一个模块。"),
         "GitHub REST API · repos/bitwarden/desktop/pulls/1379 · merged 2022-04-05"),
    ],

    "buys": [
        (("OS APIs an Electron app cannot reach", "Electron 拿不到的 OS API"),
         ("Keychain through security-framework, an SSH agent socket, PT_DENY_ATTACH process "
          "hardening, a Windows passkey plugin. JavaScript cannot reach any of it. Speed was never "
          "the constraint.",
          "通过 security-framework 访问 Keychain、SSH agent socket、PT_DENY_ATTACH 进程加固、Windows "
          "passkey 插件。JavaScript 一个都拿不到。约束从来不是速度。")),
        (("One implementation for three hosts", "一份实现，三个宿主"),
         ("autofill_provider compiles to a Node addon and to a staticlib that Swift links through "
          "uniffi. bitwarden-crypto serves desktop_native natively and the TypeScript as WASM. That "
          "sharing is the Rust argument.",
          "autofill_provider 既编成 Node 插件，也编成 Swift 通过 uniffi 链接的 staticlib。bitwarden-crypto "
          "在原生侧供 desktop_native，在 TypeScript 侧以 WASM 供上层。这种共享就是 Rust 的理由。")),
        (("A place to put the next hardening step", "下一步加固有地方放"),
         ("secure_memory already holds keys outside ordinary heap on Windows and Linux. macOS is the "
          "gap. If the user key has to leave V8, that crate is where the work goes.",
          "secure_memory 在 Windows 和 Linux 上已经把密钥放在普通堆之外。缺的是 macOS。如果 user key 必须"
          "离开 V8，活儿就落在这个 crate 上。")),
    ],
    "nobuys": [
        (("A vault whose plaintext never enters a JS heap", "一个明文永不进 JS 堆的金库"),
         ("PureCrypto.symmetric_decrypt_string returns a JavaScript string, and the biometric user "
          "key is rebuilt in the renderer. Rewriting the UI moves that heap. It does not remove it. "
          "Rust's own heap needed help here too — Cure53's 2024 SDK audit found the master password "
          "left in freed memory, fixed by adding a zeroing allocator.",
          "PureCrypto.symmetric_decrypt_string 返回的是 JavaScript 字符串，生物识别的 user key 在渲染进程"
          "里被重建。重写界面只是把这个堆搬个地方。它没有拿掉那个堆。Rust 自己的堆也一样要人管——Cure53 "
          "2024 年对 SDK 的审计发现主密码留在了已释放的内存里，修法是加一个清零的全局分配器。")),
        (("A native Mac feel", "原生 Mac 的手感"),
         ("that is a UI-framework question. The repository's own answer to it is Swift through "
          "uniffi, already building an xcframework today.",
          "那是 UI 框架的问题。这个仓库自己的答案是通过 uniffi 走 Swift，今天就已经在产出 xcframework。")),
        (("Escape from Chromium", "从 Chromium 里脱身"),
         ("swapping Electron for a system webview trades one engine you can pin for three you "
          "cannot. On Windows, WebView2 is Chromium regardless.",
          "把 Electron 换成系统 webview，是拿一个你能锁版本的引擎去换三个你锁不了的。而在 Windows 上，"
          "WebView2 本来就是 Chromium。")),
    ],

    "precedents": [
        {"name": "AgileBits · 1Password 8", "outcome": "SPLIT STACK",
         "body": ("Closed source, so nothing here was inspected. AgileBits wrote 1Password 8's "
                  "shared backend in Rust and wrapped it in Electron on macOS, Windows and Linux. "
                  "Their stated driver was organisational: four client implementations of the same "
                  "server APIs, four teams, four sets of bugs. One matched Activity Monitor "
                  "comparison put the Rust core process below the app it replaced, 83.2 MB against "
                  "109.7 MB. The whole app came out at 326.2 MB across seven processes against "
                  "134.3 MB across three.",
                  "闭源，这里没有检视过任何东西。AgileBits 把 1Password 8 的共享后端写成 Rust，在 macOS、"
                  "Windows、Linux 上用 Electron 包起来。他们自述的动因是组织层面的：同一套服务端 API 有四份"
                  "客户端实现、四个团队、四套 bug。有一份对齐条件的 Activity Monitor 对比显示，Rust 核心进程"
                  "比它取代的那个应用还省，83.2 MB 对 109.7 MB。整个应用则是七个进程 326.2 MB，对三个进程 "
                  "134.3 MB。"),
         "match": ("the same Rust-core plus Electron-UI shape, the same product category, the same "
                   "Mac audience, and the same shared-core driver Bitwarden's SDK serves",
                   "同样是 Rust 内核加 Electron 界面的形状，同一个产品品类，同一批 Mac 用户，"
                   "以及和 Bitwarden 的 SDK 一样的「共享内核」动因"),
         "mismatch": ("the direction is opposite. 1Password moved a Mac app off Apple's own UI "
                      "toolkit, by their own description of their history; Bitwarden has been "
                      "Electron since 2016 and added Rust underneath it",
                      "方向是反的。按 1Password 自己对过往的描述，他们是把一个 Mac 应用从 Apple 自家 UI "
                      "工具包上挪走；Bitwarden 自 2016 年起就是 Electron，是在下面加了 Rust"),
         "regime": "first-party retrospective (Aug 2021) plus one user's per-process Activity Monitor comparison on macOS 11 with an empty vault, N=1; 1Password staff logged it internally and did not dispute the figures, and published no counter-measurement",
         "source_label": "first-party blog · plus an N=1 user measurement on the vendor forum",
         "url": "https://1password.com/blog/1password-8-the-story-so-far"},
        {"name": "Microsoft · VS Code", "outcome": "STAYED",
         "body": ("The same architecture, tested twice. A native C++ text buffer was tried and then "
                  "reverted, because converting strings between native memory and V8 ate the gain. "
                  "Their own summary: \"TL;DR: We tried. It didn't work out for us\". ripgrep, a Rust "
                  "binary, has powered search since 2017. It runs as a subprocess and hands back "
                  "bulk results.",
                  "同一套架构，被测了两次。原生 C++ 文本缓冲试过，后来回退了，因为在原生内存和 V8 之间转"
                  "字符串把收益吃掉了。他们自己的总结是：\"TL;DR: We tried. It didn't work out for us\"。"
                  "而 Rust 写的 ripgrep 从 2017 年起就在驱动搜索。它作为子进程跑，一次交回一批结果。"),
         "match": ("an Electron product that keeps native code only at coarse seams, which is the "
                   "shape Bitwarden's 38-function napi boundary already has",
                   "一个 Electron 产品，只在粗粒度接缝上放原生代码；Bitwarden 那 38 个函数的 napi 边界就是"
                   "这个形状"),
         "mismatch": ("an editor with no vault, no OS keychain requirement and no credential-provider "
                      "extension",
                      "那是编辑器，没有金库，不需要 OS keychain，也没有凭据提供方扩展"),
         "regime": "first-party engineering blog; no controlled benchmark published for the buffer work",
         "source_label": "first-party · engineering blog",
         "url": "https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation"},
        {"name": "Zed · GPUI", "outcome": "SHIPPED",
         "body": ("A Rust desktop app that really is fast: 120fps UI, sub-10ms typing latency by the "
                  "team's own account. The cost is in the same sentence. No existing Rust GUI "
                  "framework cleared the bar, so they wrote GPUI, a game-engine-style GPU scene "
                  "graph, before they could write the editor.",
                  "一个确实快的 Rust 桌面应用：团队自述 120fps 界面、打字延迟低于 10ms。代价就在同一句话里。"
                  "当时没有现成的 Rust GUI 框架够用，所以他们先写了 GPUI——一个游戏引擎式的 GPU 场景图——"
                  "然后才写编辑器。"),
         "match": ("proof that a native Rust desktop UI is achievable, which is the strongest version "
                   "of the rewrite proposal",
                   "证明原生 Rust 桌面界面做得到，这是重写提案最强的版本"),
         "mismatch": ("greenfield, not a migration; no shared library serving three other clients; "
                      "the numbers are unaudited first-party",
                      "那是全新开发，不是迁移；没有一层要同时服务另外三个客户端的共享库；数字是未经审计的"
                      "第一方数据"),
         "regime": "first-party claims plus one unaudited third-party comparison against VS Code",
         "source_label": "first-party · engineering blog",
         "url": "https://zed.dev/blog/videogame"},
        {"name": "Tauri on Linux", "outcome": "REVERTED",
         "body": ("The obvious way to put Rust in charge of a desktop app is a Rust shell over the "
                  "system webview. Tauri's own maintainers wrote that they \"can't fully recommend "
                  "Tauri for Linux right now\" and that WebKitGTK is \"getting worse each release\". "
                  "One application measured 40fps on WebKitGTK and 240fps after converting to "
                  "Electron. On Windows, WebView2 is Chromium anyway.",
                  "让 Rust 主管一个桌面应用，最直接的路子是 Rust 外壳套系统 webview。Tauri 自己的维护者写过"
                  "他们 \"can't fully recommend Tauri for Linux right now\"，以及 WebKitGTK "
                  "\"getting worse each release\"。有一个应用实测在 WebKitGTK 上 40fps，转成 Electron 后 "
                  "240fps。而在 Windows 上，WebView2 本来就是 Chromium。"),
         "match": ("the exact option a vault would consider first, and Bitwarden ships to macOS, "
                   "Windows, snap and flatpak — all three engines",
                   "金库最先会考虑的就是这个方案，而 Bitwarden 要发 macOS、Windows、snap 和 flatpak——"
                   "三个引擎全都碰上"),
         "mismatch": ("the fps figure is one app on one machine, and Tauri's macOS story is better "
                      "than its Linux one",
                      "那个 fps 数字是一台机器上的一个应用，而且 Tauri 在 macOS 上的表现好于 Linux"),
         "regime": "maintainer statements plus a single-application frame-rate report",
         "source_label": "first-party maintainers · issue tracker",
         "url": "https://github.com/tauri-apps/tauri/discussions/8524"},
        {"name": "Amazon · Prime Video living-room UI", "outcome": "EXTRACT SHIPPED",
         "body": ("37K lines of Rust went under a React UI across more than 8,000 device types. The "
                  "WASM VM added up to 7.5MB and saved about 30MB of JS heap. The business logic "
                  "stayed in JavaScript. The split held because the seam between rendering core and "
                  "UI is coarse.",
                  "37K 行 Rust 塞到 React 界面底下，覆盖 8,000 多种设备型号。WASM 虚拟机最多增加 7.5MB，"
                  "省下大约 30MB 的 JS 堆。业务逻辑留在 JavaScript。这套拆分站得住，是因为渲染内核和界面"
                  "之间的接缝是粗的。"),
         "match": ("a shipped split-stack app where Rust owns the layer that needs it and the UI "
                   "layer is left alone",
                   "一个已经发布的分层混合应用：Rust 拿走真正需要它的那层，界面层不动"),
         "mismatch": ("a memory-constrained TV client with a real per-frame budget; a desktop vault "
                      "has neither",
                      "那是内存受限的电视客户端，有实打实的每帧预算；桌面金库两样都没有"),
         "regime": "first-party engineering post; footprint figures stated without a harness",
         "source_label": "first-party · engineering blog",
         "url": "https://www.amazon.science/blog/how-prime-video-updates-its-app-for-more-than-8-000-device-types"},
    ],

    "path": [
        {"title": ("Decide whether the user key may sit in V8", "先定 user key 能不能待在 V8 里"),
         "body": ("Bitwarden's security team writes down one sentence: is a decrypted user key in the "
                  "renderer's V8 heap acceptable while the vault is unlocked, given contextIsolation "
                  "and the process reload on lock. If the answer is yes, this report's verdict stands "
                  "and nothing moves. If it is no, the next step is funded and the scope becomes "
                  "EXTRACT. No code changes here.",
                  "Bitwarden 安全团队写下一句话：在有 contextIsolation 和锁定时 process reload 的前提下，"
                  "金库解锁期间让解密后的 user key 待在渲染进程 V8 堆里，能不能接受。答案是能，本报告的结论"
                  "就成立，什么都不动。答案是不能，下一步就有预算，范围变成 EXTRACT。这一步不改代码。"),
         "owner": "Bitwarden security team",
         "cost_range": ("1 week", "1 周"),
         "artifact": "a written threat-model decision on whether a decrypted user key may live in the renderer's V8 heap while unlocked",
         "acceptance": "the decision names the mitigations it relies on and the residual risk it accepts",
         "stop": "if the answer is yes, stop — the current split is the verdict and no work follows",
         "rollback": "documentation only; no code changes"},
        {"title": ("Give secure_memory a macOS backend", "给 secure_memory 补一个 macOS 后端"),
         "body": ("Only if step 1 said no. The desktop platform team adds a macOS backend to "
                  "secure_memory stronger than the current mlock fallback, then moves the biometric "
                  "unlock path behind it so the key handle crosses IPC instead of the key. Ship it "
                  "behind a feature flag and keep the mlock path live. If the platform cannot beat "
                  "mlock on macOS, say so in writing and stop — the answer is then a documented "
                  "residual risk, not a rewrite.",
                  "只有第 1 步答「不能」才做。桌面平台团队给 secure_memory 加一个比现在 mlock 兜底更强的 "
                  "macOS 后端，然后把生物识别解锁路径搬到它后面，让跨 IPC 传的是 key handle 而不是 key。"
                  "用 feature flag 上线，mlock 那条路留着。如果这个平台上确实赢不过 mlock，就写下来然后停——"
                  "结论是一条记录在案的残余风险，不是一次重写。"),
         "owner": "desktop platform team",
         "cost_range": ("4–8 weeks", "4–8 周"),
         "artifact": "a macOS backend for secure_memory plus the biometric unlock path moved behind it, behind a feature flag",
         "acceptance": "the renderer receives a key handle rather than key material, and the existing mlock path still passes its tests",
         "stop": "stop and document the residual risk if no macOS primitive beats mlock",
         "rollback": "clear the feature flag; the mlock path is untouched"},
        {"title": ("Publish a profile before any UI proposal", "任何界面提案之前，先出 profile"),
         "body": ("Whoever proposes replacing the UI publishes the measurement first. State the vault "
                  "size and the interaction, then split wall-clock into Chromium compositing, Angular "
                  "change detection, WASM crypto, IPC and network sync. The five shares have to sum "
                  "to the wall-clock on a harness someone else can re-run. If Angular is not a large "
                  "share, the performance argument is over.",
                  "提出换界面的人先把测量发出来。写清金库规模和具体交互，再把墙钟时间拆成 Chromium 合成、"
                  "Angular 变更检测、WASM 加解密、IPC、网络同步五块。五块之和要对得上墙钟，测量脚手架要能"
                  "被别人复跑。如果 Angular 占不了多少，性能这条论证就到此为止。"),
         "owner": "whoever proposes the UI rewrite",
         "cost_range": ("2 weeks", "2 周"),
         "artifact": "an end-to-end profile at a stated vault size splitting Chromium compositing, Angular change detection, WASM crypto, IPC and network sync",
         "acceptance": "the five shares sum to measured wall-clock and a third party can re-run the harness",
         "stop": "stop the performance track if Angular is not a large share of the time",
         "rollback": "measurement only; no code changes"},
        {"title": ("Cost the Swift Mac client before calling it a Rust question",
                   "把 Swift Mac 客户端算完价，再说这是不是 Rust 的问题"),
         "body": ("If the driver is that the app should feel like a Mac app, product and the Mac "
                  "engineers price a Swift client on the existing Rust core. uniffi already produces "
                  "the xcframework, so the estimate is about UI parity and ongoing feature lag, not "
                  "about bindings. The step passes when the estimate names which features the Swift "
                  "client would not have on day one. If nobody will fund two Mac UIs, that is the "
                  "answer and the Electron build continues.",
                  "如果动机是「应该像个 Mac 应用」，那就让产品和 Mac 工程师给「在现有 Rust 内核上做 Swift "
                  "客户端」算个价。uniffi 已经在产 xcframework，所以估算要算的是界面对齐和长期功能滞后，"
                  "不是 binding。通过标准是：估算里点名 Swift 客户端第一天会缺哪些功能。如果没人愿意养两套 "
                  "Mac 界面，那这就是答案，Electron 构建继续。"),
         "owner": "product plus the Mac engineers",
         "cost_range": ("2–3 weeks of estimation", "2–3 周做估算"),
         "artifact": "a costed plan for a Swift/AppKit Mac client on the existing Rust core, naming the day-one feature gap",
         "acceptance": "the plan states which features the Swift client lacks at launch and who owns parity afterwards",
         "stop": "if nobody funds two Mac UIs, stop — the Electron build continues unchanged",
         "rollback": "estimation only; the shipped client is untouched"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端影响面"), "state": "HIT",
         "claim": ("No profile of this app exists, so a UI-rewrite performance claim has no reach "
                   "argument available. The report records UNKNOWN and names the profile that would "
                   "settle it instead of estimating.",
                   "这个应用没有 profile，界面重写的性能主张就拿不出影响面的论证。报告记 UNKNOWN，并点名了"
                   "能了结它的那份 profile，没有拿估算去填。"),
         "evidence": "D2, D3, D4 UNKNOWN"},
        {"name": ("Attribution", "归因"), "state": "HIT",
         "claim": ("Two claims get bundled: that the app should be native, and that it should be "
                   "Rust. The repository separates them — uniffi and 569 lines of Swift already ship "
                   "the native path.",
                   "两个主张被捆在一起：应该原生，以及应该 Rust。仓库把它们分开了——uniffi 加 569 行 Swift "
                   "已经把原生那条路发出去了。"),
         "evidence": "D12 · autofill_provider/build.sh"},
        {"name": ("Safety transfer", "安全论证的搬运"), "state": "HIT",
         "claim": ("A Rust UI is often argued from memory safety. The vault crypto is already Rust "
                   "and the decrypted key still lands in the UI process's heap, so that argument does "
                   "not reach the UI language.",
                   "「Rust 界面」常常拿内存安全来论证。可金库加解密已经是 Rust，解密后的密钥照样落在界面进程"
                   "的堆里，所以这条论证够不到界面用什么语言。"),
         "evidence": "D6 · encrypt.service.implementation.ts:49"},
        {"name": ("Boundary and compatibility", "边界与兼容"), "state": "PASS",
         "claim": ("Both seams are named and counted: 38 napi functions in a 491-line .d.ts, plus the "
                   "uniffi Swift bindings. The second one is disclosed rather than folded into the "
                   "first count.",
                   "两条接缝都点了名、算了数：491 行 .d.ts 里 38 个 napi 函数，加上 uniffi 的 Swift binding。"
                   "第二条是单独披露的，没有并进第一条的计数。"),
         "evidence": "D10 · napi/index.d.ts · autofill_provider/uniffi.toml"},
        {"name": ("Delivery ownership", "交付归属"), "state": "PASS",
         "claim": ("The path requires a written threat-model decision before any Rust work, and a "
                   "costed Swift estimate before anyone calls the native complaint a Rust problem.",
                   "路径要求：任何 Rust 工作之前先有一份书面威胁模型决定；把「不够原生」说成 Rust 问题之前，"
                   "先有一份 Swift 的成本估算。"),
         "evidence": "reversible path steps 1 and 4"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "有人投入的对照方案"), "state": "PASS",
         "claim": ("Staying is not standing still. 13 Rust crates, a Rust SDK 285 TypeScript files "
                   "already import, and a Swift extension are all shipping work.",
                   "留下来不等于原地不动。13 个 Rust crate、一个已经被 285 个 TypeScript 文件 import 的 Rust "
                   "SDK、一个 Swift 扩展，全是已经在发的工作。"),
         "evidence": "D9 · 285 files importing @bitwarden/sdk-internal"},
        {"name": ("Cost of inaction", "不动的代价"), "state": "HIT",
         "claim": ("Doing nothing leaves a decrypted user key in the renderer's V8 heap while the "
                   "vault is unlocked. Electron defaults are not self-correcting either. Cure53 "
                   "rated the 2023 configuration a Critical RCE chain, and closing it took 13 pull "
                   "requests.",
                   "什么都不做，就意味着金库解锁期间解密后的 user key 一直在渲染进程 V8 堆里。Electron 的"
                   "默认值也不会自己变对。Cure53 把 2023 年那套配置定为 Critical 级的 RCE 链，收口用了 13 "
                   "个 PR。"),
         "evidence": "D6 · renderer-biometrics.service.ts:87 · Cure53 2023 BWN-08-013 and BWN-08-014"},
        {"name": ("Unsafe-surface omission", "遗漏的不安全面"), "state": "HIT",
         "claim": ("The Rust module is not the whole native surface. On macOS the app links 652 lines "
                   "of hand-written Objective-C and 166 of headers, and the Rust itself carries 177 "
                   "unsafe blocks, 88 of them in the Windows-only win_webauthn.",
                   "Rust 模块不等于全部原生面。macOS 上这个应用还链进 652 行手写 Objective-C 和 166 行头文件，"
                   "而 Rust 自己带 177 个 unsafe 块，其中 88 个在只编 Windows 的 win_webauthn 里。"),
         "evidence": "objc/src/native/*.m (13 files) · 177 `unsafe {` across 170 .rs files"},
        {"name": ("Native-advantage denial", "否认原生优势"), "state": "PASS",
         "claim": ("The report does not claim a native UI would feel the same. It records the UI "
                   "performance question as unmeasured and keeps the strongest native option, which "
                   "is Swift, in the comparison.",
                   "报告没有主张原生界面手感一样。它把界面性能这个问题记为未测量，并把最强的原生方案——"
                   "Swift——留在对比里。"),
         "evidence": "D2 UNKNOWN · swift-native-mac retained"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("Path step 2 carries an explicit stop: if no macOS primitive beats mlock, write "
                   "down the residual risk and stop rather than escalating to a rewrite.",
                   "路径第 2 步带明确的停止条件：如果 macOS 上没有比 mlock 更强的原语，就把残余风险写下来"
                   "然后停，不往重写上升级。"),
         "evidence": "reversible path step 2"},
    ],

    "gaps": [
        (("An end-to-end profile of the desktop app at a stated vault size",
          "一份端到端 profile，写明金库规模"),
         ("While it is missing, D2, D3 and D4 stay UNKNOWN and no performance claim about the UI can "
          "be authorized in any language.",
          "缺着的时候，D2、D3、D4 停在 UNKNOWN，关于界面的任何性能主张，用什么语言都授权不了。")),
        (("A written decision on whether a decrypted user key may live in the renderer's V8 heap",
          "一份书面决定：解密后的 user key 能不能待在渲染进程 V8 堆里"),
         ("This is the only trigger that changes the scope. Answer no and the verdict moves from STAY "
          "to EXTRACT, with secure_memory as the target.",
          "这是唯一能改变范围的触发条件。答「不能」，结论就从 STAY 变成 EXTRACT，目标是 secure_memory。")),
        (("Any first-party footprint or startup measurement for this app",
          "这个应用任何一方自己的内存占用或启动时间测量"),
         ("The only figures in circulation are third-party, N=1, and measured on other applications. "
          "They cannot price the Electron-replacement options.",
          "在流传的数字全是第三方、N=1，而且测的是别的应用。它们给不了「替换 Electron」这类方案定价。")),
    ],

    "assumptions": [
        "The shallow clone at the named commit represents the shipped tree; generated files such as napi/index.d.ts are counted as they are committed.",
        "The napi surface is read as one entry point per `export function` declaration in the generated index.d.ts, cross-checked against the 15 `pub mod` namespaces in napi/src/lib.rs.",
        "The crate count is the 13 entries in the `[workspace] members` array of apps/desktop/desktop_native/Cargo.toml, not the number of directories holding a Cargo.toml. A fourteenth, objc/, is a path dependency rather than a member; its 164 lines of Rust are still inside the 28,301 total.",
        "The proposal under assessment is the commonly stated one — rewrite the Bitwarden desktop app in Rust for a native feel and a tighter threat model — since no RFC exists.",
        "Line counts are raw `wc -l` on tracked files of one extension; comments and blank lines are included and no counting basis mixes extensions.",
    ],
    "objective": {
        "driver": "platform integration and secret handling",
        "requirement": "reach the macOS Keychain, Touch ID, an SSH agent socket and a credential-provider extension from an Electron app, and keep secret handling as tight as the platform allows, without forking the shared TypeScript the other three clients consume",
        "baseline": "28,301 lines of Rust in 13 crates behind 38 napi functions; 32,549 lines of the desktop app's own TypeScript on 247,757 shared lines; no published profile, footprint or startup measurement",
        "target": "OS APIs reachable and secret exposure minimised; no numeric UI performance target has been stated by anyone",
    },
    "repository": {
        "path": "https://github.com/bitwarden/clients",
        "commit": "f97b15bc4c8a0aa5236eb969e98a718c0330898b",
        "scope": "apps/desktop — the Electron/Angular desktop app plus apps/desktop/desktop_native; the browser extension, web vault and CLI in the same monorepo are context only",
        "sampling": "shallow clone; 8,362 tracked files enumerated; apps/desktop, apps/desktop/desktop_native, libs/ and the root manifests measured; the GitHub REST API supplied history because the clone is depth-1; no build, test or benchmark was run",
    },
    "user_supplied_facts": [],

    "method_title": (
        "bitwarden/clients at f97b15b · static read-only analysis · why-not-rust method 2.0",
        "bitwarden/clients @ f97b15b · 静态只读分析 · why-not-rust 方法 2.0",
    ),
    "method_body": (
        "Repository: github.com/bitwarden/clients at commit "
        "f97b15bc4c8a0aa5236eb969e98a718c0330898b, shallow clone, 8,362 tracked "
        "files. Scope: apps/desktop only. The other three clients in this monorepo are context, and "
        "the report states both counting bases wherever a share appears. Sampling: the whole tree "
        "holds 780,391 lines of TypeScript across 5,813 files and 28,301 lines of Rust across 170 "
        "files, and all 170 Rust files are under apps/desktop/desktop_native. The desktop app's own "
        "TypeScript is 32,549 lines across 238 files in apps/desktop/src, which is 4.2% of the "
        "monorepo's TypeScript. The Rust is 3.5% of the tree and 46% of the desktop app's own code "
        "on a matched .ts/.rs basis. That second figure is the one this assessment turns on. libs/ "
        "is 247,757 non-spec lines across 2,757 files. The .ts files were checked to be TypeScript "
        "and not Qt Linguist XML. The napi surface is 38 `export function` declarations and 27 "
        "exported types in a 491-line generated index.d.ts spanning 15 namespaces, matching the 15 "
        "`pub mod` declarations in napi/src/lib.rs. 15 non-spec TypeScript files import the module as "
        "a runtime value, and all 15 are main-process files. Unsafe accounting: 177 `unsafe {` "
        "blocks, 27 `unsafe fn`, 7 `unsafe extern` and 12 `unsafe impl` across the 170 .rs files, "
        "counted as occurrences and not deduplicated per file. 88 of those blocks are in "
        "win_webauthn, which carries `#![cfg(target_os = \"windows\")]`. Electron is pinned at "
        "41.7.2 in the root "
        "package.json and the desktop app version is 2026.7.1. Two history facts come from the "
        "GitHub REST API, because the clone is depth-1: PR #1379 merged 2022-04-05 in the archived "
        "bitwarden/desktop repository, and the sdk-internal language bytes. No build, test, "
        "benchmark or network call was run against the project. Objective: no RFC was supplied, so "
        "the assessment takes the commonly stated proposal. User-supplied facts: none. No Amdahl "
        "calculation appears, because no profile exists to give f a defensible value. The performance "
        "and footprint lenses are UNKNOWN, not refuted. G1 through G4 are graded against the Rust "
        "expansion under review, meaning replacement of the Angular UI or of the Electron shell. "
        "They are not graded against the OS-seam module that already ships. G1 passes: a decrypted user key does sit in the "
        "renderer's V8 heap while the vault is unlocked. G2 fails because a Rust UI relocates that "
        "heap instead of emptying it, and because the native-feel benefit is served by Swift here. "
        "G3 fails because a macOS backend for secure_memory meets the same target in weeks. G4 fails "
        "because the UI rests on a shared TypeScript layer that three other clients import, so there "
        "is no dual-run or rollback path. Nothing in this report argues against the Rust that is "
        "already there. Disclosure: this repository ships assistant-directed instruction files (.claude/, nine "
        "CLAUDE.md files, .mcp.json). They were read as data, contain ordinary coding conventions, "
        "and changed no number, gate or verdict here. Three published third-party audits are cited "
        "as documents and none was reproduced: Cure53 2023 on the Electron desktop app, Cure53 2024 "
        "on the SDK, and IOActive 2024, all indexed at bitwarden.com/help/is-bitwarden-audited/. "
        "1Password 8 is cited only from public sources and is labelled as such; it is closed-source "
        "and was not inspected, and its memory figures are one user's N=1 report. This is a "
        "structured "
        "decision protocol, not a statistical predictor.",
        "仓库：github.com/bitwarden/clients，commit f97b15bc4c8a0aa5236eb969e98a718c0330898b，"
        "shallow clone，8,362 个纳管文件。范围：只看 "
        "apps/desktop。同一个 monorepo 里另外三个客户端只作为背景，凡是出现占比，报告都把两套口径都写出来。"
        "采样：整棵树有 780,391 行 TypeScript（5,813 个文件）和 28,301 行 Rust（170 个文件），而这 170 个 "
        "Rust 文件全部在 apps/desktop/desktop_native 下。桌面端自有 TypeScript 是 apps/desktop/src 里 238 "
        "个文件、32,549 行，占整个 monorepo TypeScript 的 4.2%。Rust 占整棵树 3.5%，在对齐的 .ts/.rs 口径"
        "下占桌面端自有代码的 46%。这份评估靠的是后面这个数。libs/ 是 2,757 个文件、247,757 行非测试代码。"
        ".ts 文件已核对过是 TypeScript，不是 Qt Linguist XML。napi 面是一份 491 行生成 index.d.ts 里的 38 个 "
        "`export function` 和 27 个导出类型，跨 15 个命名空间，与 napi/src/lib.rs 里 15 个 `pub mod` 对得上；"
        "把该模块当运行时值 import 的非测试 TypeScript 文件有 15 个，全部是主进程文件。unsafe 口径：170 个 "
        ".rs 文件里 177 个 `unsafe {` 块、27 个 `unsafe fn`、7 个 `unsafe extern`、12 个 `unsafe impl`，按"
        "出现次数计，未按文件去重；其中 88 个块在 win_webauthn 里，那个 crate 带 "
        "`#![cfg(target_os = \"windows\")]`。Electron 在根 package.json 里锁 41.7.2，桌面端版本号 2026.7.1。"
        "有两条历史事实来自 GitHub REST API，因为 clone 是 depth-1：归档仓库 bitwarden/desktop 的 PR #1379 "
        "于 2022-04-05 合并，以及 sdk-internal 的语言字节数。没有对项目做过任何构建、测试、基准或网络调用。"
        "目标：没有人提供 RFC，所以按通常被提出的那个提案评估。用户提供的事实：无。本报告没有 Amdahl 计算："
        "不存在能给 f 一个站得住取值的 profile。性能和占用相关的几条是 UNKNOWN，不是被否证。G1 到 G4 评的"
        "是正在被审的那次 Rust 扩张——换掉 Angular 界面，或者换掉 Electron 外壳——不是评那个已经在发的 "
        "OS 接缝模块。G1 通过：金库解锁期间，解密后的 user key 确实待在渲染进程 V8 堆里。G2 失败，因为 Rust "
        "界面只是把这个堆搬走，不是清空它，而且「原生手感」这条在这里是 Swift 在兑现。G3 失败，因为给 "
        "secure_memory 补一个 macOS 后端，几周就能达到同一个目标。G4 失败，因为界面坐在一层被另外三个客户端"
        " import 的共享 TypeScript 上，没有双跑，也没有回滚路径。本报告没有任何一句是在反对已经存在的那些 "
        "Rust。披露：这个仓库带有面向 AI 助手的指令文件（.claude/、"
        "九个 CLAUDE.md、.mcp.json）。它们被当作数据读取，内容是普通的编码约定，没有改变这里的任何数字、"
        "证据门或结论。引用了三份公开的第三方审计，只作为文档引用，没有复现任何一份：Cure53 2023 针对 "
        "Electron 桌面端、Cure53 2024 针对 SDK、IOActive 2024，索引都在 "
        "bitwarden.com/help/is-bitwarden-audited/。1Password 8 只引用公开资料并明确标注来源；它是闭源的，"
        "没有被检视，其内存数字是某个用户的 N=1 报告。这是一套结构化决策流程，不是统计预测器。",
    ),
    "footer": (
        "public repository · static analysis at commit f97b15b · no build, benchmark or network call against the target",
        "公开仓库 · 在 commit f97b15b 上做静态分析 · 未对目标做构建、基准或网络调用",
    ),
}
