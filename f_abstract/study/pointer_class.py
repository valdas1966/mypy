from f_abstract.inittable import Inittable


class A(Inittable):

    def run(self):
        return 2


class B(Inittable):

    def run(self):
        print(self.x+1)


res = None
a = A()
b = B(x=res)
res = a.run()
b.run()
