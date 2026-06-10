from f_gui.elements.i_1_label.main import Label
from f_ds.geometry.bounds import Bounds
from f_color import RGB


class Factory:
    """
    ========================================================================
     Factory for Label objects.
    ========================================================================
    """

    @staticmethod
    def hello() -> Label:
        """
        ========================================================================
         Generate a Label with 'Hello' text.
        ========================================================================
        """
        return Label(text='Hello')

    @staticmethod
    def title() -> Label:
        """
        ========================================================================
         Generate a Label positioned as a title bar.
        ========================================================================
        """
        bounds = Bounds(top=0, left=0, bottom=10, right=100)
        return Label(bounds=bounds, text='Title')

    @staticmethod
    def full(text: str, fore: RGB, back: RGB) -> Label:
        bounds = Bounds.Factory.full()

