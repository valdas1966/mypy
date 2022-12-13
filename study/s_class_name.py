class A:

    def __init__(self):
        print(self.__class__.__name__)


class B(A):
    pass



a = A()
b = B()