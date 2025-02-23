from f_file.txt import Txt
import numpy as np


class MapGrid(Txt):
    """
    ========================================================================
     MapGrid-File class.
    ========================================================================
    """

    ROWS_TITLE = 4
    CH_VALID = '.'
    CH_INVALID = '@'

    def __init__(self, path: str) -> None:
        """
        ====================================================================
         Initialize the MapGrid object.
        ====================================================================
        """
        Txt.__init__(self, path=path)

    def to_array(self) -> np.ndarray:
        """
        ====================================================================
         Convert the MapGrid object to a numpy boolean array.
        ====================================================================
        """
        lines = self[self.ROWS_TITLE:]
        rows = len(lines)
        cols = self.length_line_max()
        array = np.zeros((rows, cols), dtype=bool)
        for row in range(rows):
            for col in range(cols):
                array[row][col] = lines[row][col] == self.CH_VALID
        # remove empty rows
        array = array[array.any(axis=1)]
        # remove empty columns
        array = array[:, array.any(axis=0)] 
        return array

