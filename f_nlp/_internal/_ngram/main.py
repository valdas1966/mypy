from collections import Counter

from f_psl.builtins.list.main import UList

from f_nlp._internal._token import _Token


class _Ngram:
    """
    ============================================================================
     N-Gram concern (private). Exposed via UNlp.ngram
      (UNlp.ngram.exact / UNlp.ngram.upto / UNlp.ngram.doc_freq).
    ============================================================================
    """

    @staticmethod
    def exact(text: str, n: int) -> list[list[str]]:
        """
        ========================================================================
         Return all N-Grams of the given Text, in order.
         * The Text is tokenized with _Token.ize (English, Arabic
            and Hebrew).
         * Each N-Gram is the list of N consecutive Words; windowing is
            delegated to UList.sliding_windows.
         * For W words and window N (with N >= 1), returns W - N + 1
            N-Grams; returns [] when N > W.
         * Example: exact(text='the cat sat', n=2) ->
            [['the', 'cat'], ['cat', 'sat']].
         * Raises ValueError when N < 1.
        ========================================================================
        """
        if n < 1:
            raise ValueError(f'n must be >= 1, got {n}')
        # Tokenize, then window — reuse existing utilities
        words = _Token.ize(text=text)
        return UList.sliding_windows(li=words, size=n)

    @staticmethod
    def upto(text: str, n: int) -> list[list[str]]:
        """
        ========================================================================
         Return every N-Gram of size 1..N (inclusive) of the Text.
         * Size-union of exact: the concatenation of exact(text, 1),
            exact(text, 2), ..., exact(text, N).
         * Grouped by size ascending — all 1-grams, then all
            2-grams, ..., then all N-grams; each group keeps word
            order. exact() stays the single-size primitive; this
            only composes it, so its length-N invariant is intact
            per group.
         * For W words: sum over k=1..min(N, W) of (W - k + 1)
            N-Grams; sizes k > W contribute nothing (graceful).
         * Example: upto(text='the cat sat', n=2) ->
            [['the'], ['cat'], ['sat'],
             ['the', 'cat'], ['cat', 'sat']].
         * Raises ValueError when N < 1.
        ========================================================================
        """
        if n < 1:
            raise ValueError(f'n must be >= 1, got {n}')
        # Tokenize once; union the windows over sizes 1..n
        words = _Token.ize(text=text)
        grams: list[list[str]] = []
        for size in range(1, n + 1):
            grams += UList.sliding_windows(li=words, size=size)
        return grams

    @staticmethod
    def doc_freq(texts: list[str],
                 n: int) -> Counter[tuple[str, ...]]:
        """
        ========================================================================
         Document frequency of N-Grams over a corpus of Texts.
         * For each N-Gram, counts how many of the input Texts
            contain it — NOT the total number of occurrences.
         * A repeat inside the same Text is counted once for that
            Text (per-Text presence, deduplicated).
         * Each N-Gram is keyed as a tuple[str, ...] (the hashable
            form of exact's list[str] window); the Counter value
            is the per-Text presence count.
         * Texts with fewer than N words contribute nothing.
            Empty corpus -> empty Counter.
         * Example: doc_freq(
              texts=['the cat sat', 'the cat ran'], n=2) ->
            Counter({('the','cat'): 2, ('cat','sat'): 1,
                     ('cat','ran'): 1}).
         * Raises ValueError when N < 1 (fail-fast, even for an
            empty corpus — mirrors exact).
        ========================================================================
        """
        if n < 1:
            raise ValueError(f'n must be >= 1, got {n}')
        doc_freq: Counter[tuple[str, ...]] = Counter()
        for text in texts:
            # Distinct N-Grams in THIS text (dedupe within text)
            seen = {tuple(g) for g in _Ngram.exact(text=text, n=n)}
            doc_freq.update(seen)
        return doc_freq
