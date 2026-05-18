from f_psl.re.u_re import URe

from f_nlp._internal._policy import _MARK_RANGES


class _Strip:
    """
    ============================================================================
     Diacritic-stripping concern (private). Exposed via UNlp.strip
      (UNlp.strip.marks / UNlp.strip.diacritics).
    ============================================================================
    """

    @staticmethod
    def marks(s: str) -> str:
        """
        ========================================================================
         Return s with optional Arabic/Hebrew marks removed, so that
          vocalized/pointed and plain spellings compare equal.
         * Removes _MARK_RANGES (harakat, tanwin, tatweel, Quranic
            signs, Hebrew niqqud/te'amim/dagesh, shin/sin dots).
         * Base letters are kept — only the optional marks are
            dropped. The regex is delegated to URe.strip_ranges.
         * Use for diacritic-insensitive comparison, e.g.
            UNlp.strip.marks(a) == UNlp.strip.marks(b).
         * Idempotent. tokenize()/ngram stay lossless — fold at the
            call site when equality is wanted.
        ========================================================================
        """
        return URe.strip_ranges(text=s, ranges=_MARK_RANGES)

    @staticmethod
    def diacritics(text: str) -> str:
        """
        ========================================================================
         Return the Text with every optional Hebrew/Arabic
          diacritic removed, keeping only the base letters.
         * Discoverable alias of marks — same _MARK_RANGES policy,
            same URe.strip_ranges mechanism, no new logic.
         * Scope: all Hebrew (niqqud + te'amim/cantillation +
            dagesh + shin/sin dots) and all Arabic (harakat,
            tanwin, tatweel, Quranic signs). Base letters,
            including Arabic alef-wasla, are preserved.
         * Idempotent. Use when a caller wants clean consonantal
            text (not specifically an equality fold).
        ========================================================================
        """
        return _Strip.marks(s=text)
