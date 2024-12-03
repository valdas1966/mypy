from f_core.protocols.comparable import Comparable


def f(a: Comparable, b: Comparable) -> bool:
    return a == b


print(f(1, 1))