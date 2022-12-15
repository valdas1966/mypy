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

    def _add_pre_log(self) -> None:
        self._d_pre_log['x'] = self._globs['x']

    def _add_post_log(self) -> None:
        self._d_post_log['x'] = self._globs['x']


p = Process(x=5)
print(p._globs['x'])
