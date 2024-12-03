from PyQt5.QtWidgets import QWidget
from f_gui.pyqt.mixins.has_widget import HasWidget
from f_gui.mixins.has_position import HasPosition
from f_ds.mixins.has_parent import HasParent
from f_core.mixins.has_name import HasName
from f_gui.components.ltwh import LTWH


class Widget(HasName, HasParent, HasWidget, HasPosition):
    """
    ============================================================================
     QWidget Encapsulation.
    ============================================================================
    """

    def __init__(self,
                 widget: QWidget,
                 name: str = 'Widget') -> None:
        """
        ========================================================================
         Initialize the Widget class.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasWidget.__init__(self, widget=widget)
        HasParent.__init__(self)
        HasPosition.__init__(self)
        self._styles = {'background-color': 'White'}
        self._apply_styles()

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

    def update_geometry(self, parent: LTWH) -> None:
        """
        ========================================================================
         Update absolute Location by Parent dimensions.
        ========================================================================
        """
        self.position.parent = parent
        self.widget.setGeometry(*self.position.absolute.to_tuple())
        for child in self.children:
            child.update_geometry(self.position.absolute)

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
