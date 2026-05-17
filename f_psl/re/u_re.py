import re
from collections.abc import Iterable

from f_psl.re._ranges import compiled_class


class URe:
    """
    ============================================================================
     Class for Regex-related utilities.
    ============================================================================
    """

    @staticmethod
    def extract_words(text: str) -> list[str]:
        """
        ========================================================================
         Return a List of Words from the given Text, in the order of their
          occurrence.
         * A Word is a maximal sequence of word-characters ([A-Za-z0-9_]);
            any other character (space, comma, period, parenthesis, colon,
            newline, tab, etc.) acts as a delimiter.
         * Duplicates are preserved.
        ========================================================================
        """
        return re.findall(pattern=r'\w+', string=text)

    @staticmethod
    def extract_runs(text: str,
                     ranges: Iterable[tuple[int, int]]) -> list[str]:
        """
        ========================================================================
         Return all maximal Runs of in-range characters, in order.
         * ranges is an iterable of inclusive (lo, hi) code-point pairs;
            a character qualifies iff its code point lies in any range.
         * Any other character delimits. Duplicates are preserved.
         * Empty ranges -> []. Raises ValueError if any lo > hi.
         * The compiled pattern is cached per distinct ranges, so
            repeated calls with the same ranges do not recompile.
         * Endpoints that are class-special (] \\ ^ - [) are escaped,
            so arbitrary ranges are handled correctly.
        ========================================================================
        """
        norm = tuple((int(lo), int(hi)) for lo, hi in ranges)
        if not norm:
            return []
        return compiled_class(norm).findall(text)

    @staticmethod
    def strip_ranges(text: str,
                     ranges: Iterable[tuple[int, int]]) -> str:
        """
        ========================================================================
         Return text with every in-range character removed (the dual
          of extract_runs).
         * ranges is an iterable of inclusive (lo, hi) code-point pairs;
            a character is removed iff its code point lies in any range.
         * Empty ranges -> text unchanged. Raises ValueError if lo > hi.
         * Uses the same cached, class-safe compiled pattern as
            extract_runs.
        ========================================================================
        """
        norm = tuple((int(lo), int(hi)) for lo, hi in ranges)
        if not norm:
            return text
        return compiled_class(norm).sub('', text)
