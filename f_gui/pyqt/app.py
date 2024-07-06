from PyQt5.QtWidgets import QApplication
from f_gui.pyqt.old_window import Window
import sys


class App:
    """
    ============================================================================
     Application Class to encapsulate the QApplication and main event loop.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Initialize the application with a specified window class.
        ========================================================================
        """
        self._app = QApplication(sys.argv)

    def run(self, window: Window) -> None:
        """
        ========================================================================
         Execute the main event loop.
        ========================================================================
        """
        window.widget.showMaximized()
        sys.exit(self._app.exec_())
