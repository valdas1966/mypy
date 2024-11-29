from f_core.mixins.cursorable import Cursorable
from f_ds.groups.group import Group


class TokenizerSingle:
    """
    ============================================================================
     Convert a Text into a List of Tokens.
    ============================================================================
    """

    def __init__(self, text: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # List of Words in the text (separated by blank spaces)
        data = text.split(' ')
        # Cursorable object of text words
        self._words = Cursorable(data=data)

    @property
    def words(self) -> Cursorable:
        return self._words

    def to_tokens(self) -> Group[str]:
        """
        ========================================================================
         Convert the Text into a List of Tokens.
        ------------------------------------------------------------------------
         Iterates over each word in the text, processes it (if needed), and
          creates a token from the current word.
        ========================================================================
        """
        tokens = Group()
        while self._words.has_next():
            self._words.advance()
            token = self._create_token()
            tokens.append(token)
        return tokens

    def _create_token(self) -> str:
        """
        ========================================================================
         Create a Token from the current word.
        ========================================================================
        """
        return self._words.current()
