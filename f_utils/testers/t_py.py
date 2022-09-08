from f_utils import u_tester
from f_utils import u_py


class TesterPy:

    def __init__(self):
        u_tester.print_start(__file__)
        TesterPy.__tester_get_funcs()
        TesterPy.__tester_snake_to_pascal()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_get_funcs():
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
        u_tester.run(p0)

    @staticmethod
    def __tester_snake_to_pascal():
        # one word
        pascal_0 = u_py.snake_to_pascal(snake='var')
        p0 = pascal_0 == 'Var'
        # multi words
        pascal_1 = u_py.snake_to_pascal(snake='my_var')
        p1 = pascal_1 == 'MyVar'
        u_tester.msg('[One-Word][Multi-Words]')
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TesterPy()

