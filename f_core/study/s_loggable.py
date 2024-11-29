from f_core.loggable import Loggable
from f_core.operation import Operation


class A(Loggable):

    def _log(self) -> None:
        super()._log()
        print('aaaaaaaaaaaaaaaaaa')


class B(Operation):

    def _post_run(self) -> None:
        super()._post_run(x=2)


b = B()
