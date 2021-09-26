from f_utils import u_tester
from f_utils import u_str


class TestStr:

    def __init__(self):
        u_tester.print_start(__file__)
        TestStr.__tester_endswith()
        self.__tester_push_at()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_endswith():
        text = 'hello'
        # No extensions
        extensions = set()
        endswith_test = u_str.endswith(text, extensions)
        endswith_true = True
        p0 = endswith_test == endswith_true
        # One extension
        extensions = {'o'}
        endswith_test = u_str.endswith(text, extensions)
        endswith_true = True
        p1 = endswith_test == endswith_true
        # Many extensions - True Answer
        extensions = {'a', 'o'}
        endswith_test = u_str.endswith(text, extensions)
        endswith_true = True
        p2 = endswith_test == endswith_true
        # Many Extension - False Answer
        extensions = {'a', 'b'}
        endswith_test = u_str.endswith(text, extensions)
        endswith_true = False
        p3 = endswith_test == endswith_true
        u_tester.run(p0, p1, p2, p3)

    @staticmethod
    def __tester_push_at():
        s1, s2 = '', ''
        p0 = u_str.push_at(s1, s2, 0) == ''
        s1, s2 = '', 'a'
        p1 = u_str.push_at(s1, s2, 0) == 'a'
        s1, s2 = 'a', ''
        p2 = u_str.push_at(s1, s2, 0) == 'a'
        s1, s2 = 'a', 'b'
        p3 = u_str.push_at(s1, s2, 0) == 'ba'
        p4 = u_str.push_at(s1, s2, 1) == 'ab'
        s1, s2 = 'ab', 'c'
        p5 = u_str.push_at(s1, s2, 1) == 'acb'
        u_tester.run(p0, p1, p2, p3, p4, p5)


if __name__ == '__main__':
    TestStr()
