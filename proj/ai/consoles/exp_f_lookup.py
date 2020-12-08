from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar_lookup import AStarLookup

dir_storage = 'D:\\Exp\\'
pickle_grids = dir_storage + 'grids.pickle'


def run():
    for i in range(1000):
        grid = GridBlocks(rows=10, percent_blocks=30)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        astar_forward = AStarLookup(grid, start, goal_1)
        astar_forward.run()
        lookup = astar_forward.lookup_start()
        astar_backward = AStarLookup(grid, goal_2, start, lookup)
        astar_backward.run()
