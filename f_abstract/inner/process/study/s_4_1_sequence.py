"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. Globs-Parameter that pass to the Operations.
    2. Dynamic argument that pass to the Operation-Constructor.
    3. Sequentially Operations-Execution.
    4. One-Operation-Fail does not cause Whole-Process-Fail.
================================================================================
"""
from f_abstract.inner.process.a_4_1_sequence import ProcessSequence
from f_abstract.operation import Operation


class Op(Operation):

    def _run(self) -> None:
        if self._index < 2:
            print(self._globs['name'], self._index)
        else:
            raise Exception('index=2')


class Process(ProcessSequence):

    def _set_globs(self) -> None:
        self._globs['name'] = self._name

    def _pre_run(self) -> None:
        super()._pre_run()
        self._ops = [Op] * self._num
        self._arg_ops = [{'index': i} for i in range(self._num)]


p = Process(name='Operation', num=3)