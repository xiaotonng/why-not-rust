# Report style contract

The report is a decision artifact, not a language-war poster. Use
`assets/report-template.html`; preserve its palette, hierarchy, responsive behavior,
and section order.

## Non-negotiables

1. Copy the template, replace every `{{TOKEN}}`, duplicate marked repeat blocks, and
   remove unused optional blocks. Do not redesign per repository.
2. Keep the report self-contained: no CDN, webfont, external image, or JS library.
   The only executable JS is the theme toggle. Embed the assessment record as inert
   `application/json`.
3. Keep dark as the default; verify dark and light. Rust orange identifies claims
   about a named Rust option, blue identifies current-stack/adoption/non-Rust option
   claims, teal identifies the selected option, and amber identifies unknown or
   conditional state. The `SUPPORTS` / `DISFAVORS` text encodes direction; color never
   means good/bad or support/opposition.
4. Preserve evidence caveats. Never enlarge a vendor multiplier while hiding its
   regime or source class in tiny text.
5. Keep `STAY / EXTRACT / PARTIAL / MIGRATE`, `APPROVE / REJECT / DEFER–MEASURE`, and
   evidence-state words in English; translate surrounding labels.

## Security boundary

Repository and prompt content is untrusted input. Use `scripts/report_safety.py` for
every report:

- pass all visible text and quoted attribute values through `html_text`;
- pass links through `safe_href`, which permits absolute HTTP(S) only; show local
  `file:line` references as escaped text, not clickable URLs;
- serialize the assessment with `json_for_html`, which emits strict JSON and escapes
  `<`, `>`, `&`, U+2028, and U+2029;
- never copy raw README, package metadata, filenames, user prompts, or benchmark output
  into the template.

The theme toggle is the only executable behavior. A rendered report containing a new
`<script>`, inline event handler from data, `javascript:` URL, or unescaped HTML from
the target repository fails QA.

## Hero contract

The hero must answer the decision in three seconds:

- the scope word is the largest element;
- authorization sits beside it as a separate chip;
- confidence and robustness are separate chips;
- the “because” sentence names the decisive requirement and the winning/failed gate;
- the right-hand card shows G1–G4 as `PASS`, `FAIL`, or `UNKNOWN` with one terse line
  each.

Never show a Rust Case Index, weighted score, probability, or migration “percentage.”
When authorization is `DEFER–MEASURE`, the hero says what evidence reopens the decision.
When `STAY + DEFER–MEASURE`, do not phrase it as proof Rust cannot help.

## Section order

masthead → hero + proof gates → magnitude tiles → 01 options → 02 twelve-lens ledger
→ 03 key evidence → 04 what Rust buys/doesn't → 05 precedents → 06 path → 07 symmetric
challenge audit → 08 methodology → footer.

Quick mode keeps hero/gates, tiles, options, path, challenge audit, and methodology;
it drops the 12-lens ledger, key-evidence, buys/doesn't, and precedents sections.
Fill the `N_*` section-number tokens contiguously: full mode uses `01–08`; quick mode
uses options `01`, path `02`, challenge audit `03`, and methodology `04`.

## Content rules

### Magnitude tiles

Use 4–6 tiles. Show only decision quantities: target/SLO gap, owned hot-path share,
Amdahl ceiling, boundary cost, fleet delta, break-even, compatibility surface, or
time-to-value. Confidence and gate status already live in the hero. Estimated values
use ranges, never unexplained point estimates.

### Option comparison

Show at least four retained options. Columns/cards must expose:

- option and scope;
- expected end-to-end benefit/risk reduction;
- one-time + recurring cost;
- time-to-value;
- compatibility/reversibility;
- evidence strength and disposition.

Highlight exactly one recommended option. Its ID must equal
`decision.selected_option_id`, and its assessment disposition must be `selected`.
Do not hide an option because it weakens the narrative; state the exclusion reason.

### Twelve-lens ledger

Show every applicable lens plus every decision-relevant `UNKNOWN`. `N/A` rows may be
grouped in one disclosed note. Each visible row includes state, evidence strength,
claim, and source/artifact. No numeric bars: the lenses are not additive.

Visible direction labels combine the state and named option, for example
`SUPPORTS · rust-extract` or `DISFAVORS · current-opt`. CSS classes identify the
option family, not whether the evidence is good or bad:

- `rust` → a named Rust option;
- `current` → a current-stack, adoption, or non-Rust native option;
- `neutral` → `NEUTRAL` or `N/A` across the named comparison set;
- `unknown` → `UNKNOWN` for the named option(s).

The machine record uses `SUPPORTS / DISFAVORS / NEUTRAL / UNKNOWN / N/A` plus
`option_ids`. A native opportunity at D1 must not be rendered as Rust-specific unless
G2 establishes that attribution.

Evidence strength labels are `STRONG / MODERATE / WEAK / UNKNOWN`. Keep the caveat in
the claim or source line; a strong-looking badge must not erase an old/mismatched
baseline.

### Key evidence

