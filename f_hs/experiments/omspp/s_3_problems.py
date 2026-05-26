"""
===============================================================================
 Script: read pair-cluster metadata from i_2_pairs_clusters.csv, randomly
 select n_per_map pairs per (domain, map), reconstruct each pair's GOAL
 ClusterDiamond, and emit -- per pair, per k -- one OMSPP ProblemGrid:
   - 1 start (taken directly from the pair row -- single cell from i_0),
   - k goals (from a single max(k)-shuffle of the goal cluster, sliced
     into NESTED prefixes per k_i: goals(k=10) ⊂ goals(k=20) ⊂ ...).
 Output:
   - a pickle of the list of (detached) problems,
   - a CSV of per-problem metadata (one row per problem).
-------------------------------------------------------------------------------
 Roles
   OMSPP is forward-only. Start is a single cell pinned in i_0 (steps=0,
   min_cells=1). Goal is a region (steps=15-20, min_cells=200). No
   fwd/rev like MOSPP -- a single cell can't supply k>=2 goals.

 Nested-k (graduate) design
   For each pair, ONE rng.sample(goal_cells, k=max(k)) is drawn; the
   problem at k_i takes goals_full[:k_i]. Each k_i+1 strictly extends
   k_i with new goals -- enables paired/nested benchmarking of the
   effect of growing k while holding pair geometry and goal identity
   fixed across the family.

 Cluster reconstruction (deterministic)
   `ClusterDiamond(grid, center, steps)` is a deterministic BFS-style
   expansion -- same (grid, center, steps) ⇒ same footprint. So storing
   only `(center, steps, cells)` in i_1 / i_2 is lossless for downstream
   re-hydration here. NOTE: relies on deterministic ClusterDiamond
   expansion -- if that ever becomes stochastic, this script silently
   emits goals different from what i_1 sampled.
-------------------------------------------------------------------------------
 Core function (general)
   generate_problems(path_drive_csv_in, path_drive_pkl_out,
                     path_drive_csv_out, path_drive_grids_pkl,
                     n_per_map, k, seed=None) -> None

 __main__ (specific use case)
   in:   Experiments/OMSPP/i_2_pairs_clusters.csv
   pkl:  Experiments/Grids/grids.pkl  (bundle of GridMaps)
   out:  Experiments/OMSPP/i_3_problems.pkl
         Experiments/OMSPP/i_3_problems.csv

   n_per_map = 1
   k         = [10, 20, ..., 190, 200]   (range(10, 201, 10))
   seed      = 0

 Memory
   - Pair-CSV is read once into dict[(domain, map)] -> list[_PairRow]
     (small; ~50 B/row).
   - Grids are loaded once from a single pickle bundle on Drive and
     held in a dict[name -> GridMap] for the duration of the run.
   - Final problem list is held in memory (detached, light) for one
     pickle dump.
===============================================================================
"""
import os
import csv
import pickle
import random
import tempfile
import logging
from collections import defaultdict
from typing import NamedTuple

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, ClusterDiamond
from f_hs.problem.i_1_grid import ProblemGrid


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'k',
    'dist_start',
    'dist_goals',
]


class _PairRow(NamedTuple):
    """Per-row record parsed from the s_2_pairs_clusters CSV."""
    domain: str
    map: str
    start_row: int
    start_col: int
    goal_center_row: int
    goal_center_col: int
    goal_steps: int


# ── Helpers ────────────────────────────────────────────────────────────────

def _read_pairs_grouped(drive: Drive,
                        path_drive_csv: str
                        ) -> dict[tuple[str, str], list[_PairRow]]:
    """
    ============================================================================
     Download the s_2 pairs CSV from Drive, parse it, and group rows by
     (domain, map). Preserves on-disk row order within each group, so
     the "first n pairs per map" semantics is well-defined.
    ============================================================================
    """
    _log.info(f'reading {path_drive_csv}')
    text = drive.read(path=path_drive_csv).text
    reader = csv.DictReader(text.splitlines())
    groups: dict[tuple[str, str], list[_PairRow]] = defaultdict(list)
    for row in reader:
        pair = _PairRow(
            domain=row.get('domain', '') or '',
            map=row['map'],
            start_row=int(row['start_row']),
            start_col=int(row['start_col']),
            goal_center_row=int(row['goal_center_row']),
            goal_center_col=int(row['goal_center_col']),
            goal_steps=int(row['goal_steps']),
        )
        groups[(pair.domain, pair.map)].append(pair)
    total = sum(len(rs) for rs in groups.values())
    _log.info(f'  loaded {total:,} pairs across '
              f'{len(groups)} (domain, map) groups')
    return groups


