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
# BPMX-off baseline (depth=0), shared by EVERY rule section.
_BASELINE = {
    'tag':   'rule_none',
    'label': r'depth=0',
    'csv':   ('Results/agg/'
              'astar_inc_nested_rule_none_bpmx_inf_prop_0_by_k.csv'),
    'color': '6BAED6',
}
# depth=1..5 line colors (shared across rules).
_DEPTH_COLORS = ['4292C6', '2171B5', '08519C', '08306B', '041F4B']


def _rule_configs(rule: str, depths=range(1, 6)) -> list[dict]:
    """
    ========================================================================
     Baseline (depth=0) + one config per depth in `depths` for
     one BPMX rule. `rule` is the inner-AStarBPMX `rule_bpmx`
     value ('1', '2', '3', 'CASCADE'); the CSV path is the `s_4`
     by-k aggregate of the raw `s_3` CSV
     (`Results/agg/astar_inc_nested_rule_{rule}_bpmx_{d}_prop_0_by_k.csv`).
     `depths` defaults to the full 1..5 ladder; pass a subset
     (e.g. `[1]`) for a rule that was only run at some depths.
    ========================================================================
    """
    return [_BASELINE] + [
        {'tag':   f'rule_{rule}__d_{d}',
         'label': f'depth={d}',
         'csv':   ('Results/agg/astar_inc_nested_'
                   f'rule_{rule}_bpmx_{d}_prop_0_by_k.csv'),
         'color': _DEPTH_COLORS[d - 1]}
        for d in depths
    ]


def _prop_configs(depths=range(1, 6)) -> list[dict]:
    """
    ========================================================================
     Baseline (depth=0) + one config per pre-search pathmax
     PROPAGATION depth in `depths`, with in-search BPMX OFF
     (`rule_none`). The orthogonal axis to the BPMX ladders:
     here `depth` = `propagate_pathmax(depth)`, not the in-search
     cascade. The depth=0 config IS `_BASELINE`
     (`rule_none_bpmx_inf_prop_0` = everything off), shared with
     every BPMX section. CSV is the `s_4` by-k aggregate of
     `astar_inc_nested_rule_none_bpmx_inf_prop_{p}.csv`.
    ========================================================================
    """
    return [_BASELINE] + [
        {'tag':   f'prop__d_{p}',
         'label': f'depth={p}',
         'csv':   ('Results/agg/astar_inc_nested_'
                   f'rule_none_bpmx_inf_prop_{p}_by_k.csv'),
         'color': _DEPTH_COLORS[p - 1]}
        for p in depths
    ]


# ── Cross-mechanism comparison at a fixed depth (categorical) ────────────────
# The depth ladders above each vary DEPTH for ONE mechanism, so
# they use the sequential blue gradient. This section is the
# orthogonal cut: it FIXES depth=1 and varies the MECHANISM, so the
# palette is QUALITATIVE (distinct hues, Tableau10) rather than a
# sequential ramp -- the axis is categorical, not ordinal. depth=0
# is the shared BPMX-off / prop-off baseline (`_BASELINE`'s CSV).
_COMPARE_COLORS = {
    'baseline': '7F7F7F',   # gray   -- the depth=0 reference
    'rule_1':   '1F77B4',   # blue
    'rule_2':   'FF7F0E',   # orange
    'rule_3':   '2CA02C',   # green
    'cascade':  'D62728',   # red
    'prop':     '9467BD',   # purple
    'combo':    '8C564B',   # brown  -- cascade+prop stacked, both d=1
}


def _compare_d1_configs() -> list[dict]:
    """
    ========================================================================
     The seven configs of the depth-1 mechanism comparison. The
     first six REUSE a depth-ladder `tag`/CSV (so the `s_4`
     aggregates are shared -- `s_5` downloads each once across all
     sections) but are RE-LABELED by mechanism and RE-COLORED from
     the qualitative `_COMPARE_COLORS` palette. depth=0 is the
     shared `_BASELINE` (BPMX off, prop off); the next five are the
     depth-1 rung of each mechanism: pathmax rules 1/2/3, their BPMX
     cascade (`rule_bpmx=CASCADE`, d=1), and pre-search pathmax
     propagation (P=1, BPMX off). The SEVENTH is the COMBINATION --
     cascade AND propagation stacked, both at depth 1 -- which (unlike
     the other six) has its OWN combined-config CSV
     (`rule_CASCADE_bpmx_1_prop_1`, the s_3 `inc_pb` run), not a
     reused single-axis aggregate.
    ========================================================================
    """
    return [
        {'tag': 'rule_none', 'label': r'depth=0',
         'csv': _BASELINE['csv'], 'color': _COMPARE_COLORS['baseline']},
        {'tag': 'rule_1__d_1', 'label': r'rule 1',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_1_bpmx_1_prop_0_by_k.csv'),
         'color': _COMPARE_COLORS['rule_1']},
        {'tag': 'rule_2__d_1', 'label': r'rule 2',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_2_bpmx_1_prop_0_by_k.csv'),
         'color': _COMPARE_COLORS['rule_2']},
        {'tag': 'rule_3__d_1', 'label': r'rule 3',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_3_bpmx_1_prop_0_by_k.csv'),
         'color': _COMPARE_COLORS['rule_3']},
        {'tag': 'rule_CASCADE__d_1', 'label': r'cascade',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_CASCADE_bpmx_1_prop_0_by_k.csv'),
         'color': _COMPARE_COLORS['cascade']},
        {'tag': 'prop__d_1', 'label': r'prop',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_none_bpmx_inf_prop_1_by_k.csv'),
         'color': _COMPARE_COLORS['prop']},
        {'tag': 'combo_d1', 'label': r'cascade+prop',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_CASCADE_bpmx_1_prop_1_by_k.csv'),
         'color': _COMPARE_COLORS['combo']},
    ]


