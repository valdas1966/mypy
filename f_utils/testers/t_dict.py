from f_utils import u_tester
from f_utils import u_dict


class TestDict:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_to_key_value_str()
        self.tester_minus()
        self.tester_sum()
        TestDict.__tester_sorted_by_value()
        TestDict.__tester_update()
        TestDict.__tester_union()
        u_tester.print_finish(__file__)

    def tester_to_key_value_str(self):
        dic = {'a': 1, 'b': 2}
        str_test = u_dict.to_key_value_str(dic)
        str_true = 'a="1", b="2"'
        p0 = str_test == str_true
        p1 = u_dict.to_key_value_str(dict()) == str()
        u_tester.run(p0, p1)

    def tester_minus(self):
        dic_1 = {1:11, 2:22, 3:33}
        dic_2 = {1:11, 2:222}
        dic_minus_test = u_dict.minus(dic_1, dic_2)
        dic_minus_true = {2:22, 3:33}
        p0 = dic_minus_test == dic_minus_true
        p1 = u_dict.minus(dic_1, dic_1) == dict()
        p2 = u_dict.minus(dict(), dict()) == dict()
        u_tester.run(p0, p1, p2)

    def tester_sum(self):
        # Same Keys in both Dicts
        dict_1 = {1: 1, 2: 2}
        dict_2 = {1: 9, 2: 8}
        dict_sum = u_dict.sum(dict_1, dict_2)
        dict_true = {1: 10, 2: 10}
        p0 = dict_sum == dict_true
        # Not Same Keys in both Dicts
        dict_3 = {1: 1}
        dict_sum = u_dict.sum(dict_1, dict_3)
        dict_true = {1: 2}
        p1 = dict_sum == dict_true
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_union():
        dict_1 = {'a': 1, 'b': 2}
        dict_2 = {'b': 2, 'c': 3}
        dict_test = u_dict.union(dict_1, dict_2)
        dict_true = {'a': 1, 'b': 2, 'c': 3}
        p0 = dict_test == dict_true
        u_tester.run(p0)

    @staticmethod
    def __tester_sorted_by_value():
        # Ascending Sort
        d = {'a': 3, 'b': 1, 'c': 2}
        d_test = u_dict.sort_by_value(d)
        d_true = {'b': 1, 'c': 2, 'a': 3}
        p0 = d_test == d_true
        # Descending Sort
        d_test = u_dict.sort_by_value(d, reverse=True)
        d_true = {'a': 3, 'c': 2, 'b': 1}
        p1 = d_test == d_true
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_update():
        # Vals in Set
        d = dict()
        d = u_dict.update(d, 1, 11)
        d = u_dict.update(d, 2, 22)
        d = u_dict.update(d, 2, 33)
        d_true = {1: [11], 2: [22, 33]}
        p0 = d == d_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestDict()

