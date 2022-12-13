from f_abstract.inittable import Inittable


class A(Inittable):

    def run(self):
        return 2


res = None
a = A(**{'x': 1})
print(a.x)