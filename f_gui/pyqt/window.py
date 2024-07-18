from PyQt5.QtWidgets import QMainWindow
from f_gui.pyqt.widget import Widget
from f_gui.pyqt.container import Container
from f_gui.pyqt.mixins.has_widget import HasWidget
from f_abstract.mixins.nameable import Nameable
from f_abstract.components.position import Position
from f_gui.u_screen import UScreen as u_screen


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
        shape = u_screen.resolution()
        self._container = Container(name='Main Container')
        self._container.position.relative = (0, 0, 100, 100)
        self._container.update_shape(*shape)
        self._widget.setCentralWidget(self._container.widget)
        self.set_title(name if name else 'Main Window')

    @property
    def background(self) -> str:
        """
        ========================================================================
         Get background color.
        ========================================================================
        """
        return self._container.background

    @background.setter
    def background(self, color: str) -> None:
        """
        ========================================================================
         Set background color.
        ========================================================================
        """
        self._container.background = color

    @property
    def position(self) -> Position:
        """
        ========================================================================
         Return Main-Container position.
        ========================================================================
        """
        return self._container.position

    def children(self) -> list[Widget]:
        """
        ========================================================================
         Return List of Main-Container children.
        ========================================================================
        """
        return self._container.children

    def set_title(self, title: str) -> None:
        """
        ========================================================================
         Set Title to Window.
        ========================================================================
        """
        self._widget.setWindowTitle(title)

    def add(self,
            child: Widget,
            pos_rel: tuple[int, int, int, int]) -> None:
        """
        ========================================================================
         Add a widget to the container's layout at the specified position.
        ========================================================================
        """
        self._container.add(child, pos_rel)
