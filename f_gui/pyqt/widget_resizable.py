from PyQt5.QtWidgets import QWidget


class WidgetResizable(QWidget):
    """
    ============================================================================
     Supports relative positioning and resizing of child Widgets.
    ============================================================================
    """

    def __init__(self, parent=None) -> None:
        """
        ========================================================================
         Initialize the ResizableWidget.
        ========================================================================
        """
        QWidget.__init__(self, parent=parent)
        self._info_children = list()

    def add(self,
            child: QWidget,
            x: int,
            y: int,
            width: int,
            height: int) -> None:
        """
        ========================================================================
         Add list child widget with relative position and size.
        ========================================================================
        """
        self._info_children.append((child, x, y, width, height))
        child.setParent(self)
        self._update_child_geometry(child, x, y, width, height)

    def resizeEvent(self, event):
        """
        ========================================================================
         Handle resize event to reposition and resize children widgets.
        ========================================================================
        """
        QWidget.resizeEvent(self, event)
        for child, x, y, width, height in self._info_children:
            self._update_child_geometry(child, x, y, width, height)

    def _update_child_geometry(self, child, x, y, width, height):
        """
        ========================================================================
         Update child widget geometry based on relative positions and sizes.
        ========================================================================
        """
        print('update child geommetry', child)
        parent_width = self.width()
        parent_height = self.height()
        print('parent:')
        print(parent_width, parent_height)

        abs_x = int(x / 100 * parent_width)
        abs_y = int(y / 100 * parent_height)
        abs_width = int(width / 100 * parent_width)
        abs_height = int(height / 100 * parent_height)

        abs_x = 10
        abs_y = 10
        abs_width = 50
        abs_height = 50
        print(abs_x, abs_y, abs_width, abs_height)
        child.setGeometry(abs_x, abs_y, abs_width, abs_height)
        print()
