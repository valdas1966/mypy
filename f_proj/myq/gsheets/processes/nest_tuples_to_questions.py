from f_abstract.processes.i_1_rows_to_groups import ProcRowsToNestedGroup
from f_proj.myq.questions.i_2_mask import QuestionMask
from typing import Type, Sequence


class ProcNestTuplesToQuestions(ProcRowsToNestedGroup):
    """
    ============================================================================
     Implementation of Abstract-Process RowsToGroups in context of GSheets.
    ----------------------------------------------------------------------------
     Convert Tuples from GSheet into NestedGroup[Question], when the Question
      is determined by the received Type.
    ============================================================================
    """

    def __init__(self,
                 type_question: Type[QuestionMask] = QuestionMask) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcRowsToNestedGroup.__init__(self)
        self._type_question = type_question

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

    def _create_item(self, row: Sequence[str]) -> QuestionMask:
        """
        ========================================================================
         Convert a GSheet-Row into a Question.
        ========================================================================
        """
        text = f'{self._group.name}: {row[0]}'
        return self._type_question(text=text, answer=row[1], pct_mask=75)
