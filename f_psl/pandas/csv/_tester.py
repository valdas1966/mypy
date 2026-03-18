import pandas as pd
from f_psl.pandas.df import UDf
from f_psl.pandas.csv import UCsv


def test_csv_group(tmp_path):
    """
    ========================================================================
     Test UCsv.group() end-to-end (read, group, write).
    ========================================================================
    """
    path_input = str(tmp_path / 'input.csv')
    path_output = str(tmp_path / 'output.csv')
    df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
    UDf.write(df=df, path=path_input)
    UCsv.group(path_input=path_input,
               path_output=path_output,
               col_a='a',
               col_b='b',
               agg='mean')
    result = UDf.read(path=path_output)
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [15.0, 35.0]


def test_csv_group_default_cols(tmp_path):
    """
    ========================================================================
     Test UCsv.group() with default columns.
    ========================================================================
    """
    path_input = str(tmp_path / 'input.csv')
    path_output = str(tmp_path / 'output.csv')
    df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
    UDf.write(df=df, path=path_input)
    UCsv.group(path_input=path_input,
               path_output=path_output,
               agg='sum')
    result = UDf.read(path=path_output)
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [30, 70]


def test_csv_add_col_agg(tmp_path):
    """
    ========================================================================
     Test UCsv.add_col_agg() end-to-end (read, add column, write).
    ========================================================================
    """
    path = str(tmp_path / 'data.csv')
    df = pd.DataFrame({'a': [1, 5, 3], 'b': [4, 2, 6]})
    UDf.write(df=df, path=path)
    UCsv.add_col_agg(path=path, cols=['a', 'b'], col='min', func=min)
    result = UDf.read(path=path)
    assert list(result['min']) == [1, 2, 3]
