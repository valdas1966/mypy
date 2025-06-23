from f_google._internal.auth import Auth, Credentials, ServiceAccount


class Factory:
    """
    ============================================================================
     Factory for the Google Authentication process.
    ============================================================================
    """

    @staticmethod
    def rami() -> Credentials:
        """
        ========================================================================
         Returns the credentials for the RAMI service account.
        ========================================================================
        """
        account = ServiceAccount.RAMI   
        return Auth.get_creds(account)
    
    @staticmethod
    def valdas() -> Credentials:
        """
        ========================================================================
         Returns the credentials for the VALDAS service account.
        ========================================================================
        """
        account = ServiceAccount.VALDAS
        return Auth.get_creds(account)
