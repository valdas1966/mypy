class A:

    x = 2

    def __init__(self):
        self.x = 5
        print('A')

class B:
    def __init__(self):
        print('B')


class C(A, B):

    def __init__(self):
        print('C')

class D(C):
    def __init__(self):
        A.__init__(self)
        print('D')

d = D()