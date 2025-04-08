from f_dv.i_1_scatter_regression import ScatterRegression
import numpy as np
import pandas as pd


class GScatterRegression:

    @staticmethod
    def highly_correlated() -> ScatterRegression:
        """
        ========================================================================
        Gen a scatter with a highly correlated relationship between x and y.
        ========================================================================
        """
        x = np.linspace(0, 10, 100)
        y = 2 * x + np.random.normal(0, 0.5, 100)  # Less noise → higher correlation
        df = pd.DataFrame({'x': x, 'y': y})
        return ScatterRegression(df, 'x', 'y', color_point='blue', color_line='red')


    @staticmethod
    def weakly_correlated() -> ScatterRegression:
        """
        ========================================================================
        Gen a scatter with a weakly correlated relationship between x and y.
        ========================================================================
        """
        x = np.linspace(0, 10, 100)
        y = 2 * x + np.random.normal(0, 1.5, 100)  # More noise → lower correlation
        df = pd.DataFrame({'x': x, 'y': y})
        return ScatterRegression(df, 'x', 'y', color_point='blue', color_line='red')



scatter = GScatterRegression.weakly_correlated()
scatter.show()