def _load_grids_from_pickle(drive: Drive,
                            path_drive_pkl: str
                            ) -> dict[str, GridMap]:
    """
    ============================================================================
     Download the grids pickle from Drive and return a name -> GridMap
     map. The pickle is expected to hold either a `dict[str, GridMap]`
     (canonical, matching ProblemGrid.Store) or a `list[GridMap]`. Each
     grid carries its own `domain` attribute.
    ============================================================================
    """
    _log.info(f'reading grids pickle: {path_drive_pkl}')
    tmp = tempfile.NamedTemporaryFile(
        suffix='.pkl', delete=False, mode='wb')
    path_local = tmp.name
    tmp.close()
    try:
        drive.download(path_src=path_drive_pkl,
                       path_dest=path_local)
        with open(path_local, 'rb') as f:
            obj = pickle.load(f)
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)
    if isinstance(obj, dict):
        grids = list(obj.values())
    elif isinstance(obj, list):
        grids = obj
    else:
        raise TypeError(
            f'expected dict[str, GridMap] or list[GridMap] in '
            f'{path_drive_pkl}; got {type(obj).__name__}')
    by_name: dict[str, GridMap] = {}
    for g in grids:
        _log.info(f'  loaded: {g.name} '
                  f'(domain={g.domain!r}, '
                  f'{g.rows}x{g.cols}, '
                  f'{len(g):,} valid cells)')
        by_name[g.name] = g
    return by_name


def _build_problems_for_pair(grid: GridMap,
                             pair: _PairRow,
                             ks: list[int],
                             rng: random.Random,
                             ) -> list[tuple[int, ProblemGrid]]:
    """
    ============================================================================
     Reconstruct the GOAL ClusterDiamond from `pair`'s metadata, draw a
     single max(ks)-shuffle of its cells, and for each k in `ks` emit
     one ProblemGrid whose goals are the prefix goals_full[:k]. Strict
     prefix => larger-k problems strictly extend smaller-k ones (paired
     /nested design for measuring the effect of growing k while holding
     start cell + goal-cluster geometry + goal identity fixed).

     The start cell is taken directly from `pair` (single cell, pinned
     in i_0). No draw needed.

     `ks` -- ascending list of distinct positive ints. max(ks) must be
     <= the reconstructed cluster's cell count.

     Returns a list of (k, problem) tuples ordered by ascending k.

     Raises ValueError if the reconstructed goal cluster has fewer
     cells than max(ks) (pipeline-tightness signal -- i_1's min_cells
     should prevent this).
    ============================================================================
    """
    start_cell = grid[pair.start_row][pair.start_col]
    goal_center = grid[pair.goal_center_row][pair.goal_center_col]
    # NOTE: relies on deterministic ClusterDiamond expansion -- same
    # (grid, center, steps) must yield the same footprint that i_1
    # originally sampled. If expansion ever becomes stochastic, this
    # silently diverges.
    cluster_goal = ClusterDiamond(grid=grid,
                                  center=goal_center,
                                  steps=pair.goal_steps)
    goal_cells = list(cluster_goal)
    k_max = ks[-1]
    if len(goal_cells) < k_max:
        raise ValueError(
            f'goal cluster has {len(goal_cells)} cells < max(k)={k_max} '
            f'on {grid.name} '
            f'(center=({pair.goal_center_row},{pair.goal_center_col}), '
            f'steps={pair.goal_steps})')
    # One shuffle, sliced into nested prefixes per k.
    goals_full = rng.sample(goal_cells, k=k_max)
    out: list[tuple[int, ProblemGrid]] = []
    for k in ks:
        name = f'{grid.name}_k{k:03d}'
        out.append((k, ProblemGrid(grid=grid,
                                   starts=[start_cell],
                                   goals=goals_full[:k],
                                   name=name)))
    return out


