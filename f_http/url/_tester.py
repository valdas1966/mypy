from f_http.url import URL


def test_suffix() -> None:
    url_mp4 = URL.Factory.mp4()
    assert url_mp4.suffix() == 'mp4'
    url_mp3 = URL.Factory.mp3()
    assert url_mp3.suffix() == 'mp3'
    url_jpeg = URL.Factory.jpeg()
    assert url_jpeg.suffix() == 'jpeg'
