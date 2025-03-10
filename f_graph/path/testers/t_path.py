from f_graph.path.generators.g_path import GenPath, Path
from f_graph.path.generators.g_node import GenNode, Node
import pytest


@pytest.fixture
def path() -> Path:
    """
    ========================================================================
     Get the path.
    ========================================================================
    """
    return GenPath.gen_first_row_3x3()


@pytest.fixture
def nodes() -> list[Node]:
    """
    ========================================================================
     Get the nodes.
    ========================================================================
    """ 
    return list(GenNode.gen_first_row_3x3())


def test_nodes(path: Path, nodes: list[Node]) -> None:
    """
    ========================================================================
     Test the nodes.
    ========================================================================
    """
    assert path == nodes


def test_start(path: Path, nodes: list[Node]) -> None:
    """
    ========================================================================
     Test the start node.
    ========================================================================
    """
    assert path.start == nodes[0]


def test_goal(path: Path, nodes: list[Node]) -> None:
    """
    ========================================================================
     Test the goal node.
    ========================================================================
    """
    assert path.goal == nodes[-1]


def test_extend(path: Path, nodes: list[Node]) -> None:
    """
    ========================================================================
     Test the extend method.
    ========================================================================
    """
    path.extend(other=path)
    assert path == nodes * 2
    path = path[:1]
    path.extend(other=path.copy())
    assert path == [path[0]]


def test_add() -> None:
    """
    ========================================================================
     Test the add method.
    ========================================================================
    """
    path_1 = GenPath.gen_first_row_3x3()
    path_2 = GenPath.last_col_3x3()
    assert len(path_1 + path_2) == 5


def test_getitem(path: Path) -> None:
    """
    ========================================================================
     Test the getitem method.
    ========================================================================
    """
    assert path[0] == path.start
    assert path[:1] == [path.start]
    assert isinstance(path[:1], Path)


def test_reversed(path: Path, nodes: list[Node]) -> None:
    """
    ========================================================================
     Test the reversed method.
    ========================================================================
    """
    assert reversed(path) == list(reversed(nodes))


def test_str(path: Path) -> None:
    """
    ========================================================================
     Test the string representation of the path.
    ========================================================================
    """
    assert str(path) == '[(0, 0) -> (0, 1) -> (0, 2)]'


def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key comparison of the path.
    ========================================================================
    """
    path_1 = GenPath.gen_first_row_3x3()
    path_2 = GenPath.gen_first_row_3x3()
    assert path_1 == path_2
