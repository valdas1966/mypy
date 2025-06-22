from f_http.client import Client


def test_valid() -> None:
    """
    ========================================================================
     Test the GET request with a valid response.
    ========================================================================
    """
    response = Client.Factory.valid()
    assert response
    assert response.status.code == 200
    assert response.status.name == 'OK'
    assert response.data


def test_invalid() -> None:
    """
    ========================================================================
     Test the GET request with an invalid response.
    ========================================================================
    """
    response = Client.Factory.invalid()
    assert not response
    assert response.status.code == 404
    assert response.status.name == 'NOT_FOUND'
    assert not response.data
