"""
================================================================
 MOSPP report render engine -- pure functions that turn an
 aggregated DataFrame + the report spec into LaTeX
 fragments (figures, tables, insights, the spliced section).
 No Drive / tectonic / Overleaf I/O -- that lives in the
 `s_5_gen_report` orchestrator. Unit-tested in
 `_tester_report_render.py`.
================================================================
"""
import numpy as np
import pandas as pd

from f_hs.experiments.mospp.report_spec import (
    CONFIGS, K_TABLE, COUNTER_GROUPS, _EXCLUDED_COUNTERS,
    _COUNTER_INFO, _DEFAULT_CAPTION_BODY, _CAPTION_INSIGHT,
    _HEAT_GREEN, _HEAT_YELLOW, _HEAT_RED, _ANNOT_K,
    TOY_CACHED_CELL, TOY_START, TOY_GOAL, TOY_GRID_ROWS,
    TOY_GRID_COLS,
)


# ── Helpers ─────────────────────────────────────────────────────────────────

def tex_esc(s: str) -> str:
    """Escape underscores for LaTeX text."""
    return s.replace('_', r'\_')


def fmt_cell(v) -> str:
    """
    ========================================================================
     Compact numeric formatting for table cells. No scientific
     notation -- large numbers use thousands separators
     (e.g., 285,235 not 2.85e+05). Always returns a string the
     reader can compare with by eye.
    ========================================================================
    """
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    if not np.isfinite(v):
        return '—'
    if v == 0:
        return '0'
    a = abs(v)
    if a >= 1000:
        return f'{v:,.0f}'
    if a >= 100:
        return f'{v:.0f}'
    if a >= 1:
        return f'{v:.2f}'
    return f'{v:.3g}'


def fmt_value(metric: str, v) -> str:
    """Compact formatter that appends `\\%` for `pct_*` metrics.

    `elapsed_*` metrics use a uniform 2-decimal format regardless
    of magnitude, so a time table does not mix integer cells
    (≥100) with 2-decimal cells (<100).
    """
    if metric.startswith('elapsed_'):
        try:
            fv = float(v)
        except (TypeError, ValueError):
            return str(v)
        if not np.isfinite(fv):
            return '—'
        return f'{fv:,.2f}'
    s = fmt_cell(v)
    if metric.startswith('pct_') and s not in ('—',):
        return s + r'\%'
    return s


def should_log(values: np.ndarray) -> bool:
    pos = values[values > 0]
    if len(pos) < 2:
        return False
    return float(pos.max()) / float(pos.min()) > 10.0


def heat_hex(t: float) -> str:
    """
    ========================================================================
     Map a normalized value $t \\in [0, 1]$ to a red-yellow-green
     hex color: t=0 -> green (smallest), t=0.5 -> yellow,
     t=1 -> red (largest). Linear RGB interpolation through the
     yellow midpoint (Excel 3-color-scale convention).
    ========================================================================
    """
    t = max(0.0, min(1.0, float(t)))
    if t <= 0.5:
        lo, hi, u = _HEAT_GREEN, _HEAT_YELLOW, t / 0.5
    else:
        lo, hi, u = _HEAT_YELLOW, _HEAT_RED, (t - 0.5) / 0.5
    c = tuple(round(lo[i] + (hi[i] - lo[i]) * u) for i in range(3))
    return f'{c[0]:02X}{c[1]:02X}{c[2]:02X}'


def heat_cell(v: float, vmin: float, vmax: float) -> str:
    """
    ========================================================================
     `\\cellcolor[HTML]{...}` prefix for one numeric cell, shaded
     by its rank within $[v_{\\min}, v_{\\max}]$ of its column.
     Returns '' for a non-finite value or a constant column
     ($v_{\\max} = v_{\\min}$) -- a flat column carries no
     larger/smaller signal, so it stays unshaded.
    ========================================================================
    """
    if not np.isfinite(v) or vmax <= vmin:
        return ''
    t = (v - vmin) / (vmax - vmin)
    return rf'\cellcolor[HTML]{{{heat_hex(t)}}}'


