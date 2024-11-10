from f_abstract.mixins.printable import Printable


class A(Printable):
    def __str__(self) -> str:
        return 'Object'


print(A())
print(repr(A()))
