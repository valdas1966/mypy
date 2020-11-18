import datetime
from f_utils import u_tester
from f_utils import u_datetime


class TestDateTime:

    def __init__(self):
        u_tester.print_start(__file__)
        TestDateTime.__tester_to_str()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_to_str():
        dt = datetime.datetime(year=2020, month=9, day=15, hour=23, minute=59,
                        second=2)
        str_test = u_datetime.to_str(dt)
        str_true = '20200915235902'
        p0 = str_test == str_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestDateTime()
