from f_ds.grids.cell._base import CellBase
from f_gui.components.component import Component


class CellGui(CellBase):
    """
    ============================================================================
     Cell-Gui for the 2D-Grid Gui.
    ============================================================================
    """

    def __init__(self,
                 # Cell's Row
                 row: int,
                 # Cell's Column
                 col: int,
                 # Widget to display in the Cell
                 widget: Component
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        CellBase.__init__(self, row=row, col=col, name=widget.name)
        self._widget = widget

    @property
    def widget(self) -> Component:
        """
        ========================================================================
         Getter for the Widget.
        ========================================================================
        """
        return self._widget
    