import re

class Replace:
    """
    ============================================================================
     Utils-Class for STR replacements.
    ============================================================================
    """

    @staticmethod
    def by_dict(s: str, d: dict[str, str]) -> str:
        """
        ========================================================================
         Replace sub-strings by dict{what -> with}.
        ------------------------------------------------------------------------
         Ex: by_dict(s='ab bc', d={'ab': '12', 'bc': '23'}) -> '12 23'
        ========================================================================
        """
        for a, b in d.items():
            s = s.replace(a, b)
        return s

    @staticmethod
    def by_dict_with_spaces(s: str, d: dict[str, str]) -> str:
        """
        ========================================================================
         Replace sub-strings by dict{what -> with} with spaces around 'what'.
        ------------------------------------------------------------------------
         Ex: by_dict(s='aba', d={'a': 'x'}) -> 'aba'
        ========================================================================
        """
        for a, b in d.items():
            s = re.sub(rf'\b{re.escape(a)}\b', b, s)
        return s

