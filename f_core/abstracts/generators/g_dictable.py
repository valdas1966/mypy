from f_core.abstracts.dictable import Dictable


class GenDictable:
    """
    ========================================================================
     Generator for Dictable objects.
    ========================================================================
    """

    @staticmethod
    def gen_empty() -> Dictable:
        """
        ========================================================================
         Generate an empty Dictable object.
        ========================================================================
        """
        return Dictable()
    
    @staticmethod
    def gen_arg() -> Dictable:
        """
        ========================================================================
         Generate a Dictable object with arguments.
        ========================================================================
        """
        d = {'a': 1, 'b': 2}
        return Dictable(d)
