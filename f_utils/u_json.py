import json
import pandas as pd
from f_utils import u_inspect
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


def to_df(str_json: str = None,
          path_json: str = None,
          col_prefix: str = None) -> (pd.DataFrame, str):
    """
    ============================================================================
     Description: Convert JSON (Str or Path) into DataFrame.
                    It works also on Nested-JSON and can return only Columns
                    with specified Prefix.
                  1. If path_json is given: Read the JSON as Str-Representation.
                  2. Convert JSON Str into Dict-Representation.
                  3. Convert Dict into DataFrame-Representation.
    ============================================================================
    """
    if path_json:
        try:
            str_json = u_file.read(path_json)
        except Exception as e:
            msg = u_inspect.gen_msg(line='str_json = u_file.read(path_json)',
                                    value=f'path_json={path_json}', e=e)
            return None, msg
    try:
        d_json = json.loads(str_json)
    except Exception as e:
        msg = u_inspect.gen_msg(line='d_json = json.loads(str_json)',
                                value=f'str_json={str_json}', e=e)
        return None, msg
    try:
        df = pd.json_normalize(d_json, sep='_')
    except Exception as e:
        msg = u_inspect.gen_msg(line="df=json_normalize(d_json, sep='_'",
                                value=f'd_json={d_json}', e=e)
        return None, msg
    return df, None