# ── Adaptive-A* comparison at a fixed depth (categorical) ────────────────────
# Companion to the mechanism comparison above, but every non-baseline curve
# additionally turns ON Adaptive A* (the C_i-g_i CLOSED-list bound store,
# `adaptive_h=True`) on top of the carried cache. Reads the `_adapt_1`
# aggregates produced by `s_3` ALGO='inc_adapt' -> `s_4`; the section is
# auto-skipped by `s_5` until those CSVs exist. Colors echo the mechanism
# section (cascade=red, prop=purple, combo=brown) so each adaptive curve is
# recognizable as the adaptive twin of its non-adaptive counterpart;
# `adaptive`-alone is blue, the depth=0 reference gray.
_ADAPT_COLORS = {
    'baseline': '7F7F7F',   # gray   -- the depth=0 reference (no adaptive)
    'adaptive': '1F77B4',   # blue
    'cascade':  'D62728',   # red    (echoes the mechanism section)
    'prop':     '9467BD',   # purple
    'combo':    '8C564B',   # brown
}


def _compare_d1_adaptive_configs() -> list[dict]:
    """
    ========================================================================
     The five curves of the depth-1 ADAPTIVE comparison: the
     non-adaptive BPMX-off baseline (depth=0, `_BASELINE`'s CSV)
     plus the four `adaptive_h=True` configs (cache + Adaptive A*),
     all at depth 1 -- adaptive alone, adaptive+cascade,
     adaptive+prop, adaptive+cascade+prop. Each adaptive curve reads
     the `_adapt_1`-tagged `s_4` aggregate from `s_3` ALGO='inc_adapt'
     (distinct tags + CSVs from the mechanism section, so no collision).
    ========================================================================
    """
    return [
        {'tag': 'rule_none', 'label': r'depth=0',
         'csv': _BASELINE['csv'], 'color': _ADAPT_COLORS['baseline']},
        {'tag': 'adapt_only', 'label': r'adaptive',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_none_bpmx_inf_prop_0_adapt_1_by_k.csv'),
         'color': _ADAPT_COLORS['adaptive']},
        {'tag': 'adapt_cascade_d1', 'label': r'adaptive+cascade',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_CASCADE_bpmx_1_prop_0_adapt_1_by_k.csv'),
         'color': _ADAPT_COLORS['cascade']},
        {'tag': 'adapt_prop_d1', 'label': r'adaptive+prop',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_none_bpmx_inf_prop_1_adapt_1_by_k.csv'),
         'color': _ADAPT_COLORS['prop']},
        {'tag': 'adapt_combo_d1', 'label': r'adaptive+cascade+prop',
         'csv': ('Results/agg/astar_inc_nested_'
                 'rule_CASCADE_bpmx_1_prop_1_adapt_1_by_k.csv'),
         'color': _ADAPT_COLORS['combo']},
    ]


def _compare_inc_vs_rep_configs() -> list[dict]:
    """
    ========================================================================
     The two curves of the value-of-reuse comparison: the
     repetitive baseline `rep` (\\texttt{AStarRepMOSPP} -- k
     independent A* searches, NO sharing; `astar_rep_nested_by_k`)
     against the incremental cache-only baseline `inc`
     (\\texttt{AStarIncMOSPP} `depth=0` = `_BASELINE`). A DIFFERENT
     algorithm comparison from the mechanism sections -- `rep`
     dwarfs every inc config (~24x expansions at k=200), so it gets
     its own section rather than squashing the bpmx-vs-prop deltas
     onto a log axis in `compare1`. Only the counters where both are
     non-trivial survive (cnt_expanded / mem_total / elapsed_total);
     the bpmx/prop counters are 0 for both and auto-dropped.
    ========================================================================
    """
    return [
        {'tag': 'rep', 'label': r'rep (no reuse)',
         'csv': 'Results/agg/astar_rep_nested_by_k.csv',
         'color': '000000'},
        {'tag': 'rule_none', 'label': r'inc (cache)',
         'csv': _BASELINE['csv'], 'color': '2CA02C'},
    ]


