from f_search.ds.priority.i_3_gh_flags.main import PriorityGHFlags


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key_comparison() method.
    ========================================================================
    """
    priority_cached = PriorityGHFlags.Factory.cached()
    priority_bounded = PriorityGHFlags.Factory.bounded()
    priority_regular = PriorityGHFlags.Factory.regular()
    assert priority_cached < priority_bounded
    assert priority_bounded < priority_regular
