from PyQt5.QtWidgets import QWidget

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
        self._widget.setFont(self._font)

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
        self._widget.setFont(self._font)

    @property
    def color(self) -> str:
        """
        ========================================================================
         Get the current font color.
        ========================================================================
        """
        return self._widget.styles.get('color', '')

    @color.setter
    def color(self, value: str) -> None:
        """
        ========================================================================
         Set the font color.
        ========================================================================
        """
        self._widget.styles['color'] = value
        self._widget.apply_styles()

    @property
    def weight(self) -> int:
        """
        ========================================================================
         Get the current font weight.
        ========================================================================
        """
        return self._font.weight()

    @weight.setter
    def weight(self, value: int) -> None:
        """
        ========================================================================
         Set the font weight.
        ========================================================================
        """
        self._font.setWeight(value)
        self._widget.setFont(self._font)
