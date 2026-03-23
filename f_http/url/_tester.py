from f_http.url import UUrl


def test_suffix_mp4() -> None:
    """
    ============================================================================
     Test suffix extraction from mime_type query param.
    ============================================================================
    """
    url = UUrl.Factory.mp4()
    assert UUrl.suffix(url=url) == 'mp4'


def test_suffix_mp3() -> None:
    """
    ============================================================================
     Test suffix extraction from path.
    ============================================================================
    """
    url = UUrl.Factory.mp3()
    assert UUrl.suffix(url=url) == 'mp3'


def test_suffix_jpeg() -> None:
    """
    ============================================================================
     Test suffix extraction from path with query params.
    ============================================================================
    """
    url = UUrl.Factory.jpeg()
    assert UUrl.suffix(url=url) == 'jpeg'


def test_suffix_none() -> None:
    """
    ============================================================================
     Test that None is returned when no suffix is found.
    ============================================================================
    """
    url = UUrl.Factory.no_suffix()
    assert UUrl.suffix(url=url) is None
