from f_abstract.inner.operation.a_4_io import OperationIO


class Op(OperationIO):

    _to_pre_log = True

    def _run(self) -> None:
        self._output = self.input + 8

    def _add_pre_log_kwargs(self) -> None:
        self._pre_log_kwargs['io'] = self.input

    def _add_post_log_kwargs(self) -> None:
        self._post_log_kwargs['io'] = self.output


output = Op(input=7).output
print(output)
