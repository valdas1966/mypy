from f_gui.pyqt.container import Container


class Window(Container):
    """
    ============================================================================
     Window Class.
    ============================================================================
    """

    def __init__(self,
                 rows: int = 100,
                 cols: int = 100,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Container.__init__(self, rows, cols, name=name)
        self.set_title(name if name else 'Window')

    def set_title(self, title: str) -> None:
        """
        ========================================================================
         Set Title to Window.
        ========================================================================
        """
        self._widget.setWindowTitle(title)

    def resizeEvent(self, event) -> None:
        """
        ========================================================================
         Capture the resize event to get the new size of the window.
        ========================================================================
        """
        super().resizeEvent(event)
        width, height = self.get_size()
        print(f"Window resized: {width}x{height}")