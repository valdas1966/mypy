import sys
sys.path.append('D:\\MyPy')
sys.path.append('G:\\MyPy')

import numpy as np
from f_utils import u_tester
from f_grid import u_grid
from f_grid import u_gen_grid

class TestGrid:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_gen_dict_weights()
        self.tester_get_center()
        self.tester_lists_to_grid()
        self.tester_to_row_col()
        self.tester_to_idd()
        self.tester_is_valid_row_col()
        self.tester_is_valid_idd()
        self.tester_get_valid_idds()
        self.tester_get_neighbors()
        self.tester_to_course()
        self.tester_to_next_idd()
        self.tester_remove_deadlocks()
        self.tester_remove_empty_rows()
        self.tester_remove_empty_cols()
        self.tester_serialize()
        self.tester_canonize()
        self.tester_xor()
        self.tester_distance()
        self.tester_to_dict_g()
        self.tester_to_dict_h()
        u_tester.print_finish(__file__)

    def tester_gen_dict_weights(self):
        n = 4
        dict_w = u_grid.gen_dict_weights(n)

        p0 = len(dict_w) == n

        p1 = True
        for w in dict_w.values():
            if (w < 1) or (w > n):
                p1 = False
        u_tester.run(p0, p1)

    def tester_get_center(self):
        grid = u_gen_grid.symmetric(4)
        center = u_grid.get_center(grid)
        p0 = center == 10

        grid = u_gen_grid.symmetric(3)
        center = u_grid.get_center(grid)
        p1 = center == 4

        grid = u_gen_grid.symmetric(5)
        grid[2][2] = -1
        grid[1][1] = -1
        center = u_grid.get_center(grid)
        p2 = center == 7

        u_tester.run(p0, p1, p2)

    def tester_lists_to_grid(self):
        li_1 = [1, 2]
        li_2 = [1, 2, 3, 4]
        li_3 = [1]
        li_4 = [1, 2, 3]
        lists = [li_1, li_2, li_3, li_4]
        grid = u_grid.lists_to_grid(lists)
        grid_true = np.array(
            [[1, 2, -1, -1], [1, 2, 3, 4], [1, -1, -1, -1], [1, 2, 3, -1]],
            dtype=int)
        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_to_row_col(self):
        li_1 = [0, 1, 2]
        li_2 = [3, 4, 5]
        lists = [li_1, li_2]
        grid = np.array(lists)
        p0 = u_grid.to_row_col(grid, 0) == (0, 0)
        p1 = u_grid.to_row_col(grid, 1) == (0, 1)
        p2 = u_grid.to_row_col(grid, 2) == (0, 2)
        p3 = u_grid.to_row_col(grid, 3) == (1, 0)
        p4 = u_grid.to_row_col(grid, 4) == (1, 1)
        p5 = u_grid.to_row_col(grid, 5) == (1, 2)
        u_tester.run(p0, p1, p2, p3, p4, p5)

    def tester_to_idd(self):
        li_1 = [-1, 1, 2]
        li_2 = [3, 4, 5]
        lists = [li_1, li_2]
        grid = np.array(lists)

        p0 = (u_grid.to_idd(grid, 0, 2) == 2)
        p1 = (u_grid.to_idd(grid, 1, 0) == 3)
        p2 = (u_grid.to_idd(grid, 1, 1) == 4)
        p3 = (u_grid.to_idd(grid, 3, 4) == -1)

        u_tester.run(p0, p1, p2, p3)

    def tester_is_valid_row_col(self):
        li_1 = [0, -1]
        li_2 = [2, 3]
        lists = [li_1, li_2]
        grid = np.array(lists)

        p0 = u_grid.is_valid_row_col(grid, 1, 0) is True
        p1 = u_grid.is_valid_row_col(grid, 2, -1) is False
        p2 = u_grid.is_valid_row_col(grid, 3, 4) is False

        u_tester.run(p0, p1, p2)

    def tester_is_valid_idd(self):
        li_1 = [0, -1]
        li_2 = [2, 3]
        lists = [li_1, li_2]
        grid = np.array(lists)

        p0 = u_grid.is_valid_idd(grid, 0) is True
        p1 = u_grid.is_valid_idd(grid, 1) is False
        p2 = u_grid.is_valid_idd(grid, 4) is False

        u_tester.run(p0, p1, p2)

    def tester_get_valid_idds(self):
        li_1 = [0, -1]
        li_2 = [2, 3]
        lists = [li_1, li_2]
        grid = np.array(lists)
        valid_idds = u_grid.get_valid_idds(grid)

        valid_idds_true = [0, 2, 3]
        p0 = valid_idds == valid_idds_true
        u_tester.run(p0)

    def tester_get_neighbors(self):
        li_1 = [-1, 1, -1]
        li_2 = [3, 4, 5]
        li_3 = [-1, 7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)

        p0 = (u_grid.get_neighbors(grid, 2, 2) == [5, 7])
        p1 = (u_grid.get_neighbors(grid, 0, 1) == [4])
        p2 = (u_grid.get_neighbors(grid, 1, 1) == [1, 5, 7, 3])
        p3 = u_grid.get_neighbors(grid, idd=4) == [1, 5, 7, 3]
        u_tester.run(p0, p1, p2, p3)

    def tester_to_course(self):
        li_1 = [-1, 1, -1]
        li_2 = [3, 4, 5]
        li_3 = [-1, 7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)

        p0 = (u_grid.to_course(grid, 1, 4) == 'DOWN')
        p1 = (u_grid.to_course(grid, 4, 1) == 'UP')
        p2 = (u_grid.to_course(grid, 3, 4) == 'RIGHT')
        p3 = (u_grid.to_course(grid, 5, 4) == 'LEFT')
        p4 = (u_grid.to_course(grid, 4, 7) == 'DOWN')
        u_tester.run(p0, p1, p2, p3, p4)

    def tester_to_next_idd(self):
        li_1 = [-1, 1, -1]
        li_2 = [3, 4, 5]
        li_3 = [-1, 7, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)

        p0 = (u_grid.to_next_idd(grid, 1, 'DOWN') == 4)
        p1 = (u_grid.to_next_idd(grid, 4, 'UP') == 1)
        p2 = (u_grid.to_next_idd(grid, 4, 'RIGHT') == 5)
        p3 = (u_grid.to_next_idd(grid, 4, 'LEFT') == 3)
        p4 = (u_grid.to_next_idd(grid, 1, 'RIGHT') == -1)
        p5 = (u_grid.to_next_idd(grid, 5, 'RIGHT') == -1)
        p6 = (u_grid.to_next_idd(grid, 4, 'BLOCK') == -1)
        u_tester.run(p0, p1, p2, p3, p4, p5, p6)

    def tester_remove_deadlocks(self):
        li_1 = [2, -1, -1]
        li_2 = [-1, 2, 2]
        lists = [li_1, li_2]
        grid = np.array(lists)
        grid = u_grid.remove_deadlocks(grid)

        li_1 = [-1, -1, -1]
        li_2 = [-1, 2, 2]
        lists = [li_1, li_2]
        grid_true = np.array(lists)

        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_remove_empty_rows(self):
        li_1 = [-1, -1, -1]
        li_2 = [2, 2, 2]
        li_3 = [-1, -1, -1]
        li_4 = [2, 2, 2]
        li_5 = [-1, -1, -1]
        lists = [li_1, li_2, li_3, li_4, li_5]
        grid = np.array(lists)
        grid = u_grid.remove_empty_rows(grid)

        grid_true = np.array([[2, 2, 2], [2, 2, 2]], dtype=int)
        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_remove_empty_cols(self):
        li_1 = [-1, 2, -1, 2, -1]
        li_2 = [-1, 2, -1, 2, -1]
        lists = [li_1, li_2]
        grid = np.array(lists)
        grid = u_grid.remove_empty_cols(grid)
        grid_true = np.array([[2, 2], [2, 2]], dtype=int)
        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_serialize(self):
        li_1 = [-1, -1, -1, -1]
        li_2 = [-1, 1, 1, -1]
        li_3 = [-1, -1, -1, -1]
        lists = [li_1, li_2, li_3]
        grid = np.array(lists)
        grid = u_grid.serialize(grid)
        li_1 = [-1, -1, -1, -1]
        li_2 = [-1, 5, 6, -1]
        li_3 = [-1, -1, -1, -1]
        lists = [li_1, li_2, li_3]
        grid_true = np.array(lists)
        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_canonize(self):
        li_1 = [-1, -1, -1, -1, -1]
        li_2 = [-1, 1, 1, -1, 1]
        li_3 = [-1, -1, -1, 1, -1]
        li_4 = [-1, 1, 1, -1, -1]
        li_5 = [-1, 1, -1, 1, -1]
        lists = [li_1, li_2, li_3, li_4, li_5]
        grid = np.array(lists)
        grid = u_grid.canonize(grid)
        li_1 = [0, 1]
        li_2 = [2, 3]
        li_3 = [4, -1]
        lists = [li_1, li_2, li_3]
        grid_true = np.array(lists)
        p0 = (grid == grid_true).all()
        u_tester.run(p0)

    def tester_xor(self):
        li_11 = [1, 2]
        li_12 = [3, 4]
        lists_1 = [li_11, li_12]
        grid_1 = u_grid.lists_to_grid(lists_1)
        li_21 = [0, 2]
        li_22 = [3, 5]
        lists_2 = [li_21, li_22]
        grid_2 = u_grid.lists_to_grid(lists_2)
        li_31 = [1, 0]
        li_32 = [0, 1]
        lists_true = [li_31, li_32]
        grid_true = u_grid.lists_to_grid(lists_true)
        p0 = (u_grid.xor(grid_1, grid_2) == grid_true).all()
        u_tester.run(p0)

    def tester_distance(self):
        li_0 = [0, 1, 2]
        li_1 = [3, 4, 5]
        lists = [li_0, li_1]
        grid = u_grid.lists_to_grid(lists)
        p0 = u_grid.distance(grid, 1, 1) == 0
        p1 = u_grid.distance(grid, 4, 5) == 1
        p2 = u_grid.distance(grid, 3, 1) == 2
        p3 = u_grid.distance(grid, 2, 3) == 3
        u_tester.run(p0, p1, p2, p3)

    """
    def tester_get_dic_h(self):
        li_0 = [0, 1, 2]
        li_1 = [3, 4, 5]
        lists = [li_0, li_1]
        grid = u_grid.lists_to_grid(lists)
        lookup = {4: 5}
        dic_h = u_grid.get_dic_h(grid, 5, lookup)
        dic_h_true = dict()
        dic_h_true[0] = (3, False)
        dic_h_true[1] = (2, False)
        dic_h_true[2] = (1, False)
        dic_h_true[3] = (2, False)
        dic_h_true[4] = (5, True)
        dic_h_true[5] = (0, False)
        p1 = dic_h == dic_h_true
        grid = u_create.synthetic(5)
        grid[1][3] = -1
        grid[2][3] = -1
        grid[3][3] = -1
        grid[4][3] = -1
        lookup = dict()
        lookup[2] = 6
        lookup[7] = 7
        lookup[12] = 8
        lookup[17] = 9
        lookup[22] = 10
        dic_h, pathmax_nodes = get_dic_h(grid, 24, lookup, True)

        dic_h_true = dict()
        dic_h_true[0] = (8, False)
        dic_h_true[1] = (7, False)
        dic_h_true[2] = (6, True)
        dic_h_true[3] = (5, False)
        dic_h_true[4] = (4, False)
        dic_h_true[5] = (7, False)
        dic_h_true[6] = (6, False)
        dic_h_true[7] = (7, True)
        dic_h_true[9] = (3, False)
        dic_h_true[10] = (6, False)
        dic_h_true[11] = (7, False)
        dic_h_true[12] = (8, True)
        dic_h_true[14] = (2, False)
        dic_h_true[15] = (7, False)
        dic_h_true[16] = (8, False)
        dic_h_true[17] = (9, True)
        dic_h_true[19] = (1, False)
        dic_h_true[20] = (8, False)
        dic_h_true[21] = (9, False)
        dic_h_true[22] = (10, True)
        dic_h_true[24] = (0, False)

        p2 = dic_h == dic_h_true

        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2):
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))
    """

    def tester_to_dict_g(self):
        # Without Obstacles
        grid = u_gen_grid.symmetric(3)
        start = 0
        dic_test = u_grid.to_dict_g(grid, start)
        dic_true = {0: 0, 1: 1, 2: 2, 3: 1, 4: 2, 5: 3, 6: 2, 7: 3, 8: 4}
        p0 = dic_test == dic_true
        # With Obstacles
        grid[0][2] = -1
        grid[1][0] = -1
        dic_test = u_grid.to_dict_g(grid, start)
        dic_true = {0: 0, 1: 1, 4: 2, 5: 3, 6: 4, 7: 3, 8: 4}
        p1 = dic_test == dic_true
        u_tester.run(p0, p1)

    def tester_to_dict_h(self):
        # Without Obstacles
        grid = u_gen_grid.symmetric(3)
        goal = 0
        dic_test = u_grid.to_dict_h(grid, goal)
        dic_true = {0: 0, 1: 1, 2: 2, 3: 1, 4: 2, 5: 3, 6: 2, 7: 3, 8: 4}
        p0 = dic_test == dic_true
        # With Obstacles
        grid[0][2] = -1
        grid[1][0] = -1
        dic_test = u_grid.to_dict_h(grid, goal)
        dic_true = {0: 0, 1: 1, 4: 2, 5: 3, 6: 2, 7: 3, 8: 4}
        p1 = dic_test == dic_true
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestGrid()