def _problem_to_meta_row(problem: ProblemGrid,
                         domain: str,
                         k: int) -> dict:
    """
    ============================================================================
     Extract per-problem metadata for the side-car CSV.

     dist_start -- average Manhattan from THE start cell to each of the
                   k goals.
     dist_goals -- average pairwise Manhattan among the k goals (0 when
                   k < 2).
    ============================================================================
    """
    starts = problem.starts_rc
    goals = problem.goals_rc
    if starts and goals:
        avg_sg = (sum(abs(sr - gr) + abs(sc - gc)
                      for sr, sc in starts
                      for gr, gc in goals)
                  / (len(starts) * len(goals)))
    else:
        avg_sg = 0.0
    if len(goals) >= 2:
        n_pairs = len(goals) * (len(goals) - 1) // 2
        total = 0
        for i in range(len(goals)):
            gri, gci = goals[i]
            for j in range(i + 1, len(goals)):
                grj, gcj = goals[j]
                total += abs(gri - grj) + abs(gci - gcj)
        avg_gg = total / n_pairs
    else:
        avg_gg = 0.0
    return {
        'domain':     domain,
        'map':        problem.grid_name,
        'k':          k,
        'dist_start': round(avg_sg, 4),
        'dist_goals': round(avg_gg, 4),
    }


# ── Public API ─────────────────────────────────────────────────────────────

