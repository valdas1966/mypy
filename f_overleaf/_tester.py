from f_overleaf import Overleaf
import pytest


@pytest.fixture(scope='module')
def overleaf() -> Overleaf:
    """
    ========================================================================
     Create an Overleaf Client with Gmail browser cookies.
    ========================================================================
    """
    return Overleaf.Factory.gmail()


def test_projects(overleaf: Overleaf) -> None:
    """
    ========================================================================
     Test projects() returns a non-empty list of project names.
    ========================================================================
    """
    names = overleaf.projects()
    assert isinstance(names, list)
    assert len(names) > 0
    assert all(isinstance(n, str) for n in names)
