from typing import Union
from abc import ABC, abstractmethod
from google.cloud import bigquery, storage
from google.oauth2.service_account import Credentials
from f_google.auth.auth import Auth


# Define the Union of possible client types
GoogleClient = Union[bigquery.Client, storage.Client]


class ClientBase(ABC):
    """
    ============================================================================
     Abstract-Class for Google Clients.
    ============================================================================
    """

    def __init__(self, user: str = None) -> None:
        self._user = user
        self._creds = Auth.get_creds(user=user)
        self._client = self._get_client()

    @property
    def user(self) -> str:
        return self._user

    @property
    def creds(self) -> Credentials:
        return self._creds

    @abstractmethod
    def _get_client(self) -> GoogleClient:
        pass
