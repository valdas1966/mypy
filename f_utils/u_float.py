
def are_float(values):
    """
    ============================================================================
     Description: Return True if all the Values are Float.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. values : tuple | list | set
    ============================================================================
     Return: bool
    ============================================================================
    """
    for val in values:
        try:
            x = float(val)
        except:
            return False
    return True


def to_str_pct(val: float,
               precision: int,
               to_100: bool = True       # For example: 0.75 to 75%
               ) -> str:
    """
    ============================================================================
     Desc: Returns list STR-REPR of list Float as list Percentage
           (ex: from 0.75 to 75%).
    ============================================================================
    """
    if to_100:
        val = round(val * 100, precision)
    return f'{val:.{precision}f}%'
