from enum import Enum


class TypeAuth(Enum):
    """
    ============================================================================
     Types of Google Authentication.
    ============================================================================
    """

    SERVICE_ACCOUNT = 'SERVICE_ACCOUNT'
    OAUTH = 'OAUTH'


class Account(Enum):
    """
    ============================================================================
     Google Accounts with their Authentication Types.
    ============================================================================
    """

    RAMI = ('RAMI', TypeAuth.SERVICE_ACCOUNT)
    VALDAS = ('VALDAS', TypeAuth.OAUTH)

    def __init__(self, account: str, type_auth: TypeAuth) -> None:
        self._account = account
        self._type_auth = type_auth

    @property
    def account(self) -> str:
        """
        ====================================================================
         Return the Account name.
        ====================================================================
        """
        return self._account

    @property
    def type_auth(self) -> TypeAuth:
        """
        ====================================================================
         Return the Authentication Type.
        ====================================================================
        """
        return self._type_auth
