from f_ds.geometry.bounds.main import Bounds


class Factory:
    """
    ========================================================================
     Generator for Bounds objects.
    ========================================================================
     The presets below use the f_gui 0-100 canvas frame; Bounds itself is
     frame-agnostic (Generic over int | float).
    ========================================================================
    """

    @staticmethod
    def full() -> Bounds[float]:
        """
        ========================================================================
         Full-canvas Bounds (0, 0, 100, 100) — a preset in the f_gui
         0-100 frame (not an intrinsic Bounds limit).
        ========================================================================
        """
        return Bounds(top=0, left=0, bottom=100, right=100)

    @staticmethod
    def half() -> Bounds[float]:
        """
        ========================================================================
         Generate a centered half-size bounds object (25, 25, 75, 75).
        ========================================================================
        """
        return Bounds(top=25, left=25, bottom=75, right=75)

    @staticmethod
    def quarter() -> Bounds[float]:
        """
        ========================================================================
         Generate a centered quarter-size bounds object
          (37.5, 37.5, 62.5, 62.5).
        ========================================================================
        """
        return Bounds(top=37.5, left=37.5, bottom=62.5, right=62.5)
