from typing import Type


class A:
    def __init__(self):
        print('A')


class B(A):
    def __init__(self):
        A.__init__(self)
        print('B')


class C:
    def __init__(self, tp: type[A]):
        tp()


c = C(tp=B)
