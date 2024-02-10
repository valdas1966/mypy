from abc import ABC, abstractmethod
from google.oauth2.service_account import Credentials
from f_google.auth.auth import Auth


class ClientBase(ABC):
    """
    ============================================================================
     Abstract-Class for Google Clients.
    ============================================================================
    """

    def __init__(self, user: str = None) -> None:
        self._user = user
        self._creds = Auth.get_creds(user=user)
        self._client = self._open_client()

    @property
    def user(self) -> str:
        return self._user

    @property
    def creds(self) -> Credentials:
        return self._creds

    @abstractmethod
    def _open_client(self):
        """
        ========================================================================
         Open and Return a specific Google-Client.
        ========================================================================
        """
        pass
