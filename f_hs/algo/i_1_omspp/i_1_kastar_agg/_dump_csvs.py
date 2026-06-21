"""
============================================================================
 KAStarAgg trace-to-CSV dumper.

 For each of the 8 param configs on the canonical OMSPP
 problem (grid_4x4_obstacle_omspp, MIN aggregator), runs the
 algorithm with `is_tracing=True` and writes one CSV per
 non-invariant counter into:

     csvs/{config}/{counter}.csv

 The 6 non-invariant counters dumped:
   cnt_h_search, cnt_h_update,
   cnt_phi_search, cnt_phi_update,
   cnt_push, cnt_pop

 Each CSV lists the states that contributed to that counter
 in process order. Lazy configs report `cnt_h_update == 0` /
 `cnt_phi_update == 0` by structure; the corresponding CSV
 has only its header row.

 Schema (per row): `order, event, state, phase` where:
   - `order` — 1-based row index within this CSV.
   - `event` — the counter name (e.g. 'cnt_h_search').
   - `state` — `canonize(state)` (e.g. `(0,0)` for cells).
   - `phase` — `'search'` or `'update'`. Matches the
     structural phase axis (the same one `elapsed_search` /
     `elapsed_update` use): rows inside the eager
     `_refresh_priorities` body show `'update'`; every other
     row (main loop pop, first-time push, lazy stale-pop,
     goal re-push) shows `'search'`. The `phase` column
     replaces the previous on_goal-separator design — sub-
     search boundaries are now visible directly via the
     `search` ↔ `update` transitions (`cnt_push` in eager is
     the most informative view).

 Run from repo root:
     python -m f_hs.algo.i_1_omspp.i_1_kastar_agg._dump_csvs
============================================================================
"""

import csv
from pathlib import Path

from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_1_grid import ProblemGrid


_NON_INVARIANT_COUNTERS: tuple[str, ...] = (
    'cnt_h_search',
    'cnt_h_update',
    'cnt_phi_search',
    'cnt_phi_update',
    'cnt_push',
    'cnt_pop',
)


def _config_name(is_lazy: bool,
                 is_opt: bool,
                 store_vector: bool) -> str:
    """
    ========================================================================
     Build a folder-safe config name like 'lazy_noopt_nosv'.
    ========================================================================
    """
    lazy = 'lazy' if is_lazy else 'eager'
    opt = 'opt' if is_opt else 'noopt'
    sv = 'sv' if store_vector else 'nosv'
    return f'{lazy}_{opt}_{sv}'


def _run_config(is_lazy: bool,
                is_opt: bool,
                store_vector: bool) -> KAStarAgg:
    """
    ========================================================================
     Run KAStarAgg-MIN on the canonical OMSPP problem with
     tracing enabled. Returns the populated algo.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    algo = KAStarAgg(
        problem=p,
        h=lambda s, g: float(s.distance(g)),
        agg='MIN',
        is_lazy=is_lazy,
        is_opt=is_opt,
        store_vector=store_vector,
        is_tracing=True,
    )
    algo.run()
    return algo


def _write_counter_csv(path: Path,
                       counter: str,
                       traces: list[dict]) -> None:
    """
    ========================================================================
     Write one CSV per counter. Filters `traces` to events
     whose `counter` is the target counter OR 'on_goal'
     (preserving original order). Writes header
     `order,event,state,n`.
    ========================================================================
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['order', 'event', 'state', 'phase'])
        order = 0
        for ev in traces:
            if ev['counter'] != counter:
                continue
            order += 1
            w.writerow([order, ev['counter'],
                        str(ev['state']), ev['phase']])


def main() -> None:
    """
    ========================================================================
     Generate `csvs/{config}/{counter}.csv` for all 8 param
     configs × 6 non-invariant counters = 48 CSV files.
    ========================================================================
    """
    here = Path(__file__).parent
    csvs_root = here / 'csvs'

    n_files = 0
    for is_lazy in (False, True):
        for is_opt in (False, True):
            for store_vector in (False, True):
                cfg = _config_name(is_lazy, is_opt, store_vector)
                algo = _run_config(is_lazy, is_opt, store_vector)
                cfg_dir = csvs_root / cfg
                for counter in _NON_INVARIANT_COUNTERS:
                    path = cfg_dir / f'{counter}.csv'
                    _write_counter_csv(
                        path=path,
                        counter=counter,
                        traces=algo.traces,
                    )
                    n_files += 1
                # Mini summary print for sanity.
                tally = {c: sum(ev['n']
                                for ev in algo.traces
                                if ev['counter'] == c)
                         for c in _NON_INVARIANT_COUNTERS}
                tally_str = ', '.join(
                    f'{c.removeprefix("cnt_")}={v}'
                    for c, v in tally.items())
                print(f'{cfg:24s} {tally_str}')
    print(f'\nWrote {n_files} CSV files under {csvs_root}/')


if __name__ == '__main__':
    main()
