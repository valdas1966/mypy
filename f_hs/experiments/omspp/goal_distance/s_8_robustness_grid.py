"""
===============================================================================
 goal_distance step s_8 -- cluster-bootstrap robustness for the
 (min_dist x max_steps) phase diagram.

 For each phase-diagram CELL (min_dist, max_steps) and each headline
 metric, compute a 95% confidence interval on the AGG / INC ratio using a
 CLUSTER bootstrap over (domain, map) -- maps are the unit of independent
 variation (instances on the same map share grid topology).

 Mirrors the parent OMSPP s_8 but swaps the per-k loop for a per-cell loop
 and drops the orig/extra/combined batch machinery (single batch here).

 Decision gate
   A (cell, metric) is ROBUST iff the CI half-width is at most `_GATE_FRAC`
   (10%) of the effect magnitude |mean_ratio - 1|.

 AGG rows are filtered to `_AGG_CONFIG = 'lazy_opt_sv'` -- the canonical
 INC-vs-AGG comparison config.

 No KAStar runs here -- pure CSV post-processing.
-------------------------------------------------------------------------------
 Headline metrics
   MEM_TOTAL    = mem_open + mem_closed
   CNT_EXPANDED = cnt_expanded
   ELAPSED      = elapsed_total
-------------------------------------------------------------------------------
 Inputs  (Drive)
   Experiments/OMSPP/goal_distance/kastar_inc_grid.csv
   Experiments/OMSPP/goal_distance/kastar_agg_grid.csv
 Output  (Drive)
   Experiments/OMSPP/goal_distance/robustness_grid.csv
   Columns: min_dist, max_steps, metric, n_clusters,
            mean_ratio, ci_lo, ci_hi, half_width,
            target_half_width, robust
===============================================================================
"""
import csv
import io
import os
import random
import statistics
import tempfile
import logging
from collections import defaultdict

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Drive paths ────────────────────────────────────────────────────────────

_PATH_INC = 'Experiments/OMSPP/goal_distance/kastar_inc_grid.csv'
_PATH_AGG = 'Experiments/OMSPP/goal_distance/kastar_agg_grid.csv'
_PATH_OUT = 'Experiments/OMSPP/goal_distance/robustness_grid.csv'


# ── Analysis config ────────────────────────────────────────────────────────

# Canonical AGG config for the INC-vs-AGG comparison.
_AGG_CONFIG = 'lazy_opt_sv'

# Phase-diagram axes (must match s_2 / s_3).
_MIN_DISTS = [100, 200, 300, 400, 500]
_MAX_STEPS = [20, 30, 40, 50, 60]

# Cluster bootstrap parameters.
_BOOTSTRAP_B = 5_000
_BOOTSTRAP_SEED = 42
_CI_ALPHA = 0.05    # 95% CI

# Decision rule: half_width <= _GATE_FRAC * |mean_ratio - 1|.
_GATE_FRAC = 0.10

# Headline metrics (same column reading for INC and AGG).
_METRICS = ['MEM_TOTAL', 'CNT_EXPANDED', 'ELAPSED']

# Output CSV columns.
_OUT_COLS = [
    'min_dist',
    'max_steps',
    'metric',
    'n_clusters',
    'mean_ratio',
    'ci_lo',
    'ci_hi',
    'half_width',
    'target_half_width',
    'robust',
]


# ── Metric reader ──────────────────────────────────────────────────────────

def _metric_value(row: dict, metric: str) -> float:
    """
    ============================================================================
     Extract one numeric value of `metric` from a CSV row. INC and AGG
     share columns for these three headline metrics.
    ============================================================================
    """
    if metric == 'CNT_EXPANDED':
        return float(row['cnt_expanded'])
    if metric == 'ELAPSED':
        return float(row['elapsed_total'])
    if metric == 'MEM_TOTAL':
        return float(row['mem_open']) + float(row['mem_closed'])
    raise ValueError(f'unknown metric: {metric}')


# ── Drive helpers ──────────────────────────────────────────────────────────

def _read_csv(drive: Drive, path: str) -> list[dict]:
    """
    ============================================================================
     Read one CSV from Drive as a list of dicts. Raises if absent.
    ============================================================================
    """
    if not drive.is_exists(path=path):
        raise FileNotFoundError(f'{path}: NOT FOUND on Drive')
    text = drive.read(path=path).text
    rows = list(csv.DictReader(io.StringIO(text)))
    _log.info(f'  {path}: {len(rows):,} rows')
    return rows


# ── Aggregation ────────────────────────────────────────────────────────────

