from f_core.runnable import Runnable


class T(Runnable):

    def _pre_run(self) -> None:
        print('pre_run')

    def _post_run(self) -> None:
        print('post_run')

    def _run(self):
        print('run')
        1 / self._x

    def _on_error(self, **kwargs) -> None:
        print('on_error', self._e_msg)


t = T(x=1)
t = T(x=0)