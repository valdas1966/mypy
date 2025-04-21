from f_dv.i_0_chart import Chart
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class ScatterRegression(Chart):
    """
    ============================================================================
     Scatter Plot with Regression Line Class.
    ============================================================================
    """

    def __init__(self,
                 df: pd.DataFrame,
                 col_x: str,
                 col_y: str,
                 label_x: str = None,
                 label_y: str = None,
                 color_point: str = 'blue',
                 color_line: str = 'red',
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize Attributes.
        ========================================================================
        """
        self._df = df
        self._col_x = col_x
        self._col_y = col_y
        self._label_x = label_x
        self._label_y = label_y
        self._color_point = color_point
        self._color_line = color_line
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
        """
        ========================================================================
         Scatter Plot with Regression Line.
        ========================================================================
        """
        x = self._df[self._col_x].values
        y = self._df[self._col_y].values

        # Scatter plot of the data
        plt.scatter(x, y, color=self._color_point, label='Data Points', s=2)

        # Fit linear regression line
        coef = np.polyfit(x, y, 1)
        poly1d_fn = np.poly1d(coef)

        # Plot regression line
        x_sorted = np.sort(x)
        plt.plot(x_sorted, poly1d_fn(x_sorted), color=self._color_line,
                 linewidth=2.5, label=f'Regression Line (y = {coef[0]:.2f}x + {coef[1]:.2f})')

        # Labels and ticks
        plt.xlabel(self._label_x, fontweight='bold')
        plt.ylabel(self._label_y, fontweight='bold')
        plt.xticks(fontweight='bold')
        plt.yticks(fontweight='bold')

        # Legend
        plt.legend(loc='upper left', fontsize=6, frameon=False)
