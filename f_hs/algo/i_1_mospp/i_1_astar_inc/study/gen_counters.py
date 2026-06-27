"""
============================================================================
 Generator for the AStarIncMOSPP COUNTERS.html table region.

 Single source of truth for the 18-config heatmap: re-runs every
 config from `study.oracle.CONFIGS`, recomputes the per-column
 traffic scale (green = column min, red = column max) + duplicate
 grouping, and splices a fresh `<table>...</table>` (new column
 order, no `uniq` column) into the existing COUNTERS.html,
 leaving the hand-written chrome (hero / fixture / notes /
 footer / CSS) untouched.

 Column order (matches the counter scaffold group order):
   expanded, generated,
   prop_attempts, prop_lifts, prop_waves,
   bpmx_attempts, bpmx_lifts, bpmx_depth

 Run:
   python -m f_hs.algo.i_1_mospp.i_1_astar_inc.study.gen_counters
============================================================================
"""
import re
from pathlib import Path

from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.algo.i_1_mospp.i_1_astar_inc.study.oracle import CONFIGS
from f_hs.problem.i_1_grid import ProblemGrid

# Shown counters, in column order (== scaffold group order).
SHOWN: tuple[str, ...] = (
    'cnt_expanded', 'cnt_generated',
    'cnt_prop_attempts', 'cnt_prop_lifts', 'cnt_prop_waves',
    'cnt_bpmx_attempts', 'cnt_bpmx_lifts', 'cnt_bpmx_depth',
)
HEADERS: tuple[str, ...] = tuple(c[len('cnt_'):] for c in SHOWN)

# Per-column header underline colour (group-coded).
UNDERLINE: dict[str, str] = {
    'cnt_expanded': '#FFD54F', 'cnt_generated': '#FFD54F',
    'cnt_prop_attempts': '#4A90E2', 'cnt_prop_lifts': '#4A90E2',
    'cnt_prop_waves': '#4A90E2',
    'cnt_bpmx_attempts': '#b07cff', 'cnt_bpmx_lifts': '#b07cff',
    'cnt_bpmx_depth': '#b07cff',
}

# Group metadata: (start_index, count, colour, title, note).
GROUPS: list[tuple[int, int, str, str, str]] = [
    (0, 1, '#ff8a3d', 'Group A — Cache',
     'Single anchor: carried on-path cache only. Sub-search 2 '
     'from (2,3) is a cache-hit-at-init.'),
    (1, 4, '#4A90E2', 'Group B — Propagation depth',
     'carry_cache + pre-search propagate_pathmax(depth). '
     'Differentiated by cnt_prop_*.'),
    (5, 13, '#7ED321', 'Group C — BPMX rule × depth',
     'carry_cache (BPMX inconsistency engine) + in-search '
     'Felner cascade. Differentiated by cnt_bpmx_* / '
     'cnt_expanded.'),
    (18, 4, '#22b8cf', 'Group D — Propagate + BPMX',
     'Combined quadrant: pre-search propagate THEN in-search '
     'BPMX (shared HBounded, max-combined). No expansion '
     'synergy here — the grid saturates at 23; convergent '
     'propagation subsumes BPMX (cnt_bpmx_lifts → 0). '
     'Optimality preserved.'),
]
NCOLS = 1 + len(SHOWN)  # config + 8 counters (no uniq).


def _kw_html(kwargs: dict) -> str:
    """
    ========================================================================
     Serialize the per-config kwargs (minus the two globally
     invariant params) the way the config cell shows them.
    ========================================================================
    """
    parts = []
    for k, v in kwargs.items():
        if k in ('carry_cache', 'adaptive_h'):
            continue
        if isinstance(v, str):
            parts.append(f"{k}=&#x27;{v}&#x27;")
        else:
            parts.append(f"{k}={v}")
    return ', '.join(parts)


def _run_all() -> list[tuple[str, dict, dict[str, int]]]:
    """
    ========================================================================
     Run every config; return (name, kwargs, shown-counter dict).
    ========================================================================
    """
    out = []
    for name, kwargs in CONFIGS:
        p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
        algo = AStarIncMOSPP(problem=p,
                             h=lambda s, g: float(s.key.distance(g.key)),
                             is_recording=False, **kwargs)
        algo.run()
        c = algo.counters
        out.append((name, kwargs,
                    {k: int(c[k]) for k in SHOWN}))
    return out


