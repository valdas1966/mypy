from f_log.old.utils import set_debug, one_line


set_debug(True)

class A:

    def __repr__(self) -> str:
        return 'A=1, B=2'

class C:

    @staticmethod
    @one_line
    def add(a: int, b: int) -> list[int]:
        return [a, b, [a, b], [a, b, a]]

x = C.add(a=1, b=2)
