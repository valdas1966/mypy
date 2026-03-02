from f_core.processes.i_3_parallel import ProcessParallel
from f_math.number.u_prime import count_primes
from time import perf_counter
import os


if __name__ == '__main__':
    items = list(range(1, 2_000_001))
    max_workers = 2 * os.cpu_count()

    # Sequential baseline
    start = perf_counter()
    baseline = count_primes(items)
    t_seq = perf_counter() - start

    print(f'Count primes in [1..2,000,000]')
    print(f'Sequential baseline: {t_seq:.3f}s (result={baseline})')
    print('=' * 55)
    print(f'{"Workers":<10} {"Elapsed":>10} {"Speedup":>10}')
    print('-' * 55)

    for w in range(1, max_workers + 1):
        proc = ProcessParallel(input=items,
                               func=count_primes,
                               workers=w,
                               use_processes=True)
        start = perf_counter()
        result = sum(proc.run())
        elapsed = perf_counter() - start
        speedup = t_seq / elapsed
        print(f'{w:<10} {elapsed:>9.3f}s {speedup:>9.2f}x')

    print('=' * 55)
