from f_core.process_io import Process
import concurrent.futures as pool


class MultiThreadingProcess(Process):

    # self._kw = {f: func,
    #             params: sequence,
    #             max_workers: int = None}

    def __init__(self,
                 f: 'func',
                 params: 'sequence',
                 max_workers: int = None):
        super().__init__(f=f, params=params, max_workers=max_workers)

    def _add_kwargs(self) -> None:
        if 'max_workers' not in self._kw or not self._kw['max_workers']:
            self._kw['max_workers'] = len(self._kw['params'])

    def _run(self) -> None:
        """
        ========================================================================
         Description: Run Workers simultaneously.
        ========================================================================
        """
        worker = pool.ThreadPoolExecutor(max_workers=self._kw['max_workers'])
        worker.map(self._kw['f'], self._kw['params'])
        worker.shutdown()
