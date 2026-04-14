"""
================================================================================
 Per-k pooled aggregation for OMSPP Table 2 / line charts.
================================================================================
 Input : Drive  2026/04/Experiments/OMSPP/results_unified.csv
 Output: stdout markdown table (20 rows, k=10..200)
         /tmp/OMSPP_by_k.dat  — pgfplots data file
         overall pooled sanity check (should match 96.6 / 3.4 / 13.6 / 0.94)
================================================================================
 Aggregation: pooled ( sum(num) / sum(den) ), NOT mean of per-instance ratios.
 S, B, P are taken from Incremental-kA*'s closed list;
 Cl/V  = |closed_inc| / |V| ;
 Ba/Bi = |border_agg| / |border_inc|  (Aggregative-kA*_min vs Incremental).
================================================================================
"""

import csv
from collections import defaultdict

from f_google.services.drive import Drive
from f_log import get_log

_log = get_log(__name__)

_PATH_SRC = '2026/04/Experiments/OMSPP/results_unified.csv'
_PATH_LOC = '/tmp/results_unified.csv'
_PATH_DAT = '/tmp/OMSPP_by_k.dat'

# Column-name candidates. If your CSV uses different names, the script
# prints the header and exits so you can tell me the right ones.
_CAND = {
    'k'    : ['k', 'K', 'goal_set_size'],
    's_inc': ['surely_inc', 'S_inc', 'surely_incremental'],
    'b_inc': ['border_inc', 'B_inc', 'borderline_inc'],
    'p_inc': ['surplus_inc', 'P_inc', 'surplus_incremental'],
    'b_agg': ['border_agg', 'B_agg', 'borderline_agg'],
    'v'    : ['valid_cells', 'V', 'n_valid', 'map_valid_cells', 'cells'],
}


def _download() -> None:
    drive = Drive.Factory.valdas()
    drive.download(path_src=_PATH_SRC, path_dest=_PATH_LOC)
    _log.info(f'downloaded {_PATH_SRC} -> {_PATH_LOC}')


def _resolve_cols(header: list[str]) -> dict[str, str] | None:
    resolved: dict[str, str] = {}
    for key, candidates in _CAND.items():
        found = next((c for c in candidates if c in header), None)
        if found is None:
            return None
        resolved[key] = found
    return resolved


def _aggregate(cols: dict[str, str]) -> dict[int, dict[str, float]]:
    acc: dict[int, dict[str, int]] = defaultdict(
        lambda: {'n': 0, 's': 0, 'b': 0, 'p': 0, 'ba': 0, 'v': 0}
    )
    with open(_PATH_LOC) as f:
        reader = csv.DictReader(f)
        for row in reader:
            k = int(row[cols['k']])
            d = acc[k]
            d['n']  += 1
            d['s']  += int(row[cols['s_inc']])
            d['b']  += int(row[cols['b_inc']])
            d['p']  += int(row[cols['p_inc']])
            d['ba'] += int(row[cols['b_agg']])
            d['v']  += int(row[cols['v']])

    out: dict[int, dict[str, float]] = {}
    for k in sorted(acc):
        d = acc[k]
        closed = d['s'] + d['b'] + d['p']
        out[k] = {
            'n'    : float(d['n']),
            'S_pct': 100 * d['s']  / closed,
            'B_pct': 100 * d['b']  / closed,
            'P_pct': 100 * d['p']  / closed,
            'ClV'  : 100 * closed  / d['v'],
            'BaBi' : d['ba'] / d['b'] if d['b'] else float('nan'),
            # keep raw sums for overall rollup
            '_s'   : d['s'], '_b': d['b'], '_p': d['p'],
            '_ba'  : d['ba'], '_v': d['v'],
        }
    return out


def _print_table(data: dict[int, dict[str, float]]) -> None:
    print()
    print('|  k  |  n  |  S%   |  B%  |  P%  | Cl/V% | Ba/Bi |')
    print('|----:|----:|------:|-----:|-----:|------:|------:|')
    for k, d in data.items():
        print(f"| {k:3d} | {int(d['n']):3d} | "
              f"{d['S_pct']:5.2f} | {d['B_pct']:4.2f} | "
              f"{d['P_pct']:4.2f} | {d['ClV']:5.2f} | "
              f"{d['BaBi']:5.3f} |")

    # Overall pooled rollup (sanity check vs 96.6 / 3.4 / 13.6 / 0.94).
    ts = sum(d['_s']  for d in data.values())
    tb = sum(d['_b']  for d in data.values())
    tp = sum(d['_p']  for d in data.values())
    tba= sum(d['_ba'] for d in data.values())
    tv = sum(d['_v']  for d in data.values())
    tn = sum(int(d['n']) for d in data.values())
    tc = ts + tb + tp
    print()
    print('Overall pooled:')
    print(f"  n={tn}  S%={100*ts/tc:.3f}  B%={100*tb/tc:.3f}  "
          f"P%={100*tp/tc:.3f}  Cl/V%={100*tc/tv:.3f}  "
          f"Ba/Bi={tba/tb:.4f}")


def _emit_pgfplots(data: dict[int, dict[str, float]]) -> None:
    with open(_PATH_DAT, 'w') as f:
        f.write('k S B P ClV BaBi\n')
        for k, d in data.items():
            f.write(f"{k} {d['S_pct']:.4f} {d['B_pct']:.4f} "
                    f"{d['P_pct']:.4f} {d['ClV']:.4f} "
                    f"{d['BaBi']:.5f}\n")
    _log.info(f'wrote {_PATH_DAT}')


def run() -> None:
    _download()
    with open(_PATH_LOC) as f:
        header = next(csv.reader(f))
    cols = _resolve_cols(header)
    if cols is None:
        print('UNRECOGNIZED CSV HEADER — tell Claude these column names:')
        print(header)
        return
    data = _aggregate(cols)
    _print_table(data)
    _emit_pgfplots(data)


if __name__ == '__main__':
    run()
