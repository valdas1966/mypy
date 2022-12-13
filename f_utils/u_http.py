import http.client


def get(host: str,
        request: str,
        headers: set) -> str:
    """
    ============================================================================
     Description: Return Get-Request from HTTP-API.
    ============================================================================
    """
    conn = http.client.HTTPSConnection(host)
    conn.request('GET', request, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode('utf-8')
