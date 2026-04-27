"""
===============================================================================
 Script: read pair-cluster metadata from i_1_pairs_clusters.csv, randomly
 select n_per_map pair_clusters per (domain, map), reconstruct the two
 ClusterDiamond objects per selected pair, sample 1 start from cluster
 A and a NESTED family of goal sets from cluster B (one prefix per
 value of k), build an OMSPP ProblemGrid for each k, and emit:
   - a pickle of the list of (detached) problems,
   - a CSV of per-problem metadata (one row per problem).
-------------------------------------------------------------------------------
 Core function (general)
   generate_problems(path_drive_csv_in, path_drive_pkl_out,
                     path_drive_csv_out, path_drive_grids_pkl,
                     n_per_map, k, seed=None) -> None

 __main__ (specific use case)
   in:   2026/04/experiments/mospp/i_1_pairs_clusters.csv
   pkl:  2026/04/experiments/grids/grids.pkl  (bundle of GridMaps)
   out:  2026/04/experiments/mospp/i_2_problems.pkl
         2026/04/experiments/mospp/i_2_problems.csv

 Sampling
   - Pair selection: per (domain, map), `n_per_map` pair_clusters are
     drawn uniformly WITHOUT replacement from the available pairs
     (clamped to the group size when fewer pairs exist).
   - Per selected pair: 1 cell sampled uniformly from cluster A
     (-> start). max(k) cells sampled WITHOUT replacement from cluster
     B once; the resulting ordered list G is sliced into nested
     prefixes G[:k_i] for each k_i in `k`. The k=4 problem's goals are
     thus exactly the k=2 problem's goals plus 2 new (and so on).
     This gives a paired/nested design for measuring the effect of
     growing k while holding start + earlier goals fixed.

 k parameter
   `k` may be an int (single problem per pair, legacy) or a list[int]
   (family: one problem per k value, sharing start + nested goals).
   Sorted ascending internally.

 Memory
   - Pair-CSV is read once into dict[(domain, map)] -> list[_PairRow]
     (small; ~50 B/row).
   - Grids are loaded once from a single pickle bundle on Drive and
     held in a dict[name -> GridMap] for the duration of the run. The
     bundle is small (a few maps in practice) so this is cheaper than
     re-downloading and re-parsing per-map .map files.
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
    'n',
    'm',
    'dist_starts_goals',
    'dist_goals',
]


class _PairRow(NamedTuple):
    """Per-row record parsed from the s_1_pairs_clusters CSV."""
    domain: str
    map: str
    steps: int
    a_center_row: int
    a_center_col: int
    b_center_row: int
    b_center_col: int


# ── Helpers ────────────────────────────────────────────────────────────────

def _read_pairs_grouped(drive: Drive,
                        path_drive_csv: str
                        ) -> dict[tuple[str, str], list[_PairRow]]:
    """
    ============================================================================
     Download the s_1 pairs CSV from Drive, parse it, and group rows by
     (domain, map). Preserves on-disk row order within each group, so the
     "first n pairs per map" semantics is well-defined.
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
            steps=int(row['steps']),
            a_center_row=int(row['a_center_row']),
            a_center_col=int(row['a_center_col']),
            b_center_row=int(row['b_center_row']),
            b_center_col=int(row['b_center_col']),
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

     `drive.read` decodes as text; pickle is binary, so download to a
     temp file and unpickle from disk.
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


