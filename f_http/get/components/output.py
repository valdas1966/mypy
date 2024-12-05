import json
from requests import Response
from f_core.mixins.validatable import Validatable
from f_http.get.components.reasons import Reasons


class Output(Validatable):
    """
    ============================================================================
     Output of the Http Get-Request process.
    ============================================================================
    """

    def __init__(self,
                 response: Response,
                 reason: Reasons) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._response = response
        self._reason = reason
        Validatable.__init__(self, is_valid=bool(response))

    @property
    def reason(self) -> Reasons:
        return self._reason

    def to_text(self) -> str:
        """
        ========================================================================
         Convert response content to text.
        =======================================================================
        """
        return self._response.text if self._response else None

    def to_dict(self) -> dict:
        """
        ========================================================================
         Convert response content to dictionary.
        ========================================================================
        """
        text = self.to_text()
        return json.loads(s=text) if text else None

    def to_json(self, path: str) -> None:
        """
        ========================================================================
         Save response content to list JSON file.
        ========================================================================
        """
        data = self.to_dict()
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
