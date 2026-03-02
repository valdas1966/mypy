from f_core.processes.i_3_parallel import ProcessParallel
from f_math.number.u_prime import count_primes
from typing import Any, Callable
from time import perf_counter


def _timed(label: str, func: Callable[[], Any]) -> tuple[float, Any]:
    """
    ============================================================================
     Run func, print elapsed time, return (elapsed, result).
    ============================================================================
    """
    start = perf_counter()
    result = func()
    elapsed = perf_counter() - start
    print(f'{label:<20} {elapsed:.3f}s (result={result})')
    return elapsed, result


if __name__ == '__main__':
    items = list(range(1, 2_000_001))
    workers = 4

    print(f'Count primes in [1..2,000,000] with {workers} workers')
    print('=' * 55)

    # Sequential
    t_seq, _ = _timed('Sequential', lambda: count_primes(items))

    # Threads
    def _run_threads() -> int:
        proc = ProcessParallel(input=items,
                               func=count_primes,
                               workers=workers,
                               use_processes=False)
        return sum(proc.run())
    t_threads, _ = _timed('Threads', _run_threads)

    # Processes
    def _run_processes() -> int:
        proc = ProcessParallel(input=items,
                               func=count_primes,
                               workers=workers,
                               use_processes=True)
        return sum(proc.run())
    t_procs, _ = _timed('Processes', _run_processes)

    print('=' * 55)
    print(f'Threads speedup:   {t_seq / t_threads:.2f}x')
    print(f'Processes speedup: {t_seq / t_procs:.2f}x')
