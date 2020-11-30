from random import randint


def get_random_int(size, x_min, x_max, y_min=None, y_max=None):
    """
    ===========================================================================
     Description: Return List of Random Points in Inclusive-Ranges.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. a : int (Random Number From).
        2. b : int (Random Number To).
    ===========================================================================
     Return: int (Random Number between a and b).
    ===========================================================================
    """
    assert type(size) == int
    assert size >= 1
    assert type(x_min) == int
    assert type(x_max) == int
    y_min = x_min if not y_min else y_min
    y_max = x_max if not y_max else y_max
    assert type(y_min) == int
    assert type(y_max) == int
    return randint(a,b)