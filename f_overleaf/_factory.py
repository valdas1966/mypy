import json
from pathlib import Path
import browsercookie
import pyoverleaf
from f_overleaf.main import OverLeaf


# Cookies JSON paths — first existing wins.
_PATHS_COOKIES = [
    Path('F:/jsons/valdas/overleaf.json'),
    Path('/mnt/f/jsons/valdas/overleaf.json'),
    Path.home() / 'prof' / 'valdas' / 'overleaf.json',
]


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
         Reads JSON from the first existing path of:
           - F:/jsons/valdas/overleaf.json        (Windows)
           - /mnt/f/jsons/valdas/overleaf.json    (WSL)
           - ~/prof/valdas/overleaf.json          (macOS / Linux)
        ====================================================================
        """
        path = next((p for p in _PATHS_COOKIES if p.exists()), None)
        if path is None:
            raise FileNotFoundError(
                f'No Overleaf cookies JSON found. Tried: '
                f'{[str(p) for p in _PATHS_COOKIES]}'
            )
        cookies = json.loads(path.read_text())
        api = pyoverleaf.Api()
        api.login_from_cookies(cookies=cookies)
        return OverLeaf(api=api)

    @staticmethod
    def firefox() -> OverLeaf:
        """
        ====================================================================
         Return an OverLeaf Client using Firefox's cookies.
        ====================================================================
        """
        cookies = browsercookie.firefox()
        api = pyoverleaf.Api()
        api.login_from_cookies(cookies=cookies)
        return OverLeaf(api=api)
