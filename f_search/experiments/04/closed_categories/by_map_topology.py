"""
================================================================================
 Per-map topology metrics vs. closed-list categories.
================================================================================
 Input : Drive  2026/04/Experiments/OMSPP/results_unified.csv
         Drive  i_0_maps/<Domain>/*.map         (25 maps)
 Output: stdout markdown table (25 rows, one per map)
         /tmp/OMSPP_by_topology.dat — pgfplots data file
================================================================================
 Topology metric: mean_deg = mean over valid cells of the count of valid
 4-connected neighbors. A passable cell is '.' (Moving AI octile); any
 other char (e.g. '@', 'T') is treated as wall. Expectation: higher
 connectivity (mean_deg) correlates with more borderline nodes --- open
 graphs admit more f(n) = C^* ties than constrained ones.
 S, B, P are taken from Incremental-kA*'s closed list; aggregation is
 pooled at the raw-count level (sum(num)/sum(den)) across all k for the
 map.
================================================================================
"""

import csv
import os
from collections import defaultdict

import numpy as np

from f_google.services.drive import Drive
from f_log import get_log

_log = get_log(__name__)

_PATH_SRC   = '2026/04/Experiments/OMSPP/results_unified.csv'
_PATH_LOC   = '/tmp/results_unified.csv'
_PATH_MAPS  = '/tmp/maps_all'
_PATH_DAT   = '/tmp/OMSPP_by_topology.dat'

_DOMAINS    = ['Cities', 'Games', 'Rooms', 'Mazes', 'Random']
_ROWS_SKIP  = 4
_CHAR_VALID = '.'


def _download_csv() -> None:
    drive = Drive.Factory.valdas()
    drive.download(path_src=_PATH_SRC, path_dest=_PATH_LOC)
    _log.info(f'downloaded {_PATH_SRC} -> {_PATH_LOC}')


def _download_maps() -> None:
    if os.path.isdir(_PATH_MAPS) and os.listdir(_PATH_MAPS):
        return
    os.makedirs(_PATH_MAPS, exist_ok=True)
    drive = Drive.Factory.valdas()
    for dom in _DOMAINS:
        for f in drive.files(path=f'i_0_maps/{dom}'):
            drive.download(path_src=f'i_0_maps/{dom}/{f}',
                           path_dest=f'{_PATH_MAPS}/{dom}__{f}')


def _bool_array(path: str) -> np.ndarray:
    with open(path) as fh:
        lines = fh.read().splitlines()
    lines = lines[_ROWS_SKIP:]
    return np.array([[c == _CHAR_VALID for c in line] for line in lines])


def _mean_degree(arr: np.ndarray) -> float:
    """
    ========================================================================
     Mean 4-connected neighbor degree over valid cells only.
    ========================================================================
    """
    up    = np.zeros_like(arr)
    down  = np.zeros_like(arr)
    left  = np.zeros_like(arr)
    right = np.zeros_like(arr)
    up[1:, :]    = arr[:-1, :]
    down[:-1, :] = arr[1:, :]
    left[:, 1:]  = arr[:, :-1]
    right[:, :-1]= arr[:, 1:]
    deg = (up & arr).astype(int) + (down & arr).astype(int) \
        + (left & arr).astype(int) + (right & arr).astype(int)
    return float(deg[arr].mean())


def _map_metrics() -> dict[str, dict[str, float]]:
    """
    ========================================================================
     For every <Domain>__<name>.map file: compute valid cells, mean
     4-connected degree, and density |V| / (rows * cols).
    ========================================================================
    """
    out: dict[str, dict[str, float]] = {}
    for fname in sorted(os.listdir(_PATH_MAPS)):
        if '__' not in fname or not fname.endswith('.map'):
            continue
        dom, name = fname[:-4].split('__', 1)
        arr = _bool_array(f'{_PATH_MAPS}/{fname}')
        v   = int(arr.sum())
        out[name] = {
            'domain'   : dom,
            'cells'    : v,
            'mean_deg' : _mean_degree(arr),
            'density'  : v / (arr.shape[0] * arr.shape[1]),
        }
    return out


