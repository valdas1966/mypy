from google.oauth2.credentials import Credentials as OAuthCredentials
from f_google.creds.oauth import OAuth


def test_valdas() -> None:
    """
    ========================================================================
     Test the VALDAS OAuth Credentials.
    ========================================================================
    """
    creds = OAuth.Factory.valdas()
    assert isinstance(creds, OAuthCredentials)
