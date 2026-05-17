import re
from functools import lru_cache


# Characters that are special inside a regex character class and
# must be escaped when used as a range endpoint.
_CLASS_SPECIAL = {']': r'\]', '\\': r'\\', '^': r'\^',
                  '-': r'\-', '[': r'\['}


def _cls(cp: int) -> str:
    """
    ============================================================================
     Class-safe single character for code point cp.
    ============================================================================
    """
    c = chr(cp)
    return _CLASS_SPECIAL.get(c, c)


@lru_cache(maxsize=None)
def compiled_class(ranges: tuple[tuple[int, int], ...]) -> 're.Pattern':
    """
    ============================================================================
     Compile [<ranges>]+ once per distinct ranges (cached).
    ============================================================================
     * ranges: tuple of inclusive (lo, hi) code-point pairs.
     * Class-special endpoints (] \\ ^ - [) are escaped, so
        arbitrary ranges compile correctly.
     * Raises ValueError if any lo > hi.
    ============================================================================
    """
    parts = []
    for lo, hi in ranges:
        if lo > hi:
            raise ValueError(f'range start {lo:#06x} > end {hi:#06x}')
        parts.append(_cls(lo) if lo == hi else f'{_cls(lo)}-{_cls(hi)}')
    return re.compile('[' + ''.join(parts) + ']+')
