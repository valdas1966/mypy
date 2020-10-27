from f_utils import u_tester
from proj.ai.model.point import  Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar_lookup import AStarLookup


class TestAStarLookup:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAStarLookup.__tester_run_manual()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run_manual():
        # Not-Perfect Heuristic (with blocks)
        grid = GridBlocks(rows=4)
        grid.set_block(Point(1, 2))
        grid.set_block(Point(1, 3))
        start = Point(0, 0)
        goal = Point(3, 3)
        lookup = {Point(0, 2): 6}
        astar = AStarLookup(grid, start, goal, lookup)
        astar.run()
        closed_test = astar.closed
        closed_true = {Point(0, 0), Point(0, 1),
                       Point(1, 1),
                       Point(2, 1), Point(2, 2), Point(2, 3),
                       Point(3, 3)}
        p0 = closed_test == closed_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestAStarLookup()
