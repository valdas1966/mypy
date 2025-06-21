from f_http.responses.f_json import FactoryResponseJson


def test_ok() -> None:
    """
    ========================================================================
     Test the ok response.
    ========================================================================
    """
    response = FactoryResponseJson.ok()
    assert response
    assert response.status.code == 200
    assert response.status.name == 'OK'
    assert response.data == {'key': 'value'}
    assert response.elapsed == 0.1
    assert response.exception is None


def test_not_found() -> None:
    """
    ========================================================================
     Test the not found response.
    ========================================================================
    """
    response = FactoryResponseJson.not_found()
    assert not response
    assert response.status.code == 404
    assert response.status.name == 'NOT_FOUND'
    assert response.data is None
    assert response.elapsed == 0.1
    assert response.exception is None


def test_unknown() -> None:
    """
    ========================================================================
     Test the unknown response.
    ========================================================================
    """
    response = FactoryResponseJson.unknown()
    assert not response
    assert response.status.code is None
    assert response.status.name == 'UNKNOWN'
    assert response.data is None
    assert response.elapsed == 0.1
    assert response.exception == 'Unknown error'
