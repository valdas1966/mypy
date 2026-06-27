from f_hs.state import StateResource as State
from f_hs.state import NodeResource
from f_ds.grids import CellMap as Cell


def test_to_tuple() -> None:
    """
    ============================================================================
     Test NodeResource.to_tuple() returns (node, resource).
    ============================================================================
    """
    node = NodeResource(node=Cell(row=1, col=2), resource=3)

    actual = node.to_tuple()

    expected = (Cell(row=1, col=2), 3)

    assert actual == expected


def test_node() -> None:
    """
    ============================================================================
     Test StateResource.node returns the underlying Cell.
    ============================================================================
    """
    state = State.Factory.at(row=1, col=2, resource=3)

    actual = state.node

    expected = Cell(row=1, col=2)

    assert actual == expected


def test_resource() -> None:
    """
    ============================================================================
     Test StateResource.resource returns the resource level.
    ============================================================================
    """
    state = State.Factory.at(row=1, col=2, resource=3)

    actual = state.resource

    expected = 3

    assert actual == expected


def test_key() -> None:
    """
    ============================================================================
     Test StateResource key is its NodeResource (node, resource).
    ============================================================================
    """
    state = State.Factory.at(row=1, col=2, resource=3)

    actual = state.key

    expected = NodeResource(node=Cell(row=1, col=2), resource=3)

    assert actual == expected


def test_eq() -> None:
    """
    ============================================================================
     Test two states with the same (node, resource) are equal.
    ============================================================================
    """
    same = {State.Factory.at(row=0, resource=3),
            State.Factory.at(row=0, resource=3)}

    actual = len(same)

    expected = 1

    assert actual == expected


def test_resource_in_identity() -> None:
    """
    ============================================================================
     Test the same node at two resource levels are distinct states (V×R).
    ============================================================================
    """
    levels = {State.Factory.at(row=0, resource=3),
              State.Factory.at(row=0, resource=0)}

    actual = len(levels)

    expected = 2

    assert actual == expected
