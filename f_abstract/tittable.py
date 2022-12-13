from f_abstract.inittable import Inittable


class Tittable(Inittable):

    # str : Object Title
    _title = None

    @property
    def title(self) -> bool:
        """
        ========================================================================
         Description: Return Object Title.
        ========================================================================
        """
        return self._title