def generate_problems(path_drive_csv_in: str,
                      path_drive_pkl_out: str,
                      path_drive_csv_out: str,
                      path_drive_grids_pkl: str,
                      n_per_map: int,
                      k: int | list[int],
                      seed: int | None = None,
                      ) -> None:
    """
    ============================================================================
     Read pair-cluster metadata from `path_drive_csv_in`, randomly
     select up to `n_per_map` pairs per (domain, map) without
     replacement, and for each selected pair build an OMSPP
     ProblemGrid family (one per value of `k`) by reconstructing the
     goal cluster, drawing max(k) goals once, and slicing the goal list
     into nested prefixes G[:k_i]. The start cell is taken directly
     from the pair row (no draw).

     Then upload:
       - the list of detached problems as a single pickle to
         `path_drive_pkl_out`,
       - per-problem metadata as a CSV to `path_drive_csv_out`
         (one row per (pair, k)).

     `k` -- int (legacy: one problem per pair) or list[int] (one
     problem per k per pair, sharing start + nested goal prefixes).
     The list is sorted ascending internally; values must be positive.

     Grids are loaded once from the bundle pickle at
     `path_drive_grids_pkl` and looked up by name. Pairs whose map is
     absent from the bundle are skipped with a warning. Problems are
     detached before being added to the list (light pickle).

     `seed` -- pass an int for reproducible sampling.
    ============================================================================
    """
    ks = sorted({k}) if isinstance(k, int) else sorted(set(k))
    if not ks or ks[0] < 1:
        raise ValueError(f'k must be a positive int or non-empty '
                         f'list of positive ints; got {k!r}')
    _log.info(f'generate_problems('
              f'in={path_drive_csv_in}, '
              f'grids_pkl={path_drive_grids_pkl}, '
              f'pkl_out={path_drive_pkl_out}, '
              f'csv_out={path_drive_csv_out}, '
              f'n_per_map={n_per_map}, k={ks})')
    drive = Drive.Factory.valdas()
    groups = _read_pairs_grouped(drive=drive,
                                 path_drive_csv=path_drive_csv_in)
    grids_by_name = _load_grids_from_pickle(
        drive=drive, path_drive_pkl=path_drive_grids_pkl)
    rng = random.Random(seed)
    problems: list[ProblemGrid] = []
    tmp_csv = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local_csv = tmp_csv.name
    try:
        writer = csv.DictWriter(tmp_csv,
                                fieldnames=_CSV_COLUMNS,
                                extrasaction='ignore')
        writer.writeheader()
        # Stable iteration order: by (domain, map) -- required for
        # seed-stable RNG draws across re-runs.
        for (domain, name), pairs in sorted(groups.items()):
            grid = grids_by_name.get(name)
            if grid is None:
                _log.warning(f'  skipping {name}: not in grids pickle '
                             f'({len(pairs):,} pairs dropped)')
                continue
            n_eff = min(n_per_map, len(pairs))
            selected = rng.sample(pairs, k=n_eff)
            _log.info(f'  building {len(selected):,} pairs * '
                      f'{len(ks)} k = '
                      f'{len(selected) * len(ks):,} '
                      f'problems on {name} '
                      f'({len(pairs):,} pairs available, '
                      f'ks=[{ks[0]}..{ks[-1]}])')
            built = 0
            for pair in selected:
                family = _build_problems_for_pair(grid=grid,
                                                  pair=pair,
                                                  ks=ks,
                                                  rng=rng)
                for k_i, problem in family:
                    writer.writerow(_problem_to_meta_row(
                        problem=problem,
                        domain=domain,
                        k=k_i))
                    problem.detach()
                    problems.append(problem)
                    built += 1
            _log.info(f'    done: {built:,} problems on {name}')
        tmp_csv.close()
        # Pickle the (detached) problem list to a temp file, upload.
        tmp_pkl = tempfile.NamedTemporaryFile(
            suffix='.pkl', delete=False, mode='wb')
        path_local_pkl = tmp_pkl.name
        try:
            pickle.dump(problems, tmp_pkl,
                        protocol=pickle.HIGHEST_PROTOCOL)
            tmp_pkl.close()
            drive.upload(path_src=path_local_pkl,
                         path_dest=path_drive_pkl_out)
            _log.info(f'uploaded pkl -> {path_drive_pkl_out} '
                      f'({len(problems):,} problems)')
            drive.upload(path_src=path_local_csv,
                         path_dest=path_drive_csv_out)
            _log.info(f'uploaded csv -> {path_drive_csv_out}')
        finally:
            if os.path.exists(path_local_pkl):
                os.unlink(path_local_pkl)
    finally:
        try:
            tmp_csv.close()
        except Exception:
            pass
        if os.path.exists(path_local_csv):
            os.unlink(path_local_csv)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters -- OMSPP step s_3: one nested-k problem family per
    # (domain, map). k=[10..200] in steps of 10 -- 20 problems per
    # map; goals are strictly nested across k (k=20's 20 goals = k=10's
    # 10 + 10 new, etc.).
    #
    # ── Mode toggle ─────────────────────────────────────────────────
    # IS_EXTRA=False -> canonical pipeline (n_per_map=1, seed=0):
    #                   writes i_3_problems.{pkl,csv}.
    # IS_EXTRA=True  -> additional robustness batch on a fresh seed
    #                   with a `_extra` suffix on the output paths,
    #                   so the canonical artefacts stay intact and
    #                   the original 25 chains remain reproducible.
    # The shared `rng` inside generate_problems means bumping
    # n_per_map in place on seed=0 reshuffles every chain's goals
    # (RNG state diverges after the larger sample). The disjoint-seed
    # path keeps the canonical 25 chains byte-identical.
    IS_EXTRA = False
    _N_PER_MAP_EXTRA = 4   # +100 new chains (25 maps x 4)
    _SEED_EXTRA = 1

    if IS_EXTRA:
        n_per_map = _N_PER_MAP_EXTRA
        seed = _SEED_EXTRA
        suffix = '_extra'
    else:
        n_per_map = 1
        seed = 0
        suffix = ''

    path_drive_csv_in = ('Experiments/OMSPP/'
                         'i_2_pairs_clusters.csv')
    path_drive_grids_pkl = 'Experiments/Grids/grids.pkl'
    k = list(range(10, 201, 10))
    path_drive_pkl_out = (f'Experiments/OMSPP/'
                          f'i_3_problems{suffix}.pkl')
    path_drive_csv_out = (f'Experiments/OMSPP/'
                          f'i_3_problems{suffix}.csv')
    # Run
    generate_problems(path_drive_csv_in=path_drive_csv_in,
                      path_drive_pkl_out=path_drive_pkl_out,
                      path_drive_csv_out=path_drive_csv_out,
                      path_drive_grids_pkl=path_drive_grids_pkl,
                      n_per_map=n_per_map,
                      k=k,
                      seed=seed)
    _log.info('--- done ---')
