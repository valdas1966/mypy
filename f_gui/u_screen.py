from screeninfo import get_monitors


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
