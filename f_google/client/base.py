from typing import Union
from abc import ABC, abstractmethod
from google.cloud import bigquery, storage
from googleapiclient.discovery import Resource
from google.oauth2.service_account import Credentials
from f_google.utils.u_authentication import UAuthentication
import gspread


# Define the Union of possible client types
GoogleClient = Union[bigquery.Client, storage.Client, gspread.Client, Resource]


class ClientBase(ABC):
    """
    ============================================================================
     Abstract-Class for Google Clients.
    ============================================================================
    """

    def __init__(self, user: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._user = user
        self._creds = UAuthentication.get(user=user)
        self._client = self._get_client()

    @property
    def user(self) -> str:
        """
        ========================================================================
         Get User-Name.
        ========================================================================
        """
        return self._user

    @property
    def creds(self) -> Credentials:
        """
        ========================================================================
         Get User-Credentials.
        ========================================================================
        """
        return self._creds

    @property
    def client(self) -> GoogleClient:
        """
        ========================================================================
         Get Google-Client.
        ========================================================================
        """
        return self._client 
    
    @abstractmethod
    def _get_client(self) -> GoogleClient:
        """
        ========================================================================
         Open and Return new Google-Client.
        ========================================================================
        """
        pass
