import pytest
from f_core.mixins.has.children import HasChildren


@pytest.fixture
def empty() -> HasChildren:
    """
    ========================================================================
     Create a HasChildren with no children.
    ========================================================================
    """
    return HasChildren.Factory.empty()


@pytest.fixture
def with_two() -> HasChildren:
    """
    ========================================================================
     Create a HasChildren with two children.
    ========================================================================
    """
    return HasChildren.Factory.with_two()


def test_children_empty(empty: HasChildren) -> None:
    """
    ========================================================================
     Test that children list is empty by default.
    ========================================================================
    """
    assert empty.children == []


def test_children(with_two: HasChildren) -> None:
    """
    ========================================================================
     Test that children are accessible.
    ========================================================================
    """
    assert len(with_two.children) == 2


def test_add_child(empty: HasChildren) -> None:
    """
    ========================================================================
     Test adding a child.
    ========================================================================
    """
    child = HasChildren()
    empty.add_child(child=child)
    assert len(empty.children) == 1
    assert empty.children[0] is child