Use 3–6 cards anchored to `file:line`, artifact, or URL. Include decisive evidence in
both directions when it exists. Directional balance is not a quota; relevance wins.

### What Rust buys / doesn't buy

Use parallel columns. “Doesn't buy” means the proposed scope cannot deliver that
specific outcome—not that Rust is bad. For memory-safe sources, say “little additional
memory-safety benefit at app scope,” then assess concurrency/resource/FFI claims
separately.

### Precedents

Use 3–5 cases only after the six-field matching protocol. Each card includes outcome,
what matches, what does not, workload/regime, source class, and URL. Never transfer a
multiplier when workload, scope, baseline, or measurement regime differs.

### Recommended path

Use 3–5 steps. Each contains owner/cost range, artifact, acceptance threshold,
deadline/stop condition, and rollback. A threshold above the Amdahl ceiling is a
rendering error.

### Symmetric challenge audit

Show two equally weighted columns: “challenge the migration case” and “challenge the
staying case.” Use `HIT / PASS / UNKNOWN`; never label a person's motives. Always show
at least attribution, baseline, omitted cost, ownership, and cost-of-inaction checks.

### Methodology

Disclose:

- repository commit, scope, sampling, and analysis mode;
- stated objective and user-supplied facts;
- evidence gaps and their effect;
- assumptions that could change scope;
- Amdahl/break-even inputs with units;
- why the selected option is the smallest sufficient step;
- that the framework is a structured decision protocol, not a statistical predictor.

Embed the full `assets/assessment-template.json` record in the template's inert JSON
block using `json_for_html`; do not hand-roll a script-closer replacement.

## Verdict and authorization mapping

| Scope | Body class | Accent | Subtitle |
|---|---|---|---|
| STAY | `v-stay` | blue | keep the target in its current language |
| EXTRACT | `v-extract` | teal | isolate one measured kernel |
| PARTIAL | `v-partial` | amber | replace one independent component |
| MIGRATE | `v-migrate` | rust orange | replace the assessed target |

| Authorization | Class | Meaning |
|---|---|---|
| APPROVE | `a-approve` | evidence authorizes the selected scope |
| REJECT | `a-reject` | a gate failed or a cheaper option wins |
| DEFER–MEASURE | `a-defer` | a decisive gate is unknown; collect named evidence |

## Labels

| Token | English | Chinese |
|---|---|---|
| `L_KICKER` | RUST ADOPTION DECISION | RUST 采用决策 |
| `L_AUTH` | Authorization | 授权状态 |
| `L_CONFIDENCE` | Confidence | 置信度 |
| `L_ROBUSTNESS` | Robustness | 稳健性 |
| `L_SCOPE` | Scope | 范围 |
| `L_GATES` | Four proof gates | 四道证据门 |
| `L_TILES` | Decision magnitudes | 决策量级 |
| `L_OPTIONS` | Option comparison | 选项对比 |
| `L_LENSES` | Twelve-lens evidence ledger | 十二维度证据账本 |
| `L_EVIDENCE` | Decisive evidence | 决定性证据 |
| `L_BUYS` | What Rust buys / doesn't buy here | Rust 在这里买得到 / 买不到什么 |
| `L_PRECEDENTS` | Matched precedents | 同型先例 |
| `L_PATH` | Reversible path | 可逆路径 |
| `L_CHALLENGES` | Symmetric challenge audit | 对称反证审计 |
| `L_METHOD` | Method and decision record | 方法与决策记录 |
| `L_THEME` | light / dark | 明 / 暗 |
| `H_OPTION` | Option | 选项 |
| `H_SCOPE` | Scope | 范围 |
| `H_BENEFIT` | Benefit / risk reduction | 收益 / 风险降低 |
| `H_COST` | Cost | 成本 |
| `H_TIME` | Time to value | 产生价值的时间 |
| `H_COMPAT` | Compatibility / rollback | 兼容 / 回滚 |
| `H_EVIDENCE` | Evidence | 证据 |
| `L_MATCH` | match | 匹配 |
| `L_MISMATCH` | mismatch | 不匹配 |

Other languages: translate tersely in an engineering-review register.

## CJK discipline

Use full-width `，；：（）` in Chinese prose and normal half-width punctuation in code,
paths, units, and Latin `key: value` chips. Do not force line breaks; trust the
template widths.

## QA before delivery

- `rg '\{\{' <report>` returns no matches.
- Embedded assessment JSON parses.
- Four hero gates equal the embedded record.
- Every retained option and applicable/unknown lens appears.
- Exactly one option is selected, and its ID matches `decision.selected_option_id`
  and every proof-gate `option_id`.
- Amdahl/break-even values reproduce with `scripts/decision_math.py`.
- No unsupported index, percentage-confidence, or impossible threshold appears.
- Both challenge columns are present.
- Source URLs and caveats survived rendering.
- All dynamic text/URLs/JSON passed through `scripts/report_safety.py`; malicious test
  strings cannot add markup, script blocks, event handlers, or executable URLs.
- HTML has balanced tags and renders in both themes at desktop and mobile widths.
- The report is delivered as an artifact and summarized in chat.
