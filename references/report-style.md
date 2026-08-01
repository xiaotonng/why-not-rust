# Report style contract

The report's uniform look across projects, users, and languages is a feature.
You do not design a report — you **fill the template** (`assets/report-template.html`)
and follow this contract. Deviations are bugs.

## Non-negotiables

1. **Copy the template file, then only:** replace `{{TOKENS}}`, duplicate
   `BEGIN/END REPEAT` blocks, delete unused OPTIONAL blocks, and set the verdict
   class on `<body>`. Never edit the `<style>` block except nothing — it is fixed.
2. **Self-contained single file.** No CDN, no webfonts, no external images, no JS
   libraries. The only JS is the theme-toggle one-liner already in the template.
3. **Dark is the default theme** (`<html data-theme="dark">`); light must also be
   correct (the toggle swaps). Both palettes in the template are pre-validated
   for contrast and CVD separation — that's why the CSS is frozen.
4. **ASCII-only in CSS color values.** (A Cyrillic `е` inside a hex once shipped;
   hence the rule.)
5. Report language = the language the user is conversing in. Translate the
   `{{L_*}}` label tokens with the table below; keep verdict words
   (STAY / EXTRACT / PARTIAL / MIGRATE) and "Rust Case Index" in English always.

## Verdict mapping

| Verdict | `<body>` class | Color role | Subtitle template (zh / en) |
|---|---|---|---|
| STAY | `v-stay` | blue | 留在现栈,按清单优化 / stay; optimize in place |
| EXTRACT | `v-extract` | teal | 提取热核,不整体迁移 / extract the hot kernel, don't migrate |
| PARTIAL | `v-partial` | amber | 只重写 X 组件 / rewrite only the X component |
| MIGRATE | `v-migrate` | rust orange | 整体迁移成立 / full migration is justified |

If cap C1 fired, append the qualifier to the verdict chip: zh `（先测量)` /
en ` (measure first)` — via `{{VERDICT_QUALIFIER}}`; otherwise fill it with "".

## The two charts and their math

- **Gauge (hero):** `INDEX_PCT = (index + 100) / 2`. Needle sits at
  `calc({{INDEX_PCT}}% - 5px)`. Band split in the track background is fixed
  (STAY 45% / EXTRACT 12.5% / PARTIAL 12.5% / MIGRATE 30%) matching the bands
  −100…−10…+15…+40…+100. `{{GAUGE_NOTE}}` = one line: formula + band meaning.
- **Scorecard bars:** rows sorted by impact descending (most pro-Rust on top).
  `DIM_WIDTH = |score × weight| ÷ 6 × 100` (cap 100), `DIM_DIR` = `pro` if
  impact > 0, `con` if < 0; omit the `.fill` span entirely when impact = 0.
  `DIM_IMPACT` shows the signed product (`+6`, `−3`, `0`) with a true minus sign
  (U+2212). Every row keeps its weight chip `w0–w3`.

Data-ink rules (inherited from the palette validation): color appears only on
marks (bars, needle, swatches, left borders, tag tints) — **all text wears text
tokens** (`--ink/-2/-3`), never a series color; exception: text sitting on a tint
chip uses that chip's ink pair as templated. The two-key legend above the
scorecard is mandatory. No third color inside the scorecard.

## Section order (fixed)

masthead → hero (verdict + gauge) → stat tiles → 01 scorecard → 02 key evidence →
03 what Rust buys / doesn't buy here → 04 precedents → 05 recommended path →
06 trap audit → 07 methodology → footer.

Omissions allowed only in `quick` mode: drop 02/03/04, keep 01 as the 5-question
gate list (reuse `.cards` with one card per question), keep 05–07.

## Content rules per block

- **Hero why:** ≤ 3 sentences; must name the decisive evidence and the decisive
  constraint. No hedging ("might", "perhaps") — confidence is expressed by the
  confidence chip, not by mushy prose.
- **Tiles:** 4–6. Tile 1 is always the Index. Every tile note says how the number
  was derived (`profiled`, `estimated`, `precedent range`). Estimated numbers use
  ranges, never point values.
- **Findings:** 3–6 cards, each anchored `file:line` or artifact name in the
  `.ref` chip. Balance is not required — direction classes must reflect content.
- **Precedents:** 3–5 from `case-library.md` only, tag class per outcome
  (`stayed`/`hybrid`/`moved`/`failed`), each with its URL in the `.src` line.
  Never cite a case that isn't in the library (add it to the library first, with
  a source).
- **Path steps:** each has a cost estimate and, where measurable, an explicit
  acceptance threshold inside the body text.
- **Traps:** always render at least the four core checks (safety-conflation,
  attribution-error, amdahl-blindness, gc-phobia) with hit/ok status; add others
  when relevant.
- **Methodology:** archetype, weight adjustments (esp. user-prompt-driven ones),
  the formula with numbers plugged in, caps/floors that fired, evidence gaps
  table.
- **Footer disclosure:** state the analysis mode honestly, e.g. zh
  「评估基于仓库静态探查 + 既有 profile,未运行项目代码」.

## Label translation table (`{{L_*}}`)

| Token | en | zh |
|---|---|---|
| L_THEME | light / dark | 明 / 暗 |
| L_KICKER | RUST MIGRATION ASSESSMENT | RUST 迁移评估 |
| L_VERDICT | Verdict | 结论 |
| L_CONFIDENCE | Confidence | 置信度 |
| L_SCOPE | Scope | 范围 |
| L_ARCHETYPE | Archetype | 原型 |
| L_SCORECARD | The 12-dimension scorecard | 十二维度记分牌 |
| L_SCORECARD_SUB | score −2…+2 (positive favors migration) × weight 0…3 (archetype + user constraints); bar length = score × weight | 分值 −2…+2（越正越支持迁移）× 权重 0…3（按原型 + 用户附加条件定），条长 = 分值×权重 |
| L_KEY_STAY | favors staying / solvable in current stack | 支持留守 / 现栈可解 |
| L_KEY_RUST | favors migration / real Rust gain | 支持迁移 / Rust 有真增益 |
| L_EVIDENCE | Key evidence | 关键证据 |
| L_BUYS | What Rust buys / doesn't buy here | Rust 在这里买得到 / 买不到什么 |
| L_BUYS_YES | Buys | 买得到 |
| L_BUYS_NO | Doesn't buy | 买不到 |
| L_PRECEDENTS | Matched precedents | 同型先例 |
| L_PATH | Recommended path (smallest sufficient step) | 建议路径（最小充分步骤原则） |
| L_TRAPS | Trap audit | 误区体检 |
| L_METHOD | Methodology & weight adjustments | 方法论与权重调整 |
| L_METHOD_SUB | Reproducible parameters of this assessment | 本次评估的可复现参数 |
| L_GAP | Evidence gap | 证据缺口 |
| L_GAP_EFFECT | Effect | 影响 |
| Trap status labels | HIT / PASS | 命中 / 通过 |
| Precedent tags | stayed & won / hybrid win / migrated / failed-reverted | 留守获胜 / 热核提取 / 整体迁移 / 失败-回退 |

Other languages: translate with the same register (engineering-report, terse).

## QA before delivering

- No `{{` remains (grep the file).
- Bar widths and the needle position recompute correctly from the scores shown.
- Numbers in tiles/prose match the scorecard and methodology.
- Both themes checked (toggle) if a browser/screenshot tool is available; at
  minimum re-read the HTML for unclosed tags.
- File is one self-contained `.html`; report path told to the user; chat TL;DR
  (verdict + index + confidence + 3 bullets) delivered alongside.
