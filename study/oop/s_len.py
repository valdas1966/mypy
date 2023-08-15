class A:

    def cells(self):
        return [1]

    def __len__(self):
        return len(self.cells())


class B(A):

    def cells(self):
        return [1, 2]

    def pct(self):
        return super().__len__()

    def __len__(self):
        return len(self.cells())


b = B()
print(b.pct())
