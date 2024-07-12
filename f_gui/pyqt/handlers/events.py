from typing import Callable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QObject, QEvent
from f_gui.pyqt.mixins.has_widget import HasWidget


class EventHandler(QObject, HasWidget):
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
        HasWidget.__init__(self, widget=widget)
        self._key_callbacks: dict[int, Callable[[], None]] = dict()
        self._resize_callback: Callable[[], None] = None
        self.widget.installEventFilter(self)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        ========================================================================
         Event filter to execute Callbacks.
        ========================================================================
        """
        if source is not self.widget:
            return QObject.eventFilter(self, source, event)
        if event.type() not in EventHandler._events_handled:
            return QObject.eventFilter(self, source, event)

        if event.type() == QEvent.KeyPress and source is self.widget:
            key = event.key()
            if key in self._key_callbacks:
                self._key_callbacks[key]()
                return True  # Event handled

        if event.type() == QEvent.Resize and source is self.widget:
            if self._resize_callback:
                self._resize_callback()
                return True  # Event handled

        return QObject.eventFilter(self, source, event)

    def set_key_callback(self, key: str, callback: Callable[[], None]) -> None:
        """
        ========================================================================
         Set the function to be called when the specified key is pressed.
        ========================================================================
        """
        if key == 'ENTER':
            self._key_callbacks[Qt.Key_Enter] = callback
            self._key_callbacks[Qt.Key_Return] = callback
        else:
            self._key_callbacks[getattr(Qt, f'Key_{key.upper()}')] = callback

    def set_resize_callback(self, callback: Callable[[], None]) -> None:
        """
        ========================================================================
         Set the function to be called when the widget is resized.
        ========================================================================
        """
        self._resize_callback = callback
