from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.grid_blocks_rooms import GridBlocksRooms
from proj.ai.algo.astar import AStar
from proj.ai.algo.astar_lookup import AStarLookup


class TestAstarLookup:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAstarLookup.__tester_run()
        TestAstarLookup.__tester_lookup_start()
        TestAstarLookup.__tester_lookup_goal()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        grid = GridBlocks(rows=10, percent_blocks=30)
        p0, p1, is_found = False, False, False
        while not is_found:
            points = grid.points_random(2)
            start = points[0]
            goal = points[1]
            astar = AStar(grid, start, goal)
            astar.run()
            if not astar.is_found:
                continue
            is_found = True
            astar_lookup = AStarLookup(grid, start, goal)
            astar_lookup.run()
            p0 = astar.closed == astar_lookup.closed
            p1 = astar.optimal_path() == astar_lookup.optimal_path()
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_lookup_start():
        grid = GridBlocks(rows=4)
        grid.set_block(1, 2)
        grid.set_block(1, 3)
        start = Point(0, 0)
        goal = Point(3, 3)
        astar = AStarLookup(grid, start, goal)
        astar.run()
        lookup_test = astar.lookup_start()
        lookup_true = {Point(0, 0): 0, Point(0, 1): 1, Point(0, 2): 2,
                       Point(0, 3): 3, Point(1, 1): 2, Point(2, 1): 3,
                       Point(2, 2): 4, Point(2, 3): 5, Point(3, 3): 6}
        p0 = lookup_test == lookup_true
        u_tester.run(p0)

    @staticmethod
    def __tester_lookup_goal():
        grid = GridBlocks(rows=4)
        grid.set_block(1, 2)
        grid.set_block(1, 3)
        start = Point(0, 0)
        goal = Point(3, 3)
        astar = AStarLookup(grid, start, goal)
        astar.run()
        lookup_test = astar.lookup_goal()
        lookup_true = {Point(0, 0): 6, Point(0, 1): 5, Point(1, 1): 4,
                       Point(2, 1): 3, Point(2, 2): 2, Point(2, 3): 1,
                       Point(3, 3): 0}
        p0 = lookup_test == lookup_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestAstarLookup()
