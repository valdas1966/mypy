from f_utils import u_tester
from f_grid import u_grid
from f_grid import u_gen_grid
from f_astar.c_astar import AStar
from f_astar.c_astar_bi import AStarBi
import random


class TestAStarBi:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAStarBi.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        # Manual Experiment
        grid = u_gen_grid.random(4)
        start = 0
        goal = 12
        astar_bi = AStarBi(grid, start, goal)
        astar_bi.run()
        p0 = astar_bi.len_optimal == 3
        # Compare to A* (len_optimal)
        p1 = True
        for i in range(1000):
            grid = u_gen_grid.random(rows=10, obstacles=30)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start, goal = idds[:2]
            astar = AStar(grid, start, goal)
            astar.run()
            if not astar.best:
                continue
            astar_bi = AStarBi(grid, start, goal)
            astar_bi.run()
            p1 = astar_bi.len_optimal == astar.f_goal
            if not p1:
                break
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestAStarBi()
