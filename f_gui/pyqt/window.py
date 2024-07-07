from PyQt5.QtWidgets import QMainWindow, QWidget
from f_gui.pyqt.container import Container
from f_gui.pyqt.mixins.has_widget import HasWidget
from f_abstract.mixins.nameable import Nameable


class Window(Nameable, HasWidget):
    """
    ============================================================================
     Main Window Class.
    ============================================================================
    """

    def __init__(self,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Window.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        HasWidget.__init__(self, widget=QMainWindow())
        self._container = Container(name=name)
        self._container.parent = self.widget
        self._widget.setCentralWidget(self._container.widget)
        self.set_title(name if name else 'Main Window')

    def set_title(self, title: str) -> None:
        """
        ========================================================================
         Set Title to Window.
        ========================================================================
        """
        self._widget.setWindowTitle(title)

    def add(self,
            child: QWidget,
            rel_x: int,
            rel_y: int,
            rel_width: int,
            rel_height: int) -> None:
        """
        ========================================================================
         Add a widget to the container's layout at the specified position.
        ========================================================================
        """
        self._container.add(child, rel_x, rel_y, rel_width, rel_height)
