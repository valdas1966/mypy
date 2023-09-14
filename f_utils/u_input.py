from datetime import datetime
from enum import Enum

"""
================================================================================
 Desc: Utils Module for Input functions.
================================================================================
"""


class Symbols(Enum):
    EXIT = '!exit'


def get(prompt: str,
        with_dt: bool = False)\
        -> str | tuple[str, datetime, datetime]:
    """
    ============================================================================
     Desc: Prints a Prompt to the User and receives its Response.
            In addition to the response, the function can return the date-times
             for when the prompt was displayed and when the response was
              received.
    ============================================================================
    """
    print(prompt)
    if not with_dt:
        return input()
    dt_start = datetime.now()
    response = input()
    dt_finish = datetime.now()
    return response, dt_start, dt_finish
