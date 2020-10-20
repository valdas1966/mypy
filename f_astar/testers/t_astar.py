from f_utils import u_tester
from f_utils import u_random
from f_utils import u_dict
from f_grid import u_grid
from f_astar.c_astar import AStar
from f_map.c_map import Map
import random


class TestAStar:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAStar.__tester_run()
        TestAStar.__tester_optimal_path()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        # Perfect Heuristic (without obstacles)
        p0 = True
        p1 = True
        for i in range(100):
            n = u_random.get_random_int(3, 10)
            map = Map(rows=n)
            points_valid = map.points_valid()
            random.shuffle(points_valid)
            start = points_valid[0]
            goal = points_valid[1]
            astar = AStar(map, start, goal)
            astar.run()
            len_optimal = start.distance(goal) + 1
            if len(astar.optimal_path()) != len_optimal:
                p0 = False
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_run_old():
        # Perfect Heuristic (without obstacles)
        p0 = True
        p1 = True
        for i in range(100):
            n = u_random.get_random_int(3, 10)
            map = Map(rows=n)
            points_valid = map.points_valid()
            random.shuffle(points_valid)
            start = points_valid[0]
            goal = points_valid[1]
            astar = AStar(map, start, goal)
            astar.run()
            len_optimal = start.distance(goal) + 1
            if len(astar.optimal_path()) != len_optimal:
                p0 = False
                break
            dict_g = u_grid.to_dict_g(map.grid, start)
            dict_h = u_grid.to_dict_h(map.grid, goal)
            dict_f = u_dict.sum(dict_g, dict_h)
            f_goal = dict_g[goal]
            astar_closed = {node.point for node in astar.closed}
            closed_true = {point for point, f in dict_f.items() if f < f_goal}
            if not closed_true.issubset(astar_closed):
                p1 = False
                break
            nodes_errors = {node.point for node in astar.closed if dict_f[
                node.point] > f_goal}
            if nodes_errors:
                p1 = False
                break
        # Not-Perfect Heuristic (with obstacles)
        p2 = True
        p3 = True
        for i in range(100):
            n = u_random.get_random_int(5, 10)
            map = Map(rows=n, obstacles=30)
            points_valid = map.points_valid()
            random.shuffle(points_valid)
            start = points_valid[0]
            goal = points_valid[1]
            astar = AStar(map, start, goal)
            astar.run()
            dict_g = u_grid.to_dict_g(map.grid, start)
            if goal not in dict_g.keys():
                break
            len_optimal = dict_g.get(goal)
            if len_optimal + 1 != len(astar.optimal_path()):
                p2 = False
                break
            dict_h = u_grid.to_dict_h(map.grid, goal)
            dict_f = u_dict.sum(dict_g, dict_h)
            f_goal = dict_g[goal]
            astar_closed = {node.point for node in astar.closed}
            closed_true = {point for point, f in dict_f.items() if f < f_goal}
            if not closed_true.issubset(astar_closed):
                p3 = False
                break
            nodes_errors = {node.point for node in astar.closed if dict_f[
                node.point] > f_goal}
            if nodes_errors:
                p3 = False
                break
        # Manual Experiment
        map = Map(rows=5)
        map.grid[2][1] = -1
        map.grid[2][2] = -1
        map.grid[3][2] = -1
        start = 16
        goal = 6
        astar = AStar(map, start, goal)
        astar.run()
        closed_true = {16, 15, 10, 5, 6}
        closed_astar = {node.point for node in astar.closed}
        p4 = closed_true == closed_astar
        # Run a new Goal - Manual
        map = Map(rows=4)
        map.grid[1][2] = -1
        map.grid[2][2] = -1
        map.grid[3][2] = -1
        start = 13
        goal = 0
        astar = AStar(map, start, goal)
        astar.run()
        goal_new = 15
        astar.run(goal_new)
        closed_astar = {node.idd for node in astar.closed}
        closed_true = {0, 1, 2, 3, 5, 7, 8, 9, 11, 12, 13, 15}
        p5 = closed_astar == closed_true
        """
        # Run a new Goal - Automatic
        p6 = True
        for i in range(100):
            n = u_random.get_random_int(5, 10)
            map = Map(rows=n, cols=n, obstacles=30)
            start, goal_1, goal_2 = map.get_random_idds(3)
            astar_true = AStar(map.grid, start, goal_2)
            astar_true.run()
            if not astar_true.best:
                continue
            path_true = astar_true.get_path()
            astar = AStar(map.grid, start, goal_1)
            astar.run()
            if not astar.best:
                continue
            astar.run(goal_2)
            path_test = astar.get_path()
            if not path_test:
                continue
            p6 = len(path_test) == len(path_true)
            if not p6:
                break
        """
        u_tester.run(p0, p1, p2, p3, p4, p5)

    @staticmethod
    def __tester_optimal_path():
        map = Map(rows=3)
        start = 0
        goal = 8
        astar = AStar(map, start, goal)
        astar.run()
        astar_test = astar.optimal_path()
        astar_true = [0, 1, 2, 5, 8]
        p0 = astar_test == astar_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestAStar()
