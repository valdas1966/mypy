class A:
    def __str__(self):
        return 'A'

class B(A):
    def __str__(self):
        return 'B'

class C(B):
    def __str__(self):
        return 'C'

    def only_c(self):
        print('only_c')