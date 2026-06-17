from f_gui.style.stroke.main import Stroke, DashPattern


class Factory:
    """
    ========================================================================
     Factory for Stroke objects.
    ========================================================================
    """

    @staticmethod
    def dashed() -> Stroke:
        """
        ========================================================================
         Generate a 2px dashed Stroke.
        ========================================================================
        """
        return Stroke(width=2, pattern=DashPattern.DASHED)
