from f_core.processes.i_3_parallel import ProcessParallel


if __name__ == '__main__':
    # Thread-based (I/O-bound)
    proc = ProcessParallel.Factory.io_bound()
    output = proc.run()
    print(f'IO-Bound Output: {output}')
    print(f'Total: {sum(x for x in output if x is not None)}')
    print(f'Elapsed: {proc.elapsed}s')
    print()

    # Process-based (CPU-bound)
    proc = ProcessParallel.Factory.cpu_bound()
    output = proc.run()
    print(f'CPU-Bound Output: {output}')
    print(f'Total: {sum(x for x in output if x is not None)}')
    print()

    # With error tolerance
    proc = ProcessParallel.Factory.with_error()
    output = proc.run()
    print(f'Tolerant Output: {output}')
    print(f'Total: {sum(x for x in output if x is not None)}')
    print(f'Errors: {len(proc.errors)}')
    for idx, chunk, exc in proc.errors:
        print(f'  Chunk {idx}: {chunk} -> {exc}')
