import pyoverleaf
from f_overleaf.main import Overleaf


class Factory:
    """
    ========================================================================
     Factory for Overleaf Client.
    ========================================================================
    """

    @staticmethod
    def gmail() -> Overleaf:
        """
        ====================================================================
         Return an Overleaf Client using browser cookies (Gmail login).
        ====================================================================
        """
        api = pyoverleaf.Api()
        api.login_from_browser()
        return Overleaf(api=api)

    @staticmethod
    def token(cookies: dict[str, str]) -> Overleaf:
        """
        ====================================================================
         Return an Overleaf Client using provided session cookies.
        ====================================================================
        """
        api = pyoverleaf.Api()
        api.login_from_cookies(cookies=cookies)
        return Overleaf(api=api)
