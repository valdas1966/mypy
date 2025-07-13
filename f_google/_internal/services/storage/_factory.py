from .main import Storage, ServiceAccount


class Factory:
    """
    ============================================================================
     Factory for Google-Cloud-Storage.
    ============================================================================
    """

    @staticmethod
    def rami() -> Storage:
        """
        ========================================================================
         Get Storage instance authenticated with RAMI service account.
        ========================================================================
        """
        return Storage(ServiceAccount.RAMI)
