from f_ds import u_df


def drop_correlated_features(df, threshold=1):
    """
    ============================================================================
     Description: Drop Correlated Features from the DataFrame
                    (when the abs(correlation) is bigger than a threshold).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. threshold : float.
    ============================================================================
     Return: DataFrame (without correlated features).
    ============================================================================
    """
    cols_to_delete = list()
    for col_1 in df.columns:
        for col_2 in df.columns:
            if col_1 >= col_2:
                continue
            corr = abs(df[col_1].corr(df[col_2]))
            if corr >= threshold:
                cols_to_delete.append(col_2)
    df = u_df.drop_columns(df, cols_to_delete)
    return df
