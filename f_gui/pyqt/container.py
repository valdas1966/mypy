from PyQt5.QtWidgets import QWidget
from f_gui.pyqt.widget import Widget


class Container(Widget):
    """
    ============================================================================
     Container Class to manage its own Layout.
    ============================================================================
    """

    def __init__(self,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Container with its own Layout.
        ========================================================================
        """
        Widget.__init__(self, widget=QWidget(), name=name)

    def add(self,
            w: QWidget,
            x: int,
            y: int,
            width: int,
            height: int) -> None:
        """
        ========================================================================
         Add a widget to the container's layout at the specified position.
        ========================================================================
        """
        w.setParent(self.widget)
        w.setGeometry(x, y, width, height)
