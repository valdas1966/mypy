from datetime import datetime
from enum import Enum

"""
================================================================================
 Utils Module for InputRequest funcs.
================================================================================
"""


class Symbols(Enum):
    EXIT = '!exit'


def get(prompt: str,
        with_dt: bool = False)\
        -> str | tuple[str, datetime, datetime]:
    """
    ============================================================================
     1. Prints list Prompt to the User and Receives its Response.
     2. In addition to the Response, the function can return the date-times for
         when the Prompt was displayed and when the Response was received.
    ============================================================================
    """
    print(prompt)
    if not with_dt:
        return input()
    # with date-times
    dt_prompt = datetime.now()
    response = input()
    dt_response = datetime.now()
    return response, dt_prompt, dt_response
