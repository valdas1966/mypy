from f_gui.pyqt.handlers.key_press import KeyPress
from f_gui.pyqt.widget_text import WidgetText
from PyQt5.QtWidgets import QTextEdit
from typing import Callable


class TextBox(WidgetText):
    """
    ============================================================================
     Wraps QTextEdit.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 set_focus: bool = True) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        WidgetText.__init__(self, widget=QTextEdit(), name=name)
        if set_focus:
            self.widget.setFocus()
        self._key_handler = KeyPress(widget=self.widget)

    def set_on_enter(self, callback: Callable[[], None]) -> None:
        """
        ========================================================================
         Set Callback-Function on Enter-Key pressed event.
        ========================================================================
        """
        self._key_handler.set_callback(key='ENTER', callback=callback)
