from f_color.rgb._colors import _CUSTOM


class ColorLog:
    """
    ============================================================================
     Wrap text with ANSI colors for dark-background console logging.
    ============================================================================
    """

    @staticmethod
    def _esc(name: str) -> str:
        """
        ========================================================================
         Return ANSI 24-bit foreground escape code for a _CUSTOM color.
        ========================================================================
        """
        r, g, b = _CUSTOM[name]
        return f'\033[38;2;{r};{g};{b}m'

    _RESET = '\033[0m'
    _LABEL = _esc('LOG_LABEL')
    _VALUE = _esc('LOG_VALUE')
    _TIME = _esc('LOG_TIME')
    _PATH = _esc('LOG_PATH')
    _WARN = _esc('LOG_WARN')
    _DIM = _esc('LOG_DIM')

    @staticmethod
    def label(text: object) -> str:
        """
        ========================================================================
         Wrap text in Label color (soft cyan).
        ========================================================================
        """
        return f'{ColorLog._LABEL}{text}{ColorLog._RESET}'

    @staticmethod
    def value(text: object) -> str:
        """
        ========================================================================
         Wrap text in Value color (light green).
        ========================================================================
        """
        return f'{ColorLog._VALUE}{text}{ColorLog._RESET}'

    @staticmethod
    def time(text: object) -> str:
        """
        ========================================================================
         Wrap text in Time color (warm amber).
        ========================================================================
        """
        return f'{ColorLog._TIME}{text}{ColorLog._RESET}'

    @staticmethod
    def path(text: object) -> str:
        """
        ========================================================================
         Wrap text in Path color (soft violet).
        ========================================================================
        """
        return f'{ColorLog._PATH}{text}{ColorLog._RESET}'

    @staticmethod
    def warn(text: object) -> str:
        """
        ========================================================================
         Wrap text in Warn color (coral red).
        ========================================================================
        """
        return f'{ColorLog._WARN}{text}{ColorLog._RESET}'

    @staticmethod
    def dim(text: object) -> str:
        """
        ========================================================================
         Wrap text in Dim color (gray).
        ========================================================================
        """
        return f'{ColorLog._DIM}{text}{ColorLog._RESET}'
