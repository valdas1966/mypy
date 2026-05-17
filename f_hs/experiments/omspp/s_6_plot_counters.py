"""
===============================================================================
 Script: plot Incremental (kA*-INC extended) vs AGG-Eager / AGG-Lazy
 (kA*-AGG, Φ=MIN, opt+sv) counters as a multi-page PDF on Drive.

 Three algorithms compared:
   - Incremental : kA*-INC, extended mode. Black.
   - AGG-Eager   : kA*-AGG `eager_opt_sv`. Blue.
   - AGG-Lazy    : kA*-AGG `lazy_opt_sv`.  Red.

 All three are SOLID lines with the same filled-circle marker. When
 AGG-Eager and AGG-Lazy coincide on a segment (mem_*, cnt_phi_*,
 ... often differ by < 1%), the visible line on that segment is
 drawn as alternating short pieces blue / red / blue / red so both
 algorithms remain visible. Non-overlapping segments are drawn as
 normal solid lines per algorithm.

 X-axis: k (number of goals).
 Y-axis: counter value, MEAN over (domain, map) at each k.

 Each page: chart on the top half, a per-k DATA TABLE on the bottom
 half (rows = k values, columns = Incremental + 2 AGG configs). The
 table surfaces the exact mean values that the chart visualises.

 The two CSVs are inner-joined on `(domain, map, k)` first, so any
 (map, k) missing from one side is dropped from both -- the
 comparison stays apples-to-apples.

 Memory accounting
   `mem_open` / `mem_closed` cover frontier struct + pro-rated g/parent
   slots (strict bucket semantics). `mem_aux` covers KAStarAgg's
   auxiliary per-state structures that live OUTSIDE OPEN/CLOSED:
   `_F_stored` (always), `_h_vector` (when store_vector=True),
   `_responsible` (when is_opt=True). For Incremental this is
   structurally 0. The derived headline `mem_total = mem_open +
   mem_closed + mem_aux` is added in `make_plots` (not stored in
   either CSV). `cnt_h_total = cnt_h_search + cnt_h_update` is the
   analogous derived headline for h-call accounting.
-------------------------------------------------------------------------------
 12 pages total:
   shared counters (Incremental + 2 AGG lines per chart)
     cnt_expanded, cnt_generated,
     elapsed_total,
     cnt_h_total (derived = cnt_h_search + cnt_h_update),
     cnt_push, cnt_pop,
     mem_open, mem_closed, mem_aux, mem_total
   AGG-only counters (2 AGG lines per chart, no Incremental)
     cnt_phi_total (derived = cnt_phi_search + cnt_phi_update)
   + 1 survival page (Incremental per-node OPEN-survival
     distribution; explains the cnt_h_update half of the
     cnt_h_total gap) -- appended when the survival CSV is
     supplied.
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/kastar_inc_extended{suffix}.csv
   Experiments/OMSPP/kastar_agg_all_configs{suffix}.csv
   Experiments/OMSPP/inc_survival_histogram{suffix}.csv

 Output  (Drive)
   Experiments/OMSPP/kastar_inc_vs_agg_counters{suffix}.pdf

 `suffix` is `''` for full-run CSVs or `'_toy{N}'` for toy CSVs.
===============================================================================
"""
import math
import os
import tempfile
import logging

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # headless: write PDF without a display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Algorithm visual specs ──────────────────────────────────────────────────
# Solid lines only; on segments where AGG-Eager and AGG-Lazy coincide
# the visible line alternates the two colours (see _draw_overlay_pair).
# alpha=1.0 throughout so the alternating colours stay vivid.

_ALGO_INC = 'Incremental'
_ALGO_EAGER = 'AGG-Eager'
_ALGO_LAZY = 'AGG-Lazy'

_ALGO_SPECS: dict[str, dict] = {
    _ALGO_INC: dict(
        color='black',
        linestyle='-',
        linewidth=2.6,
        marker='o',
        markersize=5,
        markerfacecolor='black',
        markeredgecolor='black',
        alpha=1.0,
    ),
    _ALGO_EAGER: dict(
        color='tab:blue',
        linestyle='-',
        linewidth=2.2,
        marker='o',
        markersize=5,
        markerfacecolor='tab:blue',
        markeredgecolor='tab:blue',
        alpha=1.0,
    ),
    _ALGO_LAZY: dict(
        color='tab:red',
        linestyle='-',
        linewidth=2.2,
        marker='o',
        markersize=5,
        markerfacecolor='tab:red',
        markeredgecolor='tab:red',
        alpha=1.0,
    ),
}

