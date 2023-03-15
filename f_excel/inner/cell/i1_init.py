import openpyxl.worksheet


class MyCellInit:
    """
    ============================================================================
     Desc: Wraps the openpyxl.cell.cell.Cell class.
    ============================================================================
    """

    def __init__(self, cell: openpyxl.cell.cell.Cell):
        """
        ========================================================================
         Description: Constructor. Init the Attributes.
        ========================================================================
        """
        self._cell = cell
