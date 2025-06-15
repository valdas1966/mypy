from f_gui_old.pyqt.widget_text import WidgetText
from PyQt5.QtWidgets import QLabel


class Label(WidgetText):
    """
    ============================================================================
     Label Class to wrap QLabel.
    ============================================================================
    """

    def __init__(self, name: str = 'Label') -> None:
        """
        ========================================================================
         Initialize the Label with its own QLabel.
        ========================================================================
        """
        WidgetText.__init__(self, widget=QLabel(), name=name)


