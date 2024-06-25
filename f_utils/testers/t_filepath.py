from f_utils import u_tester
from f_utils import u_filepath


class TestFilePath:

    def __init__(self):
        u_tester.print_start(__file__)
        TestFilePath.__tester_get_dir()
        TestFilePath.__tester_get_filename()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_get_filename():
        filepath = 'c:\\test\\test.old_old_txt'
        # with domain
        p0 = u_filepath.get_filename(filepath) == 'test.old_old_txt'
        # without domain
        p1 = u_filepath.get_filename(filepath, with_domain=False) == 'test'
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_get_dir():
        filepath = 'c:\\test\\test.old_old_txt'
        p0 = u_filepath.get_dir(filepath) == 'c:\\test'
        u_tester.run(p0)


if __name__ == '__main__':
    TestFilePath()

