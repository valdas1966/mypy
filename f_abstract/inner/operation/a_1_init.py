from f_abstract.runnable import Runnable
from f_abstract.tittable import Tittable
from f_abstract.loggable import Loggable


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
