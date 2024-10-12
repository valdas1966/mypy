from f_ds.groups.nested import NestedGroup
from proj.myq.gsheets.inner.tuples_to_groups import TuplesToGroups
from proj.myq.questions.i_2_mask import QuestionMask
from proj.myq.gsheets.i_0_base import SheetBase, Question
from typing import Type


class SheetGroup(SheetBase[Question]):
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
                 type_question: Type[QuestionMask] = QuestionMask) -> None:
        SheetBase.__init__(self,
                           id_spread=id_spread,
                           type_question=type_question)
        self._sheet = self.spread[0]

    def to_groups(self) -> NestedGroup[Question]:
        row_last = self._sheet.get_row_last(col=SheetGroup._COL_LABEL,
                                            row_first=SheetGroup._ROW_FIRST)
        tuples = self._sheet.to_tuples(row_first=SheetGroup._ROW_FIRST,
                                       row_last=row_last,
                                       col_first=SheetGroup._COL_LABEL,
                                       col_last=SheetGroup._COL_VALUE)
        process = TuplesToGroups(type_question=self.type_question)
        return process.run(name=self._sheet.title, rows=tuples)

    def to_questions(self) -> list[Question]:
        qs = list()
        for group in self.to_groups():
            qs += group.data
        return qs
