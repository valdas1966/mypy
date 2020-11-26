from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks


class GridBlocksRooMap(GridBlocks):

    def __init__(self, path):
        """
        ========================================================================
         Description: Create Grid of Room-Map based on Map-File.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. path : str (Path to Map-File).
        ========================================================================
        """

    def __to_grid(self, path):
        file = open(path, 'r')
        for line in file.readlines():
