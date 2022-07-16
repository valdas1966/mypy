class A:

    li = list()
    n = 1

    def __init__(self):
        print('constructor')

    def change(self):
        self.li.append(2)
        self.n = 2

    def __str__(self):
        return f'{self.n}, {self.li}'


a_1 = A()
print(a_1)
a_1.change()
print(a_1)

a_2 = A()
print(a_2)