def _cell(v: int, lo: int, hi: int) -> str:
    """
    ========================================================================
     One numeric <td>: per-column traffic scale — green at the
     column min, red at the column max, yellow at the midpoint
     (HSL hue 120 -> 0, linear in the per-column normalized
     value). A constant column (hi == lo) renders neutral —
     there is no highest / lowest to rank. Bold in the upper
     half of the column, matching the legend gradient.
    ========================================================================
    """
    if hi > lo:
        norm = (v - lo) / (hi - lo)
        hue = 120.0 * (1.0 - norm)            # 120 green .. 0 red
        bg = f'hsla({hue:.0f},65%,45%,0.45)'
        weight = 600 if norm > 0.5 else 400
    else:
        bg = 'rgba(255,255,255,0.04)'         # no variation
        weight = 400
    return (f'<td style="background:{bg};'
            f'color:var(--text);font-weight:{weight};">{v}</td>')


def _build_table(rows: list[tuple[str, dict, dict[str, int]]]
                  ) -> tuple[str, int]:
    """
    ========================================================================
     Assemble the full <table> string and the distinct-tuple
     count (for the statbar).
    ========================================================================
    """
    # Per-column min / max for independent heat scaling.
    col_lo = {k: min(r[2][k] for r in rows) for k in SHOWN}
    col_hi = {k: max(r[2][k] for r in rows) for k in SHOWN}

    # Duplicate detection on the shown tuple (first = canonical).
    first_of: dict[tuple, str] = {}
    dup_of: dict[str, str | None] = {}
    for name, _, vals in rows:
        key = tuple(vals[k] for k in SHOWN)
        if key in first_of:
            dup_of[name] = first_of[key]
        else:
            first_of[key] = name
            dup_of[name] = None
    distinct = len(first_of)

    th = ['<thead><tr><th class="cfg">config</th>']
    for k, h in zip(SHOWN, HEADERS):
        th.append(f'<th style="border-bottom:2px solid '
                  f'{UNDERLINE[k]}"><span class="cn">{h}'
                  f'</span></th>')
    th.append('</tr></thead>')
    head = ''.join(th)

    body = ['<tbody>']
    for gstart, gcount, gcol, gtitle, gnote in GROUPS:
        body.append(
            f'<tr class="grouprow"><td colspan="{NCOLS}" '
            f'style="border-left:4px solid {gcol};">'
            f'<span style="color:{gcol};font-weight:700">'
            f'{gtitle}</span> '
            f'<span class="gcount">{gcount}</span> '
            f'<span class="gnote">{gnote}</span></td></tr>')
        for name, kwargs, vals in rows[gstart:gstart + gcount]:
            canon = dup_of[name]
            tr = ('<tr class="dup">' if canon else '<tr>')
            dupe = (f'<span class="dupe">≡ {canon}</span>'
                    if canon else '')
            cfg = (f'<td class="cfg"><span class="dot" '
                   f'style="background:{gcol}"></span>{name}'
                   f'{dupe}<div class="kw">{_kw_html(kwargs)}'
                   f'</div></td>')
            cells = ''.join(
                _cell(vals[k], col_lo[k], col_hi[k])
                for k in SHOWN)
            body.append(f'{tr}{cfg}{cells}</tr>')
    body.append('</tbody>')

    table = '<table>\n' + head + '\n' + '\n'.join(body) + \
            '\n</table>'
    return table, distinct


def main() -> None:
    """
    ========================================================================
     Regenerate the <table> region of COUNTERS.html in place
     and report the distinct-tuple count.
    ========================================================================
    """
    html_path = (Path(__file__).resolve().parent.parent
                 / 'COUNTERS.html')
    html = html_path.read_text()
    rows = _run_all()
    table, distinct = _build_table(rows)

    new_html = re.sub(r'<table>.*?</table>', lambda _: table,
                       html, count=1, flags=re.DOTALL)
    html_path.write_text(new_html)
    print(f"COUNTERS.html table regenerated: "
          f"{len(rows)} configs, {distinct}/{len(rows)} "
          f"distinct on the {len(SHOWN)} shown counters.")
    for name, _, vals in rows:
        print(f"  {name:34} "
              + " ".join(f"{vals[k]:>4}" for k in SHOWN))


if __name__ == '__main__':
    main()
