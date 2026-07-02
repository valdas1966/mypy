"""
===============================================================================
 goal_distance step s_2 -- build the per-map GEOMETRIC SKELETON for the
 (min_dist x max_steps) phase-diagram grid by SAMPLING start/goal cluster
 pairs directly and BINNING them into distance bands.

 This COLLAPSES the former s_0 (START pool) + s_1 (GOAL pool) + s_2 (pair)
 three-stage pipeline into ONE script. The two intermediate pool CSVs and
 the `u_cluster_pool` dependency are gone: geometry is sampled live from
 grids.pkl via `PairCluster.Factory.random_many` (f_ds), which returns the
 full cross product of a START pool (steps=0 single cells) x a GOAL pool
 (steps=20 regions). The downstream band-bin + replicate design (and the
 `rep` dimension carried through s_3..s_6) is unchanged.

 Design (sample-pairs + band-bin + replicates)
   - For each (domain, map) in grids.pkl, sample up to `_MANY` distinct
     start diamonds (steps=0, min_cells=1) and up to `_MANY` distinct goal
     regions (steps=20, min_cells=200) and form every PairCluster(start,
     goal). `PairCluster.distance()` is the Manhattan center-to-center
     distance -- the same value s_3 re-derives as `dist_start`.
   - BIN each pair into a min_dist BAND {100,200,300,400,500} when its
     distance lands within +/- `_BAND_TOL` of the band value (non-
     overlapping windows; pairs between bands are dropped). So min_dist is
     APPROXIMATE (a binned band label); the realized `dist` is recorded
     per row.
   - Keep up to `_REPS` REPLICATES per (map, band), preferring DISTINCT
     goal centers (diverse regions) before reusing a center with a
     different start. Bands that cannot fill `_REPS` are logged (coverage
     made explicit, never hidden) -- far bands thin on small maps.

 The GOAL regions are sampled at steps=20, min_cells=200 -- guaranteeing
 k=200 goals are drawable at the smallest max_steps the downstream sweep
 rebuilds (s_3 re-grows the region radius per max_steps around the pinned
 center). s_2 keeps only the region CENTER.

 Downstream s_3 keeps each selected (start, goal_center) fixed and grows
 the goal-region radius (max_steps) -- 5 (max_steps) instances per skeleton
 row, so a (map, band) cell holds up to `_REPS` x 5 instances.

   in:  Experiments/Grids/grids.pkl                         (GridMaps)
   out: Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv
        one row per (map, min_dist band, rep) skeleton entry.
===============================================================================
"""
import random
import logging

from f_log import setup_log, get_log
from f_google.services.drive import Drive
from f_ds.grids import GridMap, PairCluster


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
# pair, preferring distinct goal centers for geometric diversity.
_REPS = 5

# Pool size PER SIDE handed to PairCluster.Factory.random_many: up to
# _MANY start cells x _MANY goal regions = up to _MANY^2 candidate pairs
# per map, binned below. Larger than the analysis needs, so the far
# 400/500 bands have enough candidates to fill their replicates.
_MANY = 200

# GOAL-region sampling: radius and min-cells floor. steps=20 is the
# SMALLEST max_steps the downstream sweep rebuilds, so a region with >= 200
# cells here supports k=200 goals at every max_steps in {20..60} (the
# region only grows). max_tries is generous -- sparse mazes need many
# attempts to expand a 200-cell diamond from a random center.
_GOAL_STEPS = 20
_GOAL_MIN_CELLS = 200
_MAX_TRIES = 10_000

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


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_grids(drive: Drive, path_drive_pkl: str) -> list[GridMap]:
    """
    ============================================================================
     Download the grids bundle pickle and return a list[GridMap]. The
     bundle is a dict[name -> GridMap] (canonical) or a list[GridMap].
    ============================================================================
    """
    _log.info(f'reading grids pickle: {path_drive_pkl}')
    obj = drive.read_pickle(path=path_drive_pkl)
    if isinstance(obj, dict):
        grids = list(obj.values())
    elif isinstance(obj, list):
        grids = obj
    else:
        raise TypeError(
            f'expected dict[str, GridMap] or list[GridMap] in '
            f'{path_drive_pkl}; got {type(obj).__name__}')
    _log.info(f'  loaded {len(grids)} grids')
    return grids


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


