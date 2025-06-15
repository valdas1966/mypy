from f_gui_old.pyqt.handlers.on_event import OnEvent
from f_gui_old.pyqt.widget_text import WidgetText
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
        self._on_event = OnEvent(widget=self.widget)

    def set_on_enter(self, callback: Callable[[str], None]) -> None:
        """
        ========================================================================
         Set Callback-Function on Enter-Key pressed event.
        ========================================================================
        """
        self._on_event.set_callback_key(key='ENTER', callback=callback)
