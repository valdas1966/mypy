from f_core.mixins.generators.g_comparable import GenComparable, Item
import pytest


@pytest.fixture
def items() -> list[Item]:
    """
    ========================================================================
     Fixture providing a list of two comparable items.
    ========================================================================
    """
    return GenComparable.gen_list(length=2)  # [Item(1), Item(2)]


def test_equal(items: list[Item]) -> None:
    """
    ========================================================================
     Test that equal items compare correctly.
    ========================================================================
    """
    assert items[0] == items[0]
    assert items[0] != items[1]
    assert items[0] == Item(val=1)


def test_less_than(items: list[Item]) -> None:
    """
    ========================================================================
     Test that less than comparison works correctly.
    ========================================================================
    """
    assert items[0] < items[1]


def test_greater_than(items: list[Item]) -> None:
    """
    ========================================================================
     Test that greater than comparison works correctly. 
    ========================================================================
    """
    assert items[1] > items[0]


def test_less_equal(items: list[Item]) -> None:
    """
    ========================================================================
     Test that less than or equal comparison works correctly.
    ========================================================================
    """
    assert items[0] <= items[0]
    assert items[0] <= items[1]


def test_greater_equal(items: list[Item]) -> None:
    """
    ========================================================================
     Test that greater than or equal comparison works correctly.
    ========================================================================
    """
    assert items[0] >= items[0]
    assert items[1] >= items[0]
    