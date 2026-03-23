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


def test_csv_add_col_bins(tmp_path):
    """
    ========================================================================
     Test UCsv.add_col_bins() end-to-end (read, bin, write).
    ========================================================================
    """
    path = str(tmp_path / 'data.csv')
    df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6]})
    UDf.write(df=df, path=path)
    UCsv.add_col_bins(path=path, col='a', bins=[2, 4, 6])
    result = UDf.read(path=path)
    assert list(result['a']) == [1, 2, 3, 4, 5, 6]
    assert list(result['binned_a']) == [2, 2, 2, 4, 4, 6]


def test_csv_union(tmp_path):
    """
    ========================================================================
     Test UCsv.union() end-to-end (read two CSVs, union, write).
    ========================================================================
    """
    path_1 = str(tmp_path / 'a.csv')
    path_2 = str(tmp_path / 'b.csv')
    path_output = str(tmp_path / 'output.csv')
    df_1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df_2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})
    UDf.write(df=df_1, path=path_1)
    UDf.write(df=df_2, path=path_2)
    UCsv.union(path_1=path_1, path_2=path_2, path_output=path_output)
    result = UDf.read(path=path_output)
    assert list(result['a']) == [1, 2, 5, 6]
    assert list(result['b']) == [3, 4, 7, 8]
