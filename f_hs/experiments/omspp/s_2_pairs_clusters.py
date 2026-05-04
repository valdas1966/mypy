"""
===============================================================================
 Script: read sampled START clusters and GOAL clusters from the s_0 / s_1
 OMSPP CSVs, sample n random (start_cluster, goal_cluster) pairs per
 (domain, map) constrained by a minimum Manhattan center-distance, and
 stream the pairs to a single CSV on Google Drive.
-------------------------------------------------------------------------------
 Roles
   OMSPP pairs are role-asymmetric: one cluster is the START pool entry
   (single-cell clusters from i_0), the other is the GOAL pool entry
   (sizeable region from i_1). Pools are disjoint by construction, so
   self-collision is impossible. Each (start, goal) is emitted at most
   once.

 Distance
   Manhattan between cluster centers — same metric as the MOSPP
   s_1_pairs_clusters convention.

 Re-sampling continues until `n` distinct pairs are collected or
 `max_tries` consecutive rejections (already-emitted, or below
 `min_dist`) abort that group.
-------------------------------------------------------------------------------
 Core function (general)
   generate_pairs(path_drive_csv_starts, path_drive_csv_goals,
                  path_drive_csv_out,
                  n, min_dist, max_tries=10_000, seed=None) -> None

 __main__ (user's specific use case)
   Read Experiments/OMSPP/i_0_clusters_start.csv +
        Experiments/OMSPP/i_1_clusters_goals.csv,
   sample n = 100 pairs per map with min_dist = 100 (Manhattan),
   write to Experiments/OMSPP/i_2_pairs_clusters.csv.

 Memory
   - Input CSVs are read once into dict[(domain, map)] -> list[_Cluster];
     each record is ~6 ints/strs (~50 B), so 1M rows ~ 50 MB.
   - Output rows are streamed (peak: ~1 row).
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


# CSV column order -- one source of truth for header and rows.
_CSV_COLUMNS = [
    'domain',
    'map',
    'start_row',
    'start_col',
    'goal_center_row',
    'goal_center_col',
    'goal_cells',
    'goal_steps',
    'dist',
]


class _Cluster(NamedTuple):
    """Lightweight per-row record parsed from an s_0 / s_1 CSV."""
    domain: str
    map: str
    steps: int
    center_row: int
    center_col: int
    cells: int


# ── Helpers ────────────────────────────────────────────────────────────────

def _read_clusters_grouped(drive: Drive,
                           path_drive_csv: str
                           ) -> dict[tuple[str, str], list[_Cluster]]:
    """
    ============================================================================
     Download a clusters CSV from Drive, parse it, and group rows by
     (domain, map). Returns dict mapping (domain, map) -> list of
     _Cluster records. Works for both s_0_clusters_start.csv and
     s_1_clusters_goals.csv (identical schema).
    ============================================================================
    """
    _log.info(f'reading {path_drive_csv}')
    text = drive.read(path=path_drive_csv).text
    reader = csv.DictReader(text.splitlines())
    groups: dict[tuple[str, str], list[_Cluster]] = defaultdict(list)
    for row in reader:
        cluster = _Cluster(
            domain=row['domain'],
            map=row['map'],
            steps=int(row['steps']),
            center_row=int(row['center_row']),
            center_col=int(row['center_col']),
            cells=int(row['cells']),
        )
        groups[(cluster.domain, cluster.map)].append(cluster)
    total = sum(len(cs) for cs in groups.values())
    _log.info(f'  loaded {total:,} clusters across '
              f'{len(groups)} (domain, map) groups')
    return groups


def _manhattan(a: _Cluster, b: _Cluster) -> int:
    """
    ============================================================================
     Manhattan distance between two cluster centers.
    ============================================================================
    """
    return (abs(a.center_row - b.center_row)
            + abs(a.center_col - b.center_col))


def _sample_pairs(starts: list[_Cluster],
                  goals: list[_Cluster],
                  n: int,
                  min_dist: int,
                  max_tries: int,
                  rng: random.Random,
                  ) -> list[tuple[_Cluster, _Cluster, int]]:
    """
    ============================================================================
     Draw n random (start, goal) pairs with replacement from `starts`
     and `goals`, accepting only pairs with Manhattan center-distance
     >= min_dist and (start, goal) not yet emitted. Aborts after
     `max_tries` consecutive rejections (duplicate or below min_dist)
     and returns what was accumulated.

     Pools are disjoint by construction (different upstream CSVs), so
     no self-collision check is needed. `min_dist` filters out the
     start-cell-inside-goal-region overlap case (per the user's
     decision to trust min_dist for that filtering).
    ============================================================================
    """
    pairs: list[tuple[_Cluster, _Cluster, int]] = []
    if not starts or not goals:
        return pairs
    seen: set[tuple[_Cluster, _Cluster]] = set()
    tries = 0
    while len(pairs) < n and tries < max_tries:
        a = rng.choice(starts)
        b = rng.choice(goals)
        if (a, b) in seen:
            tries += 1
            continue
        d = _manhattan(a=a, b=b)
        if d < min_dist:
            tries += 1
            continue
        seen.add((a, b))
        pairs.append((a, b, d))
        tries = 0
    return pairs


# ── Public API ─────────────────────────────────────────────────────────────

def generate_pairs(path_drive_csv_starts: str,
                   path_drive_csv_goals: str,
                   path_drive_csv_out: str,
                   n: int,
                   min_dist: int,
                   max_tries: int = 10_000,
                   seed: int | None = None,
                   ) -> None:
    """
    ============================================================================
     Read sampled START clusters from `path_drive_csv_starts` (output of
     s_0_clusters_start) and GOAL clusters from `path_drive_csv_goals`
     (output of s_1_clusters_goals); for each (domain, map) appearing
     in BOTH inputs, sample `n` random distinct (start, goal) pairs
     with Manhattan center-distance >= `min_dist`, and stream the pairs
     to a single CSV at `path_drive_csv_out` on Drive.

     Maps appearing in only one of the two inputs are skipped with a
     warning (matching the skip-and-warn robustness pattern used by
     s_0 / s_1 OMSPP cluster scripts).

     `max_tries` bounds consecutive rejections per (domain, map)
     before aborting that group early -- protects against infeasible
     `min_dist` choices on small grids and against pair-space
     exhaustion (e.g. n > |starts| * |goals|).

     `seed` -- pass an int for reproducible sampling.

     One row per pair. Columns:
       domain, map,
       start_row, start_col,
       goal_center_row, goal_center_col, goal_cells, goal_steps,
       dist.
    ============================================================================
    """
    _log.info(f'generate_pairs('
              f'starts={path_drive_csv_starts}, '
              f'goals={path_drive_csv_goals}, '
              f'out={path_drive_csv_out}, '
              f'n={n}, min_dist={min_dist})')
    drive = Drive.Factory.valdas()
    starts = _read_clusters_grouped(drive=drive,
                                    path_drive_csv=path_drive_csv_starts)
    goals = _read_clusters_grouped(drive=drive,
                                   path_drive_csv=path_drive_csv_goals)
    rng = random.Random(seed)
    # Skip-and-warn on asymmetric coverage: every map must appear in
    # both pools to participate in pair sampling.
    keys_both = sorted(starts.keys() & goals.keys())
    keys_only_starts = sorted(starts.keys() - goals.keys())
    keys_only_goals = sorted(goals.keys() - starts.keys())
    for k in keys_only_starts:
        _log.warning(f'  skip (no goals)  : {k[0]}/{k[1]}')
    for k in keys_only_goals:
        _log.warning(f'  skip (no starts) : {k[0]}/{k[1]}')
    tmp = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local = tmp.name
    try:
        writer = csv.DictWriter(tmp,
                                fieldnames=_CSV_COLUMNS,
                                extrasaction='ignore')
        writer.writeheader()
        total_emitted = 0
        for (domain, name) in keys_both:
            ss = starts[(domain, name)]
            gg = goals[(domain, name)]
            _log.info(f'  sampling {n:,} pairs on {name} '
                      f'({len(ss):,} starts × {len(gg):,} goals, '
                      f'min_dist={min_dist})')
            pairs = _sample_pairs(starts=ss,
                                  goals=gg,
                                  n=n,
                                  min_dist=min_dist,
                                  max_tries=max_tries,
                                  rng=rng)
            for a, b, d in pairs:
                writer.writerow({
                    'domain':          domain,
                    'map':             name,
                    'start_row':       a.center_row,
                    'start_col':       a.center_col,
                    'goal_center_row': b.center_row,
                    'goal_center_col': b.center_col,
                    'goal_cells':      b.cells,
                    'goal_steps':      b.steps,
                    'dist':            d,
                })
            total_emitted += len(pairs)
            short = (' [aborted: hit max_tries]'
                     if len(pairs) < n else '')
            _log.info(f'    done: {len(pairs):,} pairs on '
                      f'{name}{short}')
        tmp.close()
        drive.upload(path_src=path_local,
                     path_dest=path_drive_csv_out)
        _log.info(f'uploaded csv -> {path_drive_csv_out} '
                  f'({total_emitted:,} pairs total)')
    finally:
        # Close the temp file before unlinking — Windows can't delete
        # an open file. `close()` is idempotent on the success path.
        try:
            tmp.close()
        except Exception:
            pass
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters — OMSPP step s_2: pair START clusters with GOAL
    # clusters. n=100 pairs per map; min_dist=100 (Manhattan,
    # center-to-center) — same convention as MOSPP s_1.
    path_drive_csv_starts = (
        'Experiments/OMSPP/i_0_clusters_start.csv')
    path_drive_csv_goals = (
        'Experiments/OMSPP/i_1_clusters_goals.csv')
    n = 100
    min_dist = 100
    path_drive_csv_out = (
        'Experiments/OMSPP/i_2_pairs_clusters.csv')
    # Run
    generate_pairs(path_drive_csv_starts=path_drive_csv_starts,
                   path_drive_csv_goals=path_drive_csv_goals,
                   path_drive_csv_out=path_drive_csv_out,
                   n=n,
                   min_dist=min_dist)
    _log.info('--- done ---')
