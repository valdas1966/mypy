import numpy as np
from copy import deepcopy
from f_utils import u_tester
from f_grid.node import Node
from f_map.c_map import Map
from f_map.c_map_color import MapColor


class TestMapColor:

    def __init__(self):
        u_tester.print_start(__file__)
        TestMapColor.__tester_set_empty()
        TestMapColor.__tester_set()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_set_empty():
        map = Map(rows=3, cols=3)
        map.grid[1][2] = -1
        mapcolor = MapColor(map)
        li_1 = [0, 0, 0]
        li_2 = [0, 0, -1]
        li_3 = [0, 0, 0]
        lists = [li_1, li_2, li_3]
        grid_test = np.array(lists)
        p0 = (mapcolor.map.grid == grid_test).all()
        u_tester.run(p0)

    @staticmethod
    def __tester_set():
        map = Map(rows=3)
        map.grid[1][1] = -1
        map_color = MapColor(map)
        map_color.set_start_goals(start=6, goal_near=8, goal_far=2)
        map_color.set_group(group={Node(0), Node(1), Node(3)}, cat='LOOKUP')
        # Forward
        map_color_forward = deepcopy(map_color)
        map_color_forward.set_group(group={Node(5)}, cat='FORWARD')
        li_1 = [4, 4, 2]
        li_2 = [4, -1, 5]
        li_3 = [3, 0, 1]
        grid_true_forward = np.array([li_1, li_2, li_3])
        p0 = (map_color_forward.map.grid == grid_true_forward).all()
        # Backward
        map_color_backward = deepcopy(map_color)
        map_color_backward.set_group(group={Node(7)}, cat='BACKWARD')
        li_1 = [4, 4, 2]
        li_2 = [4, -1, 0]
        li_3 = [3, 6, 1]
        grid_true_backward = np.array([li_1, li_2, li_3])
        p1 = (map_color_backward.map.grid == grid_true_backward).all()
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestMapColor()


