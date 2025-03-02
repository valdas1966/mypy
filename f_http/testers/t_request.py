from f_http.generators.g_request import GenRequest


def test_get_valid() -> None:
    """
    ========================================================================
     Test the GET request with a valid response.
    ========================================================================
    """
    response = GenRequest.get_valid()
    assert response
    assert response.status == 200
    assert response.is_found
    assert response.data


def test_get_invalid() -> None:
    """
    ========================================================================
     Test the GET request with an invalid response.
    ========================================================================
    """
    response = GenRequest.get_invalid()
    assert response
    assert response.status == 404
    assert not response.is_found
    assert not response.data

