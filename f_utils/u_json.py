import json
from f_utils import u_file


def to_dict(str_json=str(), path_json=str()):
    """
    ============================================================================
     Description: Convert JSON-str into Dictionary.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1: str_json : str
    ============================================================================
     Return: dict
    ============================================================================
    """
    if path_json:
        str_json = u_file.read(path_json)
    return json.loads(str_json)
