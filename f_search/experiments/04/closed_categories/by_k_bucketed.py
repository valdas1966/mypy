"""
================================================================================
 Per-k pooled aggregation for OMSPP charts, bucketed over consecutive k values.
================================================================================
 Input : Drive  2026/04/Experiments/OMSPP/results_unified.csv
 Output: stdout markdown table (one row per bucket)
         /tmp/OMSPP_by_k_bucketed.dat — pgfplots data file
         overall pooled sanity check
================================================================================
 Aggregation is pooled at the raw-count level: sum(num) / sum(den). Each
 bucket pools _BUCKET_SIZE_IN_K consecutive k values. With 20 k values in
 the dataset and 250 instances per k, a bucket of size n pools n*250
 instances and produces 20/n chart points. Change _BUCKET_SIZE_IN_K to
 re-bucket. S, B, P are taken from Incremental-kA*'s closed list.
================================================================================
"""

import csv
from collections import defaultdict

from f_google.services.drive import Drive
from f_log import get_log

_log = get_log(__name__)

_PATH_SRC = '2026/04/Experiments/OMSPP/results_unified.csv'
_PATH_LOC = '/tmp/results_unified.csv'
_PATH_DAT = '/tmp/OMSPP_by_k_bucketed.dat'

# e.g. size 5 -> 4 points (k in [10..50], [60..100], [110..150], [160..200]).
_BUCKET_SIZE_IN_K = 5          # number of consecutive k values per bucket
_K_STEP           = 10         # step between consecutive k values
_K_MIN            = 10         # smallest k in dataset

_CAND = {
    'k'    : ['k', 'K', 'goal_set_size'],
    's_inc': ['surely_inc', 'S_inc', 'surely_incremental'],
    'b_inc': ['border_inc', 'B_inc', 'borderline_inc'],
    'p_inc': ['surplus_inc', 'P_inc', 'surplus_incremental'],
    'b_agg': ['border_agg', 'B_agg', 'borderline_agg'],
    'v'    : ['valid_cells', 'V', 'n_valid', 'map_valid_cells', 'cells'],
}


def _bucket_id(k: int) -> int:
    """
    ========================================================================
     Map k to a bucket index (pairs of consecutive k values).
    ========================================================================
    """
    return (k - _K_MIN) // (_BUCKET_SIZE_IN_K * _K_STEP)


def _bucket_midpoint(b: int) -> float:
    """
    ========================================================================
     Midpoint of the bucket in units of k.
    ========================================================================
    """
    span = _BUCKET_SIZE_IN_K * _K_STEP
    return _K_MIN + b * span + (span - _K_STEP) / 2.0


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
            d = acc[_bucket_id(k)]
            d['n']  += 1
            d['s']  += int(row[cols['s_inc']])
            d['b']  += int(row[cols['b_inc']])
            d['p']  += int(row[cols['p_inc']])
            d['ba'] += int(row[cols['b_agg']])
            d['v']  += int(row[cols['v']])

    out: dict[int, dict[str, float]] = {}
    for b in sorted(acc):
        d = acc[b]
        closed = d['s'] + d['b'] + d['p']
        out[b] = {
            'kmid' : _bucket_midpoint(b),
            'n'    : float(d['n']),
            'S_pct': 100 * d['s']  / closed,
            'B_pct': 100 * d['b']  / closed,
            'P_pct': 100 * d['p']  / closed,
            'ClV'  : 100 * closed  / d['v'],
            'BaBi' : d['ba'] / d['b'] if d['b'] else float('nan'),
            '_s'   : d['s'], '_b': d['b'], '_p': d['p'],
            '_ba'  : d['ba'], '_v': d['v'],
        }
    return out


def _print_table(data: dict[int, dict[str, float]]) -> None:
    print()
    print('| bucket (k-range) | kmid |  n  |  S%   |  B%  |  P%  | Cl/V% | Ba/Bi |')
    print('|-----------------:|-----:|----:|------:|-----:|-----:|------:|------:|')
    for b, d in data.items():
        lo = _K_MIN + b * _BUCKET_SIZE_IN_K * _K_STEP
        hi = lo + (_BUCKET_SIZE_IN_K - 1) * _K_STEP
        print(f"| {lo:3d}-{hi:3d}          | "
              f"{d['kmid']:4.0f} | {int(d['n']):3d} | "
              f"{d['S_pct']:5.2f} | {d['B_pct']:4.2f} | "
              f"{d['P_pct']:4.2f} | {d['ClV']:5.2f} | "
              f"{d['BaBi']:5.3f} |")

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
        f.write('kmid S B P ClV BaBi\n')
        for b, d in data.items():
            f.write(f"{d['kmid']:.1f} {d['S_pct']:.4f} {d['B_pct']:.4f} "
                    f"{d['P_pct']:.4f} {d['ClV']:.4f} "
                    f"{d['BaBi']:.5f}\n")
    _log.info(f'wrote {_PATH_DAT}')


def run() -> None:
    _download()
    with open(_PATH_LOC) as f:
        header = next(csv.reader(f))
    cols = _resolve_cols(header)
    if cols is None:
        print('UNRECOGNIZED CSV HEADER:')
        print(header)
        return
    data = _aggregate(cols)
    _print_table(data)
    _emit_pgfplots(data)


if __name__ == '__main__':
    run()
