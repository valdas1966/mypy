from f_gui.components.ltwh import LTWH


class GenLTWH:
    """
    ========================================================================
     Generator for LTWH objects.
    ========================================================================
    """

    @staticmethod
    def gen_ltwh_full() -> LTWH:
        """
        ========================================================================
         Generate a full-size LTWH.
        ========================================================================
        """
        return LTWH(left=0, top=0, width=100, height=100)
    
    @staticmethod
    def gen_ltwh_half() -> LTWH:
        """
        ========================================================================
         Generate a half-size LTWH.
        ========================================================================
        """
        return LTWH(left=25, top=25, width=50, height=50)
    
    @staticmethod
    def gen_ltwh_quarter() -> LTWH:
        """
        ========================================================================
         Generate a quarter-size LTWH.
        ========================================================================
        """ 
        return LTWH(left=37.5, top=37.5, width=25, height=25)
