from f_proj.rapid_api.tiktok.fetch.i_0_base import FetchBase
import pytest


@pytest.fixture
def row() -> dict:
    """
    ============================================================================
     Sample row before stamping.
    ============================================================================
    """
    return FetchBase.Factory.row()


@pytest.fixture
def anchor() -> tuple[str, str]:
    """
    ============================================================================
     Sample anchor tuple.
    ============================================================================
    """
    return FetchBase.Factory.anchor()


def test_stamp(row: dict) -> None:
    """
    ============================================================================
     Test that _stamp() adds is_ok=True and is_broken=False.
    ============================================================================
    """
    result = FetchBase._stamp(row)
    assert result['is_ok'] is True
    assert result['is_broken'] is False
    # Original fields preserved
    assert result['id_user'] == '123'
    assert result['nick'] == 'test_user'


def test_stamp_returns_same_dict(row: dict) -> None:
    """
    ============================================================================
     Test that _stamp() mutates and returns the same dict (not a copy).
    ============================================================================
    """
    result = FetchBase._stamp(row)
    assert result is row


def test_on_error(anchor: tuple[str, str]) -> None:
    """
    ============================================================================
     Test that _on_error() generates an invalid dict with status code.
    ============================================================================
    """
    status = FetchBase.Factory.status_error()
    result = FetchBase._on_error(status=status, anchor=anchor)
    assert result['status_code'] == 404
    assert result['is_ok'] is False
    assert result['id_user'] == '123'


def test_on_broken(anchor: tuple[str, str]) -> None:
    """
    ============================================================================
     Test that _on_broken() generates a broken dict with error message.
    ============================================================================
    """
    msg = FetchBase.Factory.msg()
    result = FetchBase._on_broken(msg=msg, anchor=anchor)
    assert result['is_ok'] is True
    assert result['is_broken'] is True
    assert result['msg'] == 'KeyError: user'
    assert result['id_user'] == '123'
