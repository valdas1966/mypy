from f_utils import u_tester
from proj.ai.model.grid import Grid


class TestModelGrid:

    def __init__(self):
        u_tester.print_start(__file__)
        u_tester.print_finish(__file__)

    @staticmethod
    def tester_neighbors():
        grid = Grid(rows=5)
if __name__ == '__main__':
    TestModelGrid()
