# f_hs/experiments/clusters

## Purpose
Experimental scripts that sample cluster shapes on `GridMap`s and persist
the results (CSV / pickle) to Google Drive. All scripts here are
problem-family-agnostic: a `ClusterDiamond` of `min_cells=1` is a single
cell (SPP), `min_cells>1` is a subset (OMSPP/MOSPP/MMSPP, depending on
how the downstream pipeline uses it).

## Scripts

### s_0_clusters.py

**What it does.** For each `GridMap` in an iterable, samples `n` random
`ClusterDiamond` instances and streams the metadata to a single CSV on
Drive. **Two-level streaming:**
- a. `grids` is an `Iterable` — callers pass a generator that yields
  one grid at a time; the previous grid is released before the next
  is fetched (peak: ~1 grid in RAM, regardless of map count).
- b. Each sampled `ClusterDiamond` is written to the CSV and
  discarded (peak: ~1 row, regardless of `n`).

Total peak memory is independent of both the number of maps and `n`.

**Public function.**
```python
generate_cluster_samples(grids: Iterable[GridMap],
                         path_drive_csv: str,
                         steps: int,
                         min_cells: int,
                         n: int,
                         max_tries: int = 100) -> None
```

**CSV columns.** `domain, map, center_row, center_col, steps, cells`
(six columns; `cells` is the count of valid cells reached by the BFS
ball).

**When to use.**
- You want a large random sample of cluster statistics for a fixed
  `(steps, min_cells)` pair on a set of real maps.
- You need to characterize the distribution of actual `cells` values
  given a `min_cells` floor (e.g., plot a histogram, find mean/p99).
- You need to visualize where random cluster centers land on each map.

**When NOT to use.**
- Don't use for pair experiments — use `s_1_pairs_clusters.py` instead.
- Don't use for one-off calls — just invoke
  `ClusterDiamond.Factory.random(grid, min_cells, steps)` directly.
- Don't use if you need the full `ClusterDiamond` objects for downstream
  work — the CSV drops everything except metadata. Pair version
  (`s_1`) keeps a pickle alongside the CSV.

**Runtime and size.**
- ~1,300 samples/sec on a 50×50 grid for `steps=10, min_cells=10`.
  Expect **~10–30 min/grid** at `n = 1_000_000` depending on grid size.
- CSV row is ~50 bytes → ~**50 MB/grid** at `n = 1M`.

**`__main__` defaults.** Loads every `*.map` from
`2026/04/experiments/maps`, samples `n = 1_000_000` with `steps = 10`,
`min_cells = 10`, writes
`2026/04/experiments/clusters/steps_10_min_cells_10.csv`.

### s_1_pairs_clusters.py

**What it does.** Reads the per-cluster CSV produced by
`s_0_clusters.py`, groups rows by `(domain, map)`, and for each
group draws `n` random ordered pairs `(a, b)` with `a != b` whose
**Manhattan center-distance** is `>= min_dist`. Streams the pairs
to a single CSV on Drive.

**Public function.**
```python
generate_pairs(path_drive_csv_in: str,
               path_drive_csv_out: str,
               n: int,
               min_dist: int,
               max_tries: int = 10_000,
               seed: int | None = None) -> None
```

**CSV columns.** `domain, map, steps, a_center_row, a_center_col,
a_cells, b_center_row, b_center_col, b_cells, dist` (10 columns;
`steps` is single-valued because both clusters come from the same
s_0 CSV; `dist` is the Manhattan center-distance).

**When to use.**
- Building experimental **start/goal pairs** (or any two-cluster
  instance) from an existing s_0 sample, parameterised by a
  minimum spatial separation. Family is determined by the
  `min_cells` of the source CSV — pair both endpoints from the
  same s_0 run.
- You want reproducible sampling — pass `seed=...`.

**When NOT to use.**
- You need fresh cluster sampling with different `(steps,
  min_cells)` per endpoint — re-run `s_0_clusters.py` with the
  desired parameters first, then pair from those.
- You need the full `ClusterDiamond` object (e.g., the explicit
  cell set) downstream — this script only carries center +
  `cells` count metadata.

**Sampling semantics.**
- With replacement (a cluster can appear in multiple pairs).
- Ordered: `(a, b)` and `(b, a)` are treated as distinct draws.
- `max_tries` bounds **consecutive** rejections per group; the
  counter resets on each accepted pair. Protects against
  infeasible `min_dist` on small grids by aborting that group
  early rather than spinning forever.

**`__main__` defaults.** Reads
`2026/04/experiments/clusters/steps_10_min_cells_10.csv`, samples
`n = 1_000` pairs per map with `min_dist = 20`, writes
`2026/04/experiments/clusters/pairs_min_dist_20.csv`.

## Conventions

- **Streaming Drive I/O.** Map discovery uses
  `Drive.filepaths(path, recursive=True, predicate=...)`; each grid is
  loaded via `Drive.read(path).text` + `GridMap.From.text(...)` right
  before sampling, then released when the generator advances. No
  local files touched. CSV / pickle outputs still use short-lived
  temp files (`tempfile.NamedTemporaryFile(delete=False)` +
  `os.unlink` in `try/finally`) because the Drive upload API expects
  a path.
- **Streaming CSV.** One module-level `_CSV_COLUMNS` list is used as
  both `DictWriter.fieldnames` and the source of the header, with
  `extrasaction='ignore'` so extra keys in the analytics dict are
  silently dropped. No list accumulation in memory.
- **Layer boundary.** `f_ds/` stays I/O-free. All Drive, CSV, and
  pickle logic lives under `f_hs/experiments/`.
- **Progress logging.** Long runs log every 100,000 samples (single-
  cluster) or one line per pair (pair-cluster).

## Typical workflow

1. Place `*.map` files in `2026/04/experiments/maps/`.
2. Run `s_0_clusters.py` to characterize `(steps, min_cells)` choice —
   review the CSV, verify cluster-size distribution is reasonable.
3. Tune parameters if needed; rerun `s_0_clusters.py`.
4. Run `s_1_pairs_clusters.py` to generate `(start, goal)` pairs
   from that CSV, parameterised by `min_dist` (Manhattan).
