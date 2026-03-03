from google.oauth2.service_account import Credentials as SACredentials
from google.oauth2.credentials import Credentials as OAuthCredentials
from f_google.auth import Auth


def test_rami() -> None:
    """
    ========================================================================
     Test the RAMI Account (Service Account).
    ========================================================================
    """
    creds = Auth.Factory.rami()
    assert isinstance(creds, SACredentials)
    assert creds.project_id == 'noteret'


def test_valdas() -> None:
    """
    ========================================================================
     Test the VALDAS Account (OAuth).
    ========================================================================
    """
    creds = Auth.Factory.valdas()
    assert isinstance(creds, OAuthCredentials)
