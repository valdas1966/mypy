from f_psl.file.u_txt import UTxt
import pytest


@pytest.fixture
def path() -> str:
    """
    ========================================================================
     Path to the test file.
    ========================================================================
    """
    return 'd:\\temp\\test.txt'


@pytest.fixture
def lines() -> list[str]:
    """
    ========================================================================
     Lines of the test file.
    ========================================================================
    """
    return ["Hello", "World"]


def test_to_list(path: str, lines: list[str]) -> None:
    """
    ========================================================================
     Test the to_list() method.
    ========================================================================
    """
    UTxt.from_list(lines=lines, path=path)
    lines_test = UTxt.to_list(path=path)
    assert lines == lines_test
