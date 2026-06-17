from typing import Iterable

from f_ds.clusters.i_0_base.main import Cluster


class _ClusterList(Cluster[int]):
    """
    ============================================================================
     Minimal concrete Cluster backed by a list of ints (test double).
    ============================================================================
    """

    def __init__(self,
                 items: Iterable[int],
                 name: str = 'C') -> None:
        """
        ========================================================================
         Store the items and init identity via the base.
        ========================================================================
        """
        Cluster.__init__(self, name=name)
        self._items: list[int] = list(items)

    def to_iterable(self) -> list[int]:
        """
        ========================================================================
         Return the underlying list of members.
        ========================================================================
        """
        return self._items

    @property
    def representative(self) -> int | None:
        """
        ========================================================================
         The representative is the minimum member (or None if empty).
        ========================================================================
        """
        return min(self._items) if self._items else None


def test_collectionable() -> None:
    """
    ========================================================================
     len / in / iter / bool come from Collectionable via to_iterable().
    ========================================================================
    """
    c = _ClusterList(items=[1, 2, 3])
    assert len(c) == 3
    assert 2 in c
    assert 9 not in c
    assert sorted(c) == [1, 2, 3]
    assert bool(c) is True
    assert bool(_ClusterList(items=[])) is False


def test_name() -> None:
    """
    ========================================================================
     The Cluster's identity (name) is exposed via HasName.
    ========================================================================
    """
    assert _ClusterList(items=[1], name='K').name == 'K'
    assert _ClusterList(items=[1]).name == 'C'


def test_members() -> None:
    """
    ========================================================================
     members returns a list copy of the underlying items.
    ========================================================================
    """
    c = _ClusterList(items=[1, 2, 3])
    members = c.members
    assert members == [1, 2, 3]
    # It is a copy: mutating it does not touch the Cluster.
    members.append(99)
    assert len(c) == 3


def test_representative_default() -> None:
    """
    ========================================================================
     Base default representative is None; subclass override is honoured.
    ========================================================================
    """
    class _Bare(Cluster[int]):
        def __init__(self) -> None:
            Cluster.__init__(self, name='B')
            self._items = [1, 2]

        def to_iterable(self) -> list[int]:
            return self._items

    assert _Bare().representative is None
    assert _ClusterList(items=[5, 2, 8]).representative == 2


def test_str_repr() -> None:
    """
    ========================================================================
     __str__ shows name + size; __repr__ adds the class name.
    ========================================================================
    """
    c = _ClusterList(items=[1, 2, 3], name='K')
    assert str(c) == 'K(size=3)'
    r = repr(c)
    assert r.startswith('<_ClusterList: ')
    assert 'name=K' in r
    assert 'size=3' in r
