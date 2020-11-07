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

def gen_index_test(label):
    