from PyQt5.QtWidgets import QWidget
from f_gui.pyqt.mixins.has_widget import HasWidget
from f_abstract.mixins.parentable import Parentable
from f_abstract.mixins.nameable import Nameable
from f_gui.pyqt.inner.widget.font import Font
from f_gui.pyqt.inner.widget.alignment import Alignment


class Widget(Nameable, Parentable, HasWidget):
    """
    ============================================================================
     QWidget Encapsulation.
    ============================================================================
    """

    def __init__(self, widget: QWidget, name: str = None) -> None:
        """
        ========================================================================
         Initialize the Widget class.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        HasWidget.__init__(self, widget=widget)
        Parentable.__init__(self)
        self._styles = {}
        self.font = Font(widget=self.widget)
        self.alignment = Alignment(widget=self.widget)

    @property
    def styles(self) -> dict[str, str]:
        """
        ========================================================================
         Get the current styles dictionary.
        ========================================================================
        """
        return self._styles

    @property
    def background(self) -> str:
        """
        ========================================================================
         Get the current background color.
        ========================================================================
        """
        return self._styles.get('background-color', '')

    @background.setter
    def background(self, color: str) -> None:
        """
        ========================================================================
         Set the background color.
        ========================================================================
        """
        self._styles['background-color'] = color
        self._apply_styles()

    def _apply_styles(self) -> None:
        """
        ========================================================================
         Apply the combined stylesheet.

         This method combines all the styles in the _styles dictionary and
         applies them to the widget's stylesheet.
        ========================================================================
        """
        li = [f'{key}: {val}' for key, val in self._styles.items()]
        style = "; ".join(li)
        self.widget.setStyleSheet(style)
