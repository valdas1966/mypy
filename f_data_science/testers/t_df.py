import pandas as pd
from f_data_science import u_df


def test_explode_str_kv():
    col_a = ['1', '2']
    col_b = ['{c=3, d=4}', '{d=5, e=6}']
    data = {'list': col_a, 'b': col_b}
    df = pd.DataFrame(data)
    col_c = ['3', None]
    col_d = ['4', '5']
    col_e = [None, '6']
    data_true = {'list': col_a, 'b': col_b, 'c': col_c, 'd': col_d, 'e': col_e}
    df_true = pd.DataFrame(data_true)
    assert u_df.explode_col_kv(df=df, col_kv='b').equals(df_true)