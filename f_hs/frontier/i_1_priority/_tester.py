from f_hs.frontier.i_1_priority import FrontierPriority


def test_push_pop_priority_order() -> None:
    """
    ========================================================================
     Test that pop returns States in priority order.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    assert f.pop() == 'B'
    assert f.pop() == 'C'
    assert f.pop() == 'A'


def test_len() -> None:
    """
    ========================================================================
     Test __len__ returns the correct size.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    assert len(f) == 3
    f.pop()
    assert len(f) == 2


def test_bool() -> None:
    """
    ========================================================================
     Test __bool__ is False when empty, True when not.
    ========================================================================
    """
    f = FrontierPriority.Factory.empty()
    assert not f
    f.push(state='X', priority=(1,))
    assert f


def test_contains() -> None:
    """
    ========================================================================
     Test __contains__ reflects membership.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    assert 'A' in f
    assert 'Z' not in f
    f.pop()
    assert 'B' not in f


def test_clear() -> None:
    """
    ========================================================================
     Test clear empties the Frontier.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    f.clear()
    assert not f
    assert len(f) == 0
    assert 'A' not in f


def test_decrease_reorders() -> None:
    """
    ========================================================================
     Test decrease updates the priority and reorders pop.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    f.decrease(state='A', priority=(0,))
    assert f.pop() == 'A'
    assert f.pop() == 'B'
    assert f.pop() == 'C'


def test_decrease_no_op_if_not_better() -> None:
    """
    ========================================================================
     Test decrease is a no-op when the new priority is worse.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    f.decrease(state='B', priority=(99,))
    assert f.pop() == 'B'
    assert f.pop() == 'C'
    assert f.pop() == 'A'


def test_push_existing_calls_decrease() -> None:
    """
    ========================================================================
     Test that push on an existing State decreases its key if better.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    f.push(state='A', priority=(0,))
    assert f.pop() == 'A'
    assert f.pop() == 'B'
    assert f.pop() == 'C'


def test_counters_push_pop_decrease() -> None:
    """
    ========================================================================
     Test counters tick on every push / pop / decrease call.
     Counts are by call-site: `push(existing_state)` increments
     `cnt_push` even though it routes internally to decrease_key.
    ========================================================================
    """
    f = FrontierPriority.Factory.empty()
    assert dict(f.counters) == {
        'cnt_push': 0, 'cnt_pop': 0, 'cnt_decrease': 0}
    f.push(state='A', priority=(3,))
    f.push(state='B', priority=(1,))
    f.push(state='C', priority=(2,))
    assert f.counters['cnt_push'] == 3
    f.decrease(state='A', priority=(0,))
    assert f.counters['cnt_decrease'] == 1
    f.pop()
    f.pop()
    assert f.counters['cnt_pop'] == 2
    # `push` of existing state still counts as cnt_push
    # (call-site naming, not internal-op naming).
    f.push(state='C', priority=(0,))
    assert f.counters['cnt_push'] == 4
    assert f.counters['cnt_decrease'] == 1


def test_counters_survive_clear() -> None:
    """
    ========================================================================
     Test clear() does NOT reset counters — they accumulate
     over the whole run, not over the heap state. Required for
     KAStarAgg._refresh_priorities and AlgoSPP.refresh_priorities,
     which clear-and-rebuild the frontier mid-run.
    ========================================================================
    """
    f = FrontierPriority.Factory.abc()
    f.pop()
    pre = dict(f.counters)
    f.clear()
    assert dict(f.counters) == pre


def test_tuple_priority_tiebreak() -> None:
    """
    ========================================================================
     Test tuple priorities are compared lexicographically.
    ========================================================================
    """
    f = FrontierPriority[str]()
    f.push(state='X', priority=(1, 5))
    f.push(state='Y', priority=(1, 2))
    f.push(state='Z', priority=(1, 9))
    assert f.pop() == 'Y'
    assert f.pop() == 'X'
    assert f.pop() == 'Z'
