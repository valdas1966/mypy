from f_ds.pair.main import Pair


class Factory:

    @staticmethod
    def ab() -> Pair[str, str]:
        """
        ========================================================================
         Return the Pair ('a', 'b').
        ========================================================================
        """
        return Pair(first='a', second='b')

    @staticmethod
    def ba() -> Pair[str, str]:
        """
        ========================================================================
         Return the Pair ('b', 'a').
        ========================================================================
        """
        return Pair(first='b', second='a')
