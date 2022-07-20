class Test:

    def __init__(self):
        self.d = dict()
        print('init')

    def __setitem__(self, key, value):
        i, j = key
        if i not in self.d:
            self.d[i] = dict()
        self.d[i][j] = value

    def __getitem__(self, item):
        i, j = item
        return self.d[i][j]


t = Test()
t[1, 1] = 2
print(t[1, 1])