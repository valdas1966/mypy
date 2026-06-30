from f_psl.file import u_txt
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
    u_txt.from_list(lines=lines, path=path)
    lines_test = u_txt.to_list(path=path)
    assert lines == lines_test
