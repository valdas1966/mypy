from f_psl.re.u_re import URe
from f_psl.builtins.list.main import UList


# Tokenization policy (NOT regex): which code points count as
# word characters for English + Arabic + Hebrew. Written as
# integer (lo, hi) inclusive ranges — hand-typable on any
# keyboard, verifiable 1:1 against the Unicode charts. The regex
# mechanism lives entirely in URe (URe.extract_runs); this module
# only declares the policy and delegates.
#   0x0030-0x0039 0-9      0x0041-0x005A A-Z   0x005F _   a-z
#   Arabic : signs, letters+tatweel+harakat, Arabic-Indic digits,
#            superscript alef / alef wasla, Quranic marks
#   Hebrew : cantillation+niqqud, rafe, shin/sin dots, upper/
#            lower marks, qamats qatan, letters, ligatures
# Arabic ، ؟, Hebrew maqaf (0x05BE), paseq (0x05C0), sof pasuq
# (0x05C3) and nun hafukha (0x05C6) are punctuation and are
# deliberately excluded so they delimit.
_TOKEN_RANGES = (
    # --- English / ASCII ---
    (0x0030, 0x0039),   # 0-9
    (0x0041, 0x005A),   # A-Z
    (0x005F, 0x005F),   # _
    (0x0061, 0x007A),   # a-z
    # --- Arabic ---
    (0x0610, 0x061A),   # signs / honorific marks
    (0x0621, 0x065F),   # letters + tatweel + harakat/tanwin
    (0x0660, 0x0669),   # Arabic-Indic digits
    (0x0670, 0x0671),   # superscript alef, alef wasla
    (0x06D6, 0x06ED),   # Quranic annotation signs
    # --- Hebrew ---
    (0x0591, 0x05BD),   # cantillation + niqqud
    (0x05BF, 0x05BF),   # rafe
    (0x05C1, 0x05C2),   # shin / sin dots
    (0x05C4, 0x05C5),   # upper / lower marks
    (0x05C7, 0x05C7),   # qamats qatan
    (0x05D0, 0x05EA),   # letters
    (0x05EF, 0x05F2),   # yod-triangle + ligatures
)


# Optional marks (a strict subset of the *mark* portion of
# _TOKEN_RANGES — letters/digits excluded): the diacritics that
# strip_marks() removes so vocalized/pointed and plain spellings
# compare equal. Arabic alef-wasla (0x0671) is a LETTER and is
# deliberately NOT here (removing it would corrupt the word).
_MARK_RANGES = (
    # --- Arabic optional marks ---
    (0x0610, 0x061A),   # signs / honorific marks
    (0x0640, 0x0640),   # tatweel (kashida — elongation only)
    (0x064B, 0x065F),   # harakat + tanwin + extended marks
    (0x0670, 0x0670),   # superscript alef
    (0x06D6, 0x06ED),   # Quranic annotation signs
    # --- Hebrew optional marks ---
    (0x0591, 0x05BD),   # cantillation + niqqud (incl. dagesh)
    (0x05BF, 0x05BF),   # rafe
    (0x05C1, 0x05C2),   # shin / sin dots
    (0x05C4, 0x05C5),   # upper / lower marks
    (0x05C7, 0x05C7),   # qamats qatan
)


class UNlp:
    """
    ============================================================================
     Class for NLP-related utilities.
    ============================================================================
    """

    @staticmethod
    def tokenize(text: str) -> list[str]:
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
            separate concern.
         * This method owns only the policy (_TOKEN_RANGES); the regex
            mechanism is delegated to URe.extract_runs.
        ========================================================================
        """
        return URe.extract_runs(text=text, ranges=_TOKEN_RANGES)

    @staticmethod
    def strip_marks(s: str) -> str:
        """
        ========================================================================
         Return s with optional Arabic/Hebrew marks removed, so that
          vocalized/pointed and plain spellings compare equal.
         * Removes _MARK_RANGES (harakat, tanwin, tatweel, Quranic
            signs, Hebrew niqqud/te'amim/dagesh, shin/sin dots).
         * Base letters are kept — only the optional marks are
            dropped. The regex is delegated to URe.strip_ranges.
         * Use for diacritic-insensitive comparison, e.g.
            UNlp.strip_marks(a) == UNlp.strip_marks(b).
         * Idempotent. tokenize()/ngram() stay lossless — fold at the
            call site when equality is wanted.
        ========================================================================
        """
        return URe.strip_ranges(text=s, ranges=_MARK_RANGES)

    @staticmethod
    def ngram(text: str, n: int) -> list[list[str]]:
        """
        ========================================================================
         Return all N-Grams of the given Text, in order.
         * The Text is tokenized with UNlp.tokenize (English, Arabic
            and Hebrew).
         * Each N-Gram is the list of N consecutive Words; windowing is
            delegated to UList.sliding_windows.
         * For W words and window N (with N >= 1), returns W - N + 1
            N-Grams; returns [] when N > W.
         * Example: ngram(text='the cat sat', n=2) ->
            [['the', 'cat'], ['cat', 'sat']].
         * Raises ValueError when N < 1.
        ========================================================================
        """
        if n < 1:
            raise ValueError(f'n must be >= 1, got {n}')
        # Tokenize, then window — reuse existing utilities
        words = UNlp.tokenize(text=text)
        return UList.sliding_windows(li=words, size=n)
