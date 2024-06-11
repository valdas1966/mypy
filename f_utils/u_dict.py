import collections
import json


def to_key_value_str(dic):
    """
    ============================================================================
     Description: Convert Dictionary into Key="Value" string.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. dic : dict
    ============================================================================
     Return: str ('key_1="value_1", key_2="value_2"')
    ============================================================================
    """
    li = list()
    for key, value in dic.items():
        li.append('{0}="{1}"'.format(key, value))
    return ', '.join(li)


def minus(dic_1, dic_2):
    """
    ===========================================================================
     Description: Difference of Dic_1 compared to Dic_2.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. dic_1 : dict
        2. dic_2 : dict
    ===========================================================================
     Return: dict : Difference of Dic_1 compared to Dic_2.
    ===========================================================================
    """
    dic_minus = dict()
    for key_1, value_1 in dic_1.items():
        if (key_1 not in dic_2) or (dic_2[key_1] != value_1):
            dic_minus[key_1] = value_1
    return dic_minus


def sum(dict_1, dict_2):
    """
    ============================================================================
     Description: Return Dict with sum of Values per each common key.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. dict_1 : dict
        2. dict_2 : dict
    ============================================================================
     Return: dict with sum of values.
    ============================================================================
    """
    dict_sum = dict()
    for key, value in dict_1.items():
        if key in dict_2.keys():
            dict_sum[key] = value + dict_2[key]
    return dict_sum


def union(d_1: dict, d_2: dict) -> dict:
    """
    ============================================================================
     Description: Return Union of two Dicts (on key-conflicts, d_1 is preferred)
    ============================================================================
    """
    d = dict(d_2)
    d.update(d_1)
    return d


def sort_by_value(d, reverse=False):
    """
    ============================================================================
     Description: Return Sorted Dictionary by Values.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. d : dict (Dictionary to Sort).
        2. reverse : bool (True if Descending-Sort).
    ============================================================================
     Return : dict (Sorted by Values).
    ============================================================================
    """
    s = sorted(d.items(), key=lambda kv: kv[1], reverse=reverse)
    return dict(collections.OrderedDict(s))


def filter_by_keys(d: dict, keys: 'sequence') -> dict:
    """
    ============================================================================
     Description: Return a new Dict with specified keys.
    ============================================================================
    """
    return {key: d[key] for key in keys}


def exclude_keys(d: dict, keys_to_exclude: list) -> dict:
    """
    ============================================================================
     Desc: Return a Dict without the Excluded-Keys.
    ============================================================================
    """
    d = d.copy()
    for key in keys_to_exclude:
        if key in d:
            del d[key]
    return d


def get_ordered_values(d: dict, keys_order: list) -> list:
    """
    ============================================================================
     Desc: Get Dict and List of Keys, and return List of Dict-Values
            in the order specified by the given List.
    ============================================================================
    """
    res = list()
    for key in keys_order:
        res.append(d.get(key))
    return res


def to_json_str(d: 'dict or list') -> str:
    return json.dumps(d)


def to_json_file(d: 'dict or list', path: str) -> None:
    with open(path, 'w') as file_json:
        json.dump(d, file_json)


def from_str_kv(str_kv: str,
                enclosure: str = '{}',
                delimiter: str = ', ',
                separator: str = '=',
                ) -> dict[str, str]:
    """
    ============================================================================
     Convert String with format '{k1=v1, k2=v2}' into Dict.
    ============================================================================
    """
    str_kv = str_kv.strip(enclosure)
    if not str_kv:
        return dict()
    pairs = str_kv.split(delimiter)
    return dict(pair.split(separator) for pair in pairs)
