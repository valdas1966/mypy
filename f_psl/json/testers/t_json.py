from f_psl.json.generators.g_json import GenJson
from f_psl.json.u_json import UJson
import pandas as pd


def test_to_dict_simple() -> None:
    """
    ========================================================================
     Test the to_dict() method.
    ========================================================================
    """
    str_json = GenJson.simple()
    dict_true = {'is_ok': True, 'id_user': 123, 'name': 'John'}
    assert UJson.to_dict(str_json=str_json) == dict_true


def test_to_dict_nested() -> None:
    """
    ========================================================================
     Test the to_dict() method.
    ========================================================================
    """
    str_json = GenJson.nested() 
    dict_true = {'id_user': 123,
                 'data': [{'id_video': 456},
                          {'id_video': 789}]}
    assert UJson.to_dict(str_json=str_json) == dict_true


def test_to_df() -> None:
    """
    ========================================================================
     Test the to_df() method.
    ========================================================================
    """
    str_json = GenJson.nested()
    dict_json = UJson.to_dict(str_json) 
    dict_true = {'id_user': [123, 123], 'data_id_video': [456, 789]}
    df_true = pd.DataFrame(data=dict_true)
    assert UJson.to_df(dict_json=dict_json).equals(df_true)
