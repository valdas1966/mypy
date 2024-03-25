from f_abstract.managers.i_0_base import ManagerBase
from datetime import datetime
from f_utils import u_input


class ManagerInput(ManagerBase):
    """
    ============================================================================
     Manage the Prompt-Response Process.
    ============================================================================
    """

    _response:    str | None = None        # User Response
    _dt_prompt:   datetime | None = None   # Prompt DateTime
    _dt_response: datetime | None = None   # Response DateTime

    @classmethod
    def run(cls, prompt: str, with_dt: bool = False) -> None:
        """
        ========================================================================
         Run the Prompt-Response process.
        ========================================================================
        """
        ans = u_input.get(prompt=prompt, with_dt=with_dt)
        cls._response, cls._dt_prompt, cls._dt_response = ans

    @classmethod
    def _reset(cls) -> None:
        """
        ========================================================================
         Reset the Class-Variables.
        ========================================================================
        """
        cls._response = None
        cls._dt_prompt = None
        cls._dt_response = None
