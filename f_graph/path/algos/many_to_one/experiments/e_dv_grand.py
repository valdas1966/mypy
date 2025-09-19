from f_dv.i_1_bar import Bar
import pandas as pd


cd = 'd'



def get_df() -> pd.DataFrame:
    """
    ===========================================================================
     Returns a dataframe with the results of the grand experiment.
    ===========================================================================
    """
    return pd.read_csv(csv_results)


df = get_df()
print(df)


