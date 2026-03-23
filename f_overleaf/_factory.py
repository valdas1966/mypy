import json
from pathlib import Path
import pyoverleaf
from f_overleaf.main import OverLeaf


_PATH_COOKIES = Path('F:/jsons/valdas/overleaf.json')


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
