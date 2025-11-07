from f_dv.i_1_heat_map import HeatMap
from f_psl.pandas.generators.g_pivot import GenPivot


class GenHeatMap:
    """
    ============================================================================
     HeatMap Generator Class.
    ============================================================================
    """

    @staticmethod
    def window_full() -> HeatMap:
        """
        ========================================================================
         Generate a heat i_1_map for a window full.
        ========================================================================
        """
        pivot = GenPivot.window_full()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full')
    
    @staticmethod
    def window_full_sum() -> HeatMap:
        """
        ========================================================================
         Generate a heat i_1_map for a window full sum.
        ========================================================================
        """
        pivot = GenPivot.window_full_sum()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full-Sum')
    
    @staticmethod
    def window_full_mean() -> HeatMap:
        """
        ========================================================================
         Generate a heat i_1_map for a window full mean.
        ========================================================================
        """
        pivot = GenPivot.window_full_mean()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full-Mean')   

    @staticmethod
    def window_broken() -> HeatMap:
        """
        ========================================================================
         Generate a heat i_1_map for a window broken.
        ========================================================================
        """
        pivot = GenPivot.window_broken()
        return HeatMap(pivot=pivot, name='HeatMap Window-Broken')
    
    @staticmethod
    def random_10x10() -> HeatMap:
        """
        ========================================================================
         Generate a heat i_1_map for a random 10x10 window.
        ========================================================================
        """
        pivot = GenPivot.random_10x10()
        return HeatMap(pivot=pivot, name='HeatMap Random-10x10')


# GenHeatMap.window_broken().show()
GenHeatMap.random_10x10().show()
