from f_abstract.runnable import Runnable


class T(Runnable):

    def _run(self):
        print(self.a)


t = T(a=5)
