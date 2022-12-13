from f_abstract.inittable import Inittable


class A(Inittable):
    pass


class B(Inittable):
    def __init__(self, **kwargs):
        Inittable.__init__(self, **kwargs)
        print('B')


class C(A, B):
    pass


c = C(x=2)
print(c.x)