from f_search.ds.cost import Cost


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """
    cost_a = Cost.Factory.a()
    cost_b = Cost.Factory.b()
    cost_c = Cost.Factory.c()
    cost_d = Cost.Factory.d()
    cost_e = Cost.Factory.e()
    assert cost_a < cost_b < cost_c < cost_d < cost_e
