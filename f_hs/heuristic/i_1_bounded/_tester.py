from f_hs.heuristic.i_1_bounded import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.state.i_0_base.main import StateBase


def test_call_hit_returns_max_of_base_and_bound() -> None:
    """
    ========================================================================
     On a bounded hit where bound > base, HBounded returns the
     bound (the tighter lower estimate).
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    assert h(StateBase[str](key='A')) == 2.0
    assert h(StateBase[str](key='B')) == 1.0


def test_call_hit_returns_base_when_bound_weaker() -> None:
    """
    ========================================================================
     max-combine: when base > bound, base wins on the bounded
     hit. Pins that HBounded NEVER degrades its base.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_weaker_than_base()
    assert h(StateBase[str](key='A')) == 2.0   # base=2, bound=1


def test_call_miss_delegates_to_base() -> None:
    """
    ========================================================================
     Off-bounds: HBounded delegates to the base callable.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    assert h(StateBase[str](key='C')) == 0.0   # miss; base(C)=0
    assert h(StateBase[str](key='Z')) == 0.0   # miss; base(Z)=0


def test_is_perfect_always_false() -> None:
    """
    ========================================================================
     Bounds are admissible, NOT perfect. is_perfect inherits the
     HBase default (False) for every state, including bounded
     ones — early-termination must not fire on a bounded hit.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    for k in ('A', 'B', 'C', 'Z'):
        assert h.is_perfect(StateBase[str](key=k)) is False


def test_suffix_next_always_none() -> None:
    """
    ========================================================================
     Bounds carry no path information. suffix_next inherits the
     HBase default (None) for every state.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    for k in ('A', 'B', 'C', 'Z'):
        assert h.suffix_next(StateBase[str](key=k)) is None


def test_is_bounded_true_when_bound_tightens() -> None:
    """
    ========================================================================
     is_bounded(state) is True iff bounds[state] is strictly
     greater than base(state). On `graph_abc_tight` (base=0,
     bounds={A:2, B:1}), A and B both have strict tightening.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    assert h.is_bounded(StateBase[str](key='A')) is True
    assert h.is_bounded(StateBase[str](key='B')) is True


def test_is_bounded_false_when_bound_weaker() -> None:
    """
    ========================================================================
     When bound < base, is_bounded returns False — the bound
     adds no new info (max picks base). Pins that is_bounded
     reflects EFFECTIVENESS, not mere membership in the dict.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_weaker_than_base()
    assert h.is_bounded(StateBase[str](key='A')) is False


def test_is_bounded_false_on_miss() -> None:
    """
    ========================================================================
     States not in the bounds dict return False.
    ========================================================================
    """
    h = HBounded.Factory.graph_abc_tight()
    assert h.is_bounded(StateBase[str](key='C')) is False
    assert h.is_bounded(StateBase[str](key='Z')) is False


def test_is_bounded_false_when_bound_equals_base() -> None:
    """
    ========================================================================
     Ties (bound == base) return False — the bound didn't
     TIGHTEN h beyond what the base provides. Strict semantics
     keep the flag unambiguous: is_bounded=True ⇔ bound won.
    ========================================================================
    """
    a = StateBase[str](key='A')
    h = HBounded(
        base=HCallable(fn=lambda s: 2.0),
        bounds={a: 2.0},
    )
    assert h.is_bounded(a) is False
    # But __call__ still returns the shared value.
    assert h(a) == 2.0


def test_add_bound_tightens_returns_true() -> None:
    """
    ========================================================================
     add_bound returns True and updates the internal bounds
     dict when value > current self(state). Verifies both the
     return and the post-state via __call__.
    ========================================================================
    """
    a = StateBase[str](key='A')
    h = HBounded(base=HCallable(fn=lambda s: 1.0), bounds={})
    assert h(a) == 1.0
    assert h.add_bound(state=a, value=3.0) is True
    assert h(a) == 3.0
    assert h.is_bounded(state=a) is True


def test_add_bound_no_op_when_not_tightening_returns_false() -> None:
    """
    ========================================================================
     add_bound returns False and does NOT mutate when value <=
     current self(state). Covers both tie and weaker.
    ========================================================================
    """
    a = StateBase[str](key='A')
    h = HBounded(base=HCallable(fn=lambda s: 2.0), bounds={a: 3.0})
    # h(a) = max(base=2, bound=3) = 3
    assert h.add_bound(state=a, value=3.0) is False  # tie
    assert h(a) == 3.0
    assert h.add_bound(state=a, value=2.5) is False  # weaker
    assert h(a) == 3.0


def test_constructor_takes_defensive_copy() -> None:
    """
    ========================================================================
     Mutating the source dict after construction does not affect
     HBounded's view — pins the static-bounds decision.
    ========================================================================
    """
    a = StateBase[str](key='A')
    src = {a: 2.0}
    h = HBounded(base=HCallable(fn=lambda s: 0.0), bounds=src)
    src.clear()
    assert h(a) == 2.0
