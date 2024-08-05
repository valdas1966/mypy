
class A:
    print('AAA')
    _d = dict()
    _d['list'] = 1
    __d = dict()

    def __init__(self):
        print('A')
        print(self._d)
        self.__d.update(self._d)
        print(self.__d)


class B(A):

    print('BBB')
    _d = dict()
    _d['b'] = 2

    def __init__(self):
        print('B')
        print(self._d, super()._d)
        super().__init__()


class C(B):
    print('CCC')
    _d = dict()
    _d['c'] = 3

    def __init__(self):
        print('C')
        print(self._d, super()._d)
        super().__init__()


#b = B()
#b.p()

c = C()


