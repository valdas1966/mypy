from f_nlp._internal._token import _Token
from f_nlp._internal._strip import _Strip
from f_nlp._internal._ngram import _Ngram


class UNlp:
    """
    ============================================================================
     Class for NLP-related utilities.
    ----------------------------------------------------------------------------
     Single public facade. Per-concern logic lives in
     f_nlp/_internal/ and is reached through namespaces:
       * UNlp.tokenize(text)            — flat (single op)
       * UNlp.strip.marks(s)            — _Strip
       * UNlp.strip.diacritics(text)    — _Strip
       * UNlp.ngram.exact(text, n)      — _Ngram
       * UNlp.ngram.upto(text, n)       — _Ngram
       * UNlp.ngram.doc_freq(texts, n)  — _Ngram
     The regex mechanism stays in URe; _internal holds only the
     language policy and composition.
    ============================================================================
    """

    # Namespaced operation groups (see f_nlp/_internal/)
    strip: type = _Strip
    ngram: type = _Ngram

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """
        ========================================================================
         Tokenize the given Text into Words, in order of occurrence.
         * Scope: English, Arabic and Hebrew only — out-of-scope
            scripts (Cyrillic, Greek, CJK, ...) yield no tokens.
         * Diacritic-aware: Arabic harakat/tanwin/tatweel/Quranic
            and Hebrew niqqud/cantillation stay with the base
            letter. Whitespace/punctuation delimit; duplicates kept.
         * Tokenization only — no normalization (stripping is the
            separate UNlp.strip concern).
         * Thin facade over _Token.ize; policy in
            f_nlp/_internal/_policy, regex in URe.
        ========================================================================
        """
        return _Token.ize(text=text)
