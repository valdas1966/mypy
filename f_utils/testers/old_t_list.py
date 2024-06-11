from f_utils import u_tester
from f_utils import old_u_list


class TestList:

    def __init__(self):
        u_tester.print_start(__file__)
        TestList.__tester_sublist_by_index()
        TestList.__tester_bigram()
        TestList.__tester_to_str()
        TestList.__tester_to_slices_breadth()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_sublist_by_index():
        # Simple Test
        li = ['a', 'b', 'c']
        indices = [0, 2]
        li_test = u_list.sublist_by_index(li, indices)
        li_true = ['a', 'c']
        p0 = li_test == li_true
        u_tester.run(p0)

    @staticmethod
    def __tester_bigram():
        li = list('abc')
        bigram_test = u_list.bigram(li)
        bigram_true = [tuple('ab'), tuple('bc')]
        p0 = bigram_test == bigram_true
        u_tester.run(p0)

    @staticmethod
    def __tester_to_str():
        # List of str
        li = ['a', 'b', 'c']
        str_test = u_list.to_str(li)
        str_true = 'a,b,c'
        p0 = str_test == str_true
        # List of int
        li = [1, 2, 3]
        str_test = u_list.to_str(li)
        str_true = '1,2,3'
        p1 = str_test == str_true
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_to_slices_breadth():
        li = [1, 2, 3, 4, 5, 6]
        slices_test = u_list.to_slices_breadth(li=li, num_slices=2)
        slices_true = [[1, 3, 5], [2, 4, 6]]
        p0 = slices_test == slices_true
        li = [1, 2, 3, 4, 5]
        slices_test = u_list.to_slices_breadth(li=li, num_slices=2)
        slices_true = [[1, 3, 5], [2, 4]]
        p1 = slices_test == slices_true
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestList()