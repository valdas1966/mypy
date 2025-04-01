from f_psl.pandas.generators.g_df import GenDF, pd
from f_psl.pandas.u_df import UDF


def test_format_col() -> None:
    """
    ========================================================================
     Test the format_col() function.
    ========================================================================
    """
    df = GenDF.two_hands()
    df = UDF.format_col(df=df,
                        col='x',
                        multiple=3)
    x = [0, 3, 3, 3, 6]
    y = [1, 2, 3, 4, 5]
    data = {'x': x, 'y': y}
    df_expected = pd.DataFrame(data)
    assert df.equals(df_expected)
