import json
import pandas as pd
from f_utils.u_inspect import emsg
from f_ds import u_df


def to_dict(str_json: str) -> dict:
    """
    ============================================================================
     Description: Convert JSON-Str into Dictionary.
    ============================================================================
    """
    try:
        return json.loads(str_json)
    except Exception as e:
        msg = emsg({'str_json': str_json})
        raise Exception(f'{msg}\n{e}')


def to_df(dict_json: dict,
          prefix: str = None) -> pd.DataFrame:
    """
    ============================================================================
     Description: Convert JSON (Str or Path) into DataFrame.
                    It works also on Nested-JSON and can return only Columns
                    with specified Prefix.
    ============================================================================
    """
    df_json = None
    try:
        df_json = pd.json_normalize(dict_json, sep='_')
        if prefix:
            df_json = u_df.select_cols_prefix(df_json, prefix,
                                              remain_prefix=False)
        return df_json
    except Exception as e:
        msg = emsg({'dict_json': dict_json, 'prefix': prefix,
                    'df_json': df_json})
        raise Exception(f'{msg}\n{e}')
