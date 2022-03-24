import math
import random
import pandas as pd
from f_utils import u_dict


def remove_duplicated_columns(df):
    """
    =======================================================================
     Description: Remove Duplicated Columns in the DataFrame (same names).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
         1. df : DataFrame (with duplicated columns).
    =======================================================================
     Return: DataFrame (without duplicated columns).
    =======================================================================
    """
    return df.loc[:, ~df.columns.duplicated()]


def split_to_x_y(df, col_label):
    """
    =======================================================================
     Description: Split DataFrame to X (without label) and Y (label).
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. df : DataFrame
        2. col_label : str
    =======================================================================
     Return: Tuple(DataFrame, Series) (x, y)
    =======================================================================
    """
    x = df.drop(col_label, axis=1)
    df = df.rename({col_label: 'label'}, axis=1)
    y = df['label']
    return x, y


def split_random(df, percent):
    """
    ============================================================================
     Description: Split DataFrame into 2 Random DataFrames.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame to split.
        2. percent : int (Percent of rows for first DataFrame).
    ============================================================================
     Return: Tuple (DataFrame, DataFrame).
    ============================================================================
    """
    x = len(df) * percent // 100
    li = list(df.index)
    random.shuffle(li)
    li_x = li[:x]
    li_y = list(set(li) - set(li_x))
    df_x = df.iloc[li_x, :]
    df_y = df.iloc[li_y, :]
    return df_x, df_y


def divide(df, parts):
    """
    =======================================================================
     Description: Return List of Sub-DataFrames.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. df : DataFrame (The main DataFrame).
        2. parts : int (Number of Sub-DataFrames to divide).
    =======================================================================
     Return: list of df.
    =======================================================================
    """
    len_df = len(df)
    if not len_df:
        return [pd.DataFrame() for x in parts]

    bulk = math.ceil(len_df / parts)

    li_dfs = list()
    for i in range(parts):
        a = i * bulk
        b = (i+1) * bulk
        li_dfs.append(df[a:b])

    return li_dfs


def drop_columns(df, columns):
    """
    ============================================================================
     Description: Drop Columns in DataFrame.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. columns : list of str (Columns Names).
    ============================================================================
     Return : DataFrame (without dropped columns).
    ============================================================================
    """
    return df.drop(columns, axis=1)


def to_dict(df, col_key=0, col_val=1):
    """
    ============================================================================
     Description: Return Dict-Representation of the DataFrame
                    (work only on two specified columns - key and value).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. col_key : str (Key-Column Name).
        3. col_val : str (Val-Column Name).
    ============================================================================
     Return : dict.
    ============================================================================
    """
    d = dict()
    for index, row in df.iterrows():
        key = row[col_key]
        val = row[col_val]
        d = u_dict.update(d, key, val)
    return d


