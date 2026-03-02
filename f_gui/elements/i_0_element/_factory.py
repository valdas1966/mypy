from f_gui.elements.i_0_element.main import Element
from f_ds.geometry.bounds import Bounds


class Factory:
    """
    ========================================================================
     Factory for Element objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Element:
        """
        ========================================================================
         Generate a full-size Element (0, 0, 100, 100).
        ========================================================================
        """
        return Element()

    @staticmethod
    def half() -> Element:
        """
        ========================================================================
         Generate a centered half-size Element (25, 25, 75, 75).
        ========================================================================
        """
        bounds = Bounds.Factory.half()
        return Element(bounds=bounds)
