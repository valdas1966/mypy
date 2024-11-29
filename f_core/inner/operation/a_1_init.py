from f_core.runnable import Runnable
from f_core.tittable import Tittable
from f_core.loggable import Loggable


class OperationInit(Runnable, Tittable, Loggable):
    """
    ============================================================================
     Description: Multi-Inheritance from Runnable, Tittable and
                    Loggable classes (enriched with set_title funcs).
    ============================================================================
    """

    def _set_title(self) -> None:
        """
        ========================================================================
         Description: Set Operation-Title as Class-FileName.
        ========================================================================
        """
        self._title = self.__class__.__name__
