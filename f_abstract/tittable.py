from f_abstract.inittable import Inittable


class Tittable(Inittable):
    """
    ============================================================================
     Description: Class with a Title (str).
    ============================================================================
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_title()

    def _set_title(self, title: str = None) -> None:
        """
        ========================================================================
         Description: Set object's title.
        ========================================================================
        """
        self._title = None

    @property
    def title(self) -> bool:
        return self._title
