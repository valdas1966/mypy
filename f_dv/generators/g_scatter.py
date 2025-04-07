from f_dv.i_1_scatter import Scatter
import pandas as pd
import numpy as np


class GScatter:
    """
    ============================================================================
     Scatter Plot Generator Class.
    ============================================================================
    """

    @staticmethod
    def random_highly_correlated() -> Scatter:
        """
        ========================================================================
         Generate Scatter Plot.
        ========================================================================
        """
        x = np.random.randint(0, 100, 100)
        y = x + np.random.randint(-5, 5, 100)
        df = pd.DataFrame({'x': x, 'y': y})
        name = 'Scatter Plot'
        return Scatter(df=df,
                       col_x='x',
                       col_y='y',
                       name=name)


scatter = GScatter.random_highly_correlated()
scatter.show()
