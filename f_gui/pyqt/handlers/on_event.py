from typing import Callable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QObject, QEvent
from f_gui.pyqt.mixins.has_widget import HasWidget


class OnEvent(QObject, HasWidget):
    """
    ============================================================================
     A Wrapper Class to handle Widget events.
    ============================================================================
    """
    _events_handled = {QEvent.KeyPress, QEvent.Resize}

    def __init__(self, widget: QWidget) -> None:
        """
        ========================================================================
         Initialize the EventHandler with the given widget.
        ========================================================================
        """
        QObject.__init__(self, widget=widget)
        HasWidget.__init__(self, widget=widget)
        self._callback_key: dict[int, Callable[[str], None]] = dict()
        self._callback_resize: Callable[[], None] | None = None
        self.widget.installEventFilter(self)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        ========================================================================
         Event filter to execute Callbacks.
        ========================================================================
        """
        if source is not self.widget:
            return QObject.eventFilter(self, source, event)
        if event.type() not in OnEvent._events_handled:
            return QObject.eventFilter(self, source, event)

        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in self._callback_key:
                self._callback_key[key](self.widget.toPlainText())
                return True  # Event handled

        if event.type() == QEvent.Resize:
            if self._callback_resize:
                self._callback_resize()
                return True  # Event handled

        return QObject.eventFilter(self, source, event)

    def set_callback_key(self, key: str, callback: Callable[[str], None]) -> None:
        """
        ========================================================================
         Set the function to be called when the specified key is pressed.
        ========================================================================
        """
        if key == 'ENTER':
            self._callback_key[Qt.Key_Enter] = callback
            self._callback_key[Qt.Key_Return] = callback

    def set_callback_resize(self, callback: Callable[[], None]) -> None:
        """
        ========================================================================
         Set the function to be called when the widget is resized.
        ========================================================================
        """
        self._callback_resize = callback
