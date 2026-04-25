"""
===============================================================================
 Script: read pair-cluster metadata from i_1_pairs_clusters.csv, reconstruct
 the two ClusterDiamond objects per pair, sample k random cells from
 cluster A (-> goals) and one random cell from cluster B (-> start), build
 a multi-goal ProblemGrid per pair, and emit:
   - a pickle of the list of (detached) problems,
   - a CSV of per-problem metadata (one row per problem).
-------------------------------------------------------------------------------
 Core function (general)
   generate_problems(path_drive_csv_in, path_drive_pkl_out,
                     path_drive_csv_out, path_drive_maps,
                     n_per_map, k, seed=None) -> None

 __main__ (specific use case)
   in:  2026/04/experiments/mospp/i_1_pairs_clusters.csv
   maps: 2026/04/experiments/maps
   out: 2026/04/experiments/mospp/i_2_problems.pkl
        2026/04/experiments/mospp/i_2_problems.csv

 Sampling
   - Per-pair: k cells sampled WITHOUT replacement from cluster A's valid
     cells (clamped to len(cluster_a) when k exceeds the cluster size);
     1 cell sampled uniformly from cluster B.
   - Pairs from the input CSV are taken in their on-disk order: the
     FIRST n rows per (domain, map) become problems; later rows are
     ignored.

 Memory
   - Pair-CSV is read once into dict[(domain, map)] -> list[_PairRow]
     (small; ~50 B/row).
   - Maps are streamed: one grid loaded from Drive at a time, all
     problems for that map are built and detached, the grid is
     released before the next is fetched (peak ~1 grid in RAM).
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
    'name',
    'n_starts',
    'n_goals',
    'avg_dist_starts_to_goals',
    'avg_dist_between_goals',
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


def _load_grid(drive: Drive,
               path_drive_maps: str,
               name: str) -> GridMap:
    """
    ============================================================================
     Download a single .map file and parse it to a GridMap. Map name is
     the file stem (the .map file lives at `<path_drive_maps>/<name>.map`).
    ============================================================================
    """
    path = f'{path_drive_maps}/{name}.map'
    _log.info(f'  reading grid: {path}')
    text = drive.read(path=path).text
    grid = GridMap.From.text(content=text, name=name)
    _log.info(f'    -> {grid.name}: {grid.rows}x{grid.cols}, '
              f'{len(grid):,} valid cells')
    return grid


def _build_problem(grid: GridMap,
                   pair: _PairRow,
                   k: int,
                   rng: random.Random,
                   problem_idx: int,
                   ) -> ProblemGrid | None:
    """
    ============================================================================
     Reconstruct the two ClusterDiamond instances from `pair`'s
     metadata, sample k goals (without replacement) from cluster A and
     1 start (uniform) from cluster B, and build a multi-goal
     ProblemGrid. Returns None when either cluster is empty (stale
     center under wall reshuffle, etc.) so the caller can skip cleanly.
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
    if not cells_a or not cells_b:
        return None
    # k goals from A (without replacement, clamped to cluster size).
    k_eff = min(k, len(cells_a))
    goals = rng.sample(cells_a, k=k_eff)
    # 1 start from B.
    start = rng.choice(cells_b)
    name = f'{grid.name}_{problem_idx:06d}'
    return ProblemGrid(grid=grid,
                       starts=[start],
                       goals=goals,
                       name=name)


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
        'name': problem.name,
        'n_starts': len(starts),
        'n_goals': len(goals),
        'avg_dist_starts_to_goals': round(avg_sg, 4),
        'avg_dist_between_goals': round(avg_gg, 4),
    }


# ── Public API ──────────────────────────────────────────────────────────────

def generate_problems(path_drive_csv_in: str,
                      path_drive_pkl_out: str,
                      path_drive_csv_out: str,
                      path_drive_maps: str,
                      n_per_map: int,
                      k: int,
                      seed: int | None = None,
                      ) -> None:
    """
    ============================================================================
     Read pair-cluster metadata from `path_drive_csv_in`, build up to
     `n_per_map` MOSPP-style ProblemGrid problems per (domain, map) by
     reconstructing the two clusters and sampling (k goals from A, 1
     start from B), then upload:
       - the list of detached problems as a single pickle to
         `path_drive_pkl_out`,
       - per-problem metadata as a CSV to `path_drive_csv_out`.

     Grids are loaded one at a time from `path_drive_maps`; problems
     are detached before being added to the list (light pickle).

     `seed` -- pass an int for reproducible sampling.
    ============================================================================
    """
    _log.info(f'generate_problems('
              f'in={path_drive_csv_in}, '
              f'pkl_out={path_drive_pkl_out}, '
              f'csv_out={path_drive_csv_out}, '
              f'n_per_map={n_per_map}, k={k})')
    drive = Drive.Factory.valdas()
    groups = _read_pairs_grouped(drive=drive,
                                 path_drive_csv=path_drive_csv_in)
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
            head = pairs[:n_per_map]
            _log.info(f'  building {len(head):,} problems on '
                      f'{name} '
                      f'({len(pairs):,} pairs available, '
                      f'k={k})')
            grid = _load_grid(drive=drive,
                              path_drive_maps=path_drive_maps,
                              name=name)
            built = 0
            for idx, pair in enumerate(head):
                problem = _build_problem(grid=grid,
                                         pair=pair,
                                         k=k,
                                         rng=rng,
                                         problem_idx=idx)
                if problem is None:
                    continue
                writer.writerow(_problem_to_meta_row(
                    problem=problem, domain=domain))
                problem.detach()
                problems.append(problem)
                built += 1
            _log.info(f'    done: {built:,} problems on {name}')
            # Drop the grid before fetching the next map.
            del grid
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
    path_drive_maps = '2026/04/experiments/maps'
    n_per_map = 1
    k = 10
    path_drive_pkl_out = ('2026/04/experiments/mospp/'
                          'i_2_problems.pkl')
    path_drive_csv_out = ('2026/04/experiments/mospp/'
                          'i_2_problems.csv')
    # Run
    generate_problems(path_drive_csv_in=path_drive_csv_in,
                      path_drive_pkl_out=path_drive_pkl_out,
                      path_drive_csv_out=path_drive_csv_out,
                      path_drive_maps=path_drive_maps,
                      n_per_map=n_per_map,
                      k=k)
    _log.info('--- done ---')
