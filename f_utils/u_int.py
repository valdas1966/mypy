
def is_even(n: int) -> bool:
    """
    ============================================================================
     Return True if the given N is an Even-Number.
    ============================================================================
    """
    return not n % 2

def to_percent(numerator: int,
               denominator: int,
               precision: int = 0,        # Number of Digits after the Point
               to_str: bool = False
               ) -> int | float | str:
    """
    =======================================================================
     Description: Return the PCT-REPR of the ratio of two numbers.
    =======================================================================

    -----------------------------------------------------------------------
        1. int (if not to_str and not precision).
        2. float (it not to_str and precision).
        3. str (if to_str).
    =======================================================================
    """
    if not denominator:
        res = 0.0
    else:
        res = (numerator / denominator) * 100
    # Return STR
    if to_str:
        return f'{res:.{precision}f}%'
    # Return INT
    if not precision:
        return int(res)
    # Return FLOAT
    return round(res, precision)


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
