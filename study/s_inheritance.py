
class A:
    def f(self) -> None:
        print('A')


class B(A):
    def f(self) -> None:
        print('B')


class C:
    def __init__(self):
        self._c: A | None = None

    @property
    def c(self) -> A:
        return self._c


class D(C):
    def __init__(self):
        self._c = B()


d = D()
d.c.f()

