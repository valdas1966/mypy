from f_core.mixins.cursorable import Cursorable


def ex() -> Cursorable:
    data = [1, 2, 3]
    return Cursorable(data=data)



e = ex()
print(e.current())
