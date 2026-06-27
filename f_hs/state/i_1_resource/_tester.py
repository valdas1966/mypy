from f_hs.state import StateResource, NodeResource
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


def test_node_and_resource() -> None:
    """
    ============================================================================
     Test node / resource are read off the key (NodeResource holds them).
    ============================================================================
    """
    key = NodeResource(node=Cell(row=1, col=2), resource=3)
    state = StateResource(key=key)

    assert state.key.node == Cell(row=1, col=2)
    assert state.key.resource == 3


def test_key() -> None:
    """
    ============================================================================
     Test StateResource key is its NodeResource (node, resource).
    ============================================================================
    """
    key = NodeResource(node=Cell(row=1, col=2), resource=3)
    state = StateResource(key=key)

    actual = state.key

    expected = NodeResource(node=Cell(row=1, col=2), resource=3)

    assert actual == expected


def test_eq() -> None:
    """
    ============================================================================
     Test two states with the same (node, resource) are equal.
    ============================================================================
    """
    cell = Cell(row=0, col=0)
    same = {StateResource(key=NodeResource(node=cell, resource=3)),
            StateResource(key=NodeResource(node=cell, resource=3))}

    actual = len(same)

    expected = 1

    assert actual == expected


def test_resource_in_identity() -> None:
    """
    ============================================================================
     Test the same node at two resource levels are distinct states (V×R).
    ============================================================================
    """
    cell = Cell(row=0, col=0)
    levels = {StateResource(key=NodeResource(node=cell, resource=3)),
              StateResource(key=NodeResource(node=cell, resource=0))}

    actual = len(levels)

    expected = 2

    assert actual == expected
