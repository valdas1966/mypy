class A:

    def __init__(self):
        self.d = {'list': 1}


class B:

    def __init__(self, d: dict):
        self.d = dict(d)


a = A()
b = B(d=a.d)
print(b.d)
b.d['list'] = 2
print(a.d)