
class GenJson:
    """
    ============================================================================
     Class for JSON-related utilities.
    ============================================================================
    """

    @staticmethod
    def simple() -> str:
        """
        ========================================================================
         Generate a simple JSON-String.
        ========================================================================
        """
        return '{"is_ok": true, "id_user": 123, "name": "John"}'

    @staticmethod
    def nested() -> str:
        """
        ========================================================================
         Generate a nested JSON-String.
        ========================================================================
        """
        return ('{"id_user": 123,'
                ' "data": [{"id_video": 456}, {"id_video": 789}]}')


from f_psl.json.u_json import UJson
str_json = GenJson.nested()
df_json = UJson.to_df(str_json=str_json)
print(df_json)
