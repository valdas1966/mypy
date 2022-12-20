from f_abstract.inner.process.a_3_ops import ProcessOps
import concurrent.futures as pool


class ProcessParallel(ProcessOps):

    # Runnable
    def _run(self) -> None:
        max_workers = len(self._arg_ops)
        worker = pool.ThreadPoolExecutor(max_workers=max_workers)
        worker.map(self._run_parallel, self._arg_ops)
        worker.shutdown()

    def _run_parallel(self, *args) -> None:
        """
        ========================================================================
         Description: Run Parallel-Function.
        ========================================================================
        """
        pass
