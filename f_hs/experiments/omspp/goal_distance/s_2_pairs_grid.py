"""
===============================================================================
 goal_distance step s_2 -- build the per-map GEOMETRIC SKELETON for the
 (min_dist x max_steps) phase-diagram grid by PAIRING sampled clusters and
 BINNING the pairs into distance bands.

 This replaces the retired "deterministic ray" s_2 (which pinned one start
 + five collinear due-SE goal centers per map, reading grids.pkl directly).
 The geometry is now SAMPLED from real cluster pools and selected by
 distance -- giving genuine geometric diversity (many bearings, varied wall
 context) and, crucially, REPLICATION per cell for the s_8 bootstrap.

 Design (pool-pair + band-bin + replicates)
   - Read the START pool (s_0: steps=0 single cells) and the GOAL pool
     (s_1: steps=20 regions) CSVs. Pools are disjoint by construction.
   - For each (domain, map) present in both pools, form every candidate
     (start, goal_center) pair and take its Manhattan center-to-center
     distance -- this IS PairCluster(start_cluster, goal_cluster).distance()
     (center-to-center; the radius is irrelevant to it). s_2 computes it
     cheaply from the coords; s_3 materializes the actual PairCluster per
     selected instance and re-derives the same value as `dist_start`.
   - BIN each pair into a min_dist BAND {100,200,300,400,500} when its
     distance lands within +/- `_BAND_TOL` of the band value (non-
     overlapping windows; pairs between bands are dropped). So min_dist is
     APPROXIMATE (a binned band label); the realized `dist` is recorded
     per row.
   - Keep up to `_REPS` REPLICATES per (map, band), preferring DISTINCT
     goal centers (diverse regions) before reusing a center with a
     different start. Bands that cannot fill `_REPS` are logged (coverage
     made explicit, never hidden) -- far bands thin on small maps.

 Downstream s_3 keeps each selected (start, goal_center) fixed and grows
 the goal-region radius (max_steps) -- 5 (max_steps) instances per skeleton
 row, so a (map, band) cell holds up to `_REPS` x 5 instances.

   in:  Experiments/OMSPP/goal_distance/i_0_clusters_start.csv  (s_0 pool)
        Experiments/OMSPP/goal_distance/i_1_clusters_goals.csv  (s_1 pool)
   out: Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv
        one row per (map, min_dist band, rep) skeleton entry.
===============================================================================
"""
import os
import csv
import random
import tempfile
import logging
from collections import defaultdict
from typing import NamedTuple

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# Phase-diagram distance axis (Manhattan, start -> goal center).
_MIN_DISTS = [100, 200, 300, 400, 500]

# Half-width (cells) of each band's acceptance window: a pair joins band b
# iff |dist - b| <= _BAND_TOL. Bands are 100 apart, so 25 keeps the windows
# disjoint (a pair lands in at most one band; mid-band pairs are dropped).
_BAND_TOL = 25

# Replicates kept per (map, band) -- the within-cell sample the s_8
# cluster-bootstrap resamples. Each rep is a distinct (start, goal_center)
# pair, prefering distinct goal centers for geometric diversity.
_REPS = 5

# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'min_dist',
    'rep',
    'start_row',
    'start_col',
    'goal_center_row',
    'goal_center_col',
    'dist',
]


class _Cluster(NamedTuple):
    """Lightweight per-row record parsed from an s_0 / s_1 pool CSV."""
    domain: str
    map: str
    center_row: int
    center_col: int
    steps: int
    cells: int


# ── Helpers ────────────────────────────────────────────────────────────────

