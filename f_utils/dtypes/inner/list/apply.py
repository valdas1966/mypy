
class Apply:
    """
    ============================================================================
     Utils-Class for List apply operations.
    ============================================================================
    """

    @staticmethod
    def except_last(li: list,
                    func: callable) -> list:
        """
        ========================================================================
         Apply a function to every item in the list, except for the last one.
        ========================================================================
        """
        if not li:
            return li
        return [func(item) for item in li[:-1]] + [li[-1]]
