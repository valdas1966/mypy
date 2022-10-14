import json
import pandas as pd


def to_dict(str_json: str) -> dict:
    """
    ============================================================================
     Description: Convert JSON-Str into Dictionary.
    ============================================================================
    """
    return json.loads(str_json)


def to_df(dict_json: dict) -> pd.DataFrame:
    """
    ============================================================================
     Description: Convert Dict-JSON into DataFrame.
                    It works also on Nested-JSON and can return only Columns
                    with specified Prefix.
    ============================================================================
    """
    return pd.json_normalize(dict_json, sep='_')
