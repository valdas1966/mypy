from datetime import datetime, timezone


def now(format='yyyy-mm-dd hh:mi:ss', is_utc: bool = False) -> str:
    """
    ============================================================================
     Description: Return Str-Repr of the Current-DateTime in a given Format.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. format : str (Str-Representation Format).
    ============================================================================
     Return: str
    ============================================================================
    """
    if not is_utc:
        dt = datetime.now()
    else:
        dt = datetime.now(timezone.utc)
    return to_str(dt=dt, format=format)


def to_str(dt: datetime, format: str = 'LOG') -> str:
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
    if format in {'LOG', 'yyyy-mm-dd hh:mi:ss'}:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif format in {'STD', 'dd\mm\yyyy hh:mi:ss'}:
        return dt.strftime('%d\%m\%Y %H:%M:%S')
    elif format in {'NUM', 'yyyymmddhhmiss'}:
        return dt.strftime('%Y%m%d%H%M%S')
    elif format == 'yymmdd':
        return (
                str(dt.year)[:-2] +
                str(dt.month).zfill(2) +
                str(dt.day).zfill(2)
                )
