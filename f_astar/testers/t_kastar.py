from f_utils import u_tester
from f_utils import u_random
from f_grid import u_grid
from f_grid import u_gen_grid
from f_astar.c_node import Node
from f_astar.c_astar import AStar
from f_astar.c_kastar import KAStar
import random


class TestKAStar:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStar.__tester_run()
        TestKAStar.__tester_get_path()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        p0 = True
        for i in range(1000):
            n = u_random.get_random_int(5, 10)
            k = u_random.get_random_int(2, 10)
            grid = u_gen_grid.random(n)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goals = idds[1:k + 1]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            for goal in goals:
                path_test = kastar.get_path(goal)
                astar = AStar(grid, start, goal)
                path_true = astar.get_path()
                p0 = len(path_test) == len(path_true)
                if not p0:
                    break
        p1 = True
        p2 = True
        for i in range(1000):
            n = u_random.get_random_int(5, 10)
            k = u_random.get_random_int(2, 10)
            grid = u_gen_grid.random(n, n, 30)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goals = idds[1:k + 1]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            nodes_must = set()
            for goal in goals:
                path_test = kastar.get_path(goal)
                astar = AStar(grid, start, goal)
                path_true = astar.get_path()
                p1 = len(path_test) == len(path_true)
                if not p1:
                    break
                below_f = {node for node in astar.closed if node.f <
                           astar.f_goal}
                nodes_must = nodes_must.union(below_f)
            if not p1:
                break
            p2 = nodes_must.issubset(kastar.closed)
            if not p2:
                break
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_get_path():
        grid = u_gen_grid.random(4)
        start = 0
        goal = 12
        astar = KAStar(grid, start, {goal})
        astar.run()
        optimal_path = [0, 4, 8, 12]
        p0 = astar.get_path(goal) == optimal_path
        grid = u_gen_grid.random(4)
        grid[1][1] = -1
        grid[2][1] = -1
        start = 8
        goal = 10
        astar = KAStar(grid, start, {goal})
        astar.run()
        optimal_path = [8, 12, 13, 14, 10]
        p1 = astar.get_path(goal) == optimal_path
        p2 = True
        for i in range(1000):
            n = u_random.get_random_int(4, 4)
            grid = u_gen_grid.random(n)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goals = idds_valid[1:3]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            for goal in goals:
                len_optimal = u_grid.distance(grid, start, goal) + 1
                if len(kastar.get_path(goal)) != len_optimal:
                    p2 = False
                    break
            if not p2:
                break
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestKAStar()
