from screeninfo import get_monitors
from f_gui.geometry.tlwh import LTWH


class UScreen:
    """
    ============================================================================
     Screen Utils Class.
    ============================================================================
    """

    @staticmethod
    def resolution() -> tuple[int, int]:
        """
        ========================================================================
         Return Screen Resolution (width, height).
        ========================================================================
        """
        monitor = get_monitors()[0]
        return monitor.width, monitor.height

    @staticmethod
    def full() -> LTWH:
        """
        ========================================================================
         Return Full-Screen Resolution (Left-Top-Width-Height) values.
        ========================================================================
        """
        width, height = UScreen.resolution()
        return LTWH(0, 0, width, int(height*0.91))
