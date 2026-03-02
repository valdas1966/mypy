from f_core.processes.i_3_parallel.main import ProcessParallel


def _square_chunk(chunk: list[int]) -> int:
    """
    ============================================================================
     Return the sum of squares of the chunk items.
    ============================================================================
    """
    return sum(x * x for x in chunk)


def _failing_chunk(chunk: list[int]) -> int:
    """
    ============================================================================
     Raise ValueError if chunk contains 3 or 4.
    ============================================================================
    """
    if 3 in chunk or 4 in chunk:
        raise ValueError('Simulated failure')
    return sum(chunk)


class Factory:
    """
    ============================================================================
     Factory for the ProcessParallel class.
    ============================================================================
    """

    @staticmethod
    def io_bound() -> ProcessParallel[int, int]:
        """
        ========================================================================
         Create a thread-based ProcessParallel (happy path).
        ========================================================================
        """
        return ProcessParallel(input=list(range(1, 13)),
                               func=_square_chunk,
                               workers=3)

    @staticmethod
    def cpu_bound() -> ProcessParallel[int, int]:
        """
        ========================================================================
         Create a process-based ProcessParallel (happy path).
        ========================================================================
        """
        return ProcessParallel(input=list(range(1, 13)),
                               func=_square_chunk,
                               workers=3,
                               use_processes=True)

    @staticmethod
    def with_error() -> ProcessParallel[int, int]:
        """
        ========================================================================
         Create a ProcessParallel with a failing chunk.
        ========================================================================
        """
        return ProcessParallel(input=list(range(1, 7)),
                               func=_failing_chunk,
                               workers=3)
