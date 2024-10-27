from typing import Iterable


class UFilter:
    """
    ============================================================================
     Utils-Class for Filtering bag of words.
    ============================================================================
    """

    _STOP_WORDS = {'a', 'the', 'and', 'or', 'in', 'into', 'on', 'of', 'to'}

    @staticmethod
    def stop_words(words: Iterable[str],
                   stop_words: Iterable[str] = None) -> set[str]:
        """
        ========================================================================
         Return a Set of Words excluding specified Stop-Words.
        ========================================================================
        """
        stop_words = stop_words or UFilter._STOP_WORDS
        return {word for word in words if word not in stop_words}

    @staticmethod
    def is_stop_word(word: str) -> bool:
        """
        ========================================================================
         Return True if the received Word is a Stop-Word.
        ========================================================================
        """
        return word in UFilter._STOP_WORDS

    @staticmethod
    def is_content_word(word: str) -> bool:
        """
        ========================================================================
         Return True if the received Word is a Content-Word.
        ========================================================================
        """
        return word not in UFilter._STOP_WORDS
