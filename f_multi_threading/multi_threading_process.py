from f_logging.dec import log_all_methods, log_info_class
from f_abstract.process import Process
import concurrent.futures as pool


@log_all_methods(decorator=log_info_class)
class MultiThreadingProcess(Process):

    def __init__(self,
                 f: 'func',
                 li_param: 'sequence',
                 max_workers: int = None):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. f : func (Function for each Worker).
            2. li_param : list (Param for each Worker).
            3. max_workers : int (Manually by given argument or Auto by
                                    len of li_param).
        ========================================================================
        """
        self._f = f
        self._li_param = li_param
        self._max_workers = max_workers if max_workers else len(li_param)

    def run(self) -> None:
        """
        ========================================================================
         Description: Run Workers simultaneously.
        ========================================================================
        """
        worker = pool.ThreadPoolExecutor(max_workers=self._max_workers)
        worker.map(self._f, self._li_param)
        worker.shutdown()
