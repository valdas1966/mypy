import numpy as np
from proj.ai.model.grid_blocks import GridBlocks


class GridBlocksRooMap(GridBlocks):

    def __init__(self, path, size_room, char_valid='.', rows_pass=4,
                 goals_in_room_max=10):
        """
        ========================================================================
         Description: Create Grid of Room-Map based on Map-File.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. path : str (Path to Map-File).
            2. size_room : int (Edge of the Room (Square)).
            3. char_valid : str (Char that represents Valid Point).
            4. rows_pass : int (Meta-Data rows on the top of the file).
            5. goals_in_room_max : int (Max Number of Goals in the Room).
        ========================================================================
        """
        self.size_room = size_room
        self.goals_in_room_max = goals_in_room_max
        rows = list()
        file = open(path, 'r')
        lines = file.readlines()[rows_pass:]
        for line in lines:
            row = list(line.strip())
            row = [0 if x == char_valid else -1 for x in row]
            rows.append(row)
        file.close()
        ndarray = np.array(rows)
        super().__init__(rows=ndarray.shape[0], cols=ndarray.shape[1])
        self.ndarray = ndarray
        self.rows_room = self.rows / self.size_room
        self.cols_room = self.cols / self.size_room
        self.rooms = GridBlocks(rows=self.rows_room, cols=self.cols_room)

    def random_rooms(self, amount):
        """
        ========================================================================
         Description: Return N Random-Rooms from the RooMap.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. amount : int (Amount of Random-Rooms to return).
        ========================================================================
        """
        self.rooms.points_random(amount)

    def __set_rooms(self):
        """
        ========================================================================
         Description: Set Grid of Rooms (each Point represents a Room in Map).
        ========================================================================
        """
        for row_room in range(self.rows_room):
            for col_room in range(self.cols_room):
                row_a = row_room * self.size_room
                row_b = (row_room + 1) * self.size_room
                col_a = col_room * self.size_room
                col_b = (col_room + 1) * self.size_room
                ndarray = self.ndarray[row_a:row_b, col_a:col_b]
                if (ndarray == 0).sum() < self.goals_in_room_max:
                    self.rooms.set_block(row_room, col_room)
