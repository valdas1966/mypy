import pytest
from f_ds.graphs.nodes.i_1_path import NodePath


@pytest.fixture
def ex_root() -> NodePath:
    return NodePath()

@pytest.fixture
def ex_leaf(ex_root) -> NodePath:
    return NodePath(parent=ex_root)


def test_parent(ex_root, ex_leaf):
    assert not ex_root.parent
    assert ex_leaf.parent == ex_root

def test_path_from_root(ex_root, ex_leaf):
    assert ex_root.path_from_root() == [ex_root]
    assert ex_leaf.path_from_root() == [ex_root, ex_leaf]
