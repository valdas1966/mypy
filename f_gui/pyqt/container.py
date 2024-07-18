from f_gui.pyqt.widget import Widget
from PyQt5.QtWidgets import QWidget


class Container(Widget):
    """
    ============================================================================
     Container Class to manage its own Layout.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Initialize the Container with its own Layout.
        ========================================================================
        """
        super().__init__(widget=QWidget(), name=name)

    def add(self,
            child: Widget,
            pos_rel: tuple[int, int, int, int]) -> None:
        """
        ========================================================================
         Add a Widget to Container with its relative position (x, y, w, h).
        ========================================================================
        """
        self.children.append(child)
        child.position.relative = pos_rel
        child.widget.setParent(self.widget)
