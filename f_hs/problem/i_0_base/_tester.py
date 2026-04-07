import pytest
from f_hs.problem import ProblemSPP
from f_hs.state import StateBase


@pytest.fixture
def abc() -> ProblemSPP[StateBase[str]]:
    """
    ========================================================================
     Linear Graph: A -> B -> C.
    ========================================================================
    """
    return ProblemSPP.Factory.graph_abc()


def test_start(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the start convenience property.
    ========================================================================
    """
    assert abc.start.key == 'A'


def test_goal(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the goal convenience property.
    ========================================================================
    """
    assert abc.goal.key == 'C'


def test_starts(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the starts list.
    ========================================================================
    """
    assert len(abc.starts) == 1


def test_goals(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the goals list.
    ========================================================================
    """
    assert len(abc.goals) == 1


def test_successors(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the successors method.
    ========================================================================
    """
    children = abc.successors(abc.start)
    assert len(children) == 1
    assert children[0].key == 'B'


def test_key(abc: ProblemSPP[StateBase[str]]) -> None:
    """
    ========================================================================
     Test the key property.
    ========================================================================
    """
    expected = (tuple(abc.starts), tuple(abc.goals))
    assert abc.key == expected
