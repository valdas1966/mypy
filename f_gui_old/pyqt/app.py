from PyQt5.QtWidgets import QApplication
from f_gui.layout import Position
from f_core.mixins.has.name import HasName
from f_gui_old.pyqt.window import Window
from f_gui_old.pyqt.widget import Widget

import sys


class App(HasName):
    """
    ============================================================================
     Application Class to encapsulate the QApplication and main event loop.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Initialize the application with list specified window class.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._app = QApplication(sys.argv)
        self._win = Window(name=name)

    @property
    def background(self) -> str:
        """
        ========================================================================
         Return App Background.
        ========================================================================
        """
        return self._win.background

    @background.setter
    def background(self, color: str) -> None:
        """
        ========================================================================
         Set Background Color.
        ========================================================================
        """
        self._win.background = color

    @property
    def position(self) -> Position:
        """
        ========================================================================
         Return Window position.
        ========================================================================
        """
        return self._win.position

    def children(self) -> list[Widget]:
        """
        ========================================================================
         Return List of Window children.
        ========================================================================
        """
        return self._win.children()

    def add(self, child: Widget) -> None:
        """
        ========================================================================
         Add Widget to the App.
        ========================================================================
        """
        self._win.add(child)

    def run(self) -> None:
        """
        ========================================================================
         Execute the main event loop.
        ========================================================================
        """
        self._win.widget.showMaximized()
        self._win.update_geometry()
        sys.exit(self._app.exec_())
