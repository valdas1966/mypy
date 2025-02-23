from f_file.map_grid import MapGrid


class GenMapGrid:
    """
    ========================================================================
     Generator for MapGrid objects.
    ========================================================================
    """

    @staticmethod
    def map_grid() -> MapGrid:
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
        path = 'g:\\temp\\map_grid.txt'
        return MapGrid.create(path=path, lines=lines)


map_grid = GenMapGrid.map_grid()
print(map_grid.to_array())
