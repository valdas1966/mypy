# hs_game — Heuristic Search Node Category Visualizer

## Purpose
Single-file, zero-dependency web app that lets the user design a small
2D grid (start, goals, obstacles) and see — **live, without a Run
button** — how A* classifies each cell as
**Surely expanded** (`f < C*`), **Borderline** (`f = C*`), or
**Surplus** (`f > C*`), for each prefix `T_k = {t_1,…,t_k}` of placed
goals.

Everything is OMSPP: a single goal is just `k=1`. The mathematics and
colors follow the OMSPP node-category report (Drive:
`2026/04/reports/OMSPP.tex`).

## Files
| File | Purpose |
|------|---------|
| `index.html` | Self-contained app (HTML + CSS + vanilla JS). |

No Python, no build step — runs by opening the file locally *or* by
serving the folder via GitHub Pages.

## Model
- Grid: `rows × cols`, both in `[2, 10]`.
- Movement: 4-connected, unit cost.
- Heuristic: Manhattan (consistent for this graph).
- `g*(n)` computed by BFS from start; `C*_i = g*(t_i)`.
- `f_i(n) = g*(n) + |n − t_i|₁`.

## Category rule (for the k-th grid, using goals `T_k`)
Non-obstacle, reachable cell `n`:
- **Surely** if `∃ i ≤ k : f_i(n) < C*_i`
- **Borderline** if not surely and `∃ i ≤ k : f_i(n) = C*_i`
- **Surplus** otherwise

This is the union-over-goals categorization — it equals the set any
best-first OMSPP algorithm with Manhattan heuristic must/may/never
expand for goal set `T_k`.

## Running
- **Local:** open `index.html` in a browser.
- **GitHub Pages:** serve this folder (or include it in the existing
  static site workflow).
