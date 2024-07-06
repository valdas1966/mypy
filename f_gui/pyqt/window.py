from PyQt5.QtWidgets import QMainWindow, QWidget
from f_gui.pyqt.container import Container
from f_gui.pyqt.widget import Widget


class Window(Widget):
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
        Widget.__init__(self, widget=QMainWindow(), name=name)
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
        self._container.add(w, x, y, width, height)
