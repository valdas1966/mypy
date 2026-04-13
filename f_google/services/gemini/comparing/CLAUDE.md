# comparing

## Purpose
Benchmark comparing `Gemini.ask()` vs `Gemini.ask_str()` runtime
performance. Tests whether the `ResponseGemini` wrapper adds
measurable overhead compared to returning raw text.

## Files
| File | Purpose |
|------|---------|
| `_study.py` | Benchmark script: 100 calls per method, saves CSV |
| `benchmark.csv` | Raw results: method, index, elapsed per call |
| `ABOUT.html` | Visual comparison report with charts and insights |

## Key Finding
No meaningful difference. Both methods average ~0.82s per call.
The 11ms gap (1.3%) is noise. Variance comes from network latency,
not local Python code.
