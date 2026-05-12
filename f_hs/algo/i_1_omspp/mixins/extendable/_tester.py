import pytest

from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.algo.i_1_omspp.mixins.extendable import (
    ExtendableOMSPP,
    is_extendable,
)


def test_kastarinc_is_extendable() -> None:
    """
    ========================================================================
     KAStarInc instances are flagged extendable.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    assert isinstance(algo, ExtendableOMSPP)
    assert is_extendable(algo)


def test_kastaragg_is_not_extendable() -> None:
    """
    ========================================================================
     KAStarAgg instances are NOT flagged extendable — the
     mixin deliberately stays off KAStarAgg until Φ-mode-gated
     extend semantics are designed.
    ========================================================================
    """
    algo = KAStarAgg.Factory.graph_abc_two_goals_min()
    assert not isinstance(algo, ExtendableOMSPP)
    assert not is_extendable(algo)
    assert not hasattr(algo, 'extend')


def test_is_extendable_on_non_algo() -> None:
    """
    ========================================================================
     `is_extendable` returns False on non-algo objects without
     raising.
    ========================================================================
    """
    assert not is_extendable(object())
    assert not is_extendable(None)
    assert not is_extendable([1, 2, 3])