# Pieces per overlapping segment for the alternating bicolour draw.
# 6 pieces over a k-step of 10 yields ~10px alternation at typical
# PDF zoom -- visible alternation, not noisy.
_INTERLEAVE_PIECES: int = 6

# Relative tolerance for "lines coincide on this segment". If both
# endpoints of the segment satisfy |y_a - y_b| / max(|y_a|, |y_b|)
# < tol, the segment is drawn as an alternating midline.
_OVERLAP_REL_TOL: float = 0.02


# (is_lazy, is_opt, store_vector, csv_config_label, display_label)
_AGG_CONFIGS: list[tuple[bool, bool, bool, str, str]] = [
    (False, True, True, 'eager_opt_sv', _ALGO_EAGER),
    (True,  True, True, 'lazy_opt_sv',  _ALGO_LAZY),
]


# Footer notes for caveats on mem_* / cnt_h_total pages.
_NOTE_MEM_STRICT = (
    "Strict bucket: frontier + g/parent slots only. "
    "AGG's _F_stored / _h_vector (sv) / _responsible (opt) "
    "are tallied in mem_aux."
)
_NOTE_MEM_AUX = (
    "AGG-only: _F_stored (always) + _h_vector (sv) + "
    "_responsible (opt). Incremental is structurally 0 -- no "
    "AGG-style aux structures."
)
_NOTE_MEM_TOTAL = (
    "Headline memory metric: mem_open + mem_closed + mem_aux. "
    "For Incremental the aux term is 0 by construction; for "
    "AGG it adds the _F_stored / vector / opt cost."
)
_NOTE_CNT_H_TOTAL = (
    "Derived: cnt_h_search + cnt_h_update. Captures total "
    "heuristic evaluations across both lazy-search misses "
    "(search bucket) and eager-refresh recomputes (update "
    "bucket)."
)
_NOTE_SURVIVAL = (
    "Bar: % of ALL generated nodes by #refresh-transitions "
    "survived in OPEN (= that node's cnt_h_update h-calls); "
    "sum over nodes == cnt_h_update. survival-0 = expanded "
    "within its own sub-search (never refreshed) -- the vast "
    "majority. AGG instead pays ~|A|~k h-calls for EVERY "
    "node. The h/node columns make it concrete: INC is "
    "~constant (~4); AGG-Lazy is ~k -- THAT ratio is why "
    "INC << AGG on cnt_h_total. The companion table is the "
    "same binned distribution as the bars."
)

_FOOTER_NOTE: dict[str, str] = {
    'mem_open':    _NOTE_MEM_STRICT,
    'mem_closed':  _NOTE_MEM_STRICT,
    'mem_aux':     _NOTE_MEM_AUX,
    'mem_total':   _NOTE_MEM_TOTAL,
    'cnt_h_total': _NOTE_CNT_H_TOTAL,
}


# Page list: explicit ordering. `agg_only=True` skips Incremental.
_PAGES: list[dict] = [
    {'counter': 'cnt_expanded'},
    {'counter': 'cnt_generated'},

    {'counter': 'elapsed_total'},

    {'counter': 'cnt_h_total'},

    {'counter': 'cnt_push'},
    {'counter': 'cnt_pop'},

    {'counter': 'cnt_phi_total', 'agg_only': True},

    {'counter': 'mem_open'},
    {'counter': 'mem_closed'},
    {'counter': 'mem_aux'},
    {'counter': 'mem_total'},
]


# ── Drive I/O ──────────────────────────────────────────────────────────────

def _download_csv(drive: Drive, path: str) -> pd.DataFrame:
    """
    ========================================================================
     Download a CSV from Drive into a temp file and return it as a
     DataFrame. The temp file is cleaned up before returning.
    ========================================================================
    """
    fd, local = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    try:
        drive.download(path_src=path, path_dest=local)
        df = pd.read_csv(local)
        _log.info(f'loaded {path}: {len(df):,} rows, '
                  f'{len(df.columns)} cols')
        return df
    finally:
        if os.path.exists(local):
            os.unlink(local)


