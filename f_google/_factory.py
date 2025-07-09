from .main import Google, ServiceAccount


class Factory:
    """
    ========================================================================
     Factory for the Google-Client.
    ========================================================================
    """

    @staticmethod
    def rami() -> Google:
        """
        ========================================================================
         Returns the RAMI-Client.
        ========================================================================
        """
        return Google(service_account=ServiceAccount.RAMI)
