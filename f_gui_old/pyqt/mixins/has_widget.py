from PyQt5.QtWidgets import QWidget


class HasWidget:
    """
    ============================================================================
     Mixin-Class for Objects with QWidget.
    ============================================================================
    """

    def __init__(self, widget: QWidget) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._widget = widget

    @property
    def widget(self) -> QWidget:
        return self._widget
