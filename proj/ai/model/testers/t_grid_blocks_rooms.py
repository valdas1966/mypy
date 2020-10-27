from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.grid_blocks_rooms import GridBlocksRooms


class TestGridBlocksRooms:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGridBlocksRooms.__tester_walls_and_door()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_walls_and_door():
        grid_test = GridBlocksRooms(rows=5, corner=Point(2, 3),
                                    door=Point(2, 1))
        grid_true = GridBlocks(rows=5)
        grid_true.set_block(Point(2, 0))
        grid_true.set_block(Point(2, 2))
        grid_true.set_block(Point(2, 3))
        grid_true.set_block(Point(1, 3))
        grid_true.set_block(Point(0, 3))
        p0 = grid_test == grid_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestGridBlocksRooms()
