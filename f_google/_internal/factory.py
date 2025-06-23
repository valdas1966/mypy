from f_google.google import Google, ServiceAccount


class Factory:
    """
    ========================================================================
     Factory for the Google-Client.
    ========================================================================
    """

    @staticmethod
    def RAMI() -> Google:
        """
        ========================================================================
         Returns the RAMI-Client.
        ========================================================================
        """
        return Google(ServiceAccount.RAMI)
    
