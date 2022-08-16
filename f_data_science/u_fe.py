import pandas as pd

"""
================================================================================
 Description: Feature Engineering static functions.
================================================================================
"""


def synthetic(df, columns_to_exclude=set()):
    """
    ============================================================================
     Description: Create DataFrame with Synthetic-Features (arithmetic
                    operations between each two columns).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
    ============================================================================
     Return : DataFrame that contains only synthetic-features.
    ============================================================================
    """
    df_synthetic = pd.DataFrame()
    for col_1 in df.columns:
        if col_1 in columns_to_exclude:
            continue
        for col_2 in df.columns:
            if col_2 in columns_to_exclude:
                continue
            if col_1 >= col_2:
                continue
            df_synthetic[f'{col_1}_plus_{col_2}'] = df[col_1] + df[col_2]
            df_synthetic[f'{col_1}_minus_{col_2}'] = df[col_1] - df[col_2]
            df_synthetic[f'{col_1}_mult_{col_2}'] = df[col_1] * df[col_2]
            col = f'{col_1}_divide_{col_2}'
            df_synthetic[col] = df[col_1] / df[col_2]
            df_synthetic[col].replace(float('Infinity'), 1000000, inplace=True)
            df_synthetic[col].replace(-float('Infinity'), -1000000,
                                      inplace=True)
            df_synthetic[col].fillna(0, inplace=True)
            df_synthetic[f'{col_2}_minus_{col_1}'] = df[col_2] - df[col_1]
            col = f'{col_2}_divide_{col_1}'
            df_synthetic[col] = df[col_2] / df[col_1]
            df_synthetic[col].replace(float('Infinity'), 1000000, inplace=True)
            df_synthetic[col].replace(-float('Infinity'), -1000000,
                                      inplace=True)
            df_synthetic[col].fillna(0, inplace=True)
    return df_synthetic

