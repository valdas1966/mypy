class A:

    def __init__(self, f):
        self.__dict__['x'] = 19
        self.__dict__['f'] = f


def p():
    print('hello')

a = A(f=p)
print(a.x)
a.f()