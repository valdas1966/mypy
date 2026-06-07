from f_gui.style.stroke.main import Stroke, LineStyle


class Factory:
    """
    ========================================================================
     Factory for Stroke objects.
    ========================================================================
    """

    @staticmethod
    def default() -> Stroke:
        """
        ========================================================================
         Generate a default Stroke (1px, solid, no color).
        ========================================================================
        """
        return Stroke()

    @staticmethod
    def dashed() -> Stroke:
        """
        ========================================================================
         Generate a 2px dashed Stroke.
        ========================================================================
        """
        return Stroke(width=2, style=LineStyle.DASHED)
