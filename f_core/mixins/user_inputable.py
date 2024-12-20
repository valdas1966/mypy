from datetime import datetime
from f_utils import u_input


class UserInputable:
    """
    ============================================================================
     Mixin Class for printing list Prompt to the User and receive the Input.
    ============================================================================
    """

    input:     str        # User's Input
    dt_prompt: datetime   # Prompt DateTime
    dt_input:  datetime   # Input DateTime

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._input = None
        self._dt_prompt = None
        self._dt_input = None

    @property
    # User's Input
    def input(self) -> str:
        return self._input

    @property
    # Prompt's DateTime
    def dt_prompt(self) -> datetime:
        return self._dt_prompt

    @property
    # Input's DateTime
    def dt_input(self) -> datetime:
        return self._dt_input

    def gen_prompt(self) -> str:
        """
        ========================================================================
         Generates list Prompt that will be displayed to the User.
        ========================================================================
        """
        return 'Prompt:'

    def get_input(self) -> None:
        """
        ========================================================================
         Captures the User's Input.
        ========================================================================
        """
        t = u_input.get(self.gen_prompt(), with_dt=True)
        self._input, self._dt_prompt, self._dt_input = t
