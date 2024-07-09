from typing import Callable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QObject, QEvent
from f_gui.pyqt.mixins.has_widget import HasWidget


class KeyPress(QObject, HasWidget):
    """
    ============================================================================
     A Wrapper Class to handle key press events for any QWidget.
    ============================================================================
    """

    def __init__(self, widget: QWidget):
        """
        ========================================================================
         Initialize the KeyPress handler with the given widget.
        ========================================================================
        """
        QObject.__init__(self, widget=widget)
        HasWidget.__init__(self, widget=widget)
        self._callbacks = dict()
        self.widget.installEventFilter(self)

    def eventFilter(self,
                    source: QObject,
                    event: QEvent) -> bool:
        """
        ========================================================================
         Event filter to capture key press events and execute callbacks.
        ========================================================================
        """
        if event.type() == event.KeyPress and source is self.widget:
            key = event.key()
            if key in self._callbacks:
                self._callbacks[key]()
                return True  # Event handled
        return QObject.eventFilter(self, source, event)

    def set_callback(self, key: str, callback: Callable[[], None]) -> None:
        """
        ========================================================================
         Set the function to be called when the specified key is pressed.
        ========================================================================
        """
        if key == 'ENTER':
            self._callbacks[Qt.Key_Enter] = callback
            self._callbacks[Qt.Key_Return] = callback
