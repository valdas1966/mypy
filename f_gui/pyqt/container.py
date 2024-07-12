from f_gui.pyqt.widget import Widget
from PyQt5.QtWidgets import QWidget
from f_gui.u_screen import UScreen as u_screen
from f_utils.dtypes.u_int import UInt as u_int


class Container(Widget):
    """
    ============================================================================
     Container Class to manage its own Layout.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Initialize the Container with its own Layout.
        ========================================================================
        """
        super().__init__(widget=QWidget(), name=name)
        self._children: dict[str, Widget] = dict()
        self._geometry: dict[str, tuple[int, int, int, int]] = dict()

    @property
    def children(self) -> dict[str, Widget]:
        """
        ========================================================================
         Dict of Container Children [name -> Widget].
        ========================================================================
        """
        return self._children

    def add(self,
            child: Widget,
            rel_x: int,
            rel_y: int,
            rel_width: int,
            rel_height: int) -> None:
        """
        ========================================================================
         Add a Widget at the specified relative Position [0,100].
        ========================================================================
        """
        self._children[child.name] = child
        self._geometry[child.name] = (rel_x, rel_y, rel_width, rel_height)
        child.widget.setParent(self.widget)

    def update(self) -> None:
        width = self.widget.width()
        height = self.widget.height()
        for name, child in self._children.items():
            geometry = self._geometry[name]
            geometry_abs = u_int.dims_rel_to_abs(*geometry, width, height)
            child.widget.setGeometry(*geometry_abs)