def _aggregate_by_map() -> dict[str, dict[str, float]]:
    """
    ========================================================================
     Pool closed-list counts per map across all k values.
    ========================================================================
    """
    acc: dict[str, dict[str, int]] = defaultdict(
        lambda: {'n': 0, 's': 0, 'b': 0, 'p': 0, 'ba': 0, 'v': 0}
    )
    with open(_PATH_LOC) as f:
        for row in csv.DictReader(f):
            d = acc[row['map']]
            d['n']  += 1
            d['s']  += int(row['surely_inc'])
            d['b']  += int(row['border_inc'])
            d['p']  += int(row['surplus_inc'])
            d['ba'] += int(row['border_agg'])
            d['v']  += int(row['cells'])
    out: dict[str, dict[str, float]] = {}
    for name, d in acc.items():
        closed = d['s'] + d['b'] + d['p']
        out[name] = {
            'n'    : d['n'],
            'S_pct': 100 * d['s'] / closed,
            'B_pct': 100 * d['b'] / closed,
            'ClV'  : 100 * closed / d['v'],
            'BaBi' : 100 * d['ba'] / d['b'] if d['b'] else float('nan'),
        }
    return out


def _print_table(joined: list[dict]) -> None:
    print()
    print('| Domain   | Map                | cells     | mean_deg '
          '| density |  B% | Exp/V% | Ba/Bi% |')
    print('|----------|--------------------|----------:|--------:'
          '|--------:|----:|-------:|-------:|')
    for r in joined:
        print(f"| {r['domain']:<8} | {r['map']:<18} | "
              f"{r['cells']:>9,} | {r['mean_deg']:6.3f}  | "
              f"{r['density']:6.3f}  | "
              f"{r['B_pct']:4.2f} | {r['ClV']:6.2f} | "
              f"{r['BaBi']:6.2f} |")


def _corr(x: list[float], y: list[float]) -> float:
    xa = np.array(x, dtype=float)
    ya = np.array(y, dtype=float)
    return float(np.corrcoef(xa, ya)[0, 1])


def _print_correlations(joined: list[dict]) -> None:
    """
    ========================================================================
     Pearson correlation of topology metric vs. outcome, across 25 maps.
    ========================================================================
    """
    for metric in ['mean_deg', 'density']:
        x = [r[metric] for r in joined]
        for target in ['B_pct', 'ClV', 'BaBi']:
            y = [r[target] for r in joined]
            print(f'corr({metric:>9}, {target:>6}) = {_corr(x, y):+.3f}')
        print()


def _emit_pgfplots(joined: list[dict]) -> None:
    dom_color = {'Cities': 'borderline', 'Games': 'newcolor',
                 'Rooms' : 'surely',     'Mazes': 'accentblue',
                 'Random': 'surplus'}
    with open(_PATH_DAT, 'w') as f:
        f.write('domain map cells mean_deg density B ClV BaBi\n')
        for r in joined:
            f.write(f"{r['domain']} {r['map']} {r['cells']} "
                    f"{r['mean_deg']:.4f} {r['density']:.4f} "
                    f"{r['B_pct']:.4f} {r['ClV']:.4f} "
                    f"{r['BaBi']:.4f}\n")
    _log.info(f'wrote {_PATH_DAT} (colors: {dom_color})')


def run() -> None:
    _download_csv()
    _download_maps()
    topo = _map_metrics()
    agg  = _aggregate_by_map()

    joined: list[dict] = []
    for name, t in topo.items():
        a = agg.get(name)
        if a is None:
            _log.warning(f'no CSV rows for map {name!r}')
            continue
        joined.append({
            'domain'  : t['domain'],
            'map'     : name,
            'cells'   : t['cells'],
            'mean_deg': t['mean_deg'],
            'density' : t['density'],
            **a,
        })

    joined.sort(key=lambda r: (r['domain'], r['mean_deg']))
    _print_table(joined)
    print()
    _print_correlations(joined)
    _emit_pgfplots(joined)


if __name__ == '__main__':
    run()
