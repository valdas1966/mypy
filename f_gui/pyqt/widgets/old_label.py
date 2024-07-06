from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class Label(QLabel):
    """
    ============================================================================
     Label Class to encapsulate QLabel with additional functionality.
    ============================================================================
    """

    def __init__(self,
                 text: str = str(),
                 alignment: Qt.AlignmentFlag = Qt.AlignLeft, parent=None) -> None:
        """
        ========================================================================
         Initialize the Label with optional text and alignment.
        ========================================================================
        """
        super().__init__(text, parent)
        self.setAlignment(alignment)

    def set_text(self, text: str) -> None:
        """
        ========================================================================
         Set the text of the label.
        ========================================================================
        """
        self.setText(text)

    def set_alignment(self, alignment: Qt.AlignmentFlag) -> None:
        """
        ========================================================================
         Set the alignment of the label's text.
        ========================================================================
        """
        self.setAlignment(alignment)

    def set_stylesheet(self, stylesheet: str) -> None:
        """
        ========================================================================
         Set the stylesheet for the label.
        ========================================================================
        """
        self.setStyleSheet(stylesheet)