# One report SECTION per BPMX rule (a depth ladder, baseline +
# depth 1..5). `s_5` renders a section only when at least one of
# its depth CSVs is present; otherwise it is skipped (so rule_3 /
# cascade appear automatically once their s_3 runs land). `key`
# prefixes the externalized figure names (`fig_<key>_<metric>`)
# so the sections never collide on disk / Overleaf.
RULE_SECTIONS = [
    {'key': 'rule1',   'rule': '1',
     'title': 'BPMX Rule 1 depth ladder',
     'configs': _rule_configs('1')},
    {'key': 'rule2',   'rule': '2',
     'title': 'BPMX Rule 2 (depth=1)',
     'configs': _rule_configs('2', depths=[1])},
    {'key': 'rule3',   'rule': '3',
     'title': 'BPMX Rule 3 depth ladder',
     'configs': _rule_configs('3')},
    {'key': 'cascade', 'rule': 'CASCADE',
     'title': 'BPMX Cascade depth ladder',
     'configs': _rule_configs('CASCADE')},
    # Orthogonal axis: pre-search pathmax propagation depth ladder
    # (in-search BPMX off). Renders once the `prop_{1..5}`
    # aggregates exist (they do). `key='propdepth'` prefixes its
    # figures (`fig_propdepth_*`) so it never collides with the
    # BPMX sections.
    {'key': 'propdepth', 'rule': None,
     'title': 'Pathmax Propagation depth ladder (BPMX off)',
     'configs': _prop_configs()},
    # Value-of-reuse: the repetitive (no-sharing) baseline vs the
    # incremental cache-only baseline. A DIFFERENT-algorithm
    # comparison (rep dwarfs every inc config ~24x), so it gets its
    # own section ahead of the mechanism comparison rather than
    # squashing the bpmx-vs-prop deltas onto a log axis. Renders once
    # `astar_rep_nested_by_k.csv` exists (it does, after s_4).
    {'key': 'incvsrep', 'rule': None,
     'title': r'Incremental vs Repetitive: the value of reuse',
     'intro': (
         r'\paragraph{What this compares.} The incremental '
         r'orchestrator (\texttt{AStarIncMOSPP}) carries a '
         r'goal-anchored on-path cache across the $k$ sub-searches; '
         r'the repetitive baseline (\texttt{AStarRepMOSPP}) shares '
         r'NOTHING --- it runs $k$ independent A* searches. This '
         r'isolates the value of that reuse alone, BEFORE any BPMX or '
         r'propagation: \texttt{rep} is the no-sharing ceiling and '
         r'\texttt{inc (cache)} is the same orchestrator with only '
         r'the cache (the \texttt{depth=0} baseline every mechanism '
         r'section builds on). The cache alone cuts expansions '
         r'$\approx\!24\times$ and runtime $\approx\!18\times$ at '
         r'$k{=}200$ --- at essentially equal peak memory --- and the '
         r'gap COMPOUNDS with $k$.'),
     'configs': _compare_inc_vs_rep_configs()},
    # Orthogonal cut: fix depth=1, vary the MECHANISM. Renders once
    # all six d=1 aggregates exist (they do). Placed LAST among the
    # experimental sections by `main.tex`'s \input order (a closing
    # synthesis after the per-mechanism ladders); its position in
    # this list only sets `s_5`'s build order, not the doc order.
    # `intro` is an opt-in framing paragraph (other sections omit it
    # -> unchanged). `key='compare1'` prefixes its figures
    # (`fig_compare1_*`).
    {'key': 'compare1', 'rule': None,
     'title': 'Mechanism comparison at depth=1',
     'intro': (
         r'\paragraph{What this compares.} Each preceding section is '
         r'a depth ladder for ONE mechanism; this closing section is '
         r'orthogonal --- it FIXES the depth at $1$ and varies the '
         r'MECHANISM, drawing the mechanisms side by side at their '
         r'shallowest reach. The seven curves are the BPMX-off '
         r'baseline ($d{=}0$) and, all at their depth-1 setting, the '
         r'three pathmax rules (1, 2, 3), their BPMX cascade '
         r'(\texttt{rule\_bpmx=CASCADE}, $d{=}1$), pre-search '
         r'pathmax propagation ($P{=}1$, BPMX off), and their '
         r'COMBINATION --- cascade $+$ propagation stacked, both at '
         r'depth~1.'),
     'configs': _compare_d1_configs()},
    # Adaptive-A* companion: fix depth=1, turn ON Adaptive A* on top of
    # the cache, vary which spreader (if any) is added. Auto-skipped by
    # `s_5` until the `_adapt_1` aggregates exist (run `s_3`
    # ALGO='inc_adapt' -> `s_4`). Placed LAST by `main.tex`'s \input
    # order (after the mechanism comparison). `key='compare1_adapt'`
    # prefixes its figures (`fig_compare1_adapt_*`).
    {'key': 'compare1_adapt', 'rule': None,
     'title': 'Adaptive-A* comparison at depth=1',
     'intro': (
         r'\paragraph{What this compares.} The companion to the '
         r'mechanism comparison above: every non-baseline curve here '
         r'additionally turns ON Adaptive A* (the $C_i - g_i(x)$ '
         r'CLOSED-list bound store) on top of the carried cache. '
         r'Against the BPMX-off baseline ($d{=}0$) it charts the four '
         r'depth-1 adaptive configs --- adaptive alone, and adaptive '
         r'combined with the BPMX cascade ($d{=}1$), with pre-search '
         r'pathmax propagation ($P{=}1$), and with both --- isolating '
         r'what Adaptive A* adds and whether it stacks with the '
         r'spreaders. Compare each curve against its non-adaptive twin '
         r'in the section above.'),
     'configs': _compare_d1_adaptive_configs()},
]

