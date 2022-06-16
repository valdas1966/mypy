import json
import pandas as pd
from f_ds import u_df


def to_dict(str_json: str) -> dict:
    """
    ============================================================================
     Description: Convert JSON-Str into Dictionary.
    ============================================================================
    """
    return json.loads(str_json)


def to_df(dict_json: dict,
          prefix: str = None) -> pd.DataFrame:
    """
    ============================================================================
     Description: Convert Dict-JSON into DataFrame.
                    It works also on Nested-JSON and can return only Columns
                    with specified Prefix.
    ============================================================================
    """
    df_json = pd.json_normalize(dict_json, sep='_')
    if prefix:
        df_json = u_df.select_cols_prefix(df_json, prefix,
                                          remain_prefix=False)
    return df_json
