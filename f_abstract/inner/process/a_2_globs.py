from f_abstract.inner.process.a_1_1_init import ProcessInit
from collections import defaultdict


class ProcessGlobs(ProcessInit):

    # dict : Process-Parameters
    _globs = defaultdict(str)

    # OperationLog
    def _pre_run(self, **kwargs) -> None:
        self._set_globs()
        super()._pre_run(**kwargs)

    def _set_globs(self) -> None:
        """
        ========================================================================
         Description: Set Process-Params.
        ========================================================================
        """
        pass
