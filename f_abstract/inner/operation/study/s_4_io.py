from f_abstract.inner.operation.a_4_io import OperationIO


class Op(OperationIO):

    _to_pre_log = True

    def _run(self) -> None:
        self._output = self.input + self._adder

    def _add_pre_log(self) -> None:
        self._d_pre_log['io'] = self.input

    def _add_post_log(self) -> None:
        self._d_post_log['io'] = self.output


output = Op(input=7, adder=8).output
print(output)
