"""
================================================================
 MOSPP report spec -- declarative content/config for the
 BPMX-depth-ladder report. Pure data: configs+palette, k
 snapshots, counter groups, exclusions, per-counter prose
 (`_COUNTER_INFO`), figure-caption insights
 (`_CAPTION_INSIGHT`), heatmap anchors, toy-grid layout.
 Consumed by `report_render`; no logic, no I/O.
================================================================
"""


# ── Configs to compare (order = legend / table-row order) ───────────────────
# All BPMX-active configs use rule_bpmx='1'. `depth=0` is the
# BPMX-off baseline (rule_none); deeper d = deeper cascade
# reach. Legend uses `depth=N` alone (the shared `rule=1` is
# called out once in the setup paragraph instead).
#
# Color: monotone blue gradient with perceptually-even steps
# (CIELAB L* ~ 70, 60, 46, 33, 22, 12; Delta ~ 10-14 each --
# tighter than the prior 4-entry 18-21 spread, but still
# above the ~10 perceptual-distinctness threshold) so the
# human eye can rank all six lines at a glance, even when
# they sit close together on a chart. The interior d=1..d=4
# is the canonical Colorbrewer Blues9-6..9 sequence -- which
# is designed exactly for sequential perceptual evenness; the
# light anchor (d=0=#6BAED6 = Blues9-5) and the dark anchor
# (d=5=#041F4B = custom navy) bracket the canonical sequence
# so the ramp stays in the blue family end-to-end without
# collapsing to pure black at the deepest rung.
#
#   depth=0 = #6BAED6   Colorbrewer Blues9-5   -- light blue
#   depth=1 = #4292C6   Colorbrewer Blues9-6   -- medium-light blue
#   depth=2 = #2171B5   Colorbrewer Blues9-7   -- medium blue
#   depth=3 = #08519C   Colorbrewer Blues9-8   -- dark blue
#   depth=4 = #08306B   Colorbrewer Blues9-9   -- darkest canonical
#   depth=5 = #041F4B   custom navy            -- very dark navy
CONFIGS = [
    {'tag':   'rule_none',
     'label': r'depth=0',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_none__bpmx_inf__prop_0.csv'),
     'color': '6BAED6'},
    {'tag':   'rule_1__d_1',
     'label': r'depth=1',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_1__prop_0.csv'),
     'color': '4292C6'},
    {'tag':   'rule_1__d_2',
     'label': r'depth=2',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_2__prop_0.csv'),
     'color': '2171B5'},
    {'tag':   'rule_1__d_3',
     'label': r'depth=3',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_3__prop_0.csv'),
     'color': '08519C'},
    {'tag':   'rule_1__d_4',
     'label': r'depth=4',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_4__prop_0.csv'),
     'color': '08306B'},
    {'tag':   'rule_1__d_5',
     'label': r'depth=5',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_5__prop_0.csv'),
     'color': '041F4B'},
]

# k snapshots shown in per-counter tables (rows = depth,
# cols = k). The full progression already lives in the line
# chart; 5 snapshots are the readable summary granularity.
K_TABLE: list[int] = [10, 50, 100, 150, 200]

COUNTER_GROUPS = [
    ('Search',      ['cnt_expanded', 'cnt_generated']),
    ('Propagation', ['cnt_prop_attempts', 'cnt_prop_lifts',
                     'cnt_prop_waves']),
    ('BPMX',        ['cnt_bpmx_attempts', 'cnt_bpmx_lifts',
                     'pct_bpmx_lifts', 'cnt_bpmx_depth']),
    ('Heuristic',   ['cnt_h_search']),
    ('Frontier',    ['cnt_push', 'cnt_pop', 'cnt_decrease']),
    ('Reuse',       ['cnt_cache_hits_at_init']),
    ('Memory',      ['mem_open', 'mem_closed', 'mem_cache',
                     'mem_bounds', 'mem_total']),
    ('Time',        ['elapsed_total', 'elapsed_search',
                     'elapsed_update']),
]

# Counters intentionally hidden from the report (author choice).
# These would otherwise be auto-included (non-trivial across some
# configs) but the user has chosen to omit them. Listed under
# "Omitted (excluded by author choice)" in the setup paragraph.
_EXCLUDED_COUNTERS: set[str] = {
    'cnt_h_search',
    'cnt_push',
    'cnt_pop',
    'cnt_generated',
    'cnt_decrease',
    'cnt_bpmx_depth',
    'cnt_cache_hits_at_init',
    'elapsed_search',
}