def _select_reps(cands: list[PairCluster],
                 reps: int,
                 rng: random.Random,
                 ) -> list[PairCluster]:
    """
    ============================================================================
     Pick up to `reps` pairs from one band's candidate PairClusters.
     Seeded-shuffle, then a first pass takes pairs with DISTINCT goal
     centers (diverse regions); if that yields fewer than `reps`, a second
     pass fills the remainder from the rest (reusing a goal center with a
     different start). Deterministic given `rng`.
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
        goal_center = cands[i].cluster_b.center
        gc = (goal_center.row, goal_center.col)
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


def _skeleton_rows(grids: list[GridMap], rng: random.Random) -> list[dict]:
    """
    ============================================================================
     Build the skeleton rows for every grid: sample start x goal cluster
     pairs (PairCluster.Factory.random_many), bin each by its distance
     band, and keep up to `_REPS` replicates per (map, band). Bands that
     cannot fill `_REPS` are logged. Returns the list of CSV row dicts.

     Grids are processed in a stable (sorted by name) order so the shared
     `rng` (replicate selection) and the process-global RNG (pool
     sampling) yield reproducible skeletons across re-runs.
    ============================================================================
    """
    rows: list[dict] = []
    for grid in sorted(grids, key=lambda g: g.name):
        # Sample the full start x goal cross product for this map.
        pairs = PairCluster.Factory.random_many(
            grid=grid,
            many=_MANY,
            steps_a=0,
            min_cells_a=1,
            steps_b=_GOAL_STEPS,
            min_cells_b=_GOAL_MIN_CELLS,
            min_dist=0,
            max_tries=_MAX_TRIES)
        # Bucket every candidate pair into its distance band.
        by_band: dict[int, list[PairCluster]] = {b: [] for b in _MIN_DISTS}
        for pair in pairs:
            band = _band_of(dist=pair.distance())
            if band is not None:
                by_band[band].append(pair)
        placed = []
        for band in _MIN_DISTS:
            chosen = _select_reps(cands=by_band[band], reps=_REPS, rng=rng)
            if len(chosen) < _REPS:
                _log.warning(f'  {grid.name}: band {band} short -- '
                             f'{len(chosen)}/{_REPS} reps '
                             f'({len(by_band[band])} candidates)')
            for rep, pair in enumerate(chosen):
                start = pair.cluster_a.center
                goal = pair.cluster_b.center
                rows.append({
                    'domain':          grid.domain,
                    'map':             grid.name,
                    'min_dist':        band,
                    'rep':             rep,
                    'start_row':       start.row,
                    'start_col':       start.col,
                    'goal_center_row': goal.row,
                    'goal_center_col': goal.col,
                    'dist':            pair.distance(),
                })
            placed.append(f'{band}:{len(chosen)}')
        _log.info(f'  {grid.name}: {len(pairs):,} candidate pairs -> '
                  f'reps/band [{", ".join(placed)}]')
    return rows


# ── Public API ─────────────────────────────────────────────────────────────

def generate_pairs_grid(path_drive_grids_pkl: str,
                        path_drive_csv_out: str,
                        seed: int | None = None) -> None:
    """
    ============================================================================
     Load grids from `path_drive_grids_pkl`, sample start/goal cluster
     pairs per (domain, map) via PairCluster.Factory.random_many, bin the
     pairs into min_dist bands, keep up to `_REPS` replicates per (map,
     band), and upload the skeleton as a CSV to `path_drive_csv_out`.

     One row per (map, min_dist band, rep). Columns:
       domain, map, min_dist, rep, start_row, start_col,
       goal_center_row, goal_center_col, dist.

     `min_dist` is the band label; `dist` is the realized Manhattan
     distance start -> goal center (within +/- `_BAND_TOL` of the band).
     `seed` makes both the pool sampling (process-global RNG) and the
     replicate selection reproducible.
    ============================================================================
    """
    _log.info(f'generate_pairs_grid('
              f'grids_pkl={path_drive_grids_pkl}, '
              f'out={path_drive_csv_out}, '
              f'many={_MANY}, bands={_MIN_DISTS}, tol={_BAND_TOL}, '
              f'reps={_REPS})')
    drive = Drive.Factory.valdas()
    grids = _load_grids(drive=drive, path_drive_pkl=path_drive_grids_pkl)
    if seed is not None:
        random.seed(seed)            # process-global RNG -- pool sampling.
    rng = random.Random(seed)        # local RNG -- replicate selection.
    rows = _skeleton_rows(grids=grids, rng=rng)
    drive.upload_rows(rows=rows,
                      columns=_CSV_COLUMNS,
                      path=path_drive_csv_out)
    _log.info(f'uploaded csv -> {path_drive_csv_out} '
              f'({len(rows):,} skeleton rows)')


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Parameters -- goal_distance step s_2: sample start/goal cluster pairs
    # per map straight from grids.pkl, bin by distance into the min_dist
    # bands, and keep _REPS replicates per (map, band) for the min_dist x
    # max_steps phase diagram. seed=0 -> reproducible pools + selection.
    path_drive_grids_pkl = 'Experiments/Grids/grids.pkl'
    path_drive_csv_out = (
        'Experiments/OMSPP/goal_distance/i_2_pairs_grid.csv')
    seed = 0
    # Run
    generate_pairs_grid(path_drive_grids_pkl=path_drive_grids_pkl,
                        path_drive_csv_out=path_drive_csv_out,
                        seed=seed)
    _log.info('--- done ---')