def _per_cluster_ratios(rows_inc: list[dict],
                        rows_agg: list[dict],
                        min_dist: int,
                        max_steps: int,
                        metric: str,
                        ) -> dict[tuple[str, str], float]:
    """
    ============================================================================
     For one (min_dist, max_steps, metric) cell, build a dict mapping each
     cluster `(domain, map)` to its mean ratio AGG / INC (averaging over
     any instances present within the cluster). AGG rows are filtered to
     `_AGG_CONFIG`.
    ============================================================================
    """
    def _cell(r: dict) -> bool:
        return (int(r['min_dist']) == min_dist
                and int(r['max_steps']) == max_steps)

    inc_by: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows_inc:
        if _cell(r):
            inc_by[(r['domain'], r['map'])].append(
                _metric_value(row=r, metric=metric))

    agg_by: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows_agg:
        if _cell(r) and r.get('config') == _AGG_CONFIG:
            agg_by[(r['domain'], r['map'])].append(
                _metric_value(row=r, metric=metric))

    ratios: dict[tuple[str, str], float] = {}
    for key, inc_vals in inc_by.items():
        agg_vals = agg_by.get(key, [])
        if not agg_vals or not inc_vals:
            continue
        mean_inc = statistics.fmean(inc_vals)
        if mean_inc == 0.0:
            continue
        ratios[key] = statistics.fmean(agg_vals) / mean_inc
    return ratios


def _cluster_bootstrap_ci(values: list[float],
                          B: int = _BOOTSTRAP_B,
                          alpha: float = _CI_ALPHA,
                          seed: int = _BOOTSTRAP_SEED,
                          ) -> tuple[float, float, float]:
    """
    ============================================================================
     Percentile cluster bootstrap on the mean of `values` (one entry per
     cluster). Returns `(mean, ci_lo, ci_hi)`.
    ============================================================================
    """
    n = len(values)
    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(B):
        s = 0.0
        for _ in range(n):
            s += values[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[int((alpha / 2.0) * B)]
    hi = means[int((1.0 - alpha / 2.0) * B) - 1]
    return statistics.fmean(values), lo, hi


# ── Public API ─────────────────────────────────────────────────────────────

def analyse_robustness(path_drive_inc: str = _PATH_INC,
                       path_drive_agg: str = _PATH_AGG,
                       path_drive_csv_out: str = _PATH_OUT,
                       ) -> None:
    """
    ============================================================================
     Read the INC + AGG grid CSVs from Drive and, for each phase-diagram
     cell and headline metric, compute a cluster-bootstrap CI on AGG/INC.
     Upload `robustness_grid.csv` and print a per-metric pass-rate over
     the cells.
    ============================================================================
    """
    drive = Drive.Factory.valdas()
    _log.info('reading benchmark CSVs from Drive:')
    rows_inc = _read_csv(drive=drive, path=path_drive_inc)
    rows_agg = _read_csv(drive=drive, path=path_drive_agg)

    out_rows: list[dict] = []
    for metric in _METRICS:
        n_pass = 0
        n_total = 0
        for min_dist in _MIN_DISTS:
            for max_steps in _MAX_STEPS:
                ratios = _per_cluster_ratios(rows_inc=rows_inc,
                                             rows_agg=rows_agg,
                                             min_dist=min_dist,
                                             max_steps=max_steps,
                                             metric=metric)
                values = list(ratios.values())
                if len(values) < 2:
                    continue
                mean, lo, hi = _cluster_bootstrap_ci(values=values)
                half_width = (hi - lo) / 2.0
                target = _GATE_FRAC * abs(mean - 1.0)
                robust = (target > 0.0) and (half_width <= target)
                out_rows.append({
                    'min_dist':           min_dist,
                    'max_steps':          max_steps,
                    'metric':             metric,
                    'n_clusters':         len(values),
                    'mean_ratio':         round(mean, 4),
                    'ci_lo':              round(lo, 4),
                    'ci_hi':              round(hi, 4),
                    'half_width':         round(half_width, 4),
                    'target_half_width':  round(target, 4),
                    'robust':             robust,
                })
                n_total += 1
                n_pass += int(robust)
        _log.info(f'  {metric}: {n_pass}/{n_total} cells pass the '
                  f'{int(_GATE_FRAC * 100)}%-of-effect gate')

    fd, path_local = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    try:
        with open(path_local, 'w', newline='') as f:
            writer = csv.DictWriter(f,
                                    fieldnames=_OUT_COLS,
                                    extrasaction='ignore')
            writer.writeheader()
            for row in out_rows:
                writer.writerow(row)
        drive.upload(path_src=path_local,
                     path_dest=path_drive_csv_out)
        _log.info(f'uploaded csv -> {path_drive_csv_out} '
                  f'({len(out_rows):,} rows)')
    finally:
        if os.path.exists(path_local):
            os.unlink(path_local)


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    analyse_robustness()
    _log.info('--- done ---')
