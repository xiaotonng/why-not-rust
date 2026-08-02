#!/usr/bin/env python3
"""Render the committed synthetic golden report.

The fixture is deliberately fictional: it exists to regression-test the template
and the renderer, not to describe any real project. It reuses the case renderer
in `examples/build_cases.py`, so the sample can never drift away from the markup
the published case reports use.

A few strings are bilingual pairs so the language-switch path is exercised; the
rest are English only, which is a legitimate state for a report and is worth
covering too.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

from build_cases import render as render_case  # noqa: E402

TARGET = "Reduce the synthetic 2 GB export from 3.8 s to ≤2.4 s."

LENSES = [
    {"id": "D1", "name": "Requirement & ownership", "label": "SUPPORTS · native options", "css": "neutral",
     "state": "SUPPORTS", "strength": "STRONG", "option_ids": ["wasm-adopt", "rust-extract", "go-sidecar"],
     "claim": "The synthetic CPU profile puts 62% of export wall-clock in the owned parser/diff kernel.",
     "source": "synthetic/export.cpuprofile · representative 2 GB fixture",
     "regime": "synthetic 2 GB export fixture",
     "caveat": "Illustrative synthetic data; do not transfer to a real repository."},
    {"id": "D2", "name": "End-to-end reach", "label": "SUPPORTS · rust-extract", "css": "rust",
     "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-extract"],
     "claim": "A 5× kernel with 3% boundary cost predicts 1.87× product speed. The target is 1.59×.",
     "source": "decision_math.py · f=.62, S=5, b=.03", "regime": "synthetic 2 GB export fixture",
     "caveat": "Illustrative synthetic data; do not transfer to a real repository."},
    {"id": "D3", "name": "Tail & runtime", "label": "NEUTRAL · all", "css": "neutral",
     "state": "NEUTRAL", "strength": "STRONG", "option_ids": [],
     "claim": "No GC-correlated p99 violation appears in the synthetic trace. GC is not part of this case.",
     "source": "synthetic/export-trace.json", "regime": "synthetic trace", "caveat": "Synthetic."},
    {"id": "D4", "name": "Fleet footprint", "label": "N/A", "css": "neutral",
     "state": "N/A", "strength": "MODERATE", "option_ids": [],
     "claim": "Single desktop instances create no fleet-density objective here.",
     "source": "synthetic deployment inventory", "regime": "n/a", "caveat": "Synthetic."},
    {"id": "D5", "name": "Startup shape", "label": "N/A", "css": "neutral",
     "state": "N/A", "strength": "STRONG", "option_ids": [],
     "claim": "Export begins after warm initialization, so startup sits outside the objective.",
     "source": "synthetic lifecycle trace", "regime": "n/a", "caveat": "Synthetic."},
    {"id": "D6", "name": "Safety & correctness", "label": "N/A", "css": "neutral",
     "state": "N/A", "strength": "STRONG", "option_ids": [],
     "claim": "The TypeScript app has no native or FFI surface. This proposal makes no safety claim.",
     "source": "synthetic package manifests", "regime": "n/a", "caveat": "Synthetic."},
    {"id": "D7", "name": "Concurrency & invariants", "label": "NEUTRAL · native options", "css": "neutral",
     "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["wasm-adopt", "rust-extract", "go-sidecar"],
     "claim": "Chunk parallelism is available in Go, in workers and in Rust. Nothing here is Rust-specific.",
     "source": "synthetic worker PoC", "regime": "synthetic", "caveat": "Synthetic."},
    {"id": "D8", "name": "Distribution", "label": "SUPPORTS · ts-opt", "css": "current",
     "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["ts-opt"],
     "claim": "The signed Electron packaging chain already meets every distribution requirement.",
     "source": "synthetic build config", "regime": "synthetic", "caveat": "Synthetic."},
    {"id": "D9", "name": "Ecosystem & alternatives", "label": "NEUTRAL · native options", "css": "neutral",
     "state": "NEUTRAL", "strength": "MODERATE", "option_ids": ["wasm-adopt", "rust-extract", "go-sidecar"],
     "claim": "Rust, Go and the existing WASM parser are all viable candidates.",
     "source": "synthetic dependency spike", "regime": "synthetic", "caveat": "Synthetic."},
    {"id": "D10", "name": "Boundary & compatibility", "label": "SUPPORTS · rust-extract", "css": "rust",
     "state": "SUPPORTS", "strength": "MODERATE", "option_ids": ["rust-extract"],
     "claim": "One immutable batch in, one result batch back. The measured boundary estimate is 3%.",
     "source": "synthetic boundary bench", "regime": "synthetic", "caveat": "Synthetic."},
    {"id": "D11", "name": "Delivery economics", "label": "DISFAVORS · rust-extract", "css": "rust",
     "state": "DISFAVORS", "strength": "WEAK", "option_ids": ["rust-extract"],
     "claim": "One Rust maintainer is a bus factor. The plan funds a second owner.",
     "source": "synthetic staffing plan", "regime": "synthetic", "caveat": "Synthetic."},
    {"id": "D12", "name": "Counterfactual", "label": "DISFAVORS · non-Rust options", "css": "current",
     "state": "DISFAVORS", "strength": "MODERATE", "option_ids": ["ts-opt", "wasm-adopt", "go-sidecar"],
     "claim": "Funded TypeScript, WASM and Go trials all land below 1.59× on the same fixture.",
     "source": "synthetic counterfactual benchmarks", "regime": "synthetic", "caveat": "Synthetic."},
]


def option(oid, name, note, tag, scope, impl, benefit, cost, time, compat, strength, disposition, reason):
    return {
        "id": oid, "name": name, "note": note, "scope_tag": tag, "scope": scope,
        "implementation": impl, "benefit_interval": benefit, "cost_cell": cost,
        "one_time_cost": cost, "recurring_cost": cost, "time_to_value": time,
        "compat_cell": compat, "compatibility": compat, "reversibility": compat,
        "evidence_strength": strength, "disposition": disposition, "reason": reason,
    }


CASE = {
    "slug": "sample-report",
    "lang": "en",
    "lang_default": "en",
    "project_name": "acme-desk",
    "project_desc": ("ILLUSTRATIVE SYNTHETIC EXAMPLE · no real repository was analyzed",
                     "示例用合成数据 · 未分析任何真实仓库"),
    "date": "2026-08-01",
    "archetype": ("Electron desktop · CPU export path", "Electron 桌面应用 · CPU 导出路径"),

    "scope_word": "EXTRACT",
    "auth": "APPROVE",
    "confidence": "MEDIUM",
    "robustness": "CONDITIONAL",
    "selected": "rust-extract",
    "scope_chip": ("export kernel only", "仅导出内核"),
    "scope_sub": ("isolate one measured export kernel", "只隔离一个已测量的导出内核"),

    "why": ("The synthetic profile puts 62% of export time in an owned parser/diff kernel. A coarse "
            "extraction clears the 1.59× target without touching the TypeScript application.",
            "合成 profile 显示 62% 的导出时间落在自有的 parser/diff 内核里。一次粗粒度抽取就能达到 "
            "1.59× 目标，不需要动 TypeScript 应用本身。"),
    "trigger": ("Conditional. Re-open if measured boundary cost goes above 7%, if parity drops below "
                "100%, or if the funded second owner disappears.",
                "有条件。若实测边界成本超过 7%、一致性低于 100%，或第二位维护者的预算消失，就重新评估。"),

    "gates": [
        {"id": "G1", "state": "PASS", "short": ("Requirement", "需求"), "name": "requirement",
         "hero_evidence": ("3.8 s baseline misses the 2.4 s export target.", "3.8 s 基线达不到 2.4 s 的导出目标。"),
         "evidence": "3.8 s baseline misses 2.4 s target"},
        {"id": "G2", "state": "PASS", "short": ("Causality", "因果"), "name": "rust-specific causality",
         "hero_evidence": ("62% owned CPU kernel; bounded 5× kernel result.", "62% 的 CPU 时间在自有内核；内核实测上限 5×。"),
         "evidence": "62% owned CPU kernel; 5x bounded kernel result"},
        {"id": "G3", "state": "PASS", "short": ("Economics", "经济性"), "name": "economics and smallest sufficient option",
         "hero_evidence": ("Funded TypeScript, WASM and Go trials all miss.", "已投入的 TypeScript、WASM、Go 试验都没达标。"),
         "evidence": "funded TypeScript, WASM, and Go trials miss the target"},
        {"id": "G4", "state": "PASS", "short": ("Delivery", "交付"), "name": "delivery and reversibility",
         "hero_evidence": ("Batch boundary, parity corpus, flag, rollback owner.", "批量边界、一致性语料、特性开关、回滚责任人。"),
         "evidence": "coarse boundary, feature flag, parity corpus, rollback"},
    ],

    "tiles": [
        (("Baseline → target", "基线 → 目标"), "3.8 → 2.4", ("s", "秒"),
         ("synthetic 2 GB export fixture", "合成 2 GB 导出语料")),
        (("Owned hot path", "自有热点占比"), "62", "%", ("synthetic CPU profile", "合成 CPU profile")),
        (("Predicted product gain", "预测端到端收益"), "1.87", "×", "f=.62 · S=5 · b=.03"),
        (("Physical ceiling", "物理天花板"), "2.44", "×", ("infinite kernel · same boundary", "内核无限快 · 同样的边界成本")),
        (("Pilot", "试点"), "2–3", ("weeks", "周"), ("range from a synthetic work breakdown", "来自合成工作量拆解")),
    ],

    "options_sub": ("Every option is measured against the same target: reduce the synthetic 2 GB export "
                    "from 3.8 s to 2.4 s or better.",
                    "所有方案对同一个目标：把合成 2 GB 导出从 3.8 s 降到 2.4 s 以内。"),
    "options": [
        option("ts-opt", ("TypeScript optimize", "优化 TypeScript"), ("retain · useful, not enough", "保留 · 有用但不够"),
               "STAY", "stay", "current", "1.25–1.40×", ("2–4 days; low recurring", "2–4 天；长期成本低"),
               ("days", "数天"), ("native · git revert", "原生 · git revert"), "MODERATE", "retain",
               "Does not meet 1.59x target alone"),
        option("wasm-adopt", ("Existing WASM parser", "现成的 WASM parser"), ("retain · measured below target", "保留 · 实测未达标"),
               "ADOPT", "adopt", "external", "1.38–1.52×", ("1–2 weeks; dependency", "1–2 周；引入依赖"),
               ("1 week", "1 周"), ("adapter flag · format adapter", "适配开关 · 格式适配层"), "MODERATE", "retain",
               "Same-fixture trial misses the target"),
        option("rust-extract", ("Rust kernel extraction", "抽取 Rust 内核"), ("recommended · smallest option that works", "推荐 · 最小的可行方案"),
               "EXTRACT", "extract", "rust", "1.70–1.90×", ("2–3 weeks; second owner", "2–3 周；需第二位维护者"),
               ("1 week pilot", "1 周试点"), ("batch API · feature flag", "批量 API · 特性开关"), "MODERATE", "selected",
               "Recommended smallest sufficient option"),
        option("go-sidecar", ("Go sidecar", "Go 边车进程"), ("retain · measured below target", "保留 · 实测未达标"),
               "EXTRACT", "extract", "non-rust-native", "1.44–1.55×", ("2–3 weeks; second stack", "2–3 周；多一套技术栈"),
               ("1 week pilot", "1 周试点"), ("process API · feature flag", "进程 API · 特性开关"), "MODERATE", "retain",
               "Same-fixture trial misses the target"),
        option("rust-full", ("Full Rust/Tauri app", "整体重写为 Rust/Tauri"), ("exclude · no extra export benefit", "排除 · 对导出没有额外收益"),
               "MIGRATE", "full", "rust", ("no extra export gain", "导出无额外收益"),
               ("9–14 months; full dual stack", "9–14 个月；双栈长期维护"), ("months", "数月"),
               ("whole UI · poor rollback", "整个 UI · 回滚困难"), "WEAK", "exclude",
               "Fails smallest-sufficient-option gate"),
    ],

    "amdahl": {"share": 0.62, "kernel_speedup": 5.0, "boundary": 0.03, "target": 1.59,
               "note": ("Synthetic inputs: f=.62, S=5, b=.03 against a 1.59x target.",
                        "合成输入：f=.62，S=5，b=.03，目标 1.59×。")},

    "lenses_sub": ("States are option-scoped evidence, not points to be added up.",
                   "每条状态都绑定具体方案，不是可以相加的分数。"),
    "na_note": ("N/A lenses: D4 fleet footprint, D5 startup and D6 safety do not bear on this synthetic "
                "performance objective.",
                "标记 N/A 的维度：D4 机群footprint、D5 启动、D6 安全，与这个合成性能目标无关。"),
    "lenses": LENSES,

    "findings": [
        ("rust", ("The kernel is big enough to matter", "内核足够大，值得动"),
         ("62% of export time sits in owned parse/diff work, and the 2.44× physical ceiling clears the "
          "1.59× target with room to spare.",
          "62% 的导出时间在自有的 parse/diff 上，2.44× 的物理天花板对 1.59× 的目标还有余量。"),
         "synthetic/export.cpuprofile"),
        ("current", ("In-stack work helps, and it is not enough", "栈内优化有效，但不够"),
         ("Buffer reuse and caching produce 1.25–1.40× on the same fixture. Fund them. Do not pretend "
          "they reach the target.",
          "缓冲复用和缓存在同一语料上能到 1.25–1.40×。该投就投，但别当成达标。"),
         "synthetic/ts-baseline.json"),
        ("unknown", ("Boundary cost controls the decision", "边界成本决定结论"),
         ("3% is a bounded synthetic bench, not a production measurement. Above 7% the lower benefit "
          "estimate stops clearing the target.",
          "3% 来自有界的合成基准，不是生产实测。超过 7%，收益区间下沿就够不着目标了。"),
         "synthetic/boundary-bench.json"),
        ("current", ("The UI is outside the requirement", "UI 不在需求范围内"),
         ("DOM rendering and Electron startup do not appear in export time. Replacing the shell adds "
          "cost and passes no new gate.",
          "DOM 渲染和 Electron 启动不出现在导出耗时里。换外壳只增加成本，过不了任何一道门。"),
         "synthetic/trace.json"),
    ],

    "buys": [
        (("Parser throughput", "parser 吞吐"),
         ("native batch processing can close the measured export gap", "原生批处理可以补上实测的导出差距")),
        (("Kernel-local invariants", "内核局部不变量"),
         ("ownership simplifies the extracted buffer lifecycle", "所有权模型让抽出来的缓冲区生命周期更简单")),
        (("A reversible native option", "一个可逆的原生方案"),
         ("the unchanged TypeScript API keeps rollback cheap", "TypeScript API 不变，回滚成本很低")),
    ],
    "nobuys": [
        (("Faster DOM or database work", "更快的 DOM 或数据库"),
         ("neither appears in the measured export kernel", "两者都不在实测的导出内核里")),
        (("Application memory safety", "应用层内存安全"),
         ("the TypeScript app has no unsafe native surface", "这个 TypeScript 应用没有不安全的原生面")),
        (("A reason to replace Electron", "换掉 Electron 的理由"),
         ("shell migration adds no export benefit", "换外壳对导出没有任何收益")),
    ],

    "precedents": [
        {"name": "pydantic-core", "outcome": "EXTRACT",
         "body": ("A Rust validation core kept the Python API and captured native value at a coarse seam.",
                  "Rust 验证内核保留了 Python API，在粗粒度接缝上拿到了原生收益。"),
         "match": ("scripting API over a hot pure kernel", "脚本语言 API 之下有一个纯计算热点内核"),
         "mismatch": ("different data model and workload", "数据模型和负载都不同"),
         "regime": "validation core under a Python API", "source_label": "first-party · vendor benchmark",
         "url": "https://pydantic.dev/articles/pydantic-v2"},
        {"name": "Prisma Rust-free", "outcome": "REVERSED",
         "body": ("Moving execution out of a chatty Rust boundary improved Prisma's own large-query benchmark.",
                  "把执行搬出高频的 Rust 边界之后，Prisma 自己的大查询基准反而更快了。"),
         "match": ("JS host plus boundary cost", "JS 宿主 + 边界成本"),
         "mismatch": ("ORM calls cross far more often", "ORM 调用的跨界频率高得多"),
         "regime": "internal 25k-row findMany benchmark", "source_label": "first-party · internal benchmark",
         "url": "https://www.prisma.io/blog/from-rust-to-typescript-a-new-chapter-for-prisma-orm"},
        {"name": "TypeScript native port", "outcome": "NON-RUST",
         "body": ("Go supplied native execution and shared-memory parallelism while preserving cyclic graph semantics.",
                  "Go 同时给了原生执行和共享内存并行，还保住了循环图语义。"),
         "match": ("a native alternative that is not Rust", "一个非 Rust 的原生候选"),
         "mismatch": ("a whole compiler port, not one kernel", "整个编译器移植，不是单个内核"),
         "regime": "compiler and language-service preview benchmarks", "source_label": "first-party · preview benchmark",
         "url": "https://devblogs.microsoft.com/typescript/typescript-native-port/"},
    ],

    "path": [
        {"title": ("Freeze the decision fixture", "先把判定语料冻住"),
         "body": ("The performance lead versions the 2 GB corpus and publishes a warm/cold protocol. Three "
                  "baseline runs inside ±3%, or the fixture is not stable enough to decide anything. If the "
                  "baseline stops missing 2.4 s, stop here.",
                  "性能负责人给 2 GB 语料定版本，并公布冷热两套测量协议。三次基线跑动要落在 ±3% 以内，否则这个语料"
                  "撑不起任何结论。如果基线已经不再错过 2.4 s，就到此为止。"),
         "owner": "performance lead", "cost_range": ("1 day", "1 天"),
         "artifact": "versioned 2 GB corpus, warm/cold protocol, and variance report",
         "acceptance": "three baseline runs within ±3%",
         "stop": "stop if the baseline no longer misses 2.4 s",
         "rollback": "discard the fixture commit; production is untouched"},
        {"title": ("Run the pilots on equal terms", "让试点在同一条件下跑"),
         "body": ("Two platform engineers build the Rust and Go candidates against the same batch API and the "
                  "same copies. A candidate passes at 1.59× end-to-end with 100% parity and boundary cost at "
                  "or under 7%. One week. If neither clears every threshold, both branches get deleted.",
                  "两名平台工程师用同一套批量 API、同样的拷贝方式做出 Rust 和 Go 候选。达标线是端到端 1.59×、"
                  "一致性 100%、边界成本不超过 7%。给一周。都过不了就把两个分支都删掉。"),
         "owner": "two platform engineers", "cost_range": ("1 week", "1 周"),
         "artifact": "Rust and Go candidates using the same batch API and copies",
         "acceptance": "≥1.59× end-to-end, 100% parity, and ≤7% boundary cost",
         "stop": "stop after one week if neither candidate clears every threshold",
         "rollback": "delete pilot branches and keep the TypeScript path"},
        {"title": ("Shadow the winner", "让胜出者先影子运行"),
         "body": ("The export team runs the selected kernel behind a flag that is off by default and logs the "
                  "diff. 100% fixture parity, no p95 regression. The first unexplained mismatch stops the "
                  "rollout.",
                  "导出团队把选中的内核放在默认关闭的开关后面，记录 diff。要求语料一致性 100%、p95 不退化。"
                  "出现第一个解释不了的差异就停。"),
         "owner": "export team", "cost_range": ("1 week", "1 周"),
         "artifact": "shadow diff log behind a disabled-by-default flag",
         "acceptance": "100% fixture parity and no p95 regression",
         "stop": "stop on the first unexplained mismatch",
         "rollback": "disable the flag and route all work to TypeScript"},
        {"title": ("Roll out with a kill switch", "带着急停开关上线"),
         "body": ("The on-call maintainer takes it to 5%, then 25%, then everyone, watching the error budget "
                  "for one release. The old path stays until that window closes.",
                  "值班维护者按 5% → 25% → 全量推进，观察一个发布周期的错误预算。观察窗关闭之前，旧路径不删。"),
         "owner": "on-call maintainer", "cost_range": ("1 release", "1 个版本"),
         "artifact": "5%→25%→100% rollout dashboard",
         "acceptance": "error budget stays green for one release",
         "stop": "remove the old path only after the observation window",
         "rollback": "activate the kill switch and restore the TypeScript route"},
    ],

    "migration_checks": [
        {"name": ("End-to-end reach", "端到端可达性"), "state": "PASS",
         "claim": ("Amdahl share and boundary cost are both in the number.", "Amdahl 份额和边界成本都算进去了。"),
         "evidence": "decision_math.py"},
        {"name": ("Attribution", "归因"), "state": "PASS",
         "claim": ("Rust, Go and WASM ran on the same fixture through the same interface.",
                   "Rust、Go、WASM 用同一语料、同一接口跑的。"),
         "evidence": "synthetic counterfactual benchmarks"},
        {"name": ("Boundary uncertainty", "边界成本不确定"), "state": "HIT",
         "claim": ("3% is a bench estimate. Nobody has measured it in production.",
                   "3% 是基准估计值，生产环境没人量过。"),
         "evidence": "synthetic/boundary-bench.json"},
        {"name": ("Scope control", "范围控制"), "state": "PASS",
         "claim": ("The full application migration is excluded, in writing.", "整体迁移已经被明确排除。"),
         "evidence": "option comparison"},
        {"name": ("Ownership", "归属"), "state": "PASS",
         "claim": ("A second maintainer and a rollback owner are both funded.", "第二位维护者和回滚责任人都有预算。"),
         "evidence": "synthetic staffing plan"},
    ],
    "staying_checks": [
        {"name": ("Funded counterfactual", "已投入的对照方案"), "state": "PASS",
         "claim": ("TypeScript, WASM and Go alternatives have owners and same-fixture results.",
                   "TypeScript、WASM、Go 三个替代方案都有负责人和同语料结果。"),
         "evidence": "synthetic counterfactual benchmarks"},
        {"name": ("Target shortfall", "达标差距"), "state": "HIT",
         "claim": ("1.25–1.40× measured. The target is 1.59×.", "实测 1.25–1.40×，目标是 1.59×。"),
         "evidence": "synthetic/ts-baseline.json"},
        {"name": ("Cost of inaction", "不作为的代价"), "state": "PASS",
         "claim": ("The report names the missed 2.4 s workflow target.", "报告点明了没达成的 2.4 s 目标。"),
         "evidence": "synthetic requirement"},
        {"name": ("Unsafe-surface check", "不安全面检查"), "state": "PASS",
         "claim": ("No hidden native dependency in the manifests.", "清单里没有隐藏的原生依赖。"),
         "evidence": "synthetic package manifests"},
        {"name": ("Stop condition", "停止条件"), "state": "PASS",
         "claim": ("Optimization ends when the fixture meets the target or the funded range runs out.",
                   "语料达标，或者预算用完，优化就停。"),
         "evidence": "reversible path"},
    ],

    "gaps": [
        (("Production boundary cost", "生产环境的边界成本"),
         ("Above 7%, authorization drops to DEFER–MEASURE and the TypeScript path stays.",
          "超过 7%，授权降级为 DEFER–MEASURE，继续走 TypeScript。")),
        (("Second Rust owner", "第二位 Rust 维护者"),
         ("Unfunded means G4 is UNKNOWN. The pilot may run; production extraction is not authorized.",
          "没有预算就意味着 G4 是 UNKNOWN。试点可以跑，生产抽取不授权。")),
        (("Production workload mix", "生产负载构成"),
         ("If the owned kernel falls below the measured range, rerun D2 and G3 before rollout.",
          "如果自有内核占比低于实测区间，上线前重跑 D2 和 G3。")),
    ],

    "assumptions": [
        "5x kernel result and 3% boundary cost are synthetic",
        "one additional Rust owner is funded",
    ],
    "objective": {
        "driver": "performance",
        "requirement": "reduce 2 GB export from 3.8 s to <=2.4 s",
        "baseline": "3.8 s",
        "target": "1.59x or better",
    },
    "repository": {
        "path": "synthetic://acme-desk", "commit": "illustrative",
        "scope": "export kernel", "sampling": "synthetic golden fixture",
    },
    "user_supplied_facts": [],
    "analysis_mode": "synthetic-golden",

    "method_title": ("Synthetic golden fixture · why-not-rust method 2.0",
                     "合成金标准语料 · why-not-rust 方法 2.0"),
    "method_body": (
        "This report is fictional. It exists to regression-test the template and the renderer, and it "
        "analyses no real repository. Commit: illustrative. Scope: export kernel. Sampling: synthetic "
        "golden fixture. User-supplied facts: none. Objective: reduce the 2 GB export from 3.8 s to 2.4 s "
        "or better. Amdahl inputs f=.62, S=5, b=.03 give 1.87×, against an infinite-kernel ceiling of "
        "2.44×. The method compares explicit options through four non-compensatory gates; it is a "
        "decision protocol, not a statistical predictor. No project code ran and no network call was made.",
        "这份报告是虚构的。它的作用是回归测试模板和渲染器，没有分析任何真实仓库。commit：illustrative。"
        "范围：导出内核。采样：合成金标准语料。用户提供的事实：无。目标：把 2 GB 导出从 3.8 s 降到 2.4 s 以内。"
        "Amdahl 输入 f=.62、S=5、b=.03，得到 1.87×，内核无限快时的天花板是 2.44×。这套方法用四道非补偿性的门"
        "来比较明确的备选方案，它是决策协议，不是统计预测器。没有运行任何项目代码，也没有发起网络请求。"),
    "footer": ("illustrative synthetic fixture · static analysis + synthetic artifacts",
               "示例用合成语料 · 静态分析 + 合成产物"),
}


def render() -> str:
    return render_case(CASE)


def render_quick() -> str:
    """Return a compact fixture to regression-test quick-mode section order."""
    html = render()
    for number in ("02", "03", "04", "05"):
        pattern = rf'<section>\s*<h2 class="section-title"><span class="no">{number}</span>.*?</section>'
        html, count = re.subn(pattern, "", html, count=1, flags=re.DOTALL)
        if count != 1:
            raise RuntimeError(f"quick-mode section {number} not found")
    for old, new in (("06", "02"), ("07", "03"), ("08", "04")):
        html = html.replace(f'<span class="no">{old}</span>', f'<span class="no">{new}</span>', 1)
    return html


def main() -> None:
    output = ROOT / "examples" / "sample-report.html"
    output.write_text(render(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
