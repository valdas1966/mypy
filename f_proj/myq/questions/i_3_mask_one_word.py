import string
from f_proj.myq.questions.i_2_mask import QuestionMask
from f_core.mixins.excludable import Excludable
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
        def predicate(word: str) -> bool:
            return (not UNLP.is_stop_word(word=word) and
                    not self.should_exclude(item=word) and
                    not UStr.predicates.is_wrapped(s=word, wrap="'"))
        print(self._exclude)
        words = self.answer.split()
        print(words)
        indexes_filtered = USeq.indexes.filter(seq=words,
                                               predicate=predicate)
        print(indexes_filtered)
        index_mask = USeq.items.sample(seq=indexes_filtered, size=1)[0]
        print(index_mask)
        word_unmasked = words[index_mask]
        word_masked = UStr.mask.pct(s=word_unmasked,
                                    pct_mask=self.pct_mask,
                                    exceptions=string.punctuation)
        words[index_mask] = word_masked
        self._hint = ' '.join(words)
        self._answer = UStr.filter.punctuations(s=word_unmasked).lower()