def _build_problems(grid: GridMap,
                    pair: _PairRow,
                    ks: list[int],
                    rng: random.Random,
                    pair_id: str,
                    ) -> list[tuple[int, ProblemGrid]]:
    """
    ============================================================================
     Reconstruct the two ClusterDiamond instances from `pair`'s
     metadata, sample 1 start (uniform) from cluster A and max(ks)
     goals (without replacement) from cluster B once, then emit one
     ProblemGrid per k in `ks` whose goals are the prefix G[:k] of the
     same shuffled goal list -- so larger-k problems strictly extend
     smaller-k ones (paired/nested design for measuring the effect of
     k).

     `ks` -- ascending list of distinct positive ints.

     Returns a list of (k, problem) tuples in the same order as `ks`.

     Per the experimental design, cluster A and cluster B must have
     enough cells to support the sampling (>=1 and >=max(ks)
     respectively). If either constraint is violated (e.g. stale
     center under wall reshuffle), raises ValueError so the upstream
     pipeline can be tightened rather than silently emitting an
     unbalanced design.
    ============================================================================
    """
    center_a = grid[pair.a_center_row][pair.a_center_col]
    center_b = grid[pair.b_center_row][pair.b_center_col]
    cluster_a = ClusterDiamond(grid=grid,
                               center=center_a,
                               steps=pair.steps)
    cluster_b = ClusterDiamond(grid=grid,
                               center=center_b,
                               steps=pair.steps)
    cells_a = list(cluster_a)
    cells_b = list(cluster_b)
    k_max = ks[-1]
    if len(cells_a) < 1:
        raise ValueError(
            f'cluster A empty for pair_id={pair_id} on '
            f'{grid.name} (center=({pair.a_center_row},'
            f'{pair.a_center_col}), steps={pair.steps})')
    if len(cells_b) < k_max:
        raise ValueError(
            f'cluster B has {len(cells_b)} cells < max(k)={k_max} '
            f'for pair_id={pair_id} on {grid.name} '
            f'(center=({pair.b_center_row},{pair.b_center_col}), '
            f'steps={pair.steps})')
    # Single start from A; single max(k)-shuffle of B for nested goals.
    start = rng.choice(cells_a)
    goals_full = rng.sample(cells_b, k=k_max)
    out: list[tuple[int, ProblemGrid]] = []
    for k in ks:
        goals = goals_full[:k]
        name = f'{pair_id}_k{k:02d}'
        out.append((k, ProblemGrid(grid=grid,
                                   starts=[start],
                                   goals=goals,
                                   name=name)))
    return out


def _problem_to_meta_row(problem: ProblemGrid,
                         domain: str) -> dict:
    """
    ============================================================================
     Extract per-problem metadata for the side-car CSV. Mirrors the
     fields surfaced by ProblemGrid.__repr__.
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
        'domain': domain,
        'map': problem.grid_name,
        'n': len(starts),
        'm': len(goals),
        'dist_starts_goals': round(avg_sg, 4),
        'dist_goals': round(avg_gg, 4),
    }


# ── Public API ──────────────────────────────────────────────────────────────

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
     select up to `n_per_map` pair_clusters per (domain, map) without
     replacement, and for each selected pair build an OMSPP
     ProblemGrid family (one per value of `k`) by reconstructing the
     two clusters, drawing 1 start from A and max(k) goals from B
     once, and slicing the goal list into nested prefixes G[:k_i].
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
    # CSV is streamed to a temp file as we go.
    tmp_csv = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local_csv = tmp_csv.name
    try:
        writer = csv.DictWriter(tmp_csv,
                                fieldnames=_CSV_COLUMNS,
                                extrasaction='ignore')
        writer.writeheader()
        # Stable iteration order: by (domain, map).
        for (domain, name), pairs in sorted(groups.items()):
            grid = grids_by_name.get(name)
            if grid is None:
                _log.warning(f'  skipping {name}: not in grids pickle '
                             f'({len(pairs):,} pairs dropped)')
                continue
            n_eff = min(n_per_map, len(pairs))
            selected = rng.sample(pairs, k=n_eff)
            _log.info(f'  building {len(selected):,} pairs * '
                      f'{len(ks)} k = {len(selected) * len(ks):,} '
                      f'problems on {name} '
                      f'({len(pairs):,} pairs available, '
                      f'ks={ks})')
            built = 0
            for idx, pair in enumerate(selected):
                pair_id = f'{name}_{idx:06d}'
                family = _build_problems(grid=grid,
                                         pair=pair,
                                         ks=ks,
                                         rng=rng,
                                         pair_id=pair_id)
                for k_i, problem in family:
                    writer.writerow(_problem_to_meta_row(
                        problem=problem, domain=domain))
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
        if os.path.exists(path_local_csv):
            os.unlink(path_local_csv)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters
    path_drive_csv_in = ('2026/04/experiments/mospp/'
                         'i_1_pairs_clusters.csv')
    path_drive_grids_pkl = '2026/04/experiments/grids/grids.pkl'
    n_per_map = 1
    k = [2, 4, 6, 8, 10]
    path_drive_pkl_out = ('2026/04/experiments/mospp/'
                          'i_2_problems.pkl')
    path_drive_csv_out = ('2026/04/experiments/mospp/'
                          'i_2_problems.csv')
    # Run
    generate_problems(path_drive_csv_in=path_drive_csv_in,
                      path_drive_pkl_out=path_drive_pkl_out,
                      path_drive_csv_out=path_drive_csv_out,
                      path_drive_grids_pkl=path_drive_grids_pkl,
                      n_per_map=n_per_map,
                      k=k)
    _log.info('--- done ---')
