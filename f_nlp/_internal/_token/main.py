from f_psl.re.u_re import URe

from f_nlp._internal._policy import _TOKEN_RANGES


class _Token:
    """
    ============================================================================
     Tokenization concern (private). Exposed via UNlp.tokenize.
    ============================================================================
    """

    @staticmethod
    def ize(text: str) -> list[str]:
        """
        ========================================================================
         Tokenize the given Text into Words, in order of occurrence.
         * Scope: English, Arabic and Hebrew only. Letters of any
            other script (Cyrillic, Greek, CJK, ...) are NOT matched —
            out-of-scope text yields no tokens, by design.
         * Diacritic-aware: Arabic harakat/tanwin/tatweel/Quranic marks
            and Hebrew niqqud/cantillation stay attached to their base
            letter, so vocalized/pointed text yields one token, not
            many. Hebrew maqaf/paseq/sof-pasuq/nun-hafukha stay
            delimiters.
         * Whitespace and punctuation delimit. Duplicates preserved.
         * Tokenization only — it does NOT normalize (no diacritic
            stripping, no alef/taa-marbuta unification); that is a
            separate concern (_Strip).
         * Owns only the policy (_TOKEN_RANGES); the regex mechanism
            is delegated to URe.extract_runs.
        ========================================================================
        """
        return URe.extract_runs(text=text, ranges=_TOKEN_RANGES)