# ── Inner-join + per-k mean ─────────────────────────────────────────────────

def _intersect_keys(df_inc: pd.DataFrame,
                    df_agg: pd.DataFrame
                    ) -> pd.DataFrame:
    """
    ========================================================================
     Return the set of (domain, map, k) keys present in BOTH CSVs.
    ========================================================================
    """
    keys_inc = df_inc[['domain', 'map', 'k']].drop_duplicates()
    keys_agg = df_agg[['domain', 'map', 'k']].drop_duplicates()
    common = keys_inc.merge(keys_agg, on=['domain', 'map', 'k'])
    _log.info(f'common (domain, map, k) triples: {len(common):,}')
    return common


def _filter_common(df: pd.DataFrame,
                   common: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     Keep only rows of `df` whose (domain, map, k) appears in
     `common`.
    ========================================================================
    """
    return df.merge(common, on=['domain', 'map', 'k'], how='inner')


# ── Single-counter chart + per-k table ──────────────────────────────────────

def _line_only_spec(spec: dict) -> dict:
    """
    ========================================================================
     Strip marker keys from an algorithm spec; used when drawing the
     LINE only (markers are emitted in a separate plot call so they
     land on the actual per-algo (x, y) data points even within
     overlap segments).
    ========================================================================
    """
    line_keys = {'color', 'linestyle', 'linewidth', 'alpha'}
    return {k: v for k, v in spec.items() if k in line_keys}


def _marker_only_kwargs(spec: dict) -> dict:
    """
    ========================================================================
     Return matplotlib kwargs that draw markers only (no connecting
     line) at the data points of an algorithm.
    ========================================================================
    """
    return dict(
        linestyle='None',
        marker=spec.get('marker', 'o'),
        markersize=spec.get('markersize', 5),
        markerfacecolor=spec.get('markerfacecolor', spec['color']),
        markeredgecolor=spec.get('markeredgecolor', spec['color']),
        markeredgewidth=spec.get('markeredgewidth', 1.0),
        alpha=spec.get('alpha', 1.0),
    )


def _draw_overlay_pair(ax,
                       x: list,
                       y_a: list,
                       y_b: list,
                       spec_a: dict,
                       spec_b: dict,
                       label_a: str,
                       label_b: str,
                       n_pieces: int = _INTERLEAVE_PIECES,
                       rel_tol: float = _OVERLAP_REL_TOL) -> None:
    """
    ========================================================================
     Draw two lines (A=eager, B=lazy) so that:

       - On a segment where the two lines coincide (within rel_tol),
         the visible line is rendered as `n_pieces` short pieces
         alternating colour A / colour B along the (y_a + y_b) / 2
         midline. Neither A's nor B's full-resolution line is drawn
         in that segment.
       - On a non-overlapping segment, each line is drawn solid in
         its own colour.

     Markers are always drawn at the actual data points of BOTH
     lines so each algorithm's per-k value remains visible even
     inside an overlap segment.

     Legend entries are emitted exactly once per algorithm via
     empty proxy plots.
    ========================================================================
    """
    n = len(x)
    if n == 0:
        return
    if n == 1:
        # Single point: just draw markers, no line.
        ax.plot([x[0]], [y_a[0]], label=label_a,
                **_marker_only_kwargs(spec_a))
        ax.plot([x[0]], [y_b[0]], label=label_b,
                **_marker_only_kwargs(spec_b))
        return

    # Per-segment overlap detection.
    overlap = [False] * (n - 1)
    for i in range(n - 1):
        a_i, a_j = y_a[i], y_a[i + 1]
        b_i, b_j = y_b[i], y_b[i + 1]
        if any(v is None or (isinstance(v, float) and math.isnan(v))
               for v in (a_i, a_j, b_i, b_j)):
            continue
        mag_i = max(abs(a_i), abs(b_i), 1e-12)
        mag_j = max(abs(a_j), abs(b_j), 1e-12)
        gap_i = abs(a_i - b_i) / mag_i
        gap_j = abs(a_j - b_j) / mag_j
        overlap[i] = (gap_i < rel_tol) and (gap_j < rel_tol)

    # Legend proxies (drawn once, with full spec incl. marker).
    ax.plot([], [], label=label_a, **spec_a)
    ax.plot([], [], label=label_b, **spec_b)

    line_a = _line_only_spec(spec_a)
    line_b = _line_only_spec(spec_b)

    # Draw non-overlap segments, per line, as contiguous runs.
    for y_line, line_spec in ((y_a, line_a), (y_b, line_b)):
        i = 0
        while i < n - 1:
            if overlap[i]:
                i += 1
                continue
            j = i
            while j < n - 1 and not overlap[j]:
                j += 1
            ax.plot(x[i:j + 1], y_line[i:j + 1],
                    label='_nolegend_', **line_spec)
            i = j

    # Draw overlap segments as alternating-colour midline pieces.
    color_a = spec_a['color']
    color_b = spec_b['color']
    lw = max(line_a.get('linewidth', 2), line_b.get('linewidth', 2))
    alpha_overlap = max(spec_a.get('alpha', 1.0),
                        spec_b.get('alpha', 1.0))
    for i in range(n - 1):
        if not overlap[i]:
            continue
        x_i, x_j = x[i], x[i + 1]
        mid_i = (y_a[i] + y_b[i]) / 2
        mid_j = (y_a[i + 1] + y_b[i + 1]) / 2
        for p in range(n_pieces):
            t1 = p / n_pieces
            t2 = (p + 1) / n_pieces
            x_p1 = x_i + t1 * (x_j - x_i)
            x_p2 = x_i + t2 * (x_j - x_i)
            y_p1 = mid_i + t1 * (mid_j - mid_i)
            y_p2 = mid_i + t2 * (mid_j - mid_i)
            color = color_a if p % 2 == 0 else color_b
            ax.plot([x_p1, x_p2], [y_p1, y_p2],
                    color=color, linewidth=lw,
                    solid_capstyle='butt',
                    alpha=alpha_overlap,
                    label='_nolegend_')

    # Markers at every (x, y) of each algorithm.
    ax.plot(x, y_a, label='_nolegend_', **_marker_only_kwargs(spec_a))
    ax.plot(x, y_b, label='_nolegend_', **_marker_only_kwargs(spec_b))


def _plot_counter(ax,
                  counter: str,
                  inc_by_k: pd.DataFrame | None,
                  agg_by_k_config: pd.DataFrame,
                  n_maps: int) -> None:
    """
    ========================================================================
     Draw one counter onto `ax`. `inc_by_k` may be None for
     AGG-only counters (cnt_phi_*).

     Incremental is drawn as a single solid line. The AGG-Eager and
     AGG-Lazy pair is drawn via `_draw_overlay_pair` so coincident
     segments render as alternating blue / red pieces instead of
     one colour silently masking the other.
    ========================================================================
    """
    if inc_by_k is not None and counter in inc_by_k.columns:
        spec = dict(_ALGO_SPECS[_ALGO_INC])
        ax.plot(inc_by_k.index, inc_by_k[counter],
                label=_ALGO_INC, **spec)

    # AGG pair (interleave colours on overlap).
    eager_series = None
    lazy_series = None
    for _is_lazy, _is_opt, _sv, cfg, display in _AGG_CONFIGS:
        try:
            series = agg_by_k_config.xs(cfg, level='config')[counter]
        except KeyError:
            continue
        if display == _ALGO_EAGER:
            eager_series = series
        elif display == _ALGO_LAZY:
            lazy_series = series

    if eager_series is not None and lazy_series is not None:
        x_vals = list(eager_series.index)
        _draw_overlay_pair(
            ax=ax, x=x_vals,
            y_a=list(eager_series.values),
            y_b=list(lazy_series.values),
            spec_a=_ALGO_SPECS[_ALGO_EAGER],
            spec_b=_ALGO_SPECS[_ALGO_LAZY],
            label_a=_ALGO_EAGER,
            label_b=_ALGO_LAZY,
        )
    elif eager_series is not None:
        spec = dict(_ALGO_SPECS[_ALGO_EAGER])
        ax.plot(eager_series.index, eager_series.values,
                label=_ALGO_EAGER, **spec)
    elif lazy_series is not None:
        spec = dict(_ALGO_SPECS[_ALGO_LAZY])
        ax.plot(lazy_series.index, lazy_series.values,
                label=_ALGO_LAZY, **spec)

    ax.set_xlabel('k (number of goals)')
    ax.set_ylabel(counter)
    ax.set_title(f'{counter}  '
                 f'(mean over {n_maps} (domain, map) at each k)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=8, framealpha=0.85)

    note = _FOOTER_NOTE.get(counter)
    if note is not None:
        ax.text(0.01, -0.16, note,
                transform=ax.transAxes,
                fontsize=7, color='dimgray', style='italic')


def _format_value(counter: str, value: float) -> str:
    """
    ========================================================================
     Format a single mean value for the per-k data table. Elapsed
     counters get 3 decimals; large counts use K / M / B suffixes
     for readability (no scientific notation):
       >= 1e9  -> 1.23B
       >= 1e6  -> 1.23M
       >= 1e4  -> 12.3K
       else    -> thousands-separator
    ========================================================================
    """
    if pd.isna(value):
        return '—'
    if counter.startswith('elapsed_'):
        return f'{value:.3f}'
    av = abs(value)
    if av >= 1_000_000_000:
        return f'{value / 1_000_000_000:.2f}B'
    if av >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    if av >= 10_000:
        return f'{value / 1_000:.1f}K'
    return f'{value:,.0f}'


def _render_table(ax,
                  counter: str,
                  inc_by_k: pd.DataFrame | None,
                  agg_by_k_config: pd.DataFrame) -> None:
    """
    ========================================================================
     Render the per-k data table on `ax`. Columns: 'k' + 'Incremental'
     (if applicable) + 2 AGG display labels. Rows: 20 k values.

     Cells are center-aligned and shaded with a per-row red-yellow-
     green gradient: the row's max is red, min is green, others are
     linearly interpolated. `k` and header cells are not shaded.
    ========================================================================
    """
    ax.axis('off')
    ks = sorted(agg_by_k_config.index.get_level_values('k').unique())

    has_inc = (inc_by_k is not None
               and counter in inc_by_k.columns)
    col_labels: list[str] = ['k']
    if has_inc:
        col_labels.append(_ALGO_INC)
    for _is_lazy, _is_opt, _sv, _cfg, display in _AGG_CONFIGS:
        col_labels.append(display)

    cells: list[list[str]] = []
    raw: list[list[float]] = []
    for k in ks:
        row_str: list[str] = [str(k)]
        row_val: list[float] = [float('nan')]
        if has_inc:
            v = inc_by_k.loc[k, counter]
            row_str.append(_format_value(counter, v))
            row_val.append(float(v) if not pd.isna(v) else float('nan'))
        for _is_lazy, _is_opt, _sv, cfg, _display in _AGG_CONFIGS:
            try:
                v = agg_by_k_config.xs(
                    cfg, level='config').loc[k, counter]
            except KeyError:
                v = float('nan')
            row_str.append(_format_value(counter, v))
            row_val.append(float(v) if not pd.isna(v) else float('nan'))
        cells.append(row_str)
        raw.append(row_val)

    table = ax.table(cellText=cells,
                     colLabels=col_labels,
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(6.5)
    table.scale(1.0, 1.18)
    for j in range(len(col_labels)):
        table[(0, j)].set_text_props(weight='bold')
    for i in range(1, len(cells) + 1):
        table[(i, 0)].set_text_props(weight='bold')

    cmap = plt.get_cmap('RdYlGn_r')
    softness = 0.55
    for i_row, vals in enumerate(raw, start=1):
        data_vals = [v for v in vals[1:] if not pd.isna(v)]
        if len(data_vals) < 2:
            continue
        vmin, vmax = min(data_vals), max(data_vals)
        if vmin == vmax:
            continue
        for j in range(1, len(vals)):
            v = vals[j]
            if pd.isna(v):
                continue
            pos = (v - vmin) / (vmax - vmin)
            r, g, b, _ = cmap(pos)
            r = 1 - (1 - r) * (1 - softness)
            g = 1 - (1 - g) * (1 - softness)
            b = 1 - (1 - b) * (1 - softness)
            table[(i_row, j)].set_facecolor((r, g, b))


# ── Public API ─────────────────────────────────────────────────────────────

def _plot_survival_page(pdf: PdfPages,
                        surv: pd.DataFrame,
                        df_inc: pd.DataFrame) -> None:
    """
    ============================================================================
     One extra page: INC per-node OPEN-survival distribution at
     the largest k.

     survival = #inter-sub-search transitions a node sat in OPEN
     = that node's cnt_h_update h-calls. Bar histogram + a
     2-column companion table, both keyed on the same bins:
     fine bins of 10 from 0 to 99, then a single 100+ bin
     (100..k-1). y / table value = % of ALL generated nodes.
     survival-0 nodes (never refreshed -- expanded within their
     own sub-search; absent from the CSV by design) are
     reconstructed from cnt_generated and fall in bin 0-9, which
     dominates. AGG instead pays ~|A|~k h-calls for EVERY node.
    ============================================================================
    """
    fig = plt.figure(figsize=(13, 9.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.16)
    ax = fig.add_subplot(gs[0])
    ax_t = fig.add_subplot(gs[1])

    ks_all = sorted(surv['k'].unique())
    k_focus = max(ks_all)                 # 200 on the full run

    # Denominator = ALL generated nodes at k_focus (pooled over
    # the common maps). survival-0 nodes are absent from the
    # survival CSV by design, so reconstruct them as
    # cnt_generated - sum(survival >= 1).
    gen_total = float(df_inc[df_inc['k'] == k_focus]
                      ['cnt_generated'].sum())
    sf = surv[surv['k'] == k_focus]
    n_zero = max(0.0, gen_total - float(sf['num_nodes'].sum()))

    # Bins: 0-9, 10-19, ..., 90-99, then a single 100+ bin.
    n_fine = 10
    labels = [f'{i * 10}-{i * 10 + 9}'
              for i in range(n_fine)] + ['100+']
    counts = [0.0] * (n_fine + 1)
    counts[0] = n_zero                    # survival 0 -> bin 0-9
    for sc, n in zip(sf['survival_count'], sf['num_nodes']):
        idx = int(sc) // 10
        counts[idx if idx < n_fine else n_fine] += n
    pct = [c / gen_total * 100.0 for c in counts]

    x = np.arange(len(labels))
    bars = ax.bar(x, pct, width=0.82,
                   color='#3b6fb5', edgecolor='black',
                   linewidth=0.6)
    bars[0].set_color('#c0392b')          # the dominant bin
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    for xi, p in zip(x, pct):
        ax.annotate(f'{p:.2f}%', (xi, p),
                    textcoords='offset points', xytext=(0, 3),
                    ha='center', fontsize=8, fontweight='bold')
    ax.set_ylim(0, 105)
    pct0 = n_zero / gen_total * 100.0
    ax.set_xlabel('sub-searches the node survived in OPEN '
                  'after insertion  (bins of 10; 100+ = 100..'
                  f'{k_focus - 1})')
    ax.set_ylabel(f'% of all generated nodes  (k={k_focus})')
    ax.set_title(
        f'Incremental kA*: per-node OPEN-survival, k={k_focus}\n'
        f'{pct0:.1f}% of generated nodes are NEVER refreshed '
        f'(survival 0); {pct[0]:.1f}% survive <10 sub-searches '
        f'-- AGG pays ~k h-calls for EVERY node',
        fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)

    # ── Companion table: the same binned distribution ──
    headers = ['Survived', '% of generated']
    rows = [[lab, f'{p:.2f}%'] for lab, p in zip(labels, pct)]
    ax_t.axis('off')
    tbl = ax_t.table(cellText=rows, colLabels=headers,
                     loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    for c in range(len(headers)):
        tbl[0, c].set_text_props(fontweight='bold')
    for c in range(len(headers)):           # highlight bin 0-9
        tbl[1, c].set_facecolor('#f6d8d4')
    fig.text(0.5, 0.03, _NOTE_SURVIVAL, ha='center', va='bottom',
             fontsize=8, style='italic', wrap=True)

    pdf.savefig(fig)
    plt.close(fig)


def make_plots(path_drive_csv_inc: str,
               path_drive_csv_agg: str,
               path_drive_pdf_out: str,
               path_drive_csv_survival: str | None = None) -> None:
    """
    ============================================================================
     Read the INC and AGG CSVs from Drive, derive `mem_total` and
     `cnt_h_total`, inner-join on (domain, map, k), aggregate each
     counter to a per-k mean, and write the multi-page PDF to
     Drive (11 counter pages + 1 survival page when
     `path_drive_csv_survival` is given).
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    df_inc = _download_csv(drive=drive, path=path_drive_csv_inc)
    df_agg = _download_csv(drive=drive, path=path_drive_csv_agg)

    # Derived headline metrics (computed once, used everywhere).
    for df in (df_inc, df_agg):
        df['mem_total'] = (df['mem_open']
                           + df['mem_closed']
                           + df['mem_aux'])
        df['cnt_h_total'] = (df['cnt_h_search']
                             + df['cnt_h_update'])
    # AGG-only derived metric.
    df_agg['cnt_phi_total'] = (df_agg['cnt_phi_search']
                               + df_agg['cnt_phi_update'])

    common = _intersect_keys(df_inc=df_inc, df_agg=df_agg)
    df_inc = _filter_common(df=df_inc, common=common)
    df_agg = _filter_common(df=df_agg, common=common)
    n_maps = common.drop_duplicates(['domain', 'map']).shape[0]
    _log.info(f'after filter: INC={len(df_inc):,} rows, '
              f'AGG={len(df_agg):,} rows; n_maps={n_maps}')

    counters_used = {p['counter'] for p in _PAGES}
    inc_cols = [c for c in counters_used if c in df_inc.columns]
    agg_cols = [c for c in counters_used if c in df_agg.columns]
    inc_by_k = df_inc.groupby('k')[inc_cols].mean()
    agg_by_k_config = df_agg.groupby(['k', 'config'])[agg_cols].mean()

    fd, path_pdf = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    try:
        with PdfPages(path_pdf) as pdf:
            for page in _PAGES:
                counter = page['counter']
                inc_arg = None if page.get('agg_only') else inc_by_k

                fig = plt.figure(figsize=(13, 9.5))
                gs = fig.add_gridspec(2, 1,
                                      height_ratios=[3, 2],
                                      hspace=0.35)
                ax_chart = fig.add_subplot(gs[0])
                ax_table = fig.add_subplot(gs[1])
                _plot_counter(ax=ax_chart,
                              counter=counter,
                              inc_by_k=inc_arg,
                              agg_by_k_config=agg_by_k_config,
                              n_maps=n_maps)
                _render_table(ax=ax_table,
                              counter=counter,
                              inc_by_k=inc_arg,
                              agg_by_k_config=agg_by_k_config)
                pdf.savefig(fig)
                plt.close(fig)

            # Extra page: INC per-node OPEN-survival distribution
            # (explains the cnt_h_update half of the cnt_h_total
            # gap). Restricted to the same common (domain,map,k).
            if path_drive_csv_survival is not None:
                surv = _download_csv(drive=drive,
                                     path=path_drive_csv_survival)
                surv = _filter_common(df=surv, common=common)
                _log.info(f'survival: {len(surv):,} rows after '
                          f'common filter')
                _plot_survival_page(pdf=pdf, surv=surv,
                                    df_inc=df_inc)
        _log.info(f'wrote {path_pdf}')
        drive.upload(path_src=path_pdf,
                     path_dest=path_drive_pdf_out)
        _log.info(f'uploaded -> {path_drive_pdf_out}')
    finally:
        if os.path.exists(path_pdf):
            os.unlink(path_pdf)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Full-run CSVs (2026-05-15). Switch to '_toy50' to read the
    # historical 8-config toy snapshot.
    suffix = ''
    path_drive_csv_inc = (f'Experiments/OMSPP/'
                          f'kastar_inc_extended{suffix}.csv')
    path_drive_csv_agg = (f'Experiments/OMSPP/'
                          f'kastar_agg_all_configs{suffix}.csv')
    path_drive_pdf_out = (f'Experiments/OMSPP/'
                          f'kastar_inc_vs_agg_counters{suffix}.pdf')
    path_drive_csv_survival = (f'Experiments/OMSPP/'
                               f'inc_survival_histogram{suffix}.csv')

    make_plots(path_drive_csv_inc=path_drive_csv_inc,
               path_drive_csv_agg=path_drive_csv_agg,
               path_drive_pdf_out=path_drive_pdf_out,
               path_drive_csv_survival=path_drive_csv_survival)
    _log.info('--- done ---')