# Per-counter semantic description: one sentence each. Joined
# with an auto-computed min/max observation in `build_insight`.
_COUNTER_INFO: dict[str, str] = {
    'cnt_expanded': (
        'Inner-A* node expansions, summed across the $k$ '
        'sub-searches --- the headline cost metric; lower means '
        'fewer states the inner search had to settle.'),
    'cnt_bpmx_attempts': (
        'BPMX sweeps launched --- one per inner-A* expansion that '
        'runs the cascade, so it mirrors \\texttt{cnt\\_expanded} '
        '(the \\texttt{depth=0} baseline is BPMX-off, hence 0). It '
        '\\emph{falls} with \\texttt{depth\\_bpmx} as deeper lifts '
        'prune expansions, and peaks at \\texttt{depth=1}, where a '
        'depth-1 sweep cannot lift on a consistent base heuristic '
        'and so pays the per-expansion cost over the full baseline '
        'expansion set.'),
    'cnt_bpmx_lifts': (
        'BPMX lifts that actually raised an $h$-value '
        '--- the cascade work that pays off, summed across '
        'the $k$ sub-searches.'),
    'pct_bpmx_lifts': (
        'BPMX hit-rate per attempt '
        '($\\text{cnt\\_bpmx\\_lifts} / \\text{cnt\\_bpmx\\_attempts}$); '
        'an efficiency measure --- a falling rate at deeper $d$ '
        'signals diminishing returns from extra cascade depth.'),
    'cnt_bpmx_depth': (
        'Deepest BFS-level any single sub-search reached '
        '(MAX-aggregated across sub-searches, not summed): '
        'the empirical horizon where lifts stop being '
        'applicable.'),
    'cnt_cache_hits_at_init': (
        'Starts solved instantly because $h^{*}(s,t)$ was '
        'already in the carried cache from an earlier '
        'sub-search --- the incremental-reuse headline win '
        '(one pop, zero expansions).'),
    'mem_open': (
        'Peak OPEN size across the $k$ sub-searches '
        '(MAX-aggregated; each sub-search probe uses its '
        'own \\texttt{frontier.max\\_size}).'),
    'mem_closed': (
        'Peak CLOSED size across the $k$ sub-searches '
        '(MAX-aggregated).'),
    'mem_cache': (
        'Final size of the carried $h^{*}$ cache (rule-4 '
        'final-on-owner) --- the goal-anchored suffix store '
        'harvested via \\texttt{to\\_cache} after each reached '
        'sub-search; folded into \\texttt{mem\\_total}.'),
    'mem_bounds': (
        'Final size of the admissible-bounds store. This '
        'experiment runs \\texttt{adaptive\\_h=False}, so the '
        'store stays empty and the value is the bare dict '
        'overhead ($64$\\,B) at every depth.'),
    'mem_total': (
        'Sum of every per-region peak --- a conservative '
        'coincident-peak upper bound on memory.'),
    'elapsed_total': (
        'Total wall-clock seconds for the orchestrator run; '
        'cumulative across the $k$ sub-searches.'),
    'elapsed_update': (
        'Time in the goal-anchored cache/bounds update phase; '
        '$\\equiv 0$ here since \\texttt{adaptive\\_h=False}.'),
}


# Default figure caption body (used when a metric has no curated
# insight in `_CAPTION_INSIGHT`).
_DEFAULT_CAPTION_BODY: str = (
    r'Arithmetic mean across all 25~maps (5~domains $\times$ 5~maps)'
    '\n'
    r'at each $k$.')

