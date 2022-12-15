"""
================================================================================
 Check:
--------------------------------------------------------------------------------
    1. Execute Input\Output Operations.
    2. Process Input & Output.
    3. Operation-Fail causes Process-Fail.
================================================================================
"""

from f_abstract.inner.process.a_4_2_io import ProcessIO
from f_abstract.inner.operation.a_4_io import OperationIO


class Operation(OperationIO):

    _to_pre_log = True

    def _run(self) -> None:
        if self.input == 4:
            raise Exception('input == 4')
        self._output = self.input * 2

    def _add_pre_log(self) -> None:
        self._d_pre_log['input'] = self.input
        self._d_pre_log['output'] = self.output

    def _add_post_log(self) -> None:
        self._d_post_log['input'] = self.input
        self._d_post_log['output'] = self.output


class Process(ProcessIO):

    _ops = [Operation] * 2

    _arg_ops = [{}] * 2

    def _add_pre_log(self) -> None:
        self._d_pre_log['input'] = self.input
        self._d_pre_log['output'] = self.output

    def _add_post_log(self) -> None:
        self._d_post_log['input'] = self.input
        self._d_post_log['output'] = self.output


p = Process(input=2)
print(f'output={p.output}')
