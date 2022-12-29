class C:

    d = dict()
    _d = dict()

    def __init__(self):
        self.d['a'] = 1
        print(self.__class__.__dict__['d']['a'])

    def _f(self):
        pass





c = C()
print(c.get_protected_atts())



