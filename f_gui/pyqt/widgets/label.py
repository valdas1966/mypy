from PyQt5.QtWidgets import QLabel
from f_gui.pyqt.widget import Widget


class Label(Widget):
    """
    ============================================================================
     QLabel Encapsulation.
    ============================================================================
    """

    def __init__(self,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Label.
        ========================================================================
        """
        Widget.__init__(self, widget=QLabel(), name=name)

    def set_text(self, text: str) -> None:
        """
        ========================================================================
         Set the text of the label.
        ========================================================================
        """
        self.widget.setText(text)
