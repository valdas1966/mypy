from f_abstract.inittable import Inittable


class Tittable(Inittable):
    """
    ============================================================================
     Description: Class with list Title (str).
    ============================================================================
    """

    def __init__(self, **kwargs):
        self._set_title()
        super().__init__(**kwargs)

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
