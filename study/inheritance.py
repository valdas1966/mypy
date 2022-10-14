class A:

    def __init__(self, x: int):
        self.x = x

    def p(self):
        print(self.x)


class B(A):

    pass


b = B(2)
b.p()