import collections


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


def update(d, key, val):
    """
    ============================================================================
     Description: Update Dictionary with new Key and Val.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. d : dict (Dictionary to Update).
        2. key : obj.
        3. val : obj.
    ============================================================================
     Return: dict (Updated Dictionary).
    ============================================================================
    """
    if key in d:
        d[key].append(val)
    else:
        d[key] = [val]
    return d


def union(dict_1, dict_2):
    """
    ============================================================================
     Description: Return Dict as Union of two Dicts (must have the same value
                    on the same key).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. dict_1 : dict
        2. dict_2 : dict
    ============================================================================
     Return: dict
    ============================================================================
    """
    assert type(dict_1) == dict
    assert type(dict_2) == dict
    left = dict_1.keys() - dict_2.keys()
    right = dict_2.keys() - dict_1.keys()
    intersect = set.intersection(set(dict_1.keys()), set(dict_2.keys()))
    d_union = dict()
    for key in left:
        d_union[key] = dict_1[key]
    for key in right:
        d_union[key] = dict_2[key]
    for key in intersect:
        assert dict_1[key] == dict_2[key]
        d_union[key] = dict_1[key]
    return d_union


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
