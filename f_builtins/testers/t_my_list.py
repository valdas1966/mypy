from f_utils import u_tester


class TestMyList:

    def __init__(self):
        u_tester.print_start(__file__)
        TestMyList.__tester_()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_():
        pass


if __name__ == '__main__':
    TestMyList()
