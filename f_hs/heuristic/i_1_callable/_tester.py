from f_hs.heuristic.i_1_callable import HCallable
from f_hs.state.i_0_base.main import StateBase


def test_calls_wrapped_fn() -> None:
    """
    ========================================================================
     HCallable delegates __call__ to the wrapped function.
    ========================================================================
    """
    h = HCallable.Factory.graph_abc()
    assert h(StateBase[str](key='A')) == 2.0
    assert h(StateBase[str](key='B')) == 1.0
    assert h(StateBase[str](key='C')) == 0.0


def test_unknown_key_falls_back() -> None:
    """
    ========================================================================
     HCallable's behavior on unknown keys is dictated by the
     wrapped fn. graph_abc's map returns 0.0 for unknown keys.
    ========================================================================
    """
    h = HCallable.Factory.graph_abc()
    assert h(StateBase[str](key='Z')) == 0.0


def test_inherits_hbase_defaults() -> None:
    """
    ========================================================================
     HCallable inherits is_perfect=False and suffix_next=None
     from HBase (no per-state perfection info).
    ========================================================================
    """
    h = HCallable.Factory.zero()
    s = StateBase[str](key='A')
    assert h.is_perfect(s) is False
    assert h.suffix_next(s) is None
