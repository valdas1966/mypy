from f_hs.frontier.i_1_fifo import FrontierFIFO


def test_push_pop_fifo_order() -> None:
    """
    ========================================================================
     Test that pop returns States in insertion order.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    assert f.pop() == 'A'
    assert f.pop() == 'B'
    assert f.pop() == 'C'


def test_len() -> None:
    """
    ========================================================================
     Test __len__ returns the correct size.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    assert len(f) == 3
    f.pop()
    assert len(f) == 2


def test_bool() -> None:
    """
    ========================================================================
     Test __bool__ is False when empty, True when not.
    ========================================================================
    """
    f = FrontierFIFO.Factory.empty()
    assert not f
    f.push(state='X')
    assert f


def test_contains() -> None:
    """
    ========================================================================
     Test __contains__ reflects membership.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    assert 'A' in f
    assert 'Z' not in f
    f.pop()
    assert 'A' not in f


def test_clear() -> None:
    """
    ========================================================================
     Test clear empties the Frontier.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    f.clear()
    assert not f
    assert len(f) == 0
    assert 'A' not in f


def test_priority_ignored() -> None:
    """
    ========================================================================
     Test that push accepts but ignores a priority argument.
    ========================================================================
    """
    f = FrontierFIFO[str]()
    f.push(state='X', priority=99)
    f.push(state='Y', priority=1)
    assert f.pop() == 'X'
    assert f.pop() == 'Y'


def test_decrease_is_noop() -> None:
    """
    ========================================================================
     Test that decrease is a no-op on FrontierFIFO.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    f.decrease(state='C', priority=0)
    assert f.pop() == 'A'
    assert f.pop() == 'B'
    assert f.pop() == 'C'


def test_counters_inherited_from_base() -> None:
    """
    ========================================================================
     Test FrontierFIFO inherits the 3-counter scaffold from
     FrontierBase. Push and pop increment; decrease is a no-op
     and does NOT increment cnt_decrease.
    ========================================================================
    """
    f = FrontierFIFO[str]()
    assert dict(f.counters) == {
        'cnt_push': 0, 'cnt_pop': 0, 'cnt_decrease': 0}
    f.push(state='A')
    f.push(state='B')
    f.push(state='C')
    f.pop()
    f.pop()
    f.decrease(state='C', priority=0)
    assert f.counters['cnt_push'] == 3
    assert f.counters['cnt_pop'] == 2
    assert f.counters['cnt_decrease'] == 0


def test_counters_survive_clear() -> None:
    """
    ========================================================================
     Test counters accumulate across clear() — they reflect
     the run, not the heap state.
    ========================================================================
    """
    f = FrontierFIFO[str]()
    f.push(state='A')
    f.push(state='B')
    f.pop()
    f.clear()
    assert f.counters['cnt_push'] == 2
    assert f.counters['cnt_pop'] == 1
