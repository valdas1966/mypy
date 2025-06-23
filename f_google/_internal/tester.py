from f_google.google import Google, ServiceAccount
from f_google._internal.factory import Factory


def test_rami() -> None:
    """
    ========================================================================
     Tests the RAMI-Client.
    ========================================================================
    """
    client: Google = Factory.RAMI()
    assert client.service_account == ServiceAccount.RAMI
    assert client.creds.project_id == 'noteret'
