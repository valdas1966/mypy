from f_abstract.operation import Operation
from f_abstract.inner.process.a_4_4_parallel import ProcessParallel


class Op(Operation):

    def _run(self) -> None:
        print(self._id_session, self._globs['x'])


class Process(ProcessParallel):

    _ops = Op

    _arg_ops = [(1), (2)]

    def _set_globs(self) -> None:
        self._globs['x'] = 2

    def _run_parallel(self, *args) -> None:
        id_session = args[0]
        Op(globs=self._globs, id_session=id_session)


p = Process()
