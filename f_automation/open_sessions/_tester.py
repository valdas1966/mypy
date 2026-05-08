import pytest

from f_automation.open_sessions.main import OpenSessions


def test_detect_os() -> None:
    """
    ============================================================================
     Test OS-Detection returns one of three known values.
    ============================================================================
    """
    assert OpenSessions._detect_os() in ('windows', 'mac', 'linux')


def test_open_empty_raises() -> None:
    """
    ============================================================================
     Test that opening with empty names raises ValueError.
    ============================================================================
    """
    opener = OpenSessions.Factory.a()
    with pytest.raises(ValueError):
        opener.open(names=[])


def test_invalid_name_raises() -> None:
    """
    ============================================================================
     Test that names with shell-special characters are rejected.
    ============================================================================
    """
    bad = ['foo;bar', 'foo bar', '$(rm -rf /)', '../etc',
           '', '-leading-dash', 'has"quote']
    for name in bad:
        with pytest.raises(ValueError):
            OpenSessions._validate_name(name=name)


def test_valid_name_passes() -> None:
    """
    ============================================================================
     Test that well-formed names pass validation.
    ============================================================================
    """
    good = ['automation', 'kids_math', 'inc-kastar',
            'a1b2_c3', '_private', 'A_B_C']
    for name in good:
        OpenSessions._validate_name(name=name)


def test_repr() -> None:
    """
    ============================================================================
     Test __repr__ surfaces the project path.
    ============================================================================
    """
    opener = OpenSessions.Factory.at(path_project='/tmp/proj')
    assert repr(opener) == "OpenSessions(path_project='/tmp/proj')"
