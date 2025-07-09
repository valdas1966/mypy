from .main import Google, ServiceAccount


def test_rami() -> None:
    """
    ========================================================================
     Tests the RAMI-Client.
    ========================================================================
    """
    client: Google = Google.Factory.rami()
    assert client.service_account == ServiceAccount.RAMI
    assert client.creds.project_id == 'noteret'
