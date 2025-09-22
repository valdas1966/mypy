from f_hs.ds.nodes.i_2_flags import NodeFlags


def test_key_comparison():
    """
    ========================================================================
     Test the key comparison.
    ========================================================================
    """
    a = NodeFlags.Factory.a()
    b = NodeFlags.Factory.b()
    c = NodeFlags.Factory.c()
    d = NodeFlags.Factory.d()
    e = NodeFlags.Factory.e()
    f = NodeFlags.Factory.f()
    assert a < b < c < d < e < f
    