def run_toy_example() -> dict:
    """
    ========================================================================
     Build the toy, run AStarBPMX at three configs, return the
     numbers. Imports are local so the toy stays optional --
     `s_5_gen_report.py` can run even if the algo packages move.
    ========================================================================
    """
    from f_hs.problem.i_1_grid import ProblemGrid
    from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
    from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
    from f_ds.grids.grid.map import GridMap

    grid = GridMap(rows=TOY_GRID_ROWS, cols=TOY_GRID_COLS)
    for c in range(1, 5):
        grid[1][c].set_invalid()
    for c in range(0, 5):
        grid[3][c].set_invalid()
    goal_cell = grid[TOY_GOAL[0]][TOY_GOAL[1]]

    # Seed: full optimal-path cache for (0,0) -> (5,0).
    p_seed = ProblemGrid(grid=grid, start=grid[0][0], goal=goal_cell)
    h = lambda s: float(s.distance(p_seed.goals[0]))
    seed_algo = AStarLookup(problem=p_seed, h=h, goal=p_seed.goals[0])
    seed_algo.run()
    full_cache = seed_algo.to_cache()
    cache_rc = {(st.key.row, st.key.col): st for st in full_cache}

    # Prune to a single cached cell: TOY_CACHED_CELL.
    cached_state = cache_rc[TOY_CACHED_CELL]
    h_star_cached = float(full_cache[cached_state].h_perfect)
    cache = {cached_state: full_cache[cached_state]}

    # Run at three configs from TOY_START.
    p_toy = ProblemGrid(grid=grid,
                        start=grid[TOY_START[0]][TOY_START[1]],
                        goal=goal_cell)
    runs = []
    popped_by_label: dict[str, set[tuple[int, int]]] = {}
    for label, rule, depth in [
        ('depth=0 (rule=none)', None, 1),
        ('depth=1',             '1',  1),
        ('depth=2',             '1',  2),
    ]:
        algo = AStarBPMX(problem=p_toy, h=h, cache=cache,
                         goal=p_toy.goals[0],
                         rule_bpmx=rule, depth_bpmx=depth,
                         is_recording=True)
        sol = algo.run()
        popped_by_label[label] = {
            (e['state'].key.row, e['state'].key.col)
            for e in algo.recorder.events
            if e['type'] == 'pop'}
        runs.append({
            'label': label,
            'cnt_expanded': int(algo.counters['cnt_expanded']),
            'cnt_bpmx_lifts': int(algo.counters['cnt_bpmx_lifts']),
            'cnt_bpmx_attempts': int(algo.counters['cnt_bpmx_attempts']),
            'cost': float(sol.cost),
        })

    # Cells expanded by depth=0 AND depth=1 but NOT by depth=2 --
    # the saving the cascade buys. Computed at render time so the
    # marker on the toy grid can never drift from the algo.
    saved = sorted(
        (popped_by_label['depth=0 (rule=none)']
         & popped_by_label['depth=1'])
        - popped_by_label['depth=2'])

    walls: list[tuple[int, int]] = []
    for c in range(1, 5):
        walls.append((1, c))
    for c in range(0, 5):
        walls.append((3, c))

    return {
        'rows': TOY_GRID_ROWS,
        'cols': TOY_GRID_COLS,
        'walls': walls,
        'start': TOY_START,
        'goal': TOY_GOAL,
        'cached': [TOY_CACHED_CELL],
        'saved': saved,
        'h_star_cached': h_star_cached,
        'runs': runs,
    }


