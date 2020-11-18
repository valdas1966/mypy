
def to_str(dt):
    """
    ============================================================================
     Description: Return Str-Representation of DateTime in format:
                    yyyymmddhhmiss
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. dt : DateTime
    ============================================================================
     Return: str
    ============================================================================
    """
    return (
            str(dt.year) +
            str(dt.month).zfill(2) +
            str(dt.day).zfill(2) +
            str(dt.hour).zfill(2) +
            str(dt.minute).zfill(2) +
            str(dt.second).zfill(2)
          )
