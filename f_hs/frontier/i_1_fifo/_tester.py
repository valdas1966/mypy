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


def test_no_decrease_op() -> None:
    """
    ========================================================================
     Test FrontierFIFO has no `decrease` operation at all — it
     is a priority-only op, absent on an insertion-order queue.
    ========================================================================
    """
    f = FrontierFIFO.Factory.abc()
    assert not hasattr(f, 'decrease')


def test_counters_inherited_from_base() -> None:
    """
    ========================================================================
     Test FrontierFIFO inherits the 2-counter scaffold
     (cnt_push, cnt_pop) from FrontierBase. It carries no
     cnt_decrease — FIFO has no decrease op.
    ========================================================================
    """
    f = FrontierFIFO[str]()
    assert dict(f.counters) == {'cnt_push': 0, 'cnt_pop': 0}
    assert 'cnt_decrease' not in dict(f.counters)
    f.push(state='A')
    f.push(state='B')
    f.push(state='C')
    f.pop()
    f.pop()
    assert f.counters['cnt_push'] == 3
    assert f.counters['cnt_pop'] == 2


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
