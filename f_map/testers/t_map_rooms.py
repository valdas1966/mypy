from f_utils import u_tester
from f_map.c_map_rooms import MapRooms
from f_grid import u_grid


class TestMapRooms:

    def __init__(self):
        u_tester.print_start(__file__)
        TestMapRooms.__tester_init()
        TestMapRooms.__tester_set_blocks()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        map_rooms = MapRooms(rows=5, row_block=2, col_block=3, row_door=4)
        p0 = (map_rooms.cols, map_rooms.col_door) == (5, 3)
        u_tester.run(p0)

    @staticmethod
    def __tester_set_blocks():
        map_rooms = MapRooms(rows=5, row_block=2, col_block=3, row_door=1)
        map_rooms.zfill()
        li_0 = [0, 0, 0, -1, 0]
        li_1 = [0, 0, 0, 0, 0]
        li_2 = [-1, -1, -1, -1, 0]
        li_3 = [0, 0, 0, 0, 0]
        li_4 = [0, 0, 0, 0, 0]
        lists = [li_0, li_1, li_2, li_3, li_4]
        grid_true = u_grid.lists_to_grid(lists)
        p0 = (map_rooms.grid == grid_true).all()
        u_tester.run(p0)
        print(map_rooms.grid)


if __name__ == '__main__':
    TestMapRooms()
