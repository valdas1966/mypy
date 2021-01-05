from f_utils import u_tester
from f_excel.c_excel import Excel


class TestExcel:



    def __init__(self):
        u_tester.print_start(__file__)
        TestExcel.__tester_to_linked_list()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_to_linked_list():
        xlsx_test = 'test_to_linked_list.xlsx'
        excel = Excel(xlsx_test)
        linked_list_test = excel.to_linked_list()
        excel.close()
        li_1 = ['Programming Language', 'B']
        li_2 = ['Programming Language', 'Html', 'A']
        li_3 = ['Programming Language', 'Html', 'Basic', 'C']
        linked_list_true = [li_1, li_2, li_3]
        p0 = linked_list_test == linked_list_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestExcel()
