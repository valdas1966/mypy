from PyQt5.QtWidgets import QMainWindow
from f_gui_old.pyqt.widget import Widget
from f_gui_old.pyqt.container import Container
from f_gui_old.pyqt.mixins.has_widget import HasWidget
from f_core.mixins.has_name import HasName
from f_gui.layout.bounds import Position
from f_gui_old.u_screen import UScreen as u_screen


class Window(HasName, HasWidget):
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
        HasName.__init__(self, name=name)
        HasWidget.__init__(self, widget=QMainWindow())
        self._container = Container(name='Main Container')
        self._container.position = Position()
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

    def add(self, child: Widget) -> None:
        """
        ========================================================================
         Add list widget to the container's layout at the specified position.
        ========================================================================
        """
        self._container.add(child)

    def update_geometry(self) -> None:
        """
        ========================================================================
         Update Full-Screen layout for all Window's children.
        ========================================================================
        """
        parent = u_screen.full()
        self._container.update_geometry(parent=parent)

