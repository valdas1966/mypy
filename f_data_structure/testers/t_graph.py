from f_utils import u_tester
from f_data_structure import u_graph


class TestGraph:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGraph.__tester_descendants()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_descendants():
        edges = {(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)}
        descendants_test = u_graph.get_descendants(edges=edges, root=1)
        descendants_true = {2, 3, 4, 5, 6, 7}
        p0 = descendants_test == descendants_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestGraph()
