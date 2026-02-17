from f_ds.old_groups import ProcRowsToNested, Input
from f_core.old_mixins.excludable import Excludable
from f_proj.myq.questions.i_3_mask_one_word import QuestionMaskOneWord as Question
from typing import Type, Sequence


class ProcNestTuplesToQuestions(ProcRowsToNested[Question]):
    """
    ============================================================================
     Implementation of Abstract-Process RowsToGroups in context of GSheets.
    ----------------------------------------------------------------------------
     Convert Tuples from GSheet into NestedGroup[Question], when the Question
      is determined by the received Type.
    ============================================================================
    """

    def __init__(self,
                 rows: Sequence[Sequence[str]],
                 type_question: Type[Question] = Question,
                 exclude: set[str] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._type_question = type_question
        Excludable.__init__(self, exclude=exclude)
        _input = Input(rows=rows)
        ProcRowsToNested.__init__(self, _input=_input)

    def _is_group_start(self, row: Sequence[str]) -> bool:
        """
        ========================================================================
         Return True if the Second-Col is Empty
          (Merged Cell of the Group-Title).
        ========================================================================
        """
        return not row[1]

    def _extract_group_name(self, row: Sequence[str]) -> str:
        """
        ========================================================================
         Return the first Value of the Row (Group-Name on merged cell).
        ========================================================================
        """
        return row[0]

    def _create_item(self, row: Sequence[str]) -> Question:
        """
        ========================================================================
         Convert a GSheet-Row into a Question.
        ========================================================================
        """
        text = f'{self._group.name}: {row[0]}'
        return self._type_question(text=text,
                                   answer=row[1],
                                   pct_mask=75,
                                   exclude=self._exclude)
