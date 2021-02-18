
def to_percent(count_true, count_all, precision=0, to_str=False):
    """
    =======================================================================
     Description: Return Percent-Representation of ratio of two value.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. count_true : int (Count of True-Values).
        2. count_all : int (Count of All-Values).
        3. precision : int (Amount of digits after the dot).
        4. to_str : bool (if return Str-Representation).
    =======================================================================
     Return: int of float or str
    -----------------------------------------------------------------------
        1. int (if not to_str and not precision).
        2. float (it not to_str and precision).
        3. str (if to_str).
    =======================================================================
    """
    f = f'.{precision}f'
    percent = format(0, f)
    # Prevent divided-by-zero problem
    if count_all:
        percent = format(count_true / count_all * 100, f)
    if to_str:
        return percent + '%'
    if not precision:
            return int(percent)
    return float(percent)


def to_commas(n):
    """
    ============================================================================
     Description: Return Str-Representation of the int with commas
                    between each 3 digits (thousands).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int.
    ============================================================================
     Return: str.
    ============================================================================
    """
    return f'{n:,}'


def sign(n):
    """
    ============================================================================
     Description: Return the Sign of Number.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int
    ============================================================================
     Return: int (1: Positive, 0: Zero, -1: Negative).
    ============================================================================
    """
    if n > 0:
        return 1
    if n == 0:
        return 0
    if n < 0:
        return -1


def are_int(values):
    """
    ============================================================================
     Description: Return True if all the Values are int.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. values : tuple | list | set
    ============================================================================
     Return : bool
    ============================================================================
    """
    for val in values:
        if '.' in str(val):
            return False
        try:
            x = int(val)
        except:
            return False
    return True
