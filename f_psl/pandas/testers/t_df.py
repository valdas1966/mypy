from f_psl.pandas.generators.g_df import GenDF, pd
from f_psl.pandas.u_df import UDF


def test_nearest_multiple() -> None:
    """
    ========================================================================
     Test the nearest_multiple() function.
    ========================================================================
    """
    df = GenDF.three_hands()
    d_cols = {'a': 2, 'b': 3}
    actual = UDF.nearest_multiple(df=df, d_cols=d_cols)
    print(actual)
    a_expected = [2, 2, 4, 4, 6]
    b_expected = [0, 3, 3, 3, 6]
    c_expected = [1, 2, 3, 4, 5]
    data_expected = {'a': a_expected, 'b': b_expected, 'c': c_expected}
    expected = pd.DataFrame(data_expected)
    assert actual.equals(expected)
