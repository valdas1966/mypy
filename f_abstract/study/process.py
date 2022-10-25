from f_abstract.process import Process


class P(Process):

    def _add_kwargs(self) -> None:
        self._title = 'Title'

    def _run(self):
        print('run')

    def _log(self, status: str, state: str, title: str):
        print(status, state, title)


p = P()