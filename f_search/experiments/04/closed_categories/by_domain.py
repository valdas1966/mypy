"""
================================================================================
 Per-domain pooled aggregation for OMSPP by-domain figure.
================================================================================
 Input : Drive  2026/04/Experiments/OMSPP/results_unified.csv
 Output: stdout markdown table (5 rows, one per domain)
         /tmp/OMSPP_by_domain.dat — pgfplots data file
         overall pooled sanity check
================================================================================
 Aggregation is pooled at the raw-count level: sum(num) / sum(den).
 Pools all 1,000 instances per domain (25 maps * k in {10,...,200}, 250 per k).
 S, B, P are taken from Incremental-kA*'s closed list.
================================================================================
"""

import csv
from collections import defaultdict

from f_google.services.drive import Drive
from f_log import get_log

_log = get_log(__name__)

_PATH_SRC = '2026/04/Experiments/OMSPP/results_unified.csv'
_PATH_LOC = '/tmp/results_unified.csv'
_PATH_DAT = '/tmp/OMSPP_by_domain.dat'

_CAND = {
    'domain': ['domain', 'Domain', 'map_domain'],
    's_inc' : ['surely_inc', 'S_inc', 'surely_incremental'],
    'b_inc' : ['border_inc', 'B_inc', 'borderline_inc'],
    'p_inc' : ['surplus_inc', 'P_inc', 'surplus_incremental'],
    'b_agg' : ['border_agg', 'B_agg', 'borderline_agg'],
    'v'     : ['valid_cells', 'V', 'n_valid', 'map_valid_cells', 'cells'],
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


def _aggregate(cols: dict[str, str]) -> dict[str, dict[str, float]]:
    acc: dict[str, dict[str, int]] = defaultdict(
        lambda: {'n': 0, 's': 0, 'b': 0, 'p': 0, 'ba': 0, 'v': 0}
    )
    with open(_PATH_LOC) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = acc[row[cols['domain']]]
            d['n']  += 1
            d['s']  += int(row[cols['s_inc']])
            d['b']  += int(row[cols['b_inc']])
            d['p']  += int(row[cols['p_inc']])
            d['ba'] += int(row[cols['b_agg']])
            d['v']  += int(row[cols['v']])

    out: dict[str, dict[str, float]] = {}
    for dom in sorted(acc):
        d = acc[dom]
        closed = d['s'] + d['b'] + d['p']
        out[dom] = {
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


def _print_table(data: dict[str, dict[str, float]]) -> None:
    print()
    print('| Domain   |   n  |  S%   |  B%   |  P%  | Cl/V% | Ba/Bi  |')
    print('|----------|-----:|------:|------:|-----:|------:|-------:|')
    for dom, d in data.items():
        print(f"| {dom:<8} | {int(d['n']):4d} | "
              f"{d['S_pct']:5.2f} | {d['B_pct']:5.2f} | "
              f"{d['P_pct']:4.2f} | {d['ClV']:5.2f} | "
              f"{d['BaBi']:6.4f} |")

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


def _emit_pgfplots(data: dict[str, dict[str, float]]) -> None:
    with open(_PATH_DAT, 'w') as f:
        f.write('domain S B P ClV BaBi\n')
        for dom, d in data.items():
            f.write(f"{dom} {d['S_pct']:.4f} {d['B_pct']:.4f} "
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
