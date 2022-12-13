class A:

    _y = 2
    __x = 5


class B(A):

    def __init__(self):
        print(self._y)
        print(self.__x)


b = B()