# Per-figure caption insight: a concise, data-grounded reading of
# the curve, shown in the figure caption in place of the generic
# "mean vs. k" boilerplate. One-to-two sentences, ASCII-only.
_CAPTION_INSIGHT: dict[str, str] = {
    'cnt_expanded': (
        r'Deeper $d$ tightens more nodes, so fewer expand; the '
        r'$\approx\!44\%$ drop at $d{=}1\!\to\!2$ dominates and '
        r'gains then diminish. $d{=}1$ equals $d{=}0$ because a '
        r'depth-1 sweep cannot lift on a consistent base $h$.'),
    'cnt_bpmx_attempts': (
        r'One sweep is launched per inner-A* expansion, so this '
        r'mirrors \texttt{cnt\_expanded} for $d{\ge}1$. $d{=}1$ '
        r'peaks because it expands the full BPMX-off baseline; '
        r'$d{\ge}2$ prunes expansions and so launches fewer sweeps.'),
    'cnt_bpmx_lifts': (
        r'Absolute lifts are non-monotone in depth --- the product '
        r'of rising per-sweep yield and falling sweep count over '
        r'heterogeneous maps ($d{=}1$ lifts nothing on consistent '
        r'$h$). The cleaner monotone trend is the per-attempt rate '
        r'in the next figure (\texttt{pct\_bpmx\_lifts}).'),
    'pct_bpmx_lifts': (
        r'Hit-rate rises monotonically with depth '
        r'($17\%\!\to\!23\%$): deeper sweeps reach more '
        r'cached-boundary inconsistencies per attempt. Unweighted '
        r'mean of per-map rates, so it need not equal '
        r'charted-lifts$/$charted-attempts.'),
    'mem_open': (
        r'Mean over maps of the per-run peak OPEN (MAX over the $k$ '
        r'sub-searches). The $\approx\!1.1\times$ spread is nearly '
        r'flat because the peak is set by the hardest, '
        r'mostly-uncached sub-search that BPMX prunes only late, so '
        r'depth barely moves it.'),
    'mem_closed': (
        r'Identical across all depths: the peak-CLOSED sub-search '
        r'explores mostly uncached space where BPMX finds no '
        r'inconsistency, so it expands the same at every depth. '
        r'Depth only prunes the smaller cache-interior sub-searches '
        r'the MAX does not see.'),
    'mem_cache': (
        r'Final size of the carried $h^{*}$ cache, which holds only '
        r'optimal-path cells. The $\approx\!9\%$ depth variation is '
        r'not pruning --- cached cells lie on optimal paths and are '
        r'always found; it is a tie-break artifact, as inconsistent '
        r'lifted $h$ selects different equally-optimal path-sets '
        r'covering slightly fewer cells (non-monotone).'),
    'mem_bounds': (
        r'Identically $64$\,B (empty-dict overhead) at every depth '
        r'because this experiment runs \texttt{adaptive\_h=False}; '
        r'the admissible-bounds store is never populated, so the '
        r'line carries no depth signal.'),
    'mem_total': (
        r'Dominated by \texttt{mem\_closed} ($\approx\!93\%$, '
        r'depth-invariant), so total memory barely moves: $d{\le}1$ '
        r'at the max and $d{\ge}2$ about $0.6\%$ lower, with a small '
        r'non-monotone wiggle inherited from '
        r'\texttt{mem\_open}$+$\texttt{mem\_cache}.'),
    'elapsed_total': (
        r'Wall-clock rises $\approx\!10\times$ with depth '
        r'($15$s$\to\!148$s) even as expansions fall, because '
        r'per-expansion cascade cost outgrows the expansion savings '
        r'on this consistent-base grid. $d{=}1$ already doubles '
        r'$d{=}0$ as pure overhead (it lifts nothing).'),
}


# ── Per-column heatmap shading (red = larger, green = smaller) ───────────────

# Excel-style 3-color-scale anchors: smallest -> green, mid ->
# yellow, largest -> red. Black cell text stays legible on all
# three. Every numeric table cell is shaded by its rank within
# its own column so the reader can rank a column at a glance.
_HEAT_GREEN = (0x63, 0xBE, 0x7B)
_HEAT_YELLOW = (0xFF, 0xEB, 0x84)
_HEAT_RED = (0xF8, 0x69, 0x6B)


# ── Toy example: depth=0 ≡ depth=1, depth=2 expands less ────────────────────

# Toy lives on the canonical `grid_6x6_zigzag` topology (two
# horizontal walls forcing a snake-shape detour (0,0) -> (5,0),
# h*-Manhattan gap up to 10). Seed cache from a sub-search-1
# run, prune it to a single cached cell, then run AStarBPMX
# from a non-cached start at three depths. Numbers are computed
# at report-generation time (not pinned) so the toy can never
# drift from the codebase.

TOY_CACHED_CELL: tuple[int, int] = (2, 3)
TOY_START: tuple[int, int] = (0, 3)
TOY_GOAL: tuple[int, int] = (5, 0)
TOY_GRID_ROWS: int = 6
TOY_GRID_COLS: int = 6


# k positions at which the top-two-line gap is annotated.
_ANNOT_K: list[int] = [100, 200]