# Back-compat: the flat 6-config list (rule 1) some callers import.
CONFIGS = RULE_SECTIONS[0]['configs']

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
    ('Adaptive',    ['cnt_adapt_attempts', 'cnt_adapt_lifts',
                     'pct_adapt_lifts']),
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
    # Per-region memory metrics are hidden: each swings with the
    # coincident-peak RELOCATION (a sub-search-selection artifact,
    # not a real memory change), so individually they mislead. Only
    # mem_total -- the honest coincident peak -- is shown; the
    # regions are still summed into it.
    'mem_open',
    'mem_closed',
    'mem_cache',
    'mem_bounds',
}

# Per-counter semantic description: one sentence each. Joined
# with an auto-computed min/max observation in `build_insight`.
_COUNTER_INFO: dict[str, str] = {
    'cnt_expanded': (
        'Inner-A* node expansions, summed across the $k$ '
        'sub-searches --- the headline cost metric; lower means '
        'fewer states the inner search had to settle.'),
    'cnt_bpmx_attempts': (
        'BPMX sweeps launched --- one per inner-A* expansion, so '
        '\\texttt{depth=0} (BPMX off) is $0$ and the others track '
        '\\texttt{cnt\\_expanded}.'),
    'cnt_bpmx_lifts': (
        'BPMX lifts that actually raised an $h$-value '
        '--- the cascade work that pays off, summed across '
        'the $k$ sub-searches.'),
    'pct_bpmx_lifts': (
        'BPMX hit-rate per attempt '
        '($\\text{cnt\\_bpmx\\_lifts} / \\text{cnt\\_bpmx\\_attempts}$); '
        'higher means a sweep more often finds an $h$ to raise.'),
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
        'Per-sub-search peak OPEN-list size, averaged over the '
        '$k$ sub-searches.'),
    'mem_closed': (
        'Per-sub-search peak CLOSED-list size, averaged over the '
        '$k$ sub-searches.'),
    'mem_cache': (
        'Size of the carried $h^{*}$ cache DURING the '
        'coincident-peak sub-search (not the final cache size) '
        '--- the cache component of the memory peak; folded into '
        '\\texttt{mem\\_total}.'),
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
        r'Lifts are non-monotone in depth: rising per-sweep yield '
        r'times falling sweep count ($d{=}1$ lifts nothing on '
        r'consistent $h$). The per-attempt rate in the next figure '
        r'(\texttt{pct\_bpmx\_lifts}) is the cleaner, monotone trend.'),
    'pct_bpmx_lifts': (
        r'Hit-rate rises monotonically with depth '
        r'($17\%\!\to\!23\%$): deeper sweeps reach more '
        r'cached-boundary inconsistencies per attempt. Unweighted '
        r'mean of per-map rates, so it need not equal '
        r'charted-lifts$/$charted-attempts.'),
    'cnt_prop_attempts': (
        r'Pre-search pathmax-propagation attempts, summed across '
        r'the $k$ sub-searches. Grows steeply with propagation '
        r'depth (zero at $P{=}0$); each deeper wave revisits more '
        r'cells.'),
    'cnt_prop_lifts': (
        r'Propagation attempts that raised an $h$-value. Grows with '
        r'depth, but per-attempt yield falls --- deeper waves reach '
        r'fewer fresh inconsistencies.'),
    'cnt_prop_waves': (
        r'Mean propagation-wave count per sub-search '
        r'(MAX-aggregated, so a depth horizon, not work). Stays '
        r'below the depth cap $P$ because many maps converge '
        r'before reaching it.'),
    'mem_open': (
        r'Nearly flat across depth ($\approx\!1.1\times$): the OPEN '
        r'component of the coincident-peak sub-search; pruning '
        r'barely moves it.'),
    'mem_closed': (
        r'NOT flat --- it steps UP from the depth-0 baseline '
        r'($\approx\!+0.9\%$) then plateaus. A coincident-peak '
        r'RELOCATION artifact: pruning (BPMX cascade or pathmax '
        r'propagation) shrinks the cache-interior sub-searches, so '
        r'the memory peak relocates from a cache-heavy to a '
        r'closed-heavy sub-search --- raising the reported CLOSED '
        r'component even as total work falls. \texttt{mem\_total} is '
        r'the honest memory summary.'),
    'mem_cache': (
        r'Mirror-image of \texttt{mem\_closed}: drops sharply from '
        r'the depth-0 baseline ($\approx\!-40\%$) then declines '
        r'slowly. The cache component of the RELOCATED coincident '
        r'peak --- not cache pruning (cached cells lie on optimal '
        r'paths and are always found).'),
    'mem_bounds': (
        r'Flat at $64$\,B (empty-dict overhead) for every depth: '
        r'with \texttt{adaptive\_h=False} the store is never '
        r'populated, so the line carries no depth signal.'),
    'mem_total': (
        r'Nearly flat (within $\approx\!0.4\%$), gently decreasing: '
        r'dominated by the $\approx$depth-invariant '
        r'\texttt{mem\_closed} ($\approx\!97\%$ of total), so total '
        r'memory barely moves with depth.'),
    'elapsed_total': (
        r'Wall-clock rises $\approx\!10\times$ with depth '
        r'($15$s$\to\!148$s) even as expansions fall, because '
        r'per-expansion cascade cost outgrows the expansion savings '
        r'on this consistent-base grid. $d{=}1$ already doubles '
        r'$d{=}0$ as pure overhead (it lifts nothing).'),
}


