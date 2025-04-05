from f_dv.heat_map import HeatMap
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
         Generate a heat map for a window full.
        ========================================================================
        """
        pivot = GenPivot.window_full()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full')
    
    @staticmethod
    def window_full_sum() -> HeatMap:
        """
        ========================================================================
         Generate a heat map for a window full sum.
        ========================================================================
        """
        pivot = GenPivot.window_full_sum()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full-Sum')
    
    @staticmethod
    def window_full_mean() -> HeatMap:
        """
        ========================================================================
         Generate a heat map for a window full mean.
        ========================================================================
        """
        pivot = GenPivot.window_full_mean()
        return HeatMap(pivot=pivot, name='HeatMap Window-Full-Mean')   

    @staticmethod
    def window_broken() -> HeatMap:
        """
        ========================================================================
         Generate a heat map for a window broken.
        ========================================================================
        """
        pivot = GenPivot.window_broken()
        return HeatMap(pivot=pivot, name='HeatMap Window-Broken')


# HeatMap(pivot=GenPivot.window_full()).show()
# HeatMap(pivot=GenPivot.window_full_sum()).show()
# HeatMap(pivot=GenPivot.window_full_mean()).show()
HeatMap(pivot=GenPivot.window_broken()).show()