def _read_clusters_grouped(drive: Drive,
                           path_drive_csv: str
                           ) -> dict[tuple[str, str], list[_Cluster]]:
    """
    ============================================================================
     Download a pool CSV from Drive (schema: domain, map, center_row,
     center_col, steps, cells) and group rows by (domain, map). Works for
     both the s_0 START pool and the s_1 GOAL pool (identical schema).
    ============================================================================
    """
    _log.info(f'reading {path_drive_csv}')
    text = drive.read(path=path_drive_csv).text
    reader = csv.DictReader(text.splitlines())
    groups: dict[tuple[str, str], list[_Cluster]] = defaultdict(list)
    for row in reader:
        cluster = _Cluster(
            domain=row.get('domain', '') or '',
            map=row['map'],
            center_row=int(row['center_row']),
            center_col=int(row['center_col']),
            steps=int(row['steps']),
            cells=int(row['cells']),
        )
        groups[(cluster.domain, cluster.map)].append(cluster)
    total = sum(len(cs) for cs in groups.values())
    _log.info(f'  loaded {total:,} clusters across '
              f'{len(groups)} (domain, map) groups')
    return groups


def _band_of(dist: int) -> int | None:
    """
    ============================================================================
     Return the min_dist band a center-to-center distance falls in -- the
     band b with |dist - b| <= `_BAND_TOL` (the nearest one if several were
     ever in range, though the windows are disjoint). None if the distance
     sits between bands.
    ============================================================================
    """
    best: int | None = None
    best_diff: int | None = None
    for band in _MIN_DISTS:
        diff = abs(dist - band)
        if diff <= _BAND_TOL and (best_diff is None or diff < best_diff):
            best = band
            best_diff = diff
    return best


def _select_reps(cands: list[tuple[_Cluster, _Cluster, int]],
                 reps: int,
                 rng: random.Random,
                 ) -> list[tuple[_Cluster, _Cluster, int]]:
    """
    ============================================================================
     Pick up to `reps` pairs from one band's candidates. Seeded-shuffle,
     then a first pass takes pairs with DISTINCT goal centers (diverse
     regions); if that yields fewer than `reps`, a second pass fills the
     remainder from the rest (reusing a goal center with a different
     start). Deterministic given `rng`.
    ============================================================================
    """
    order = list(range(len(cands)))
    rng.shuffle(order)
    chosen_idx: list[int] = []
    used_goals: set[tuple[int, int]] = set()
    # Pass 1 -- distinct goal centers first (region diversity).
    for i in order:
        if len(chosen_idx) >= reps:
            break
        _, goal, _ = cands[i]
        gc = (goal.center_row, goal.center_col)
        if gc in used_goals:
            continue
        used_goals.add(gc)
        chosen_idx.append(i)
    # Pass 2 -- fill the remainder if region diversity ran out.
    if len(chosen_idx) < reps:
        taken = set(chosen_idx)
        for i in order:
            if len(chosen_idx) >= reps:
                break
            if i in taken:
                continue
            chosen_idx.append(i)
            taken.add(i)
    return [cands[i] for i in chosen_idx]