def _toy_tikz_grid(rows: int, cols: int,
                   walls: list[tuple[int, int]],
                   start: tuple[int, int],
                   goal: tuple[int, int],
                   cached: list[tuple[int, int]],
                   saved: list[tuple[int, int]]) -> str:
    """
    ========================================================================
     Emit a TikZ block visualizing the toy grid. Cells are
     unit squares; row 0 at top (y flipped); walls black,
     start green, goal red, cached blue, saved (expanded by
     depth=0/1 but skipped by depth=2) yellow with a "x" mark.
    ========================================================================
    """
    walls_set = set(walls)
    cached_set = set(cached)
    saved_set = set(saved)
    cell_fills = []
    cell_labels = []
    for r in range(rows):
        for c in range(cols):
            y = -r
            if (r, c) in walls_set:
                cell_fills.append(
                    rf'  \fill[black] ({c},{y}) rectangle ({c+1},{y-1});')
            elif (r, c) == start:
                cell_fills.append(
                    rf'  \fill[green!45] ({c},{y}) rectangle ({c+1},{y-1});')
                cell_labels.append(
                    rf'  \node[font=\small\bfseries] at ({c+0.5},{y-0.5}) {{$S$}};')
            elif (r, c) == goal:
                cell_fills.append(
                    rf'  \fill[red!40] ({c},{y}) rectangle ({c+1},{y-1});')
                cell_labels.append(
                    rf'  \node[font=\small\bfseries] at ({c+0.5},{y-0.5}) {{$T$}};')
            elif (r, c) in cached_set:
                cell_fills.append(
                    rf'  \fill[blue!30] ({c},{y}) rectangle ({c+1},{y-1});')
                cell_labels.append(
                    rf'  \node[font=\small\bfseries] at ({c+0.5},{y-0.5}) {{$C$}};')
            elif (r, c) in saved_set:
                cell_fills.append(
                    rf'  \fill[yellow!55] ({c},{y}) rectangle ({c+1},{y-1});')
                cell_labels.append(
                    rf'  \node[font=\small\bfseries] at ({c+0.5},{y-0.5}) {{$\times$}};')
    grid_lines = (
        rf'  \foreach \r in {{0,...,{rows-1}}} '
        rf'\foreach \c in {{0,...,{cols-1}}} '
        rf'{{ \draw[gray!60] (\c,-\r) rectangle (\c+1,-\r-1); }}'
    )
    col_labels = '\n'.join(
        rf'  \node[font=\scriptsize,gray] at ({c+0.5},0.35) {{{c}}};'
        for c in range(cols))
    row_labels = '\n'.join(
        rf'  \node[font=\scriptsize,gray] at (-0.4,{-r-0.5}) {{{r}}};'
        for r in range(rows))
    return (
        '\\begin{tikzpicture}[scale=0.55]\n'
        + '\n'.join(cell_fills) + '\n'
        + grid_lines + '\n'
        + '\n'.join(cell_labels) + '\n'
        + col_labels + '\n'
        + row_labels + '\n'
        + '\\end{tikzpicture}'
    )


def build_toy_subsection(toy: dict) -> str:
    """
    ========================================================================
     Emit the toy subsection: explanatory text + TikZ grid +
     counters table + reading paragraph.
    ========================================================================
    """
    tikz = _toy_tikz_grid(
        rows=toy['rows'], cols=toy['cols'], walls=toy['walls'],
        start=toy['start'], goal=toy['goal'],
        cached=toy['cached'], saved=toy['saved'])
    runs = toy['runs']
    toy_metrics = ['cnt_expanded', 'cnt_bpmx_lifts', 'cnt_bpmx_attempts']
    col_min = {m: float(min(r[m] for r in runs)) for m in toy_metrics}
    col_max = {m: float(max(r[m] for r in runs)) for m in toy_metrics}
    rows_tex = []
    for r in runs:
        cells = [
            rf"{heat_cell(float(r[m]), col_min[m], col_max[m])}{r[m]:,}"
            for m in toy_metrics]
        rows_tex.append(rf"  {r['label']} & " + ' & '.join(cells) + r" \\")
    table_body = '\n'.join(rows_tex)
    h_star = toy['h_star_cached']
    saved_tex = ', '.join(
        rf"$({r},{c})$" for r, c in toy['saved']) or '---'
    return rf"""\subsection{{Toy: why \texttt{{depth=1}} lifts
nothing on consistent~$h$}}

\begin{{figure}}[H]
\centering
{tikz}
\caption{{Legend: $S$ start, $T$ goal,
$C$ cache ($h^{{*}}(C,T)={h_star:.0f}$),
$\times$ = expanded by \texttt{{depth=0}} and
\texttt{{depth=1}} but skipped by \texttt{{depth=2}}
({saved_tex}).}}
\end{{figure}}

\begin{{table}}[H]
\centering
\setlength{{\tabcolsep}}{{8pt}}
\begin{{tabular}}{{lrrr}}
\toprule
\textbf{{config}}
  & \textbf{{\texttt{{cnt\_expanded}}}}
  & \textbf{{\texttt{{cnt\_bpmx\_lifts}}}}
  & \textbf{{\texttt{{cnt\_bpmx\_attempts}}}} \\
\midrule
{table_body}
\bottomrule
\end{{tabular}}
\end{{table}}
"""


