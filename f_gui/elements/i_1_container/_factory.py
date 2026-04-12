from f_gui.elements.i_1_container.main import Container
from f_ds.geometry.bounds import Bounds


class Factory:
    """
    ========================================================================
     Factory for Container objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Container:
        """
        ========================================================================
         Generate a full-size Container (0, 0, 100, 100).
        ========================================================================
        """
        return Container()

    @staticmethod
    def half() -> Container:
        """
        ========================================================================
         Generate a centered half-size Container (25, 25, 75, 75).
        ========================================================================
        """
        return Container(bounds=Bounds.Factory.half())