def _skeleton_rows(starts: dict[tuple[str, str], list[_Cluster]],
                   goals: dict[tuple[str, str], list[_Cluster]],
                   rng: random.Random,
                   ) -> list[dict]:
    """
    ============================================================================
     Build the skeleton rows for every (domain, map) in BOTH pools: pair
     each start with each goal center, bin by distance band, and keep up to
     `_REPS` replicates per (map, band). Maps in only one pool are skipped
     with a warning; bands that cannot fill `_REPS` are logged. Returns the
     list of CSV row dicts.
    ============================================================================
    """
    keys_both = sorted(starts.keys() & goals.keys())
    for key in sorted(starts.keys() - goals.keys()):
        _log.warning(f'  skip (no goals)  : {key[0]}/{key[1]}')
    for key in sorted(goals.keys() - starts.keys()):
        _log.warning(f'  skip (no starts) : {key[0]}/{key[1]}')

    rows: list[dict] = []
    for (domain, name) in keys_both:
        ss = starts[(domain, name)]
        gg = goals[(domain, name)]
        # Bucket every candidate pair into its distance band.
        by_band: dict[int, list[tuple[_Cluster, _Cluster, int]]] = {
            band: [] for band in _MIN_DISTS}
        for a in ss:
            for b in gg:
                dist = (abs(a.center_row - b.center_row)
                        + abs(a.center_col - b.center_col))
                band = _band_of(dist=dist)
                if band is not None:
                    by_band[band].append((a, b, dist))
        placed = []
        for band in _MIN_DISTS:
            chosen = _select_reps(cands=by_band[band], reps=_REPS, rng=rng)
            if len(chosen) < _REPS:
                _log.warning(f'  {name}: band {band} short -- '
                             f'{len(chosen)}/{_REPS} reps '
                             f'({len(by_band[band])} candidates)')
            for rep, (a, b, dist) in enumerate(chosen):
                rows.append({
                    'domain':          domain,
                    'map':             name,
                    'min_dist':        band,
                    'rep':             rep,
                    'start_row':       a.center_row,
                    'start_col':       a.center_col,
                    'goal_center_row': b.center_row,
                    'goal_center_col': b.center_col,
                    'dist':            dist,
                })
            placed.append(f'{band}:{len(chosen)}')
        _log.info(f'  {name}: {len(ss)} starts x {len(gg)} goals -> '
                  f'reps/band [{", ".join(placed)}]')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def generate_pairs_grid(path_drive_csv_starts: str,
                        path_drive_csv_goals: str,
                        path_drive_csv_out: str,
                        seed: int | None = None) -> None:
    """
    ============================================================================
     Read the START pool (`path_drive_csv_starts`, from s_0) and the GOAL
     pool (`path_drive_csv_goals`, from s_1), pair clusters per (domain,
     map), bin the pairs into min_dist bands, keep up to `_REPS` replicates
     per (map, band), and upload the skeleton as a CSV to
     `path_drive_csv_out`.

     One row per (map, min_dist band, rep). Columns:
       domain, map, min_dist, rep, start_row, start_col,
       goal_center_row, goal_center_col, dist.

     `min_dist` is the band label; `dist` is the realized Manhattan
     distance start -> goal center (within +/- `_BAND_TOL` of the band).
     `seed` makes the replicate selection reproducible.
    ============================================================================
    """
    _log.info(f'generate_pairs_grid('
              f'starts={path_drive_csv_starts}, '
              f'goals={path_drive_csv_goals}, '
              f'out={path_drive_csv_out}, '
              f'bands={_MIN_DISTS}, tol={_BAND_TOL}, reps={_REPS})')
    drive = Drive.Factory.valdas()
    starts = _read_clusters_grouped(drive=drive,
                                    path_drive_csv=path_drive_csv_starts)
    goals = _read_clusters_grouped(drive=drive,
                                   path_drive_csv=path_drive_csv_goals)
    rng = random.Random(seed)
    rows = _skeleton_rows(starts=starts, goals=goals, rng=rng)
    drive.upload_rows(rows=rows,
                      columns=_CSV_COLUMNS,
                      path=path_drive_csv_out)
    _log.info(f'uploaded csv -> {path_drive_csv_out} '
              f'({len(rows):,} skeleton rows)')


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters -- goal_distance step s_2: pair the s_0 START pool with the
    # s_1 GOAL pool, bin by distance into the min_dist bands, and keep
    # _REPS replicates per (map, band) for the min_dist x max_steps phase
    # diagram. seed=0 -> reproducible replicate selection.
    path_drive_csv_starts = (
        'Experiments/OMSPP/goal_distance/i_0_clusters_start.csv')
    path_drive_csv_goals = (
        'Experiments/OMSPP/goal_distance/i_1_clusters_goals.csv')
    path_drive_csv_out = (
        'Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv')
    seed = 0
    # Run
    generate_pairs_grid(path_drive_csv_starts=path_drive_csv_starts,
                        path_drive_csv_goals=path_drive_csv_goals,
                        path_drive_csv_out=path_drive_csv_out,
                        seed=seed)
    _log.info('--- done ---')
