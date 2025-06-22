from f_http.status import Status


def test_200() -> None:
    """
    ========================================================================
     Test the 200 status.
    ========================================================================
    """
    status = Status.Factory.ok()
    assert status
    assert status.code == 200
    assert status.name == 'OK'
    assert str(status) == 'Code=200, Name=OK'
    assert repr(status) == '<Status: Code=200, Name=OK>'


def test_404() -> None:
    """
    ========================================================================
     Test the 404 status.
    ========================================================================
    """
    status = Status.Factory.not_found()
    assert not status
    assert status.code == 404
    assert status.name == 'NOT_FOUND'   
    assert str(status) == 'Code=404, Name=NOT_FOUND'
    assert repr(status) == '<Status: Code=404, Name=NOT_FOUND>'


def test_unknown() -> None:
    """
    ========================================================================
     Test the unknown status.
    ========================================================================
    """
    status = Status.Factory.none()
    assert not status
    assert status.code is None
    assert status.name == 'UNKNOWN' 
    assert str(status) == 'Code=None, Name=UNKNOWN'
    assert repr(status) == '<Status: Code=None, Name=UNKNOWN>'
    