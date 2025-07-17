from f_google.auth import Auth, ServiceAccount
from abc import ABC


class BaseGoogleService:
    """
    ============================================================================
     Base class for all Google-Services Clients.
    ============================================================================
    """

    def __init__(self,
                 service_account: ServiceAccount = ServiceAccount.RAMI) -> None:
        """
        ========================================================================
         Initialize the Google-Service Client.
        ========================================================================
        """
        self._service_account = service_account
        self._creds = Auth.get_creds(account=service_account)
        self._client = None
        
    def __bool__(self) -> bool:
        """
        ========================================================================
         Check if the client is valid.
        ========================================================================
        """
        return bool(self._client)
    