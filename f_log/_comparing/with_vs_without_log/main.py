import csv
import logging
import os
import sys
import time
from pathlib import Path
from f_log import setup_log


_DIR = Path(__file__).parent
_LOG_PATH = str(_DIR / '_debug.log')
_CSV_PATH = str(_DIR / 'results.csv')

_ITERATIONS = (1_000, 10_000, 100_000)

_METHODS = ['no_log', 'disabled', 'console', 'file']


def _no_log(n: int) -> float:
    start = time.time()
    for _ in range(n):
        _ = 2 + 2
    return time.time() - start


def _disabled(n: int) -> float:
    log = logging.getLogger(__name__)
    setup_log(enabled=False)
    start = time.time()
    for _ in range(n):
        _ = 2 + 2
        log.debug('result: %d', 4)
    return time.time() - start


def _console(n: int) -> float:
    log = logging.getLogger(__name__)
    # Redirect stdout before setup so the handler writes to devnull
    old = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    setup_log(enabled=True, level=logging.DEBUG, sink='console')
    start = time.time()
    for _ in range(n):
        _ = 2 + 2
        log.debug('result: %d', 4)
    elapsed = time.time() - start
    sys.stdout.close()
    sys.stdout = old
    return elapsed


def _file(n: int) -> float:
    log = logging.getLogger(__name__)
    setup_log(enabled=True, level=logging.DEBUG,
              sink='file', path=_LOG_PATH)
    start = time.time()
    for _ in range(n):
        _ = 2 + 2
        log.debug('result: %d', 4)
    elapsed = time.time() - start
    # Cleanup log files
    for p in _DIR.glob('_debug.log*'):
        p.unlink()
    return elapsed


_FUNCS = {
    'no_log': _no_log,
    'disabled': _disabled,
    'console': _console,
    'file': _file,
}


def _run() -> list[dict]:
    rows = []
    for n in _ITERATIONS:
        row = {'iterations': n}
        for method in _METHODS:
            elapsed = _FUNCS[method](n)
            row[method] = f'{elapsed:.5f}'
        rows.append(row)
    return rows


def _write_csv(rows: list[dict]) -> None:
    fields = ['iterations'] + _METHODS
    with open(_CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _print_results(rows: list[dict]) -> None:
    G = '\033[32m'
    Y = '\033[33m'
    R = '\033[31m'
    C = '\033[36m'
    B = '\033[1m'
    D = '\033[2m'
    X = '\033[0m'
    W = 72

    print()
    print(f'{C}{B}{"=" * W}{X}')
    print(f'{C}{B} Logging Overhead: 4 Methods Compared{X}')
    print(f'{C}{B}{"=" * W}{X}')
    print()
    print(f'{B} {"Iters":>10}'
          f'  {"No-Log":>10}'
          f'  {"Disabled":>10}'
          f'  {"Console":>10}'
          f'  {"File":>10}{X}')
    print(f'{D} {"-" * (W - 2)}{X}')

    colors = {
        'no_log': G,
        'disabled': Y,
        'console': R,
        'file': R,
    }

    for row in rows:
        n = int(row['iterations'])
        parts = f' {n:>10,}'
        for method in _METHODS:
            c = colors[method]
            parts += f'  {c}{row[method]:>10}{X}'
        print(parts)

    print()
    print(f'{D} no_log   = pure 2+2 (no logging code)')
    print(f' disabled = log.debug() + setup(enabled=False)')
    print(f' console  = log.debug() + sink=console')
    print(f' file     = log.debug() + sink=file{X}')
    print()
    print(f'{D} Values in seconds (5 decimal places){X}')
    print(f'{C}{"=" * W}{X}')
    print()


rows = _run()
_write_csv(rows=rows)
_print_results(rows=rows)
print(f'\033[32mCSV saved: {_CSV_PATH}\033[0m')
