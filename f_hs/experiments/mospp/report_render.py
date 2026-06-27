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
    _TITLES, _INSIGHT_ITEMS, _COUNTER_NEUTRAL,
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
    h = lambda s: float(s.key.distance(p_seed.goals[0].key))
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

    # f-value story for the single skipped cell, all computed at
    # render time so it can never drift from the toy: optimal cost
    # C* (any run's cost; BPMX preserves optimality), g(START->cell),
    # base Manhattan h(cell->T), and the depth-2 BPMX lift from the
    # one-step-away cached cell (h*(C) - dist).
    c_star = float(runs[0]['cost'])
    saved_detail: dict | None = None
    if len(saved) == 1:
        sc = saved[0]
        cell = grid[sc[0]][sc[1]]
        p_g = ProblemGrid(grid=grid,
                          start=grid[TOY_START[0]][TOY_START[1]],
                          goal=cell)
        a_g = AStarLookup(problem=p_g,
                          h=lambda s: float(s.key.distance(p_g.goals[0].key)),
                          goal=p_g.goals[0])
        g_saved = float(a_g.run().cost)
        h_base = float(cell.distance(goal_cell))
        dist_cache = float(abs(sc[0] - TOY_CACHED_CELL[0])
                           + abs(sc[1] - TOY_CACHED_CELL[1]))
        h_lift = max(h_base, float(h_star_cached) - dist_cache)
        saved_detail = {
            'cell': sc, 'g': g_saved, 'h_base': h_base,
            'dist_cache': dist_cache, 'h_lift': h_lift,
            'c_star': c_star,
        }

    return {
        'rows': TOY_GRID_ROWS,
        'cols': TOY_GRID_COLS,
        'walls': walls,
        'start': TOY_START,
        'goal': TOY_GOAL,
        'cached': [TOY_CACHED_CELL],
        'saved': saved,
        'h_star_cached': h_star_cached,
        'c_star': c_star,
        'saved_detail': saved_detail,
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


def build_toy_subsection(toy: dict) -> tuple[str, tuple[str, str]]:
    """
    ========================================================================
     Emit the toy subsection: explanatory text + TikZ grid +
     counters table + reading paragraph. Returns
     `(subsection, ('fig_toy', standalone))` -- the grid TikZ is
     externalized like the per-counter charts.
    ========================================================================
    """
    grid_tikz = _toy_tikz_grid(
        rows=toy['rows'], cols=toy['cols'], walls=toy['walls'],
        start=toy['start'], goal=toy['goal'],
        cached=toy['cached'], saved=toy['saved'])
    toy_standalone = standalone_doc(grid_tikz)
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
    # f-value reading of the skipped cell (answers "why expanded at
    # d<=1 but pruned at d=2"): the depth-2 BPMX lift pushes f above
    # C*. All numbers render-computed in `run_toy_example`.
    sd = toy.get('saved_detail')
    if sd:
        r, c = sd['cell']
        g, hb, hl = sd['g'], sd['h_base'], sd['h_lift']
        cs, hs, dc = sd['c_star'], float(h_star), sd['dist_cache']
        fval_prose = (
            rf"""
\paragraph{{Reading the skipped cell.}} Cell $({r},{c})$ has
$g={g:g}$ and base (Manhattan) $h={hb:g}$, so $f=g+h={g + hb:g}
=C^{{*}}={cs:g}$: it sits exactly on the optimal frontier, so
\texttt{{depth=0/1}} expand it --- a depth-1 sweep cannot lift on a
consistent base~$h$. \texttt{{depth=2}}'s cascade lifts its
heuristic via the one-step-away cache to
$\max({hb:g},\,h^{{*}}(C){{-}}{dc:g})=\max({hb:g},\,{hs:g}{{-}}{dc:g})={hl:g}$,
giving $f={g:g}+{hl:g}={g + hl:g}>C^{{*}}$, so it is pruned.
"""
        )
    else:
        fval_prose = ''
    sub = rf"""\subsection{{Toy: why \texttt{{depth=1}} lifts
nothing on consistent~$h$}}

\begin{{figure}}[H]
\centering
\includegraphics{{fig_toy}}
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
{fval_prose}"""
    return sub, ('fig_toy', toy_standalone)


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

     `pct_adapt_lifts` is the symmetric Adaptive-A* harvest
     hit-rate (`cnt_adapt_lifts / cnt_adapt_attempts * 100`),
     built the same per-row way.
    ========================================================================
    """
    if ('cnt_bpmx_lifts' in df.columns
            and 'cnt_bpmx_attempts' in df.columns):
        att = df['cnt_bpmx_attempts'].astype(float)
        lifts = df['cnt_bpmx_lifts'].astype(float)
        rate = lifts / att.replace(0, np.nan) * 100.0
        df['pct_bpmx_lifts'] = rate.fillna(0.0)
    if ('cnt_adapt_lifts' in df.columns
            and 'cnt_adapt_attempts' in df.columns):
        att = df['cnt_adapt_attempts'].astype(float)
        lifts = df['cnt_adapt_lifts'].astype(float)
        rate = lifts / att.replace(0, np.nan) * 100.0
        df['pct_adapt_lifts'] = rate.fillna(0.0)
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
    """
    ========================================================================
     Combined legend label for a coincident group. A depth ladder
     shares a `depth=` prefix, so a 2-way merge factors it out and
     reads `depth=0/1`. The mechanism-comparison section instead
     carries categorical labels (`depth=0`, `rule 1`, ...) with no
     shared `x=` prefix; those are joined whole (`depth=0/rule 1`),
     which still reads as "these curves coincide". A solo group is
     just its own label.
    ========================================================================
    """
    labels = [used[i]['label'] for i in group]
    if len(labels) == 1:
        return labels[0]
    # Shared `head=` prefix (every member is `head=<tail>`)? Factor
    # it so the depth ladders keep their compact `depth=0/1` form.
    if all('=' in lab for lab in labels):
        heads = {lab.split('=', 1)[0] for lab in labels}
        if len(heads) == 1:
            head = next(iter(heads))
            tails = [lab.split('=', 1)[1] for lab in labels]
            return f'{head}=' + '/'.join(tails)
    return '/'.join(labels)


def _diff_annotations(per_kc: pd.DataFrame,
                      metric: str,
                      used: list[dict],
                      is_log: bool) -> str:
    """
    ========================================================================
     Dotted vertical spans at each $k$ in `_ANNOT_K`, drawn from
     the second-highest visible line up to the highest at that $k$.
     Visible lines are the coincident GROUPS (so merged curves
     count once). Each span is labelled with the ratio of the
     higher line to the second as an $N\\times$ multiplier (e.g.
     $1.77\\times$). The line-id tags now live at each line's
     left start (see `_start_labels`), not on these spans. Skips
     a $k$ when fewer than two groups have data, when the top two
     coincide (no visible gap), or when a log axis would need a
     non-positive endpoint.
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
        top_val = gv[0][0]
        second_val = gv[1][0]
        if top_val - second_val <= 1e-9 * max(abs(top_val), 1.0):
            continue
        if is_log and (top_val <= 0 or second_val <= 0):
            continue
        # Gap label: the ratio of the higher line to the second as
        # an N-fold multiplier (e.g. 1.77x). Always a multiplier so
        # the annotation is unambiguous about direction and never
        # disagrees with the caption's framing of the same gap.
        if second_val > 0:
            diff_txt = rf'{top_val / second_val:.2f}$\times$'
        else:
            diff_txt = fmt_value(metric, top_val - second_val)
        if is_log:
            mid = (top_val * second_val) ** 0.5
        else:
            mid = (top_val + second_val) / 2.0
        side = 'west' if k < k_right else 'east'
        xsh = '2pt' if side == 'west' else '-2pt'
        out.append(
            rf'\draw[dotted, thick, |-|] '
            rf'(axis cs:{k},{second_val:.6g}) -- '
            rf'(axis cs:{k},{top_val:.6g});')
        out.append(
            rf'\node[anchor={side}, font=\scriptsize, fill=white, '
            rf'fill opacity=0.85, text opacity=1, inner sep=1pt, '
            rf'xshift={xsh}] at (axis cs:{k},{mid:.6g}) {{{diff_txt}}};')
    return '\n'.join(out)


def _start_labels(per_kc: pd.DataFrame,
                  metric: str,
                  used: list[dict],
                  is_log: bool) -> str:
    """
    ========================================================================
     Inline line-id tags (e.g. \\texttt{d=0}) drawn ONCE at the
     left start of each visible line -- replacing the per-$k$ tags
     that used to sit on the gap spans at $k=100/200$.

     Which lines get a tag is decided at the MIDDLE $k$ (the median
     of the k-grid -- $k=100$ here), where the lines are spread
     enough to rank but not yet maximally fanned out: the topmost
     line is always tagged; every lower line is tagged only when it
     sits at least $1.1\\times$ below the line IMMEDIATELY above it
     at that middle $k$, so a cluster of near-coincident neighbours
     collapses to a single tag and the start margin stays readable.
     The tag is then placed just above the line's leftmost point;
     lines left untagged remain identifiable via the legend.

     Visible lines are the coincident GROUPS, so a merged curve
     (e.g. \\texttt{d=0/1}) carries one combined tag.
    ========================================================================
    """
    groups = _coincident_groups(per_kc, metric, used)
    ks = sorted(int(k) for k in per_kc['m'].unique())
    if not ks:
        return ''
    start_k = ks[0]
    mid_k = ks[(len(ks) - 1) // 2]

    def val_at(g: list[int], k: int) -> float | None:
        mask = ((per_kc['config'] == used[g[0]]['tag'])
                & (per_kc['m'] == k))
        if not mask.any():
            return None
        return float(per_kc.loc[mask, metric].iloc[0])

    # Rank visible groups top-to-bottom by their MIDDLE-k value.
    ranked: list[tuple[float, list[int]]] = []
    for g in groups:
        v = val_at(g, mid_k)
        if v is not None:
            ranked.append((v, g))
    if not ranked:
        return ''
    ranked.sort(key=lambda t: t[0], reverse=True)

    # Greedy top-down keep: the top line always; a lower line only
    # when its ratio to the line IMMEDIATELY above it is >= 1.1x.
    keep: list[list[int]] = []
    for i, (v, g) in enumerate(ranked):
        if i == 0:
            keep.append(g)
            continue
        v_above = ranked[i - 1][0]
        if v > 0 and v_above / v >= 1.1:
            keep.append(g)

    out: list[str] = []
    for g in keep:
        y = val_at(g, start_k)
        if y is None or (is_log and y <= 0):
            continue
        d_label = _group_label(g, used).replace('depth=', 'd=')
        # Sit the tag a little ABOVE the line's start point
        # (south-west anchor + upward yshift), so it clears the
        # curve rather than overprinting it.
        out.append(
            rf'\node[anchor=south west, font=\scriptsize\bfseries, '
            rf'fill=white, fill opacity=0.85, text opacity=1, '
            rf'inner sep=1pt, xshift=2pt, yshift=2pt] '
            rf'at (axis cs:{start_k},{y:.6g}) {{{d_label}}};')
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


def standalone_doc(body: str, color_defs: str = '') -> str:
    """
    ========================================================================
     Wrap a TikZ / PGFPlots `body` in a `standalone` document so it
     compiles to a single tightly-cropped PDF (an "externalized"
     figure). The preamble mirrors the report's font + math + color
     setup so the externalized image is faithful to the former
     inline render; `color_defs` injects the per-config
     \\texttt{cfgcolorN} definitions the plot curves reference.

     Externalizing the heavy PGFPlots figures lets Overleaf render
     the report by \\includegraphics-ing pre-built PDFs instead of
     re-running PGFPlots on every compile -- which is what blew the
     Overleaf compile timeout (the same document builds in ~2.5s
     under `tectonic` locally).
    ========================================================================
    """
    return rf"""\documentclass[border=3pt]{{standalone}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\usepackage{{amsmath, amssymb}}
\usepackage{{xcolor}}
\usepackage{{pgfplots}}
\pgfplotsset{{compat=1.18}}
\usetikzlibrary{{arrows.meta, positioning, calc}}
{color_defs}
\begin{{document}}
{body}
\end{{document}}
"""


def build_insight(metric: str, rule_key: str = 'rule1') -> str:
    """
    ========================================================================
     The curated Insights box for one counter in one rule
     section: a numbered `sentences` list inside the lightblue
     `insights` callout. Items come from
     `_INSIGHT_ITEMS[rule_key][metric]`; a (rule, counter) with
     no curated items falls back to the rule-agnostic
     `_COUNTER_NEUTRAL` one-liner (e.g. rule_3 / cascade before
     their data lands).
    ========================================================================
    """
    items = _INSIGHT_ITEMS.get(rule_key, {}).get(metric)
    if not items:
        neutral = _COUNTER_NEUTRAL.get(metric, '')
        items = [neutral] if neutral else []
    if not items:
        return ''
    body = '\n'.join(rf'\item {it}' for it in items)
    return ('\\begin{insights}\n'
            '\\begin{sentences}\n'
            f'{body}\n'
            '\\end{sentences}\n'
            '\\end{insights}')


def build_single_figure(metric: str,
                        per_kc: pd.DataFrame,
                        used: list[dict],
                        rule_key: str = '') -> tuple[str, tuple[str, str]]:
    """
    ========================================================================
     Single-axis line chart for one counter: N config-colored
     curves of the (config, k) mean across all 25 maps. Log-y
     applied automatically when the dynamic range exceeds one
     decade. `pct_*` metrics use a percent y-label.

     The PGFPlots body is externalized: returns
     `(figure_float, (fig_name, standalone_source))` where the
     float \\includegraphics-es `fig_name` and `standalone_source`
     is the self-contained doc the orchestrator compiles to
     `fig_name.pdf`. Externalizing keeps the heavy plot off
     Overleaf's compile path.
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
    start_labels = _start_labels(per_kc, metric, used, is_log)
    caption_body = _CAPTION_INSIGHT.get(metric, _DEFAULT_CAPTION_BODY)
    # NOTE: keep the axis-options block on contiguous lines
    # (no blank line allowed inside `\begin{axis}[...]` --
    # TeX treats it as `\par` and closes the options early).
    tikz = rf"""\begin{{tikzpicture}}
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
{start_labels}
\end{{axis}}
\end{{tikzpicture}}"""
    fig_name = f'fig_{rule_key}_{metric}' if rule_key else f'fig_{metric}'
    standalone = standalone_doc(tikz, color_definitions(used))
    figure = rf"""\begin{{figure}}[H]
\centering
\includegraphics{{{fig_name}}}
\caption{{Line chart.}}
\end{{figure}}
"""
    return figure, (fig_name, standalone)


def render_counter(metric: str,
                   per_kc: pd.DataFrame,
                   used: list[dict],
                   k_values: list[int],
                   rule_key: str = 'rule1') -> tuple[str, tuple[str, str]]:
    """
    ========================================================================
     Render one counter as a self-contained subsection:
     semantic description + data-driven observation + line
     chart + per-$k$ table. Each subsection is the unit the
     reader scans. Returns `(subsection, (fig_name, standalone))`
     -- the externalized line chart travels alongside the prose.
    ========================================================================
    """
    insight = build_insight(metric=metric, rule_key=rule_key)
    fig, fig_art = build_single_figure(metric=metric, per_kc=per_kc,
                                       used=used, rule_key=rule_key)
    tab = build_table_for_metric(per_kc=per_kc, used=used,
                                 metric=metric, k_values=k_values)
    title = _TITLES.get(metric, rf'\texttt{{{tex_esc(metric)}}}')
    sub = rf"""\subsection{{{title}}}
{fig}

{tab}

{insight}
"""
    return sub, fig_art


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
\caption{{Data results.}}
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

def build_section(per_kc: pd.DataFrame,
                  used: list[dict],
                  nontrivial: set[str],
                  k_values: list[int],
                  rule_key: str,
                  section_title: str,
                  intro: str = ''
                  ) -> tuple[str, list[tuple[str, str]]]:
    """
    ========================================================================
     One report SECTION (a BPMX-rule depth ladder): a `\\section`
     header (`Experimental Results --- {section_title}`) followed
     directly by one per-counter subsection (figure + table +
     Insights box). `rule_key` selects the rule-specific insight
     text and prefixes the externalized figure names
     (`fig_{rule_key}_{metric}`) so sections never collide.
     Setup/convention paragraphs + the Toy + excluded counters
     are all dropped. `intro`, when given (the mechanism-comparison
     section uses it), is an opt-in framing paragraph emitted right
     after the header; other sections pass '' and are unchanged.
    ========================================================================
    """
    setup = rf'\section{{Experimental Results --- {section_title}}}'
    blocks = [setup]
    if intro:
        blocks.append(intro)
    figures: list[tuple[str, str]] = []
    for _, metrics in COUNTER_GROUPS:
        for m in metrics:
            if m in nontrivial:
                sub, fig = render_counter(
                    metric=m, per_kc=per_kc, used=used,
                    k_values=k_values, rule_key=rule_key)
                blocks.append(sub)
                figures.append(fig)
    return '\n\n'.join(blocks), figures


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
    # 2b. Insights callout box + its colors / list style, if the
    #     base predates them (idempotent: each guarded by a probe).
    if '\\usepackage{tcolorbox}' not in tex:
        tex = tex.replace(
            '\\begin{document}',
            '\\usepackage{tcolorbox}\n'
            '\\tcbuselibrary{skins, breakable}\n\n\\begin{document}', 1)
    if '\\definecolor{lightblue}' not in tex:
        tex = tex.replace(
            '\\begin{document}',
            '\\definecolor{accentblue}{RGB}{30, 90, 160}\n'
            '\\definecolor{lightblue}{RGB}{220, 235, 252}\n\n'
            '\\begin{document}', 1)
    if '\\newlist{sentences}' not in tex:
        tex = tex.replace(
            '\\begin{document}',
            '\\newlist{sentences}{enumerate}{1}\n'
            '\\setlist[sentences]{label=\\textbf{\\color{accentblue}'
            '(\\arabic*)}, leftmargin=2.4em, itemsep=3pt, '
            'parsep=0pt, topsep=4pt}\n\n\\begin{document}', 1)
    if '\\newtcolorbox{insights}' not in tex:
        ins = (
            '\n% -- Insights callout box --\n'
            '\\newtcolorbox{insights}{%\n'
            '    enhanced, breakable,\n'
            '    colback=lightblue, colframe=accentblue,\n'
            '    coltitle=white, fonttitle=\\bfseries\\small,\n'
            '    title=Insights, fontupper=\\small,\n'
            '    boxrule=0.4pt, arc=2pt,\n'
            '    left=6pt, right=6pt, top=3pt, bottom=3pt,\n'
            '    before skip=8pt, after skip=10pt,\n'
            '}\n')
        tex = tex.replace(
            '\\begin{document}', ins + '\n\\begin{document}', 1)
    # 3. Idempotent: strip ALL prior "Experimental Results"
    #    sections (prefix match -- there may now be one per BPMX
    #    rule), from the FIRST such header to \end{document},
    #    then insert the freshly built block before it.
    marker = r'\section{Experimental Results'
    if marker in tex:
        i = tex.index(marker)
        j = tex.index('\\end{document}', i)
        tex = tex[:i] + tex[j:]
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
