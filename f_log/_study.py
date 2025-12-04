from f_log.utils import set_debug, log_calls


set_debug(True)

class A:

    def __repr__(self) -> str:
        return 'A=1, B=2'

class C:

    @staticmethod
    @log_calls
    def add(a: int, b: int) -> list[int]:
        return A()

x = C.add(a=1, b=2)
