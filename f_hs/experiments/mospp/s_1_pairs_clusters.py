"""
===============================================================================
 Script: read sampled clusters from s_0_clusters CSV and emit n random
 *distinct* ordered pairs per (domain, map), constrained by a minimum
 center-distance, to a single CSV on Google Drive.
-------------------------------------------------------------------------------
 Distinctness
   Pairs are ordered-distinct: each (a, b) is emitted at most once, but
   (A, B) and (B, A) may both appear (different orientations are
   different pairs). Re-sampling continues until `n` distinct pairs are
   collected or `max_tries` consecutive rejections (collision, self,
   or below `min_dist`) abort the group.
-------------------------------------------------------------------------------
 Core function (general)
   generate_pairs(path_drive_csv_in, path_drive_csv_out,
                  n, min_dist, max_tries=10_000, seed=None) -> None

 __main__ (user's specific use case)
   Read 2026/04/experiments/clusters/steps_10_min_cells_10.csv, sample
   n = 1_000 pairs per map with min_dist = 20 (Manhattan), write to
   2026/04/experiments/clusters/pairs_min_dist_20.csv.

 Distance
   Manhattan between cluster centers -- natural metric for diamond
   (4-connected BFS) clusters.

 Memory
   - Input CSV is read once into dict[(domain, map)] -> list[_Cluster];
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
    'steps',
    'a_center_row',
    'a_center_col',
    'a_cells',
    'b_center_row',
    'b_center_col',
    'b_cells',
    'dist',
]


class _Cluster(NamedTuple):
    """Lightweight per-row record parsed from the s_0_clusters CSV."""
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
     Download the s_0 clusters CSV from Drive, parse it, and group rows
     by (domain, map). Returns dict mapping (domain, map) -> list of
     _Cluster records.
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


def _sample_pairs(clusters: list[_Cluster],
                  n: int,
                  min_dist: int,
                  max_tries: int,
                  rng: random.Random,
                  ) -> list[tuple[_Cluster, _Cluster, int]]:
    """
    ============================================================================
     Draw n random ordered-distinct pairs (a, b) with replacement from
     `clusters`, accepting only pairs with a != b, Manhattan distance
     between centers >= min_dist, and (a, b) not yet emitted (ordered:
     (A, B) and (B, A) are distinct). Aborts after `max_tries`
     consecutive rejections (collision, self, or below min_dist) and
     returns what was accumulated.
    ============================================================================
    """
    pairs: list[tuple[_Cluster, _Cluster, int]] = []
    if len(clusters) < 2:
        return pairs
    seen: set[tuple[_Cluster, _Cluster]] = set()
    tries = 0
    while len(pairs) < n and tries < max_tries:
        a = rng.choice(clusters)
        b = rng.choice(clusters)
        if a is b:
            tries += 1
            continue
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


# ── Public API ──────────────────────────────────────────────────────────────

def generate_pairs(path_drive_csv_in: str,
                   path_drive_csv_out: str,
                   n: int,
                   min_dist: int,
                   max_tries: int = 100,
                   seed: int | None = None,
                   ) -> None:
    """
    ============================================================================
     Read sampled clusters from `path_drive_csv_in` (output of
     s_0_clusters), for each (domain, map) sample `n` random
     ordered-distinct pairs (a, b) with Manhattan center-distance
     >= `min_dist` (each (a, b) emitted at most once; (A, B) and
     (B, A) are distinct), and stream the pairs to a single CSV at
     `path_drive_csv_out` on Drive.

     `max_tries` bounds consecutive rejections per (domain, map)
     before aborting that group early -- protects against infeasible
     `min_dist` choices on small grids and against pair-space
     exhaustion (e.g. n > |clusters| * (|clusters| - 1)).

     `seed` -- pass an int for reproducible sampling.

     One row per pair. Columns:
       domain, map, steps,
       a_center_row, a_center_col, a_cells,
       b_center_row, b_center_col, b_cells,
       dist.
    ============================================================================
    """
    _log.info(f'generate_pairs('
              f'in={path_drive_csv_in}, '
              f'out={path_drive_csv_out}, '
              f'n={n}, min_dist={min_dist})')
    drive = Drive.Factory.valdas()
    groups = _read_clusters_grouped(drive=drive,
                                    path_drive_csv=path_drive_csv_in)
    rng = random.Random(seed)
    tmp = tempfile.NamedTemporaryFile(
        suffix='.csv', delete=False, mode='w', newline='')
    path_local = tmp.name
    try:
        writer = csv.DictWriter(tmp,
                                fieldnames=_CSV_COLUMNS,
                                extrasaction='ignore')
        writer.writeheader()
        total_emitted = 0
        for (domain, name), clusters in sorted(groups.items()):
            _log.info(f'  sampling {n:,} pairs on {name} '
                      f'({len(clusters):,} clusters available, '
                      f'min_dist={min_dist})')
            pairs = _sample_pairs(clusters=clusters,
                                  n=n,
                                  min_dist=min_dist,
                                  max_tries=max_tries,
                                  rng=rng)
            for a, b, d in pairs:
                writer.writerow({
                    'domain': domain,
                    'map': name,
                    'steps': a.steps,
                    'a_center_row': a.center_row,
                    'a_center_col': a.center_col,
                    'a_cells': a.cells,
                    'b_center_row': b.center_row,
                    'b_center_col': b.center_col,
                    'b_cells': b.cells,
                    'dist': d,
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
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters
    path_drive_csv_in = ('2026/04/experiments/mospp/i_0_clusters.csv')
    n = 100
    min_dist = 100
    path_drive_csv_out = (f'2026/04/experiments/mospp/i_1_pairs_clusters.csv')
    # Run
    generate_pairs(path_drive_csv_in=path_drive_csv_in,
                   path_drive_csv_out=path_drive_csv_out,
                   n=n,
                   min_dist=min_dist)
    _log.info('--- done ---')
