from collections.abc import Mapping

import pytest

from f_hs.solution import SolutionMOSPP, SolutionOMSPP, SolutionSPP


def _spp(cost: float) -> SolutionSPP:
    """
    ========================================================================
     Build a SolutionSPP with the given cost.
    ========================================================================
    """
    return SolutionSPP(cost=cost)


# ── SolutionOMSPP ─────────────────────────────────────────


def test_omspp_is_valid_when_non_empty() -> None:
    """
    ========================================================================
     SolutionOMSPP.is_valid ⇔ at least one per-goal entry.
    ========================================================================
    """
    sol = SolutionOMSPP({'g1': _spp(3.0)})
    assert bool(sol) is True


def test_omspp_is_invalid_when_empty() -> None:
    """
    ========================================================================
     Empty SolutionOMSPP is invalid (no goals attempted).
    ========================================================================
    """
    sol = SolutionOMSPP({})
    assert bool(sol) is False


def test_omspp_is_all_reached_true() -> None:
    """
    ========================================================================
     is_all_reached True iff every per-goal cost is finite.
    ========================================================================
    """
    sol = SolutionOMSPP({'g1': _spp(3.0), 'g2': _spp(7.0)})
    assert sol.is_all_reached is True


def test_omspp_is_all_reached_false_with_unreachable() -> None:
    """
    ========================================================================
     is_all_reached False if any per-goal cost is inf.
    ========================================================================
    """
    sol = SolutionOMSPP({'g1': _spp(3.0),
                         'g2': _spp(float('inf'))})
    assert bool(sol) is True               # non-empty
    assert sol.is_all_reached is False     # one unreachable


def test_omspp_mapping_protocol() -> None:
    """
    ========================================================================
     SolutionOMSPP behaves as a Mapping over the per-goal dict.
    ========================================================================
    """
    a, b = _spp(1.0), _spp(2.0)
    sol = SolutionOMSPP({'g1': a, 'g2': b})
    assert isinstance(sol, Mapping)
    assert len(sol) == 2
    assert set(sol) == {'g1', 'g2'}
    assert sol['g1'] is a
    assert dict(sol.items()) == {'g1': a, 'g2': b}
    assert 'g1' in sol


def test_omspp_costs_view() -> None:
    """
    ========================================================================
     costs returns the {goal: cost} view (inf preserved).
    ========================================================================
    """
    sol = SolutionOMSPP({'g1': _spp(1.0),
                         'g2': _spp(float('inf'))})
    assert sol.costs == {'g1': 1.0, 'g2': float('inf')}


def test_omspp_per_goal_alias() -> None:
    """
    ========================================================================
     per_goal exposes the underlying {goal: SolutionSPP} dict.
    ========================================================================
    """
    a = _spp(1.0)
    sol = SolutionOMSPP({'g1': a})
    assert sol.per_goal['g1'] is a


def test_omspp_eq_against_plain_dict() -> None:
    """
    ========================================================================
     Mapping equality against a plain dict (preserves the
     pre-existing OMSPP recording-test idiom
     `algo.counters == {...}`-style assertions; here:
     `sol == {goal: SolutionSPP}`).
    ========================================================================
    """
    a = _spp(1.0)
    sol = SolutionOMSPP({'g1': a})
    assert sol == {'g1': a}


# ── SolutionMOSPP ─────────────────────────────────────────


def test_mospp_is_valid_when_non_empty() -> None:
    """
    ========================================================================
     SolutionMOSPP.is_valid ⇔ at least one per-start entry.
    ========================================================================
    """
    sol = SolutionMOSPP({'s1': _spp(5.0)})
    assert bool(sol) is True


def test_mospp_is_all_reached_false_with_unreachable() -> None:
    """
    ========================================================================
     is_all_reached False if any per-start cost is inf.
    ========================================================================
    """
    sol = SolutionMOSPP({'s1': _spp(5.0),
                         's2': _spp(float('inf'))})
    assert sol.is_all_reached is False


def test_mospp_mapping_protocol() -> None:
    """
    ========================================================================
     SolutionMOSPP behaves as a Mapping over the per-start dict.
    ========================================================================
    """
    a, b = _spp(1.0), _spp(2.0)
    sol = SolutionMOSPP({'s1': a, 's2': b})
    assert isinstance(sol, Mapping)
    assert len(sol) == 2
    assert sol['s2'] is b


def test_mospp_per_start_alias() -> None:
    """
    ========================================================================
     per_start exposes the underlying {start: SolutionSPP} dict.
    ========================================================================
    """
    a = _spp(7.0)
    sol = SolutionMOSPP({'s1': a})
    assert sol.per_start['s1'] is a


def test_mospp_costs_view() -> None:
    """
    ========================================================================
     costs returns {start: cost}.
    ========================================================================
    """
    sol = SolutionMOSPP({'s1': _spp(1.0),
                         's2': _spp(2.0)})
    assert sol.costs == {'s1': 1.0, 's2': 2.0}


# ── Spine recursion (proxy for future SolutionMMSPP) ──────


def test_per_key_is_all_reached_recurses_into_nested() -> None:
    """
    ========================================================================
     The spine's `is_all_reached` recurses into nested per-key
     wrappers via their own `is_all_reached`. Demonstrated by
     wrapping a SolutionOMSPP that itself has an unreachable
     goal — the outer wrapper must report is_all_reached=False.
    ========================================================================
    """
    inner_all = SolutionOMSPP({'g1': _spp(1.0),
                               'g2': _spp(2.0)})
    inner_partial = SolutionOMSPP({'g1': _spp(1.0),
                                   'g2': _spp(float('inf'))})
    # Use SolutionMOSPP as a stand-in nested wrapper
    # whose Val happens to be a SolutionOMSPP (illegal at the
    # type level, fine at runtime — the spine logic is
    # type-erased and Mapping-based).
    nested_all = SolutionMOSPP({'s1': inner_all})
    nested_partial = SolutionMOSPP({'s1': inner_partial})
    assert nested_all.is_all_reached is True
    assert nested_partial.is_all_reached is False