# ── Per-subsection custom titles (override the default \texttt{metric}) ──────
_TITLES: dict[str, str] = {
    'cnt_expanded':       r'Mean |Expanded Nodes| per k.',
    'cnt_bpmx_attempts':  r'Mean |BPMX Attempts| per k.',
    'cnt_bpmx_lifts':     r'Mean |BPMX Lifts| per k.',
    'pct_bpmx_lifts':     r'Mean \%(BPMX Lifts / Attempts) per k.',
    'cnt_prop_attempts':  r'Mean |Propagation Attempts| per k.',
    'cnt_prop_lifts':     r'Mean |Propagation Lifts| per k.',
    'cnt_prop_waves':     r'Mean |Propagation Waves| per k.',
    'elapsed_total':      r'Mean Runtime (in seconds) per k',
}

# ── Insight-box items: the curated takeaways rendered as a
#    numbered `sentences` list inside the lightblue `insights`
#    callout (LAST element of each subsection). Keyed by section
#    `key` then counter; ASCII-only, math in $...$. A (rule,
#    counter) with no curated items falls back to the rule-
#    agnostic `_COUNTER_NEUTRAL` line below. ───────────────────────────────────
_INSIGHT_ITEMS: dict[str, dict[str, list[str]]] = {
    'rule1': {
        'cnt_expanded': [
            r'$d{=}0$ and $d{=}1$ are identical -- a depth-1 sweep '
            r'lifts nothing on consistent~$h$.',
            r'The largest drop is $d{=}1\to d{=}2$ '
            r'($\approx 1.8\times$).',
            r'Expansions keep falling with depth, but the gains '
            r'diminish past $d{=}2$.',
        ],
        'cnt_bpmx_attempts': [
            r'$d{=}0$: no BPMX attempts (BPMX is off).',
            r'$d{\ge}1$: attempts equal the expanded-node count -- '
            r'one sweep per expansion.',
        ],
        'cnt_bpmx_lifts': [
            r'$d{\le}1$: no lifts.',
            r'$d{\ge}2$: small spread, no monotonic pattern across '
            r'depths.',
        ],
        'pct_bpmx_lifts': [
            r'$d{\le}1$: no lifts, so the rate is $0\%$.',
            r'$d{\ge}2$: the hit-rate rises monotonically with '
            r'depth.',
        ],
        'mem_total': [
            r'Nearly flat, within $\approx\!0.3\%$ '
            r'($36161\to36045$ over $d{=}0\!\to\!5$): the '
            r'coincident memory peak barely moves with depth.',
            r'The honest memory summary --- its OPEN/CLOSED/cache '
            r'components individually shift as the peak sub-search '
            r'relocates with depth, but the total (the quantity '
            r'that matters) is stable.',
        ],
        'elapsed_total': [
            r'Runtime rises monotonically with depth.',
            r'The $d{=}1$ to $d{=}2$ step adds the least.',
        ],
    },
    # Rule 2 was only run at depth=1: it lifts (~19k at k=200)
    # but raises h too little to prune -- |Expanded| stays at the
    # baseline, so it is pure overhead here (contrast Rule 1,
    # inert at d=1). mem_* fall back to _COUNTER_NEUTRAL.
    'rule2': {
        'cnt_expanded': [
            r'$d{=}1$ expands exactly the BPMX-off baseline -- '
            r'the depth-1 lifts raise $h$ but never enough to '
            r'prune.',
        ],
        'cnt_bpmx_attempts': [
            r'$d{=}0$: BPMX off. $d{=}1$: one sweep per expansion '
            r'(equals |Expanded Nodes|).',
        ],
        'cnt_bpmx_lifts': [
            r'$d{=}1$ lifts $h$-values -- unlike Rule 1 (inert at '
            r'$d{=}1$ on consistent $h$), Rule 2 fires at depth 1.',
            r'But the lifts never prune: |Expanded| stays at the '
            r'baseline.',
        ],
        'pct_bpmx_lifts': [
            r'$d{=}1$ has a nonzero per-attempt hit-rate -- Rule 2 '
            r'lifts at depth 1 where Rule 1 does not.',
        ],
        'elapsed_total': [
            r'$d{=}1$ is slower than the baseline (per-expansion '
            r'sweep cost) with no expansion savings -- pure '
            r'overhead here.',
        ],
    },
    # rule3 / cascade: no curated items yet -> every subsection's
    # Insights box falls back to `_COUNTER_NEUTRAL`. Replace with
    # data-derived insights once their s_3 runs land.
    'rule3': {},
    'cascade': {},
    # Propagation depth ladder (BPMX off). Data-derived from the
    # prop_0..5 aggregates.
    'propdepth': {
        'cnt_expanded': [
            r'Propagation prunes expansions monotonically: '
            r'$285$k ($P{=}0$) $\to214$k ($P{=}1$, $-25\%$) '
            r'$\to131$k ($P{=}5$).',
            r'Unlike BPMX rule~1 (inert at $d{=}1$), propagation '
            r'already lifts at $P{=}1$ --- it seeds from the '
            r'exact-$h^{*}$ cache.',
            r'Diminishing returns past $P{=}3$.',
        ],
        'cnt_prop_attempts': [
            r'$0$ at $P{=}0$ (off) up to $\approx\!2.2$M at '
            r'$P{=}5$ --- grows steeply; each deeper wave revisits '
            r'more cells.',
        ],
        'cnt_prop_lifts': [
            r'Grows with depth ($\approx\!241$k at $P{=}1$ to '
            r'$\approx\!822$k at $P{=}5$).',
            r'Per-attempt yield falls --- deeper waves reach fewer '
            r'fresh inconsistencies.',
        ],
        'cnt_prop_waves': [
            r'Mean rises with $P$ but stays below it '
            r'($1.0, 1.9, 2.8, 3.6, 4.4$): many maps converge '
            r'before the depth cap.',
        ],
        'elapsed_total': [
            r'RISES $\approx\!3.5\times$ ($21$s$\to75$s) despite '
            r'fewer expansions.',
            r'The per-wave $h$-evaluation cost dominates '
            r'(\texttt{cnt\_h\_search} grows $\approx\!14\times$) '
            r'--- propagation trades compute for pruning.',
        ],
        'mem_total': [
            r'Nearly flat, slightly decreasing '
            r'($36161\to36003$): the coincident memory peak is '
            r'essentially depth-invariant --- propagation buys '
            r'fewer expansions, not less peak memory.',
        ],
    },
    # Value-of-reuse (rep vs inc cache-only baseline). Data-derived
    # from astar_rep_nested_by_k vs rule_none_..._prop_0_by_k.
    'incvsrep': {
        'cnt_expanded': [
            r'\texttt{rep} expands roughly LINEARLY in $k$ ($347$k at '
            r'$k{=}10 \to 6.9$M at $k{=}200$, $\approx\!20\times$ for '
            r'$20\times$ the starts): with no sharing, every start '
            r'pays a full independent A*.',
            r'\texttt{inc} grows SUBLINEARLY ($114$k$\to285$k, only '
            r'$\approx\!2.5\times$): cache-hit-at-init terminates a '
            r'later start in ONE pop once its optimal path is cached.',
            r'So the gap COMPOUNDS with $k$: $3.1\times$ ($k{=}10$) '
            r'$\to24.3\times$ ($k{=}200$), and is unbounded --- the '
            r'more starts share the goal, the more the cache pays.',
        ],
        'elapsed_total': [
            r'Runtime tracks expansions: \texttt{rep} is $18.2\times$ '
            r'slower at $k{=}200$ ($385$s vs $21$s), the gap widening '
            r'from $3.1\times$ at $k{=}10$.',
        ],
        'mem_total': [
            r'Essentially equal (within $\approx\!4\%$) --- '
            r'\texttt{inc} is even marginally LOWER despite carrying '
            r'the cache, because its early-terminating sub-searches '
            r'hold smaller OPEN/CLOSED peaks.',
            r'So the $\approx\!24\times$ compute win costs no extra '
            r'memory: incremental reuse is close to a free lunch here.',
        ],
    },
    # Cross-mechanism comparison at depth=1. Data-derived from the
    # six d=1 aggregates (rule_none / rule_{1,2,3}_d1 / cascade_d1 /
    # prop_1); numbers quoted at k=200 unless noted.
    'compare1': {
        'cnt_expanded': [
            r'\texttt{depth=0}, rule 1, rule 2 and rule 3 expand '
            r'the IDENTICAL count ($285$k at $k{=}200$): no single '
            r'pathmax rule prunes at depth~1.',
            r'rule 1 is inert (it lifts nothing on consistent~$h$); '
            r'rule 2 and rule 3 DO lift, but the lifts never prune '
            r'at $d{=}1$.',
            r'The cascade and propagation each cut expansions on '
            r'their own: cascade $2.6\times$ fewer '
            r'($285$k$\to109$k, $-62\%$), propagation $-25\%$ '
            r'($\to214$k).',
            r'Stacking them (cascade$+$prop) prunes the MOST '
            r'($\to103$k, $-64\%$) --- but only $\approx\!5\%$ below '
            r'cascade alone ($109$k): once the cascade has pruned, '
            r'propagation on top adds almost nothing.',
            r'Takeaway: at depth~1 the in-search cascade does nearly '
            r'all the pruning; neither the isolated pathmax rules '
            r'nor the pre-search prop stacked on top moves '
            r'expansions much further.',
        ],
        'cnt_bpmx_attempts': [
            r'\texttt{depth=0} and prop launch no sweeps (BPMX off).',
            r'rule 1/2/3 launch one sweep per expansion, so they sit '
            r'at the full baseline expansion count ($285$k).',
            r'cascade launches fewer ($109$k): it prunes its own '
            r'expansions, so there are fewer nodes to sweep.',
            r'cascade$+$prop launches the fewest ($103$k) --- it '
            r'expands the fewest nodes, and one sweep fires per '
            r'expansion.',
        ],
        'cnt_bpmx_lifts': [
            r'\texttt{depth=0}, rule 1 and prop lift nothing (rule 1 '
            r'is inert on consistent~$h$; prop is not a BPMX rule).',
            r'rule 3 lifts the MOST ($219$k) --- yet prunes nothing '
            r'(its |Expanded| stays at the baseline).',
            r'Lift count does not predict pruning: rule 3 lifts '
            r"$3.5\times$ the cascade ($63$k), but only the cascade's "
            r'lifts translate into fewer expansions.',
            r'cascade$+$prop lifts $\approx\!62$k --- essentially '
            r'the same as cascade alone ($63$k): the pre-search '
            r'propagation slightly SUBSUMES the cascade (it pre-'
            r'raises some $h$, so a few cascade lifts no longer '
            r'fire).',
        ],
        'pct_bpmx_lifts': [
            r'Per-attempt hit-rate ranks rule 3 ($41\%$) $>$ '
            r'cascade$+$prop ($32\%$) $\gtrsim$ cascade ($30\%$) $>$ '
            r'rule 2 ($8\%$); \texttt{depth=0}, rule 1 and prop are '
            r'$0\%$.',
            r'The combination edges cascade-alone on hit-rate '
            r'($32\%$ vs $30\%$): propagation enriches $h$ first, so '
            r'each cascade sweep finds an inconsistency to lift '
            r'slightly more often.',
            r'The highest hit-rate (rule 3) still yields zero '
            r'pruning: lifting the PARENT is wasted unless it is '
            r"propagated DOWN to children --- the cascade's rule-1 "
            r'step.',
        ],
        'cnt_prop_attempts': [
            r'Two configs propagate: prop-alone ($\approx\!468$k '
            r'attempts at $k{=}200$) and cascade$+$prop '
            r'($\approx\!409$k); the other five run pre-search '
            r'pathmax OFF.',
            r'The combination makes FEWER prop attempts than '
            r'prop-alone --- the in-search cascade pre-raises some '
            r'$h$, leaving fewer fresh cells for propagation to '
            r'reach.',
        ],
        'cnt_prop_lifts': [
            r'prop-alone lifts $\approx\!241$k of its $\approx\!468$k '
            r'attempts ($\approx\!52\%$); cascade$+$prop lifts '
            r'$\approx\!223$k --- slightly fewer, the cascade having '
            r'already raised some of the same cells (mutual '
            r'subsumption).',
        ],
        'cnt_prop_waves': [
            r'Propagation at depth~1 is a SINGLE wave (mean $=1.0$) '
            r'for both prop-alone and cascade$+$prop; the in-search-'
            r'only mechanisms run no propagation waves.',
        ],
        'mem_total': [
            r'Essentially flat across all seven (within '
            r'$\approx\!0.4\%$): the mechanism choice barely moves '
            r'the coincident memory peak.',
            r'cascade, propagation and their combination sit '
            r'marginally lower (fewer expansions), but memory is not '
            r'where depth-1 mechanisms differ --- expansions and '
            r'runtime are.',
        ],
        'elapsed_total': [
            r'cascade is the standout: $\approx$baseline runtime '
            r'($21.1$s vs $21.2$s at $k{=}200$) while expanding '
            r'$2.6\times$ fewer nodes --- the per-sweep cost is '
            r'offset by the expansions it saves.',
            r'rule 1 and rule 3 are pure overhead '
            r'($\approx\!1.9\times$ baseline); rule 2 costs '
            r'$1.6\times$ --- all three pay the per-expansion sweep '
            r'yet prune nothing.',
            r'propagation costs $1.6\times$ baseline (pre-search wave '
            r'cost) to buy its $-25\%$ expansions.',
            r'cascade$+$prop is the SLOWEST ($40.3$s, '
            r'$\approx\!1.9\times$ baseline and $\approx\!1.9\times$ '
            r'cascade alone): it pays BOTH the per-expansion cascade '
            r'sweeps AND the pre-search propagation waves.',
            r'Verdict at depth~1: the cascade dominates --- it prunes '
            r'substantially AND stays runtime-neutral. Stacking '
            r'propagation on top buys only $\approx\!5\%$ fewer '
            r'expansions for $\approx\!2\times$ the runtime, so the '
            r'combination does NOT pay off here.',
        ],
    },
    # Adaptive-A* comparison. No curated items yet -> every subsection's
    # Insights box falls back to `_COUNTER_NEUTRAL`. Replace with
    # data-derived insights once the `_adapt_1` runs land (s_3 inc_adapt).
    'compare1_adapt': {},
}


