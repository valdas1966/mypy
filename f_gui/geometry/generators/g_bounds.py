from f_gui.geometry.bounds import Bounds


class GenBounds:
    """
    ========================================================================
     Generator for LTWH objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Bounds:
        """
        ========================================================================
         Generate a full-size LTWH.
        ========================================================================
        """
        return Bounds(top=0, left=0, width=100, height=100)
    
    @staticmethod
    def half() -> Bounds:
        """
        ========================================================================
         Generate a half-size LTWH.
        ========================================================================
        """
        return Bounds(top=25, left=25, width=50, height=50)
    
    @staticmethod
    def quarter() -> Bounds:
        """
        ========================================================================
         Generate a quarter-size LTWH.
        ========================================================================
        """ 
        return Bounds(top=37.5, left=37.5, width=25, height=25)
