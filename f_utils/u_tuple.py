from random import randint


def random_tuples(size_list, size_tuple, value_min, value_max):
    """
    ============================================================================
     Description: Return List of Tuples of Random-Integer Values.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. size_list : int (Size of the List).
        2. size_tuple : int (Size of the Tuples).
        3. value_min : int (Min Value to Random).
        4. value_max : int (Max Value to Random).
    ============================================================================
     Return: list of tuple of int
    ============================================================================
    """
    assert type(size_list) == int
    assert type(size_tuple) == int
    assert type(value_min) == int
    assert type(value_max) == int
    assert size_list > 0
    assert size_tuple > 0
    li = list()
    for _ in range(size_list):
        t = tuple(randint(value_min, value_max) for _ in range(size_tuple))
        li.append(t)
    return li
