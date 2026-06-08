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
