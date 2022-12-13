from f_abstract.operation import Operation
from f_abstract.inner.process.a_3_ops_io import ProcessOpsIO


class Op(Operation):

    def _run(self):
        self._output = self._input * 2
        if self._input == 8:
            1  / 0

    def _post_run(self, **kwargs) -> None:
        kwargs = {'input': self.input,
                  'output': self.output,
                  'x': self._globs}
        super()._post_run(**kwargs)


class P(ProcessOpsIO):

    _ops = [Op]*3
    _arg_ops = [{'_title': 'Square'}]*3
    _input = 2

    def _set_globs(self) -> None:
        self._globs = 55

print(P().output)
