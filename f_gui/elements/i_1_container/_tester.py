from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_0_element.main import Element
from f_ds.geometry.bounds import Bounds


def test_bounds() -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert Container.Factory.full().bounds.to_tuple() == (0, 0, 100, 100)


def test_children_empty() -> None:
    """
    ========================================================================
     Test that children list is empty by default.
    ========================================================================
    """
    assert Container.Factory.full().children == []


def test_add() -> None:
    """
    ========================================================================
     Test adding a child Element.
    ========================================================================
    """
    container = Container.Factory.full()
    child = Element(bounds=Bounds(top=10, left=10, bottom=50, right=50))
    container.add_child(child=child)
    assert len(container.children) == 1
    assert container.children[0] is child


def test_add_sets_parent() -> None:
    """
    ========================================================================
     Test that add_child() sets the child's parent.
    ========================================================================
    """
    container = Container.Factory.full()
    child = Element(bounds=Bounds(top=10, left=10, bottom=50, right=50))
    container.add_child(child=child)
    assert child.parent is container


def test_add_multiple() -> None:
    """
    ========================================================================
     Test adding multiple children.
    ========================================================================
    """
    container = Container.Factory.full()
    a = Element(bounds=Bounds(top=0, left=0, bottom=50, right=50))
    b = Element(bounds=Bounds(top=50, left=50, bottom=100, right=100))
    container.add_child(child=a)
    container.add_child(child=b)
    assert len(container.children) == 2


def test_remove_child() -> None:
    """
    ========================================================================
     Test removing a Child clears its Parent and drops it from children.
    ========================================================================
    """
    container = Container.Factory.full()
    child = Element(bounds=Bounds(top=0, left=0, bottom=10, right=10))
    container.add_child(child=child)
    container.remove_child(child=child)
    assert container.children == []
    assert child.parent is None


def test_reparent() -> None:
    """
    ========================================================================
     Test that adding a Child already owned by another Container detaches
     it from the old Parent automatically.
    ========================================================================
    """
    old = Container.Factory.full()
    new = Container.Factory.full()
    child = Element(bounds=Bounds(top=0, left=0, bottom=10, right=10))
    old.add_child(child=child)
    new.add_child(child=child)
    assert child.parent is new
    assert old.children == []
    assert new.children == [child]


def test_add_same_parent_is_noop() -> None:
    """
    ========================================================================
     Test that re-adding an already-owned child does not duplicate it.
    ========================================================================
    """
    container = Container.Factory.full()
    child = Element(bounds=Bounds(top=0, left=0, bottom=10, right=10))
    container.add_child(child=child)
    container.add_child(child=child)
    assert container.children == [child]


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Container.Factory.full()) == 'Container(0, 0, 100, 100)'
