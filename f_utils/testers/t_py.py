import sys
sys.path.append('D:\\MyPy')
from f_utils import u_py, u_tester


class TesterPy:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_get_funcs()
        u_tester.print_finish(__file__)

    def tester_get_funcs(self):
        print('ok')
        path = '../temp.py'
        file = open(path, 'w')
        file.write('class TesterPy:\n')
        file.write('\tdef tester_1(self):')
        file.write('\t\tpass\n')
        file.write('\tdef tester_2(self):')
        file.write('\t\tpass')
        file.close()
        funcs_test = u_py.get_funcs(path)
        funcs_true = ['tester_1', 'tester_2']
        p0 = funcs_test == funcs_true
        u_tester.run([p0])


if __name__ == '__main__':
    TesterPy()

