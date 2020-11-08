from sklearn.model_selection import train_test_split


def split(x, y, is_classifier=True):
    """
    =======================================================================
     Description: Divide X and Y into Train and Test (75% Train).
                    stratify=y means that the label's ration in the Test
                     will be the same as the ratio in the Train.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. x : DataFrame (Features).
        2. y : Series (Label).
        3. is_classifier : bool.
    =======================================================================
     Return: Tuple(DataFrame, DataFrame, Series, Series)
                  (x_train, x_test, y_train, y_test).
    =======================================================================
    """
    if is_classifier:
        return train_test_split(x, y, stratify=y)
    return train_test_split(x, y)


def index_train_test(label):
    """
    ============================================================================
     Description: Return Indeces of Splitted Train and Test.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. label : Series
    ============================================================================
     Return : Tuple(Index, Index)
    ============================================================================
    """
    x_train, x_test, _, _ = split(label, label)
    return x_train.index, x_test.index
