from f_ds.groups.nested import NestedGroup
from f_abstract.mixins.excludable import Excludable
from f_proj.myq.gsheets.processes.nest_tuples_to_questions import ProcNestTuplesToQuestions
from f_proj.myq.questions.i_3_mask_one_word import (QuestionMaskOneWord as
                                                    Question)
from f_proj.myq.gsheets.i_0_base import SheetBase
from typing import Type


class SheetGroup(SheetBase, Excludable):
    """
    ============================================================================
     Abstract-Class for Questions-Sheet in Myq.
    ============================================================================
    """
    _ROW_FIRST = 5
    _COL_LABEL = 2
    _COL_VALUE = 3

    def __init__(self,
                 id_spread: str,
                 type_question: Type[Question] = Question,
                 exclude: set[str] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Excludable.__init__(self, exclude=exclude)
        SheetBase.__init__(self,
                           id_spread=id_spread,
                           type_question=type_question)
        self._sheet = self.spread[0]

    def to_nested_group(self) -> NestedGroup[Question]:
        """
        ========================================================================
         Return a NestedGroup of Questions (Group per Sub-Topic of the Sheet).
        ========================================================================
        """
        # Last Row in the Sheet (EOF)
        row_last = self._sheet.get_row_last(col=SheetGroup._COL_LABEL,
                                            row_first=SheetGroup._ROW_FIRST)
        # Convert all the filled range into Tuples (from first to last row)
        tuples = self._sheet.to_tuples(row_first=SheetGroup._ROW_FIRST,
                                       row_last=row_last,
                                       col_first=SheetGroup._COL_LABEL,
                                       col_last=SheetGroup._COL_VALUE)
        # Convert Tuples into Nested-Group and return the Result
        process = ProcNestTuplesToQuestions(type_question=self.type_question,
                                            exclude=self._exclude,
                                            rows=tuples)
        return process.run()
