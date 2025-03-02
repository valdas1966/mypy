import json
import pandas as pd


class UJson:
    """
    ============================================================================
     Class for JSON-related utilities.
    ============================================================================
    """

    @staticmethod
    def to_dict(str_json: str) -> dict:
        """
        ========================================================================
         Convert JSON-Str into Dictionary.
        ========================================================================
        """
        return json.loads(str_json)

    @staticmethod
    def to_df(str_json: str = None,
              dict_json: dict = None) -> pd.DataFrame:
        """
        ========================================================================
         Convert Dict-JSON into DataFrame.
         * It works also on Nested-JSON and can return only Columns with
            specified Prefix.
        ========================================================================
        """
        if str_json is not None:
            dict_json = UJson.to_dict(str_json)
        return pd.json_normalize(dict_json, sep='_')
