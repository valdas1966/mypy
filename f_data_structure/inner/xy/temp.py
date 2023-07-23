class A:

    def __init__(self, x):
        print('A', x)


class B:

    def __init__(self, x, y=2):
        x += 1
        print('B', x)
        self._y = y


class C(A, B):
    pass
    """
    def __init__(self, x):
        A.__init__(self, x)
        B.__init__(self, x)
    """



c = C(x=1)
print(c._y)