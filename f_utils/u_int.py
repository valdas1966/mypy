
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
