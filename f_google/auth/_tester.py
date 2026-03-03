from google.oauth2.service_account import Credentials as SACredentials
from f_google.auth import Auth


def test_rami() -> None:
    """
    ========================================================================
     Test the RAMI Service-Account Credentials.
    ========================================================================
    """
    creds = Auth.Factory.rami()
    assert isinstance(creds, SACredentials)
    assert creds.project_id == 'noteret'
