from f_core.mixins.tupleable import Tupleable


def test_to_tuple() -> None:
    """
    ========================================================================
     Test the to_tuple() method.
    ========================================================================
    """
    coord_12 = Tupleable.Factory.coord_12()
    coord_34 = Tupleable.Factory.coord_34()
    assert coord_12.to_tuple() == (1, 2)
    assert coord_34.to_tuple() == (3, 4)


def test_iter() -> None:
    """
    ========================================================================
     Test __iter__() — tuple unpacking and list().
    ========================================================================
    """
    coord_12 = Tupleable.Factory.coord_12()
    x, y = coord_12
    assert (x, y) == (1, 2)
    assert list(coord_12) == [1, 2]


def test_getitem() -> None:
    """
    ========================================================================
     Test __getitem__() — positional indexing.
    ========================================================================
    """
    coord_12 = Tupleable.Factory.coord_12()
    assert coord_12[0] == 1
    assert coord_12[1] == 2


def test_eq() -> None:
    """
    ========================================================================
     Test __eq__() — equality by the tuple.
    ========================================================================
    """
    coord_12 = Tupleable.Factory.coord_12()
    coord_34 = Tupleable.Factory.coord_34()
    assert coord_12 == coord_12
    assert coord_12 != coord_34


def test_repr() -> None:
    """
    ========================================================================
     Test __repr__() / __str__() — standardized via HasRepr.
    ========================================================================
    """
    coord_12 = Tupleable.Factory.coord_12()
    assert str(coord_12) == '(1, 2)'
    assert repr(coord_12) == '<Coord: (1, 2)>'
