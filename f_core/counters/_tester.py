import pytest
from f_core.counters import Counters


def test_init_flat() -> None:
    """
    ========================================================================
     Test that flat names initialize all counters to 0.
    ========================================================================
    """
    c = Counters.Factory.flat()
    assert len(c) == 3
    assert c['cnt_a'] == 0
    assert c['cnt_b'] == 0
    assert c['cnt_c'] == 0


def test_init_grouped() -> None:
    """
    ========================================================================
     Test that grouped names flatten correctly.
    ========================================================================
    """
    c = Counters.Factory.grouped()
    assert len(c) == 8
    assert c['cnt_h_search'] == 0
    assert c['cnt_decrease'] == 0


def test_init_empty() -> None:
    """
    ========================================================================
     Test that an empty Counters has length 0.
    ========================================================================
    """
    c = Counters.Factory.empty()
    assert len(c) == 0
    assert repr(c) == 'Counters()'


def test_init_rejects_duplicates() -> None:
    """
    ========================================================================
     Test that duplicate names raise ValueError at init.
    ========================================================================
    """
    with pytest.raises(ValueError, match='duplicate'):
        Counters(names=('cnt_a', 'cnt_b', 'cnt_a'))


def test_inc() -> None:
    """
    ========================================================================
     Test inc() with default and explicit step.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a')
    c.inc('cnt_a')
    c.inc('cnt_b', n=5)
    assert c['cnt_a'] == 2
    assert c['cnt_b'] == 5
    assert c['cnt_c'] == 0


def test_inc_unknown_raises() -> None:
    """
    ========================================================================
     Test that inc() of an undeclared name raises KeyError.
    ========================================================================
    """
    c = Counters.Factory.flat()
    with pytest.raises(KeyError, match='unknown counter'):
        c.inc('cnt_nope')


def test_assign() -> None:
    """
    ========================================================================
     Test assign() overwrites with an absolute value.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=3)
    c.assign('cnt_a', 100)
    assert c['cnt_a'] == 100
    c.assign('cnt_b', 0)
    assert c['cnt_b'] == 0


def test_assign_unknown_raises() -> None:
    """
    ========================================================================
     Test that assign() of an undeclared name raises KeyError.
    ========================================================================
    """
    c = Counters.Factory.flat()
    with pytest.raises(KeyError, match='unknown counter'):
        c.assign('cnt_nope', 5)


