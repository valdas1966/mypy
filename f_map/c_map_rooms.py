from f_map.c_map import Map


class MapRooms(Map):

    def __init__(self, rows, row_block, col_block,
                 cols=None, row_door=None, col_door=None):
        """
        ========================================================================
         Description: Constructor - Init Arguments.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int (Amount of Rows in the Map).
            2. cols : int (Amount of Columns in the Map).
            3. row_block : int (Row to build the blocks between the rooms).
            4. col_block : int (Column to build the blocks between the rooms).
            5. row_door : int (Row of the Door).
            6. col_door : int (Columns of the Door).
        ========================================================================
        """
        if not cols:
            cols = rows
        if not row_door:
            row_door = row_block
        if not col_door:
            col_door = col_block
        super().__init__(rows=rows, cols=cols)
        self.row_block = row_block
        self.col_block = col_block
        self.row_door = row_door
        self.col_door = col_door
        self.zfill()
        self.__set_blocks()

    def __set_blocks(self):
        """
        ========================================================================
         Description: Build the Blocks in the Map the separates between Rooms.
        =======================================================================
        """
        # Block Column
        for row in range(self.row_block+1):
            self.grid[row][self.col_block] = -1
        # Block Row
        for col in range(self.col_block+1):
            self.grid[self.row_block][col] = -1

