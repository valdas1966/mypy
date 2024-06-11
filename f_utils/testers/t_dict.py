from f_utils import u_dict


def test_from_str_kv():
    ex_0 = '{}'
    assert u_dict.from_str_kv(str_kv=ex_0) == dict()
    ex_1 = '{k1=v1}'
    assert u_dict.from_str_kv(str_kv=ex_1) == {'k1': 'v1'}
    ex_2 = '{k1=v1, k2=v2}'
    assert u_dict.from_str_kv(str_kv=ex_2) == {'k1': 'v1', 'k2': 'v2'}
