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

    def add(self,
            child: QWidget,
            rel_x: int,
            rel_y: int,
            rel_width: int,
            rel_height: int) -> None:
        """
        ========================================================================
         Add a Widget at the specified relative Position [0,100].
        ========================================================================
        """
        child.setParent(self.widget)
        screen_width, screen_height = u_screen.resolution()
        screen_height = int(screen_height*0.9)
        geometry_abs = u_int.dims_rel_to_abs(rel_x, rel_y,
                                             rel_width, rel_height,
                                             screen_width, screen_height)
        child.setGeometry(*geometry_abs)
