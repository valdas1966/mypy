from f_abstract.protocols.equable import Equable


def f(a: Equable, b: Equable) -> bool:
    return a == b


print(f(1, 1))