# Rule-agnostic one-line fallback used when a (section, counter)
# has no curated insight items (e.g. rule_3 / cascade until their
# data exists). Keeps every subsection's Insights box populated
# without asserting rule-1-specific claims.
_COUNTER_NEUTRAL: dict[str, str] = {
    'cnt_expanded':
        r'Inner-A* node expansions, summed across the $k$ '
        r'sub-searches.',
    'cnt_bpmx_attempts':
        r'BPMX sweeps launched -- one per inner-A* expansion.',
    'cnt_bpmx_lifts':
        r'BPMX lifts that raised an $h$-value, summed across the '
        r'$k$ sub-searches.',
    'pct_bpmx_lifts':
        r'BPMX hit-rate per attempt (lifts / attempts).',
    'cnt_adapt_attempts':
        r'Adaptive-A* harvest trials -- one per plausibly-liftable '
        r'($C_i{-}g_i{>}0$) closed node, summed across the $k$ '
        r'sub-searches.',
    'cnt_adapt_lifts':
        r'Adaptive-A* harvests that tightened the carried bound '
        r'store ($C_i{-}g_i$ beat the prior bound).',
    'pct_adapt_lifts':
        r'Adaptive-A* harvest hit-rate per trial (lifts / '
        r'attempts) -- the symmetric counterpart to '
        r'\texttt{pct\_bpmx\_lifts}.',
    'cnt_prop_attempts':
        r'Pre-search pathmax-propagation attempts, summed across '
        r'the $k$ sub-searches.',
    'cnt_prop_lifts':
        r'Propagation attempts that raised an $h$-value.',
    'cnt_prop_waves':
        r'Mean propagation-wave count per sub-search (a depth '
        r'horizon, MAX-aggregated).',
    'mem_total':
        r'Coincident peak: $\sum$ of the OPEN/CLOSED/cache/bounds '
        r'components of the peak sub-search.',
    'elapsed_total':
        r'Total wall-clock seconds, cumulative across the $k$ '
        r'sub-searches.',
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
