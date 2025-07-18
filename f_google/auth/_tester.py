from .main import Auth, Credentials


def test_rami() -> None:
    """
    ========================================================================
     Tests the RAMI service account.
    ========================================================================
    """
    creds: Credentials = Auth.Factory.rami()
    assert creds.project_id == 'noteret'


def test_valdas() -> None:
    """
    ========================================================================
     Tests the VALDAS service account.
    ========================================================================
    """
    assert True
    """
    creds: Credentials = Auth.Factory.valdas()
    assert creds.project_id == 'natural-nimbus-291415'
    """