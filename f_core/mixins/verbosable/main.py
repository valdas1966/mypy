from f_utils import u_datetime
from enum import Enum

class Color(Enum):
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    UNDERLINE = "\033[4m"

    GRAY    = "\033[90m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

class Verbosable:
    """
    ============================================================================
     Mixin for objects with a verbose attribute.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 verbose: bool = True,
                 name: str = 'Verbosable') -> None:
        """
        ========================================================================
        Init private Attributes.
        ========================================================================
        """
        self._verbose = verbose
        self._name = name

    @property
    def verbose(self) -> bool:
        """
        ========================================================================
        Return the Verbose Attribute.
        ========================================================================
        """
        return self._verbose
    
    def print(self, msg: str) -> None:
        """
        ========================================================================
        Print a message if verbose is True.
        ========================================================================
        """
        if self.verbose:
            s = f'{Color.GREEN.value}[{u_datetime.now()[11:]}]'
            s += f' {Color.RED.value}[{self._name}]'
            s += f' {Color.RESET.value}{msg}'
            print(s)
