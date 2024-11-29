from f_core.mixins.id_auto_increment import MixinIdAutoIncrement


def test_id_autoincrement():
    a = MixinIdAutoIncrement()
    assert a.id == 1
    b = MixinIdAutoIncrement()
    assert b.id == 2