def metric_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns
            if c.startswith(('cnt_', 'pct_', 'mem_', 'elapsed_'))]


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     Inject derived counters into the per-row DataFrame.

     `pct_bpmx_lifts` is the per-row hit-rate
     `cnt_bpmx_lifts / cnt_bpmx_attempts * 100`, with 0/0 set
     to 0 (a row with no BPMX attempts has 0% lift rate by
     convention). Per-row division → aggregate-by-mean gives
     the "average lift rate across maps", which is the
     reading we want; mean(lifts) / mean(attempts) would
     size-weight by map and is a different quantity.
    ========================================================================
    """
    if ('cnt_bpmx_lifts' in df.columns
            and 'cnt_bpmx_attempts' in df.columns):
        att = df['cnt_bpmx_attempts'].astype(float)
        lifts = df['cnt_bpmx_lifts'].astype(float)
        rate = lifts / att.replace(0, np.nan) * 100.0
        df['pct_bpmx_lifts'] = rate.fillna(0.0)
    return df


# ── Figure (one per counter, single axis) ───────────────────────────────────

def _coincident_groups(per_kc: pd.DataFrame,
                       metric: str,
                       used: list[dict]) -> list[list[int]]:
    """
    ========================================================================
     Group configs whose (k -> value) series are bit-identical on
     this metric. Preserves CONFIGS order: each config belongs to
     the earliest already-formed group with a matching series, or
     starts a new group.

     Floating-point tolerance is 1e-9 of the larger magnitude --
     counters are deterministic means of integer per-map values,
     so true coincidences are exact; the tolerance only absorbs
     pandas / numpy round-trip noise.
    ========================================================================
    """
    series_by_idx: dict[int, list[tuple[int, float]]] = {}
    for idx, cfg in enumerate(used):
        sub = (per_kc[per_kc['config'] == cfg['tag']]
               .sort_values('m'))
        series_by_idx[idx] = [
            (int(k), float(v)) for k, v in zip(sub['m'], sub[metric])]

    def equal(s1, s2) -> bool:
        if len(s1) != len(s2):
            return False
        for (k1, v1), (k2, v2) in zip(s1, s2):
            if k1 != k2:
                return False
            tol = 1e-9 * max(abs(v1), abs(v2), 1.0)
            if abs(v1 - v2) > tol:
                return False
        return True

    groups: list[list[int]] = []
    placed: set[int] = set()
    for idx in range(len(used)):
        if idx in placed:
            continue
        group = [idx]
        placed.add(idx)
        for jdx in range(idx + 1, len(used)):
            if jdx in placed:
                continue
            if equal(series_by_idx[idx], series_by_idx[jdx]):
                group.append(jdx)
                placed.add(jdx)
        groups.append(group)
    return groups


def _group_label(group: list[int], used: list[dict]) -> str:
    """`depth=0` for solo, `depth=0/1` for 2-way, etc."""
    nums = [used[i]['label'].replace('depth=', '') for i in group]
    return 'depth=' + '/'.join(nums)


def _diff_annotations(per_kc: pd.DataFrame,
                      metric: str,
                      used: list[dict],
                      is_log: bool) -> str:
    """
    ========================================================================
     Dotted vertical spans at each $k$ in `_ANNOT_K`, drawn from
     the second-highest visible line up to the highest at that $k$.
     Visible lines are the coincident GROUPS (so merged curves
     count once). Each span is labelled with the top-two gap --
     a percentage when the top is $<100\\%$ larger, else a
     $\\times$ multiplier -- and the highest line is tagged with
     its short id (e.g. \\texttt{d=0}). Skips a $k$ when fewer
     than two groups have data, when the top two coincide (no
     visible gap), or when a log axis would need a non-positive
     endpoint.
    ========================================================================
    """
    groups = _coincident_groups(per_kc, metric, used)
    out: list[str] = []
    k_right = max(_ANNOT_K)
    for k in _ANNOT_K:
        gv: list[tuple[float, list[int]]] = []
        for g in groups:
            mask = ((per_kc['config'] == used[g[0]]['tag'])
                    & (per_kc['m'] == k))
            if mask.any():
                gv.append((float(per_kc.loc[mask, metric].iloc[0]), g))
        if len(gv) < 2:
            continue
        gv.sort(key=lambda t: t[0], reverse=True)
        top_val, top_g = gv[0]
        second_val = gv[1][0]
        if top_val - second_val <= 1e-9 * max(abs(top_val), 1.0):
            continue
        if is_log and (top_val <= 0 or second_val <= 0):
            continue
        # Gap label: percentage if top is <100% larger, else x-fold.
        if second_val > 0:
            pct = (top_val / second_val - 1.0) * 100.0
            diff_txt = (rf'{pct:.0f}\%' if pct < 100.0
                        else rf'{top_val / second_val:.1f}$\times$')
        else:
            diff_txt = fmt_value(metric, top_val - second_val)
        d_label = _group_label(top_g, used).replace('depth=', 'd=')
        if is_log:
            mid = (top_val * second_val) ** 0.5
        else:
            mid = (top_val + second_val) / 2.0
        side = 'west' if k < k_right else 'east'
        xsh = '2pt' if side == 'west' else '-2pt'
        d_anchor = 'south' if k < k_right else 'south east'
        out.append(
            rf'\draw[dotted, thick, |-|] '
            rf'(axis cs:{k},{second_val:.6g}) -- '
            rf'(axis cs:{k},{top_val:.6g});')
        out.append(
            rf'\node[anchor={side}, font=\scriptsize, fill=white, '
            rf'fill opacity=0.85, text opacity=1, inner sep=1pt, '
            rf'xshift={xsh}] at (axis cs:{k},{mid:.6g}) {{{diff_txt}}};')
        out.append(
            rf'\node[anchor={d_anchor}, font=\scriptsize\bfseries, '
            rf'inner sep=1pt, yshift=2pt] '
            rf'at (axis cs:{k},{top_val:.6g}) {{{d_label}}};')
    return '\n'.join(out)


def panel_addplots(per_kc: pd.DataFrame,
                   metric: str,
                   used: list[dict]) -> tuple[str, list[str]]:
    """
    ========================================================================
     Emit one \\addplot per config, with COINCIDENT configs merged
     into a single visual line as overlaid offset-dash plots so
     the colors alternate in 4pt segments (e.g. d=0 light-blue +
     d=1 medium-light-blue dashed together when both produce
     identical curves).
     Returns (addplots_string, legend_labels) -- the legend
     entries are 1-per-group, not 1-per-config, with combined
     labels like `depth=0/1`.

     Markers are dropped globally: dashed overlays interleave
     visually only without per-point marker glyphs clashing with
     the dash pattern; the per-k tables already carry the exact
     numbers.
    ========================================================================
    """
    groups = _coincident_groups(per_kc, metric, used)
    seg = 4  # pt; segment length per color in striped overlay
    lines: list[str] = []
    legend_labels: list[str] = []
    for group in groups:
        # Coords are the same across the group by construction.
        anchor_idx = group[0]
        sub = (per_kc[per_kc['config'] == used[anchor_idx]['tag']]
               .sort_values('m'))
        coords = ' '.join(
            f'({int(k)},{float(v):.6g})'
            for k, v in zip(sub['m'], sub[metric]))
        if len(group) == 1:
            idx = anchor_idx
            lines.append(
                rf"\addplot[color=cfgcolor{idx}, no markers, "
                rf"line width=1.0pt] coordinates {{{coords}}};")
        else:
            off = (len(group) - 1) * seg
            for i, idx in enumerate(group):
                phase = i * seg
                forget = (', forget plot'
                          if i < len(group) - 1 else '')
                lines.append(
                    rf"\addplot[color=cfgcolor{idx}, no markers, "
                    rf"line width=1.2pt, "
                    rf"dash pattern=on {seg}pt off {off}pt, "
                    rf"dash phase={phase}pt{forget}] "
                    rf"coordinates {{{coords}}};")
        legend_labels.append(_group_label(group, used))
    return '\n'.join(lines), legend_labels


def color_definitions(used: list[dict]) -> str:
    """`\\definecolor{cfgcolorN}{HTML}{RRGGBB}` for every config.
    Named refs are the safe xcolor syntax (inline `{HTML,...}`
    is rejected by xcolor's color-name parser)."""
    return '\n'.join(
        rf"\definecolor{{cfgcolor{idx}}}{{HTML}}{{{cfg['color']}}}"
        for idx, cfg in enumerate(used))


def build_insight(metric: str,
                  overall: pd.DataFrame,
                  used: list[dict],
                  k_max: int) -> str:
    """
    ========================================================================
     Curated semantic description + auto-computed min/max
     observation at $k=k_{\\max}$ (overall mean across all 25
     maps). Skips the observation when the metric is
     uniformly zero or all configs share a single value.
    ========================================================================
    """
    desc = _COUNTER_INFO.get(metric, '')
    pairs: list[tuple[str, float]] = []
    for cfg in used:
        mask = overall['config'] == cfg['tag']
        if mask.any():
            pairs.append(
                (cfg['label'], float(overall.loc[mask, metric].iloc[0])))
    if not pairs:
        return desc
    vmin = min(v for _, v in pairs)
    vmax = max(v for _, v in pairs)
    if vmax == 0 or vmin == vmax:
        return desc
    lab_min = next(lab for lab, v in pairs if v == vmin)
    lab_max = next(lab for lab, v in pairs if v == vmax)
    if vmin > 0:
        ratio = vmax / vmin
        obs = (rf'At $k={k_max}$, mean across all 25~maps: '
               rf'min $= {fmt_value(metric, vmin)}$ ({lab_min}); '
               rf'max $= {fmt_value(metric, vmax)}$ ({lab_max}); '
               rf'spread $\approx {ratio:.2g}\times$.')
    else:
        obs = (rf'At $k={k_max}$, mean across all 25~maps: '
               rf'max $= {fmt_value(metric, vmax)}$ ({lab_max}); '
               rf'other configs at or near zero.')
    sep = ' ' if desc else ''
    return desc + sep + obs


def build_single_figure(metric: str,
                        per_kc: pd.DataFrame,
                        used: list[dict]) -> str:
    """
    ========================================================================
     Single-axis line chart for one counter: N config-colored
     curves of the (config, k) mean across all 25 maps. Log-y
     applied automatically when the dynamic range exceeds one
     decade. `pct_*` metrics use a percent y-label.
    ========================================================================
    """
    vals = per_kc[metric].astype(float).to_numpy()
    is_pct = metric.startswith('pct_')
    # Linear y for percentages (bounded [0, 100]); auto-log
    # only when the dynamic range exceeds one decade on a
    # numeric-magnitude metric.
    is_log = (not is_pct) and should_log(vals)
    ymode_opt = 'ymode=log, ' if is_log else ''
    if is_pct:
        ylabel = (r'mean \texttt{' + tex_esc(metric)
                  + r'} (\%)')
    else:
        ylabel = r'mean \texttt{' + tex_esc(metric) + r'}'
    addplots, legend_labels = panel_addplots(per_kc, metric, used)
    legend_entries = ', '.join(legend_labels)
    annotations = _diff_annotations(per_kc, metric, used, is_log)
    caption_body = _CAPTION_INSIGHT.get(metric, _DEFAULT_CAPTION_BODY)
    # NOTE: keep the axis-options block on contiguous lines
    # (no blank line allowed inside `\begin{axis}[...]` --
    # TeX treats it as `\par` and closes the options early).
    return rf"""\begin{{figure}}[H]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
    width=11.5cm, height=5.6cm,
    xlabel={{$k$}},
    ylabel={{{ylabel}}},
    {ymode_opt}grid=both,
    tick label style={{font=\scriptsize}},
    label style={{font=\small}},
    every axis plot/.append style={{line width=0.9pt}},
    legend style={{font=\tiny, fill=white, fill opacity=0.92,
                   at={{(1.02,1.0)}}, anchor=north west}},
    legend cell align=left,
]
{addplots}
\legend{{{legend_entries}}}
{annotations}
\end{{axis}}
\end{{tikzpicture}}
\caption{{\textbf{{\texttt{{{tex_esc(metric)}}} --- mean vs.~$k$.}}\\
{caption_body}}}
\end{{figure}}
"""


def render_counter(metric: str,
                   per_kc: pd.DataFrame,
                   overall: pd.DataFrame,
                   used: list[dict],
                   k_values: list[int],
                   k_max: int) -> str:
    """
    ========================================================================
     Render one counter as a self-contained subsection:
     semantic description + data-driven observation + line
     chart + per-$k$ table. Each subsection is the unit the
     reader scans.
    ========================================================================
    """
    insight = build_insight(metric=metric, overall=overall,
                            used=used, k_max=k_max)
    fig = build_single_figure(metric=metric, per_kc=per_kc,
                              used=used)
    tab = build_table_for_metric(per_kc=per_kc, used=used,
                                 metric=metric, k_values=k_values)
    return rf"""\subsection{{\texttt{{{tex_esc(metric)}}}}}
{insight}

{fig}

{tab}
"""


# ── Tables (one per counter; rows = depth, cols = k) ────────────────────────

def build_table_for_metric(per_kc: pd.DataFrame,
                           used: list[dict],
                           metric: str,
                           k_values: list[int]) -> str:
    """
    ========================================================================
     Rows = configs (depths), cols = k snapshots. Each cell
     is the mean across all 25 maps at that k (already pre-
     aggregated in `per_kc`). The line chart shows the full
     progression; this table snapshots specific k values.
    ========================================================================
    """
    head = ' & '.join(
        [r'\textbf{depth}']
        + [rf'\textbf{{$k{{=}}{k}$}}' for k in k_values]
    )
    # Raw value grid (rows = configs, cols = k). Column-wise
    # min/max drive the heatmap shading (red = larger within the
    # column, green = smaller), so each $k$ column is ranked
    # across the depth rows.
    raw: list[list[float]] = []
    for cfg in used:
        vals_row = []
        for k in k_values:
            mask = ((per_kc['config'] == cfg['tag'])
                    & (per_kc['m'] == k))
            v = (float(per_kc.loc[mask, metric].iloc[0])
                 if mask.any() else 0.0)
            vals_row.append(v)
        raw.append(vals_row)
    col_min, col_max = [], []
    for j in range(len(k_values)):
        col = [raw[i][j] for i in range(len(used))
               if np.isfinite(raw[i][j])]
        col_min.append(min(col) if col else 0.0)
        col_max.append(max(col) if col else 0.0)
    rows = []
    for i, cfg in enumerate(used):
        cells = []
        for j in range(len(k_values)):
            v = raw[i][j]
            shade = heat_cell(v, col_min[j], col_max[j])
            cells.append(f'{shade}{fmt_value(metric, v)}')
        rows.append(rf'  {cfg["label"]} & ' + ' & '.join(cells) + r' \\')
    n_cols = len(k_values) + 1
    align = 'l' + 'r' * (n_cols - 1)
    return rf"""\begin{{table}}[H]
\centering
\caption{{\textbf{{\texttt{{{tex_esc(metric)}}} --- mean across 25~maps
at selected~$k$.}}\\Rows are BPMX cascade depths (depth=0 is the
BPMX-off baseline); columns are $k$ snapshots.}}
\small
\setlength{{\tabcolsep}}{{6pt}}
\begin{{tabular}}{{{align}}}
\toprule
{head} \\
\midrule
{chr(10).join(rows)}
\bottomrule
\end{{tabular}}
\end{{table}}
"""


# ── Section assembly ────────────────────────────────────────────────────────

def build_section(df: pd.DataFrame,
                  per_kc: pd.DataFrame,
                  overall: pd.DataFrame,
                  used: list[dict],
                  metric_cols: list[str],
                  nontrivial: set[str],
                  omitted_user: list[str],
                  k_values: list[int],
                  k_max: int) -> str:
    depth_list = ', '.join(cfg['label'] for cfg in used)
    color_defs = color_definitions(used)
    setup = rf"""\section{{Experimental Results --- BPMX depth ladder}}

{color_defs}

\paragraph{{Setup.}} \texttt{{AStarIncMOSPP}} compared across
{len(used)}~BPMX depths ({depth_list}). \textbf{{All BPMX-active
configs use \texttt{{rule\_bpmx='1'}}; \texttt{{depth=0}} is the
BPMX-off baseline (rule\_none), deeper $d$ = deeper cascade
reach.}} Configs are referred to by depth alone in the
legends and tables below. Shared params:
\texttt{{depth\_prop=0}}, \texttt{{order\_starts='given'}},
\texttt{{carry\_cache=True}}, \texttt{{carry\_bounds=False}}.
Problem set: 500~OMSPP instances ($=$ 5~domains $\times$
5~maps $\times$ 20~$k$-values $\in
\{{10, 20, \ldots, 200\}}$, Moving~AI grids), flipped to
MOSPP via \texttt{{ProblemSPP.flipped()}}. CSVs are
nested-chain output: each row is the cumulative counter
state after $k$ starts on its map. Each subsection below
covers one counter: a short description and a min/max
observation at $k={k_max}$, followed by its line chart
and per-$k$ table.

\paragraph{{Color \& line convention.}} Monotone blue gradient
with perceptually-even steps so all six lines remain
distinguishable even when they sit close together on a chart:
\textbf{{\textcolor[HTML]{{6BAED6}}{{depth=0 (light blue)}}}}
$=$ BPMX off,
\textbf{{\textcolor[HTML]{{4292C6}}{{depth=1 (medium-light blue)}}}}
$=$ BPMX on but inert on consistent $h$,
\textbf{{\textcolor[HTML]{{2171B5}}{{depth=2 (medium blue)}}}}
$=$ cascade fires,
\textbf{{\textcolor[HTML]{{08519C}}{{depth=3 (dark blue)}}}}
$=$ deeper cascade,
\textbf{{\textcolor[HTML]{{08306B}}{{depth=4 (darkest canonical)}}}}
$=$ near-saturation,
\textbf{{\textcolor[HTML]{{041F4B}}{{depth=5 (very dark navy)}}}}
$=$ gains saturated. Each step is strictly darker than the
previous (Colorbrewer Blues9-5..9 plus a custom navy at the
deepest rung), so the reader can rank depth at a glance.
When two or more configs coincide exactly on a counter, their
curves are merged into a single line that alternates 4\,pt
segments of each config's color (e.g.~\texttt{{depth=0/1}}
reads as a light-blue~--~medium-light-blue dashed band). The
legend entry shows the merged label (\texttt{{depth=0/1}},
\texttt{{depth=0/1/2/3/4/5}}, etc.) so the coincidence is
visible without consulting the table.

\paragraph{{Table shading.}} In every results table each cell is
shaded by its value relative to the other cells in the same
column: \textbf{{\textcolor[HTML]{{F8696B}}{{red}}}} $=$ largest,
\textbf{{\textcolor[HTML]{{D9C24A}}{{yellow}}}} $=$ middle,
\textbf{{\textcolor[HTML]{{63BE7B}}{{green}}}} $=$ smallest; a
column whose values are all equal is left unshaded.

\paragraph{{Chart annotations.}} In every line chart, dotted
vertical spans at $k=100$ and $k=200$ mark the gap between the
two highest lines at that $k$, labelled with their relative
difference (a percentage when the top line is $<100\%$ larger,
otherwise an $N\times$ multiplier). The short tag at the top of
each span (e.g.~\texttt{{d=0}}) names the highest line.
"""
    omitted_zero = sorted(set(metric_cols)
                          - nontrivial
                          - set(omitted_user))
    if omitted_zero:
        setup += (rf"""
\paragraph{{Omitted (uniformly zero across every config).}}
""" + ', '.join(rf'\texttt{{{tex_esc(m)}}}' for m in omitted_zero)
                  + '.\n')
    if omitted_user:
        setup += (rf"""
\paragraph{{Omitted (excluded by author choice).}}
""" + ', '.join(rf'\texttt{{{tex_esc(m)}}}' for m in omitted_user)
                  + '.\n')

    blocks = [setup]
    # Toy example -- explains depth=0 == depth=1 vs. depth=2
    # mechanism in miniature, before the macro per-counter
    # comparison.
    toy = run_toy_example()
    blocks.append(build_toy_subsection(toy))
    for _, metrics in COUNTER_GROUPS:
        for m in metrics:
            if m in nontrivial:
                blocks.append(
                    render_counter(metric=m, per_kc=per_kc,
                                   overall=overall, used=used,
                                   k_values=k_values, k_max=k_max))
    return '\n\n'.join(blocks)


# ── Splice into MOSPP.tex ───────────────────────────────────────────────────

def splice(tex: str, new_section: str) -> str:
    # 1. Add pgfplots packages if missing.
    pkg_block = ('\\usepackage{pgfplots}\n'
                 '\\pgfplotsset{compat=1.18}\n'
                 '\\usepgfplotslibrary{groupplots}\n')
    if r'\usepackage{pgfplots}' not in tex:
        tex = tex.replace(
            '\\usepackage{float}',
            '\\usepackage{float}\n' + pkg_block,
            1)
    # 2. Add the mandatory \me / \you block if missing.
    me_block = (
        '\n% -- Author annotations (draft only) --\n'
        '\\newif\\ifdraft\\drafttrue\n'
        '\\newcommand{\\me}[1]{%\n'
        '    \\ifdraft\\textcolor{red}{\\textbf{[me:\\,#1]}}\\fi%\n'
        '}\n'
        '\\newcommand{\\you}[1]{%\n'
        '    \\ifdraft\\textcolor{blue}{\\textbf{[you:\\,#1]}}\\fi%\n'
        '}\n'
    )
    if '\\newcommand{\\me}' not in tex:
        tex = tex.replace(
            '\\begin{document}',
            me_block + '\n\\begin{document}',
            1)
    # 3. Idempotent: strip the prior "Experimental Results"
    #    section if present, then insert the new one before
    #    \end{document}.
    for marker in (
            r'\section{Experimental Results --- BPMX depth ladder}',
            r'\section{Experimental Results}'):
        if marker in tex:
            i = tex.index(marker)
            j = tex.index('\\end{document}', i)
            tex = tex[:i] + tex[j:]
            break
    tex = tex.replace(
        '\\end{document}',
        new_section + '\n\n\\end{document}',
        1)
    return tex


def sanitize_ascii(text: str) -> tuple[str, dict[str, int]]:
    """ASCII-only sanitizer for Overleaf upload."""
    counts = {c: text.count(c) for c in ['─', '═']}
    text = text.replace('─', '-').replace('═', '=')
    return text, counts
