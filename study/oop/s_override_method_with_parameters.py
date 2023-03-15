class A:

    def p(self) -> None:
        print(1)


class B(A):

    def p(self, x: int = None) -> None:
        print(x)
        super().p()


b = B()
b.p()