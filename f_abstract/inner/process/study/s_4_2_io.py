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

    def _add_pre_log_kwargs(self) -> None:
        self._pre_log_kwargs['input'] = self.input
        self._pre_log_kwargs['output'] = self.output

    def _add_post_log_kwargs(self) -> None:
        self._post_log_kwargs['input'] = self.input
        self._post_log_kwargs['output'] = self.output


class Process(ProcessIO):

    _ops = [Operation] * 2

    _arg_ops = [{}] * 2

    def _add_pre_log_kwargs(self) -> None:
        self._pre_log_kwargs['input'] = self.input
        self._pre_log_kwargs['output'] = self.output

    def _add_post_log_kwargs(self) -> None:
        self._post_log_kwargs['input'] = self.input
        self._post_log_kwargs['output'] = self.output


p = Process(input=2)
print(f'output={p.output}')
