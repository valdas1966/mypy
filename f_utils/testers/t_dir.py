from f_utils import u_tester
from f_utils import u_dir


class TestDir:

    def __init__(self):
        u_tester.print_start(__file__)
        TestDir.__tester_is_exist()
        TestDir.__tester_create()
        TestDir.__tester_delete()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_is_exist():
        # existed dir
        p0 = u_dir.is_exist(path='d:\\mypy')
        # not existed dir
        p1 = not u_dir.is_exist(path='')
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_create():
        path = 'd:\\tester_dir_create'
        u_dir.create(path, overwrite=True)
        p0 = u_dir.is_exist(path)
        u_tester.run(p0)

    @staticmethod
    def __tester_delete():
        path = 'd:\\tester_dir_create'
        u_dir.create(path)
        u_dir.delete(path)
        p0 = not u_dir.is_exist(path)
        u_tester.run(p0)


if __name__ == '__main__':
    TestDir()
