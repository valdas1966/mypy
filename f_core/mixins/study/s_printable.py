from f_core.mixins.printable import Printable


class A(Printable):
    def __str__(self) -> str:
        return 'Object'


print(A())
print(repr(A()))
