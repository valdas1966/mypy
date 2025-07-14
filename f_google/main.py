from f_google.auth import Auth, Credentials, ServiceAccount


class Google:
    """
    ========================================================================
     Google-Client.
    ========================================================================
    """

    # Factory for the Google-Client.
    Factory: type = None

    def __init__(self,
                 service_account: ServiceAccount = ServiceAccount.RAMI) -> None:
        """
        ========================================================================
         Initializes the Google-Client.
        ========================================================================
        """
        self._service_account: ServiceAccount = service_account
        self._creds: Credentials = Auth.get_creds(self._service_account)

    @property
    def service_account(self) -> ServiceAccount:
        """
        ========================================================================
         Returns the ServiceAccount used by the client.
        ========================================================================
        """
        return self._service_account
    
    @property
    def creds(self) -> Credentials:
        """
        ========================================================================
         Returns the Credentials used by the client.
        ========================================================================
        """
        return self._creds