def test_absorb_subset_all_present() -> None:
    """
    ========================================================================
     Test absorb() mirrors a name-subset from a source that
     declares all of them (priority-frontier case).
    ========================================================================
    """
    frontier = Counters.Factory.frontier_priority()
    frontier.inc('cnt_push', n=16)
    frontier.inc('cnt_pop', n=13)
    frontier.inc('cnt_decrease', n=4)
    algo = Counters.Factory.algo()
    algo.absorb(frontier,
                names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
    assert algo['cnt_push'] == 16
    assert algo['cnt_pop'] == 13
    assert algo['cnt_decrease'] == 4
    # Names outside the subset are untouched.
    assert algo['cnt_expanded'] == 0


def test_absorb_missing_source_name_uses_default() -> None:
    """
    ========================================================================
     Test absorb() synthesizes the structural 0 when the
     source lacks a name (FIFO-frontier case: no cnt_decrease).
    ========================================================================
    """
    frontier = Counters.Factory.frontier_fifo()
    frontier.inc('cnt_push', n=9)
    frontier.inc('cnt_pop', n=9)
    assert 'cnt_decrease' not in frontier
    algo = Counters.Factory.algo()
    algo.absorb(frontier,
                names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
    assert algo['cnt_push'] == 9
    assert algo['cnt_pop'] == 9
    assert algo['cnt_decrease'] == 0


def test_absorb_full_schema_when_names_none() -> None:
    """
    ========================================================================
     Test absorb() with names=None walks this Counters' full
     schema, filling source-absent names with default.
    ========================================================================
    """
    source = Counters(names=('cnt_push', 'cnt_pop'))
    source.inc('cnt_push', n=3)
    target = Counters(names=(
        'cnt_push', 'cnt_pop', 'cnt_decrease'))
    target.absorb(source, default=-1)
    assert target.as_dict() == {
        'cnt_push': 3, 'cnt_pop': 0, 'cnt_decrease': -1}


def test_absorb_overwrites_prior_values() -> None:
    """
    ========================================================================
     Test absorb() assigns absolute values, overwriting any
     prior counts in the target.
    ========================================================================
    """
    source = {'cnt_a': 5}
    target = Counters.Factory.flat()
    target.inc('cnt_a', n=99)
    target.absorb(source, names=('cnt_a',))
    assert target['cnt_a'] == 5


def test_absorb_from_plain_dict() -> None:
    """
    ========================================================================
     Test absorb() accepts any Mapping source, incl. a plain
     dict.
    ========================================================================
    """
    target = Counters.Factory.flat()
    target.absorb({'cnt_a': 7, 'cnt_b': 2})
    assert target.as_dict() == {
        'cnt_a': 7, 'cnt_b': 2, 'cnt_c': 0}


def test_absorb_unknown_target_raises() -> None:
    """
    ========================================================================
     Test absorb() of a name not declared in the target raises
     KeyError (typo guard, via assign).
    ========================================================================
    """
    target = Counters.Factory.flat()
    with pytest.raises(KeyError, match='unknown counter'):
        target.absorb({'cnt_nope': 1}, names=('cnt_nope',))


def test_reset() -> None:
    """
    ========================================================================
     Test reset() zeroes all counters.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=10)
    c.inc('cnt_b', n=20)
    c.reset()
    assert c['cnt_a'] == 0
    assert c['cnt_b'] == 0
    assert c['cnt_c'] == 0


def test_as_dict_is_copy() -> None:
    """
    ========================================================================
     Test as_dict() returns a copy.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=3)
    d = c.as_dict()
    assert d == {'cnt_a': 3, 'cnt_b': 0, 'cnt_c': 0}
    d['cnt_a'] = 999
    assert c['cnt_a'] == 3


def test_iter_in_declaration_order() -> None:
    """
    ========================================================================
     Test iteration follows declaration order, including
     across grouped construction.
    ========================================================================
    """
    c = Counters.Factory.grouped()
    expected = ['cnt_h_search', 'cnt_h_update',
                'cnt_phi_search', 'cnt_phi_update',
                'cnt_push', 'cnt_pop',
                'cnt_pop_stale', 'cnt_decrease']
    assert list(c) == expected
    assert list(c.keys()) == expected


def test_eq_with_dict() -> None:
    """
    ========================================================================
     Test equality against a plain dict (Mapping back-compat
     for existing test suites).
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=2)
    assert c == {'cnt_a': 2, 'cnt_b': 0, 'cnt_c': 0}
    assert c != {'cnt_a': 999, 'cnt_b': 0, 'cnt_c': 0}


def test_eq_with_counters() -> None:
    """
    ========================================================================
     Test equality between two Counters with the same values
     regardless of group structure.
    ========================================================================
    """
    c1 = Counters(names=('a', 'b'))
    c2 = Counters(names=(('a',), ('b',)))
    assert c1 == c2
    c1.inc('a', n=3)
    assert c1 != c2
    c2.inc('a', n=3)
    assert c1 == c2


def test_unhashable() -> None:
    """
    ========================================================================
     Test Counters is unhashable (mutable container).
    ========================================================================
    """
    c = Counters.Factory.flat()
    with pytest.raises(TypeError):
        hash(c)


def test_dict_constructor_interop() -> None:
    """
    ========================================================================
     Test dict(Counters) builds a plain dict from the
     Mapping protocol.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=7)
    assert dict(c) == {'cnt_a': 7, 'cnt_b': 0, 'cnt_c': 0}


def test_repr_flat() -> None:
    """
    ========================================================================
     Test __repr__ on a flat Counters: aligned columns,
     no blank lines.
    ========================================================================
    """
    c = Counters.Factory.flat()
    c.inc('cnt_a', n=5)
    text = repr(c)
    assert text.startswith('Counters(')
    assert text.endswith(')')
    # No blank lines (no groups).
    assert '\n\n' not in text
    # Each declared name appears exactly once.
    for name in ('cnt_a', 'cnt_b', 'cnt_c'):
        assert text.count(name) == 1


def test_repr_grouped_has_blank_lines() -> None:
    """
    ========================================================================
     Test __repr__ on a grouped Counters has a blank line
     between groups.
    ========================================================================
    """
    c = Counters.Factory.grouped()
    text = repr(c)
    # Three groups → two inter-group blank lines.
    assert text.count('\n\n') == 2
