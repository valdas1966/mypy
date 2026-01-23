from f_search.ds.priority.i_1_g.main import PriorityG


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """
    priority_a = PriorityG.Factory.a()
    priority_b = PriorityG.Factory.b()
    assert priority_b < priority_a
    priority_c = PriorityG.Factory.c()
    assert priority_b < priority_c
