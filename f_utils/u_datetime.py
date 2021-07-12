from datetime import datetime


def now(format='yyyymmddhhmiss'):
    """
    ============================================================================
     Description: Return Str-Representation of Current-DateTime.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. format : str (Str-Representation Format).
    ============================================================================
     Return: str
    ============================================================================
    """
    return to_str(datetime.now(), format)


def to_str(dt, format='yyyymmddhhmiss'):
    """
    ============================================================================
     Description: Return Str-Representation of DateTime.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. dt : DateTime
        2. format : str
    ============================================================================
     Return: str
    ============================================================================
    """
    if format == 'yyyymmddhhmiss':
        return (
                str(dt.year) +
                str(dt.month).zfill(2) +
                str(dt.day).zfill(2) +
                str(dt.hour).zfill(2) +
                str(dt.minute).zfill(2) +
                str(dt.second).zfill(2)
              )
    elif format == 'yymmdd':
        return (
                str(dt.year)[:-2] +
                str(dt.month).zfill(2) +
                str(dt.day).zfill(2)
                )
