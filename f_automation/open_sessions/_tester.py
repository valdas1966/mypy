import pytest

from f_automation.open_sessions.main import OpenSessions
from f_automation.open_sessions._backend_windows import _sq, open_windows


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


def test_sq_no_quotes() -> None:
    """
    ============================================================================
     Test _sq() wraps a quote-free string in single quotes only.
    ============================================================================
    """
    assert _sq('automation') == "'automation'"
    assert _sq('/mnt/f/mypy') == "'/mnt/f/mypy'"


def test_sq_escapes_inner_quote() -> None:
    """
    ============================================================================
     Test _sq() escapes embedded single quotes via the '\\'' idiom.
    ============================================================================
    """
    assert _sq("it's") == "'it'\\''s'"


def test_open_windows_emits_no_double_quote(monkeypatch) -> None:
    """
    ============================================================================
     Test the bash command argv has no `"` (chain-fragility regression).
    ============================================================================
    """
    captured: dict = {}

    def fake_popen(args: list[str], **_: object) -> None:
        captured['args'] = args

    monkeypatch.setattr(
        'f_automation.open_sessions._backend_windows.subprocess.Popen',
        fake_popen,
    )
    open_windows(names=['automation', 'kids_math'],
                 path_project='/mnt/f/mypy')
    args = captured['args']
    bash_cmds = [a for a in args if a.startswith('cd ')]
    assert len(bash_cmds) == 2
    for cmd in bash_cmds:
        assert '"' not in cmd, f'double-quote leaked into: {cmd!r}'


def test_open_windows_bash_cmd_shape(monkeypatch) -> None:
    """
    ============================================================================
     Test the bash command for one tab matches the expected form.
    ============================================================================
    """
    captured: dict = {}

    def fake_popen(args: list[str], **_: object) -> None:
        captured['args'] = args

    monkeypatch.setattr(
        'f_automation.open_sessions._backend_windows.subprocess.Popen',
        fake_popen,
    )
    open_windows(names=['automation'], path_project='/mnt/f/mypy')
    args = captured['args']
    expected = (
        "cd '/mnt/f/mypy' && claude "
        "'start session '\\''automation'\\'';'"
    )
    assert expected in args
