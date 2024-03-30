import os
from f_utils import u_json


def get(name_spread: str) -> str:
    """
    ============================================================================
     Receive a Name of the Myq-Spread and Return its Key.
    ============================================================================
    """
    path = os.environ.get('MYQ_JSON')
    return u_json.file_to_dict(path=path)[name_spread]
