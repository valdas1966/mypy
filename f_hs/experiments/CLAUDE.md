# f_hs/experiments

## Purpose
Empirical studies for the heuristic-search algorithms in `f_hs`. Each
domain has its own pipeline of numbered `s_N` scripts (e.g. `omspp/`,
`mospp/`); shared, reusable building blocks live as top-level `u_`
utilities here so the per-domain pipelines stay thin.

## Layout
```
f_hs/experiments/
├── u_cluster_pool.py          shared: sample candidate-location pools
├── _tester_cluster_pool.py    tests for the pure sampler
├── u_cluster_pool_ABOUT.html  visual overview (human reading)
├── mospp/                     MOSPP pipeline (s_0 … )
└── omspp/                     OMSPP pipeline (s_0 … s_8) + goal_distance/
                               + early_stop/    (mission-cancellation: run
                                 k=200, cancel at r reached goals, price cost)
                               + goal_removal/  (broader quota + online-removal
                                 plan; early_stop supersedes its quota half)
```

## u_cluster_pool — candidate-location pool sampler
Samples random `ClusterDiamond`s across grid maps. The pool's character
is set by **parameters**, not by separate scripts:

| Pool | `steps` | `min_cells` | Result |
|------|---------|-------------|--------|
| START | 0 | 1 | single cells |
| GOAL | ≥1 | k | regions of ≥ k cells (k goals drawable later) |

So the per-domain `s_0_clusters_start` (START) and `s_1_clusters_goals`
(GOAL) are the **same** sampler with different `(steps, min_cells)` — they
are thin wrappers over this module.

### API
```python
from f_hs.experiments.u_cluster_pool import sample_pool, generate_pool_csv
```
| Function | Role |
|----------|------|
| `sample_pool(grids, steps, min_cells, n, max_tries)` | pure core — yields one metadata-row dict per sampled cluster; no Drive (unit-testable on an in-memory `GridMap`) |
| `generate_pool_csv(path_drive_grids_pkl, path_drive_csv, steps, min_cells, n, seed, max_tries, drive)` | orchestration — `drive.read_pickle` grids → `sample_pool` → `drive.upload_rows` CSV; what the `s_N` wrappers call |

Drive plumbing (pickle / CSV / temp-file round-trips) lives on the
**`Drive`** facade — `drive.read_pickle(path)`, `drive.upload_pickle(obj,
path)`, `drive.upload_rows(rows, columns, path)` — not in this module.

### CSV schema (shared contract)
`domain, map, center_row, center_col, steps, cells` — one row per cluster.

### Reproducibility
Grid sampling draws from the **process-global** `random` module
(`GridMap.random.cells` → `random.sample`). `generate_pool_csv` seeds via
`random.seed(seed)` when `seed` is set; `sample_pool` leaves the global
RNG to the caller. ⚠ Re-running a wrapper with a seed regenerates the pool
and would cascade to downstream pinned artifacts (`i_2` pairs, `i_3`
problems) — re-run only to deliberately regenerate.

## Conventions
- Per-domain pipelines are `s_N` scripts (numbered by pipeline position).
- Cross-pipeline reusable logic is extracted to `u_` utilities here, with
  Drive I/O kept at the edge (orchestration fn) and pure logic separable
  (testable without Drive).
- Run the sampler tests: `python -m pytest f_hs/experiments/_tester_cluster_pool.py -q`.
