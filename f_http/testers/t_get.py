from f_http.get import HttpGet


def test_success():
    http_get = HttpGet("https://api.example.com/data")
    assert http_get.response
    assert http_get.status() == 200
