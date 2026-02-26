import pytest
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_0_base.main import Element
from f_ds.geometry.bounds import Bounds


@pytest.fixture
def full() -> Container:
    """
    ========================================================================
     Create a full-size Container.
    ========================================================================
    """
    return Container.Factory.full()


def test_bounds(full: Container) -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert full.bounds.to_tuple() == (0, 0, 100, 100)


def test_children_empty(full: Container) -> None:
    """
    ========================================================================
     Test that children list is empty by default.
    ========================================================================
    """
    assert full.children == []


def test_add(full: Container) -> None:
    """
    ========================================================================
     Test adding a child Element.
    ========================================================================
    """
    bounds = Bounds(top=10, left=10, bottom=50, right=50)
    child = Element(bounds=bounds)
    full.add(child=child)
    assert len(full.children) == 1
    assert full.children[0] is child


def test_add_sets_parent(full: Container) -> None:
    """
    ========================================================================
     Test that add() sets the child's parent.
    ========================================================================
    """
    bounds = Bounds(top=10, left=10, bottom=50, right=50)
    child = Element(bounds=bounds)
    full.add(child=child)
    assert child.parent is full


def test_add_multiple(full: Container) -> None:
    """
    ========================================================================
     Test adding multiple children.
    ========================================================================
    """
    a = Element(bounds=Bounds(top=0, left=0, bottom=50, right=50))
    b = Element(bounds=Bounds(top=50, left=50, bottom=100, right=100))
    full.add(child=a)
    full.add(child=b)
    assert len(full.children) == 2


def test_str(full: Container) -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(full) == 'Container(0, 0, 100, 100)'
