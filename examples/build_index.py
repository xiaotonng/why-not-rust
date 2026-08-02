#!/usr/bin/env python3
"""Generate examples/index.html — the landing page for the published gallery.

The verdict of every card is read from the case modules themselves, so the
index cannot drift from the reports it links to. Same escaping contract and the
same self-contained rule as the reports: no external asset of any kind.

Usage:
    python3 examples/build_index.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "why-not-rust" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_cases import CASES_DIR, VERDICT_CLASS, en, load_case  # noqa: E402
from report_safety import html_text  # noqa: E402

DESKTOP = [
    "remacs", "xi-editor", "lapce", "spacedrive", "zed",
    "fish-shell", "ghostty", "bitwarden-desktop", "signal-desktop", "keepassxc",
]
SYSTEMS = [
    "curl", "sqlite", "openssl", "ffmpeg", "redis",
    "esbuild", "flake8", "prisma-engines", "coreutils", "bun",
]

PAGE = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>why-not-rust — twenty worked Rust decisions</title>
<meta name="description" content="Twenty open-source projects run through four non-compensatory proof gates. \
Each report is self-contained, bilingual, and pinned to a public commit.">
<style>
  :root {{
    --page:#0b0c0e; --ink:#e9eaec; --ink-2:#b9bcc2; --ink-3:#83878f; --line:#22252a;
    --rust:#e06c3f; --teal:#3fb99a; --blue:#5b9cf0; --amber:#d9a441;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;
    --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  }}
  @media (prefers-color-scheme:light) {{
    :root:not([data-theme="dark"]) {{
      --page:#fbfbfa; --ink:#16181c; --ink-2:#4a4e57; --ink-3:#7c818b; --line:#e3e4e7;
    }}
  }}
  :root[data-theme="light"] {{
    --page:#fbfbfa; --ink:#16181c; --ink-2:#4a4e57; --ink-3:#7c818b; --line:#e3e4e7;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--page); color:var(--ink); font-family:var(--sans);
    font-size:16px; line-height:1.62; -webkit-font-smoothing:antialiased;
    padding:0 32px 96px; overflow-wrap:break-word;
  }}
  .wrap {{ max-width:1080px; margin:0 auto; }}
  a {{ color:inherit; }}
  .mono {{ font-family:var(--mono); }}
  .mast {{
    display:flex; align-items:center; justify-content:space-between; gap:12px;
    padding:26px 0; border-bottom:1px solid var(--line); flex-wrap:wrap;
  }}
  .logo {{ font-family:var(--mono); font-weight:700; letter-spacing:-.02em; }}
  .logo i {{ font-style:normal; color:var(--rust); }}
  .btn {{
    font:inherit; font-size:.76rem; color:var(--ink-2); background:none;
    border:1px solid var(--line); border-radius:6px; padding:5px 11px; cursor:pointer;
  }}
  h1 {{ font-size:2.6rem; line-height:1.1; letter-spacing:-.035em; margin:54px 0 18px; }}
  .lede {{ font-size:1.06rem; color:var(--ink-2); max-width:60ch; margin:0 0 10px; }}
  .meta {{ font-size:.82rem; color:var(--ink-3); margin-top:22px; }}
  h2 {{
    font-size:.78rem; letter-spacing:.09em; text-transform:uppercase; color:var(--ink-3);
    margin:62px 0 4px; font-weight:600;
  }}
  .sub {{ font-size:.9rem; color:var(--ink-3); margin:0 0 20px; max-width:64ch; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:1px; background:var(--line); border:1px solid var(--line); }}
  .card {{
    background:var(--page); padding:18px 20px; text-decoration:none; display:block;
  }}
  .card:hover {{ background:color-mix(in srgb, var(--ink) 5%, var(--page)); }}
  .card .top {{ display:flex; align-items:baseline; justify-content:space-between; gap:10px; }}
  .card .name {{ font-weight:640; letter-spacing:-.01em; }}
  .card .verdict {{
    font-family:var(--mono); font-size:.66rem; font-weight:700; letter-spacing:.07em;
    white-space:nowrap; display:inline-flex; align-items:center; gap:5px;
  }}
  .card .verdict::before {{ content:""; width:6px; height:6px; border-radius:50%; background:currentColor; }}
  .v-stay .verdict {{ color:var(--blue); }}
  .v-extract .verdict {{ color:var(--teal); }}
  .v-partial .verdict {{ color:var(--amber); }}
  .v-migrate .verdict {{ color:var(--rust); }}
  .card .finding {{ font-size:.86rem; color:var(--ink-2); margin-top:7px; }}
  footer {{ margin-top:70px; padding-top:22px; border-top:1px solid var(--line); font-size:.82rem; color:var(--ink-3); }}
  @media (max-width:640px) {{ body {{ padding:0 20px 70px; }} h1 {{ font-size:2rem; }} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="mast">
    <span class="logo">why<i>&ndash;not&ndash;</i>rust</span>
    <button class="btn" onclick="document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark'">light / dark</button>
  </div>

  <h1>Twenty worked Rust decisions</h1>
  <p class="lede">Twenty open-source projects, each run through the same four non-compensatory
  proof gates. Every report is self-contained, reads in English and 中文, and is pinned to a
  public commit you can re-measure.</p>
  <p class="meta">{approve} APPROVE &middot; {reject} REJECT &middot; {defer} DEFER&ndash;MEASURE &middot;
  all four scope words &middot; <a href="https://github.com/xiaotonng/why-not-rust">source on GitHub</a></p>

  <h2>Desktop applications</h2>
  <p class="sub">Apps whose teams believed a Rust rewrite was the answer. Six of the ten already bet
  on Rust: two are dead, two have stalled, two are thriving. Same language, opposite outcomes.</p>
  <div class="grid">{desktop}</div>

  <h2>Systems and developer tooling</h2>
  <p class="sub">The projects people most often demand a rewrite of.</p>
  <div class="grid">{systems}</div>

  <footer>Static read-only analysis of public repositories. No build, test, benchmark or network
  call was run against any target project. Where a decisive measurement does not exist, the report
  records <span class="mono">UNKNOWN</span> rather than estimating it.</footer>
</div>
</body>
</html>
"""


def card(slug: str) -> str:
    case = load_case(CASES_DIR / f"{slug}.py")
    finding = en(case["scope_sub"])
    return (
        f'<a class="card {VERDICT_CLASS[case["scope_word"]]}" '
        f'href="{html_text(slug)}-why-not-rust.html">'
        f'<span class="top"><span class="name">{html_text(case["project_name"])}</span>'
        f'<span class="verdict">{html_text(case["scope_word"])} / {html_text(case["auth"])}</span></span>'
        f'<span class="finding">{html_text(finding)}</span></a>'
    )


def main() -> int:
    cases = {p.stem: load_case(p) for p in CASES_DIR.glob("*.py") if not p.name.startswith("_")}
    missing = (set(DESKTOP) | set(SYSTEMS)) - set(cases)
    extra = set(cases) - (set(DESKTOP) | set(SYSTEMS))
    if missing or extra:
        print(f"index is out of step with the case modules: missing={sorted(missing)} "
              f"unlisted={sorted(extra)}", file=sys.stderr)
        return 1

    auths = [c["auth"] for c in cases.values()]
    html = PAGE.format(
        approve=auths.count("APPROVE"),
        reject=auths.count("REJECT"),
        defer=auths.count("DEFER–MEASURE"),
        desktop="".join(card(s) for s in DESKTOP),
        systems="".join(card(s) for s in SYSTEMS),
    )
    out = CASES_DIR.parent / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(cases)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
