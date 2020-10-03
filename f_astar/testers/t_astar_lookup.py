from f_utils import u_tester
from f_utils import u_random
from f_grid import u_grid
from f_grid import u_gen_grid
from f_astar.c_astar import AStar
from f_astar.c_astar_lookup import AStarLookup
from f_astar.c_node import Node
from f_map.c_map import Map
import random


class TestAStarLookup:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAStarLookup.__tester_run()
        TestAStarLookup.__tester_get_path()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        # Comparision to original A*
        p0 = True
        for i in range(100):
            grid = u_gen_grid.random(10, 10, 30)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goal = idds[1]
            astar_lookup = AStarLookup(grid, start, goal)
            astar_lookup.run()
            if not astar_lookup.is_found:
                continue
            astar = AStar(grid, start, goal)
            astar.run()
            if astar_lookup.len_optimal != len(astar.get_path())-1:
                p0 = False
                break
        # Manual Example
        grid = u_gen_grid.random(4)
        grid[1][2] = -1
        grid[2][2] = -1
        grid[3][2] = -1
        node_4 = Node(4)
        node_4.g = 7
        node_5 = Node(5)
        node_5.g = 6
        node_8 = Node(8)
        node_8.g = 8
        node_9 = Node(9)
        node_9.g = 7
        lookup = {node_4, node_5, node_8, node_9}
        start = 13
        goal = 15
        astar_lookup = AStarLookup(grid, start, goal, lookup)
        astar_lookup.run()
        closed_true = {Node(x) for x in [13, 12]}
        p1 = astar_lookup.closed == closed_true
        p2 = astar_lookup.len_optimal == 8
        u_tester.run(p0, p1, p2)


    @staticmethod
    def __tester_get_path():
        p0 = True
        for i in range(100):
            n = u_random.get_random_int(5, 10)
            map = Map(rows=n, cols=n, obstacles=30)
            start, goal_1, goal_2 = map.get_random_idds(3)
            astar = AStar(map.grid, start, goal_1)
            astar.run()
            astar_lookup = AStarLookup(map.grid, goal_2, start, astar.closed)
            astar_lookup.run()
            path_test = astar_lookup.get_path()
            astar_true = AStar(map.grid, start, goal_2)
            astar_true.run()
            path_true = astar_true.get_path()
            p0 = len(path_test) == len(path_true)
            if not p0:
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestAStarLookup()
