from f_core.processes.i_2_io import ProcessIO
from f_ds.groups import Group
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Generic, TypeVar, Callable
import multiprocessing
import sys

Item = TypeVar('Item')
Output = TypeVar('Output')


class ProcessParallel(Generic[Item, Output],
                      ProcessIO[list[Item], list[Output | None]]):
    """
    ============================================================================
     Parallel Process that distributes items across workers.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 input: list[Item],
                 func: Callable[[list[Item]], Output | None],
                 workers: int,
                 use_processes: bool = False,
                 name: str = 'ProcessParallel') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, input=input, name=name)
        self._func = func
        self._workers = min(workers, len(input)) if input else 0
        self._use_processes = use_processes
        self._errors: list[tuple[int, list[Item], Exception]] = []

    @property
    def errors(self) -> list[tuple[int, list[Item], Exception]]:
        """
        ========================================================================
         Return the collected errors from failed chunks.
        ========================================================================
        """
        return self._errors

    def _run(self) -> list[Output | None]:
        """
        ========================================================================
         Distribute items across workers and execute in parallel.
        ========================================================================
        """
        # Reset errors
        self._errors = []
        # Handle empty input
        if not self._input:
            return []
        # Split input into chunks
        chunks = Group.to_groups(data=self._input,
                                  n=self._workers,
                                  name='Chunk')
        # Pre-allocate ordered result slots
        results: list[Output | None] = [None] * len(chunks)
        # Select executor
        if self._use_processes:
            # Use forkserver on macOS/Linux (no __main__ guard needed).
            # On Windows only spawn is available (requires __main__ guard
            # in the caller script).
            mp_context = None
            if sys.platform != 'win32':
                mp_context = multiprocessing.get_context('forkserver')
            executor_cls = ProcessPoolExecutor
            executor_kwargs = dict(max_workers=self._workers,
                                   mp_context=mp_context)
        else:
            executor_cls = ThreadPoolExecutor
            executor_kwargs = dict(max_workers=self._workers)
        # Execute chunks in parallel
        with executor_cls(**executor_kwargs) as executor:
            # Submit all chunks
            future_to_idx = {}
            for i, chunk in enumerate(chunks):
                chunk_data = list(chunk)
                future = executor.submit(self._func, chunk_data)
                future_to_idx[future] = (i, chunk_data)
            # Collect results
            for future, (i, chunk_data) in future_to_idx.items():
                try:
                    results[i] = future.result()
                except Exception as exc:
                    self._errors.append((i, chunk_data, exc))
        return results
