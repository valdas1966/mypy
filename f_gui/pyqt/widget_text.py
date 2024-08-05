from PyQt5.QtWidgets import QWidget
from f_gui.pyqt.widget import Widget
from f_gui.pyqt.inner.widget.font import Font
from f_gui.pyqt.inner.widget.alignment import Alignment


class WidgetText(Widget):
    """
    ============================================================================
     Generic Text Widget Class to handle text-related properties.
    ============================================================================
    """

    def __init__(self, widget: QWidget, name: str = None) -> None:
        """
        ========================================================================
         Initialize the TextWidget with list text-capable QWidget.
        ========================================================================
        """
        super().__init__(widget=widget, name=name)
        self.font = Font(widget=widget)
        self.alignment = Alignment(widget=widget)

    @property
    def text(self) -> str:
        """
        ========================================================================
         Get the current text of the widget.
        ========================================================================
        """
        return self.widget.Text()

    @text.setter
    def text(self, value: str) -> None:
        """
        ========================================================================
         Set the text of the widget.
        ========================================================================
        """
        self.widget.setText(value)
        self.alignment = Alignment(self.widget)

    @property
    def color(self) -> str:
        """
        ========================================================================
         Get the current text color.
        ========================================================================
        """
        return self._styles.get('color', '')

    @color.setter
    def color(self, value: str) -> None:
        """
        ========================================================================
         Set the text color.
        ========================================================================
        """
        self._styles['color'] = value
        self._apply_styles()
