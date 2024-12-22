from f_core.mixins.has_uid import HasUID


def test_key_comparison():
    a = HasUID(uid='a')
    b = HasUID(uid='b')
    assert a < b
