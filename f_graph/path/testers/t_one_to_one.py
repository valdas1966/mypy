from f_graph.path.one_to_one import PathOneToOne, NodePath
import pytest


@pytest.fixture
def node() -> NodePath:
    return NodePath()


@pytest.fixture
def path(node) -> PathOneToOne:
    return PathOneToOne(goal=node)


def test_is_found(path) -> None:
    assert not path
    path.set_valid()
    assert path


def test_get(path, node) -> None:
    assert path.get() == [node]
