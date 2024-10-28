import string

from f_proj.myq.questions.i_2_mask import QuestionMask
from f_abstract.mixins.excludable import Excludable
from f_utils.dtypes.u_str import UStr
from f_utils.dtypes.u_seq import USeq
from f_ai.nlp.u_nlp import UNLP


class QuestionMaskOneWord(QuestionMask, Excludable):
    """
    ============================================================================
     QuestionText with one random word Masked-Answer.
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 answer: str,
                 pct_mask: int = 100,
                 exclude: set[str] = None):
        """
        ========================================================================
         Init private Attributes.
        ------------------------------------------------------------------------
         Exclude is set of words to exclude of masking.
        ========================================================================
        """
        Excludable.__init__(self, exclude=exclude)
        QuestionMask.__init__(self,
                              text=text,
                              answer=answer,
                              pct_mask=pct_mask)

    def _set_private_attributes(self) -> None:
        """
        ========================================================================
         Return Masked-Answer.
        ========================================================================
        """
        words = self.answer.split()
        indexes_content = USeq.indexes.filter(seq=words,
                                              predicate=UNLP.is_content_word)
        indexes_filtered = USeq.items.filter(seq=indexes_content,
                                             predicate=self.should_remain)
        index_mask = USeq.items.sample(seq=indexes_filtered, size=1)[0]
        word_unmasked = words[index_mask]
        word_masked = UStr.mask.pct(s=word_unmasked,
                                    pct_mask=self.pct_mask,
                                    exceptions=string.punctuation)
        words[index_mask] = word_masked
        self._hint = ' '.join(words)
        self._answer = UStr.filter.punctuations(s=word_unmasked).lower()
