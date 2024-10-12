from f_proj.myq.questions.i_2_mask import QuestionMask
from f_ai.nlp.tokenizers.i_1_join import TokenizerJoin
from f_utils.dtypes.u_str import UStr
from random import randint


class QuestionMaskOneToken(QuestionMask):

    def _set_private_attributes(self) -> None:
        """
        ========================================================================
         Set private Attributes.
        ========================================================================
        """
        tokens = TokenizerJoin(text=self.answer).to_tokens()
        index_masked = randint(0, len(tokens))
        token_masked = tokens[index_masked]
        self._answer = token_masked.lower()
        tokens[index_masked] = UStr.mask.full(token_masked)
        self._hint = ' '.join(tokens)
