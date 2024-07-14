from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
import json


class Json(Nameable):
    """
    ============================================================================
     JSON-File Manager.
    ============================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Init the Object with the given JSON-File path.
        ========================================================================
        """
        Nameable.__init__(self, name=path)

    @classmethod
    def from_data(cls,
                  path: str,
                  data: dict[str, str] | list[dict[str, str]]) -> Json:
        """
        ========================================================================
         Create a JSON-Object from given Data and save it to the given Path.
        ========================================================================
        """
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
        return Json(path=path)
