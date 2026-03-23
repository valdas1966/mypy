from f_overleaf import OverLeaf
from f_overleaf.project import ProjectOverLeaf
import pytest


@pytest.fixture(scope='module')
def overleaf() -> OverLeaf:
    """
    ========================================================================
     Create an OverLeaf Client with Valdas session cookies.
    ========================================================================
    """
    return OverLeaf.Factory.valdas()


def test_len(overleaf: OverLeaf) -> None:
    """
    ========================================================================
     Test that OverLeaf contains at least one project.
    ========================================================================
    """
    assert len(overleaf) > 0


def test_getitem(overleaf: OverLeaf) -> None:
    """
    ========================================================================
     Test that getitem returns a ProjectOverLeaf.
    ========================================================================
    """
    name = overleaf.keys()[0]
    project = overleaf[name]
    assert isinstance(project, ProjectOverLeaf)
    assert project.name == name
