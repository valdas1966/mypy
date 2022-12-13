"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. Globs assignment by private attribute (__init__()).
    2. Globs validity in Pre & Post Logging (_pre_log() & _post_log()).
================================================================================
"""

from f_abstract.inner.process.a_2_globs import ProcessGlobs


class Process(ProcessGlobs):

    def _set_globs(self) -> None:
        self._globs['x'] = self._x

    def _add_pre_log_kwargs(self) -> None:
        self._pre_log_kwargs['x'] = self._globs['x']

    def _add_post_log_kwargs(self) -> None:
        self._post_log_kwargs['x'] = self._globs['x']


p = Process(x=5)
print(p._globs['x'])
