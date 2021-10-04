from f_utils import u_tester
from f_utils import u_file


class TestFile:

    def __init__(self):
        u_tester.print_start(__file__)
        TestFile.__tester_replace_in_file()
        TestFile.__tester_replace_filename()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_replace_in_file():
        txt_test = 'test.txt'
        text = 'First Row\nSecond Row\n'
        u_file.write(txt_test, text)
        u_file.replace_in_file(txt_test, [('o', 'a')])
        text_test = u_file.read(txt_test)
        text_true = 'First Raw\nSecand Raw\n'
        p0 = text_test == text_true
        u_tester.run(p0)

    @staticmethod
    def __tester_replace_filename():
        path = 'c:\\temp\\test_1.txt'
        filename = 'test_2.csv'
        path_test = u_file.replace_filename(path, filename)
        path_true = 'c:\\temp\\test_2.csv'
        p0 = path_test == path_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestFile()
