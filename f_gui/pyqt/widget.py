from PyQt5.QtWidgets import QWidget
from f_gui.pyqt.mixins.has_widget import HasWidget
from f_abstract.mixins.has_position import HasPosition
from f_abstract.mixins.parentable import Parentable
from f_abstract.mixins.nameable import Nameable


class Widget(Nameable, Parentable, HasWidget, HasPosition):
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
        HasPosition.__init__(self)
        self._styles = {}

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

    def update_shape(self,
                     width_full: int,
                     height_full: int) -> None:
        """
        ========================================================================
         Update Shape follow to parent shape updating.
        ========================================================================
        """
        print('widget.update_shape()', str(self))
        self.position.update(width_full, height_full)
        self.widget.setGeometry(*self.position.absolute)
        for child in self.children:
            child.update_shape()

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
