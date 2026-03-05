from google.oauth2.service_account import Credentials as SACredentials


class Auth:
    """
    ============================================================================
     Static-Methods for Google Service-Account Authentication.
    ============================================================================
    """

    # Factory
    Factory: type = None

    @staticmethod
    def get_creds(path: str, scopes: list[str]) -> SACredentials:
        """
        ====================================================================
         Return Service-Account Credentials from a JSON key file.
        ====================================================================
        """
        return SACredentials.from_service_account_file(
            filename=path,
            scopes=scopes
        )
