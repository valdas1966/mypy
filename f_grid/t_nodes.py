from f_utils import u_tester
from f_grid import u_grid
from f_grid import u_create
from f_grid import u_nodes


class TesterUNodes:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_get_farthest()
        u_tester.print_finish(__file__)

    def tester_get_farthest(self):
        grid = u_create.synthetic(5)
        start = 0
        goals = {4, 5}
        farthest = u_nodes.get_farthest(grid, start, goals)
        p0 = farthest == 4

        u_tester.run([p0])


if __name__ == '__main__':
    TesterUNodes()
