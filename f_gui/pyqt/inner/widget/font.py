from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont


class Font:
    """
    ============================================================================
     Font management class to encapsulate font-related properties and methods
     for a given QWidget.
    ============================================================================
    """

    def __init__(self, widget: QWidget) -> None:
        """
        ========================================================================
         Initialize the Font class.
        ========================================================================
        """
        self._widget = widget
        self._font = widget.font()

    @property
    def family(self) -> str:
        """
        ========================================================================
         Get the current font family name.
        ========================================================================
        """
        return self._font.family()

    @family.setter
    def family(self, value: str) -> None:
        """
        ========================================================================
         Set the font family name.
        ========================================================================
        """
        self._font.setFamily(value)
        self._update()

    @property
    def size(self) -> int:
        """
        ========================================================================
         Get the current font size.
        ========================================================================
        """
        return self._font.pointSize()

    @size.setter
    def size(self, value: int) -> None:
        """
        ========================================================================
         Set the font size.
        ========================================================================
        """
        self._font.setPointSize(value)
        self._update()

    @property
    def is_bold(self) -> bool:
        """
        ========================================================================
         Return True if the Font is Bold.
        ========================================================================
        """
        return self._font.weight() == QFont.Bold

    @is_bold.setter
    def is_bold(self, val: bool) -> None:
        """
        ========================================================================
         Set the Font to Bold or not.
        ========================================================================
        """
        weight = QFont.Bold if val else QFont.Normal
        self._font.setWeight(weight)
        self._update()

    def _update(self) -> None:
        """
        ========================================================================
         Update the widget's font.
        ========================================================================
        """
        self._widget.setFont(self._font)
