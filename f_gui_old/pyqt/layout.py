from PyQt5.QtWidgets import QGridLayout, QSpacerItem, QSizePolicy
from f_core.mixins.has.rows_cols import HasRowsCols


class Layout(HasRowsCols):
    """
    ============================================================================
     Layout Class to encapsulate QGridLayout management.
    ============================================================================
    """

    def __init__(self,
                 rows: int = 100,
                 cols: int = 100) -> None:
        """
        ========================================================================
         Initialize the QGridLayout.
        ========================================================================
        """
        HasRowsCols.__init__(self, rows, cols)
        self._layout = QGridLayout()
        self._init_grid()

    def get(self) -> QGridLayout:
        """
        ========================================================================
         Return the QGridLayout object.
        ========================================================================
        """
        return self._layout

    def _init_grid(self) -> None:
        """
        ========================================================================
        Initialize the grid with spacers to set up the desired size.
        ========================================================================
        """
        for row in range(self._rows):
            for col in range(self._cols):
                min_policy = QSizePolicy.Minimum
                spacer = QSpacerItem(1, 1, min_policy, min_policy)
                self._layout.addItem(spacer, row, col)
