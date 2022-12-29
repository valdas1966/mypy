"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. Globs assignment by private attribute (__init__()).
    2. Globs-Params in Pre & Post Logging.
================================================================================
"""

from f_abstract.inner.process.a_3_proc_atts import ProcessGlobs


class Process(ProcessGlobs):

    def _set_globs(self) -> None:
        self._globs['x'] = self._x


p = Process(x=5)
print(p._globs['x'])
