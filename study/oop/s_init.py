class A:
    def __init__(self, a):
        print('a')
        self.a = a

class X(A):
    def __init__(self, a):
        A.__init__(self, a)

class B(X):
    def __init__(self, a, b):
        X.__init__(self, a)
        self.b = b

class C(X):
    def __init__(self, a, c):
        X.__init__(self, a)
        self.c = c

class D(B, C):
    def __init__(self, a, b, c):
        B.__init__(self, a, b)
        C.__init__(self, a, c)

d = D(a=1, b=2, c=3)
