class A:

    _x = 2

    @property
    def x(self):
        return self._x

    def __init__(self):
        pass
        #self.x = 2


a = A()
print(a.x)