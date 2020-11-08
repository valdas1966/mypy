def score(df, col_true, col_false, col_pred='pred'):
    """
    ============================================================================
     Description: Return Score based on Pred.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame
        2. col_true : str
        3. col_false : str
        4. col_pred : str
    ============================================================================
     Return : int
    ============================================================================
    """
    summer = 0
    for index, row in df.iterrows():
        if row[col_pred] == 1:
            summer += row[col_true]
        elif row[col_pred] == 0:
            summer += row[col_false]
    return summer