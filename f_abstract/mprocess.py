from f_abstract.process import Process
from f_multi_threading.multi_threading_process import MultiThreadingProcess


class MultiProcess(Process):

    def __init__(self, f: 'func') -> None:
        self.f = f

    def _run(self):
        print('run')


mp = MultiProcess('a')
print(mp.f)
