class A:

    def f_1(self):
        self.f_2()

    def f_2(self):
        print(1)


class B(A):

    def f_2(self):
        print(2)


a = A()
a.f_1()
b = B()
b.f_1()