from PyQt5.QtWidgets import QMessageBox
from f_gui_old.pyqt.widget import Widget
from f_gui_old.pyqt.inner.widget.font import Font


class MsgBox(Widget):
    """
    ============================================================================
     MsgBox Class to wrap QMessageBox.
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 title: str = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the MsgBox with its own QMessageBox.
        ========================================================================
        """
        Widget.__init__(self, widget=QMessageBox(), name=name)
        self._font = Font(widget=self.widget)
        self._font.family = 'heebo'
        self._font.is_bold = True
        self._font.size = 24
        self.widget.setIcon(QMessageBox.Information)
        self.widget.setWindowTitle(title)
        self.widget.setText(text)
        self.widget.adjustSize()
        self.widget.exec_()

    @property
    def font(self) -> Font:
        return self._font
