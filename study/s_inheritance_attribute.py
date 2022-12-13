class A:

    d = dict()

    def __init__(self):
        self.d['a'] = 1


class B(A):

    e = dict()
    e['b'] = 2

    def __init__(self):
        super().__init__()
        for key, val in self.e.items():
            self.d[key] = val


b = B()
print(b.d)