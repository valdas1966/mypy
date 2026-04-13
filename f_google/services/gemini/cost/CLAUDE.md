# cost

## Purpose
Cost study for Gemini API calls. Runs `ask()` 100 times with a
simple prompt and logs the full `ResponseGemini.__repr__()` (including
text, tokens, elapsed, and cost) to CSV.

## Files
| File | Purpose |
|------|---------|
| `_study.py` | Benchmark script: 100 `ask()` calls, saves repr to CSV |
| `benchmark_cost.csv` | Raw results: index + repr per call |
| `ABOUT.html` | Visual report: latency stats, cost analysis, heatmap |
