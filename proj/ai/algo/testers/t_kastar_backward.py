from f_utils import u_tester
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar import AStar
from proj.ai.algo.kastar_backward import KAStarBackward


class TestKAStarBackward:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStarBackward.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        p0 = True
        for i in range(100):
            grid = GridBlocks(5, 5, 30)
            start, goal_1, goal_2 = grid.points_random(3)
            kastar = KAStarBackward(grid, start, [goal_1, goal_2])
            kastar.run()
            expanded_nodes_test = len(kastar.closed)
            astar_1 = AStar(grid, goal_1, start)
            astar_1.run()
            closed = astar_1.closed
            astar_2 = AStar(grid, goal_2, start)
            astar_2.run()
            closed = closed.union(astar_2.closed)
            expanded_nodes_true = len(closed)
            p0 = expanded_nodes_test == expanded_nodes_true
            if not p0:
                print(grid)
                print(start, goal_1, goal_2)
                print(expanded_nodes_true, expanded_nodes_test)
                print(sorted(closed))
                print(sorted(kastar.closed))
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestKAStarBackward()
