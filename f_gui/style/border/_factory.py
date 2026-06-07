from f_gui.style.border.main import Border
from f_gui.style.stroke import Stroke


class Factory:
    """
    ========================================================================
     Factory for Border objects.
    ========================================================================
    """

    @staticmethod
    def all(stroke: Stroke) -> Border:
        """
        ========================================================================
         Generate a uniform Border — the same Stroke on all four sides.
        ========================================================================
        """
        return Border(top=stroke, left=stroke, bottom=stroke, right=stroke)

    @staticmethod
    def solid() -> Border:
        """
        ========================================================================
         Generate a uniform default (1px, solid) Border on all four sides.
        ========================================================================
        """
        return Factory.all(stroke=Stroke())
