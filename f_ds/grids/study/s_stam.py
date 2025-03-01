def f(x: int) -> int:
    return x


def g():
    h = f
    y = h(2)
    print(y)


g()

