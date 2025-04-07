from f_dv.i_0_chart import Chart
import pandas as pd
import matplotlib.pyplot as plt


class Scatter(Chart):
    """
    ============================================================================
     Scatter Plot Class.
    ============================================================================
    """

    def __init__(self,
                 df: pd.DataFrame,
                 col_x: str,
                 col_y: str,
                 color_x: str = 'red',
                 color_y: str = 'blue',
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._df = df
        self._col_x = col_x
        self._col_y = col_y
        self._color_x = color_x
        self._color_y = color_y
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
        """
        ========================================================================
        Scatter Plot with Two Custom Colors.
        ========================================================================
        """
        x = self._df[self._col_x]
        y = self._df[self._col_y]

        plt.scatter(x, y, color=self._color_x, label=self._col_x)
        plt.scatter(y, x, color=self._color_y, label=self._col_y)

        # Set axis titles with colors
        plt.xlabel(self._col_x, fontweight='bold', color=self._color_x)
        plt.ylabel(self._col_y, fontweight='bold', color=self._color_y)

        # Make x and y ticks bold
        plt.xticks(fontweight='bold')
        plt.yticks(fontweight='bold')

        # Legend in top-left corner
        plt.legend(loc='upper left', fontsize='large', frameon=False)
