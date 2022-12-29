from f_utils import u_tester
from f_abstract.tittable import Tittable


class TestTittable:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_title()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_title():
        class T(Tittable):
            def _set_title(self, title: str = None) -> None:
                self._title = self._name
        t = T(name='title')
        p0 = t.title == 'title'
        u_tester.run(p0)


if __name__ == '__main__':
    TestTittable()
