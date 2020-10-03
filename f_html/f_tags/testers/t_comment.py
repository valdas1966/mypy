import sys
sys.path.append('D:\\MyPy')

from f_utils import u_tester
from f_html.f_tags.c_comment import TagComment

class TestComment:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_init()
        u_tester.print_finish(__file__)

    def __tester_init(self):
        comment = TagComment('comment')
        p0 = str(comment) == '<!-- comment -->'
        u_tester.run(p0)

if __name__ == '__main__':
    TestComment()