from f_http.client.inner.f_request import FactoryRequest


def test_valid() -> None:
    """
    ========================================================================
     Test the GET request with a valid response.
    ========================================================================
    """
    response = FactoryRequest.valid()
    assert response
    assert response.status == 200
    assert response.is_found
    assert response.data


def test_invalid() -> None:
    """
    ========================================================================
     Test the GET request with an invalid response.
    ========================================================================
    """
    response = FactoryRequest.invalid()
    assert response
    assert response.status == 404
    assert not response.is_found
    assert not response.data

