from f_utils import u_tester
from c_res import Res


class Tester_Res:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_bool()
        self.tester_empty()
        self.tester_val()
        self.tester_msg()
        u_tester.print_finish(__file__)

    def tester_bool(self):
        res = Res(1, True)
        p0 = True if res else False

        res = Res('Error', False)
        p1 = True if not res else False

        u_tester.run([p0, p1])

    def tester_empty(self):
        res = Res()
        p0 = True if res else False

        res = Res('Error', False)
        p1 = True if not res else False

        u_tester.run([p0, p1])

    def tester_val(self):
        res = Res(1)
        p0 = res.val == 1

        res = Res('Error', False)
        p1 = res.val is None

        u_tester.run([p0, p1])

    def tester_msg(self):
        res = Res()
        p0 = res.msg == str()

        res = Res('Text', True)
        p1 = res.msg == str()

        res = Res('Error', False)
        p2 = res.msg == 'Error'

        u_tester.run([p0, p1, p2])


if __name__ == '__main__':
    Tester_Res()


