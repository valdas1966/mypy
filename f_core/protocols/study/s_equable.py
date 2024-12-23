from f_core.protocols.equable import Equable


def f(a: Equable, b: Equable) -> bool:
    return a == b


print(f((1), (1)))
