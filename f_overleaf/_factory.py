import json
from pathlib import Path
import pyoverleaf
from f_overleaf.main import OverLeaf


_PATH_WIN = Path('F:/jsons/valdas/overleaf.json')
_PATH_WSL = Path('/mnt/f/jsons/valdas/overleaf.json')
_PATH_COOKIES = _PATH_WIN if _PATH_WIN.exists() else _PATH_WSL


class Factory:
    """
    ========================================================================
     Factory for OverLeaf Client.
    ========================================================================
    """

    @staticmethod
    def valdas() -> OverLeaf:
        """
        ====================================================================
         Return an OverLeaf Client using Valdas session cookies.
        ====================================================================
        """
        cookies = json.loads(_PATH_COOKIES.read_text())
        api = pyoverleaf.Api()
        api.login_from_cookies(cookies=cookies)
        return OverLeaf(api=api)
