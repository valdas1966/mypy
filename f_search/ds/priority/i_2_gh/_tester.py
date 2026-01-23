from f_search.ds.priority.i_2_gh.main import PriorityGH


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """
    priority_a = PriorityGH.Factory.a()
    priority_b = PriorityGH.Factory.b()
    assert priority_b < priority_a
    priority_c = PriorityGH.Factory.c()
    assert priority_a < priority_c
    