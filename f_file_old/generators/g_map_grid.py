from f_file_old.map_grid import MapGrid


class GenMapGrid:
    """
    ========================================================================
     Generator for MapGrid objects.
    ========================================================================
    """

    @staticmethod
    def map_grid(path: str = 'd:\\temp\\map_grid.txt') -> MapGrid:
        """
        ====================================================================
         Create a MapGrid object.
        ====================================================================
        """
        lines = list()
        lines.append('type')
        lines.append('heig')
        lines.append('widt')
        lines.append('map')
        lines.append('@...')
        lines.append('@.@.')
        lines.append('@...')
        lines.append('@@@@')
        return MapGrid.create(path=path, lines=lines)
