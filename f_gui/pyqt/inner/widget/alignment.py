from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class Alignment:
    """
    ============================================================================
     Text-Alignment properties Manager for a given QWidget.
    ============================================================================
    """

    LEFT = Qt.AlignLeft

    def __init__(self, widget: QWidget) -> None:
        """
        ========================================================================
         Initialize the Alignment class.
        ========================================================================
        """
        self._widget = widget
        self._horizontal: Qt.AlignmentFlag = Qt.AlignCenter
        self._vertical: Qt.AlignmentFlag = Qt.AlignVCenter
        self._update()

    @property
    def horizontal(self) -> Qt.AlignmentFlag:
        """
        ========================================================================
         Get the current horizontal alignment.
        ========================================================================
        """
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value: Qt.AlignmentFlag) -> None:
        """
        ========================================================================
         Set the horizontal alignment.
        ========================================================================
        """
        self._horizontal = value
        self._update()

    @property
    def vertical(self) -> Qt.AlignmentFlag:
        """
        ========================================================================
         Get the current vertical alignment.
        ========================================================================
        """
        return self._vertical

    @vertical.setter
    def vertical(self, value: Qt.AlignmentFlag) -> None:
        """
        ========================================================================
         Set the vertical alignment.
        ========================================================================
        """
        self._vertical = value
        self._update()

    def _update(self) -> None:
        """
        ========================================================================
         Apply the current alignment settings to the widget.

         This method combines the horizontal and vertical alignment flags and
         applies them to the widget.
        ========================================================================
        """
        alignment = self._horizontal | self._vertical
        self._widget.setAlignment(alignment)
