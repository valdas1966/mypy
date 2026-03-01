from f_google.auth import Auth, Credentials


def test_rami() -> None:
    """
    ========================================================================
     Test the RAMI Service Account.
    ========================================================================
    """
    creds: Credentials = Auth.Factory.rami()
    assert creds.project_id == 'noteret'
