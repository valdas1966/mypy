from f_http.old import HttpGet


def test_success():
    http_get = HttpGet("https://api.example.com/data")
    assert http_get.response
    assert http_get.status() == 200
