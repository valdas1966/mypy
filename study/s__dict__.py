class C:

    d = dict()

    def __init__(self):
        self.d['a'] = 1
        print(self.__class__.__dict__['d']['a'])


c = C()
