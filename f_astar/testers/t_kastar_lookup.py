from f_utils import u_tester
from f_grid import u_gen_grid
from f_astar.c_kastar_lookup import KAStarLookup


class TestKAStarLookup:

    def __init__(self):
        u_tester.print_start(__file__)
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        grid = u_gen_grid.random(4)
