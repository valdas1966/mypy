from f_abstract.processes.rows_to_groups import RowsToGroups
from proj.myq.questions.i_2_mask import QuestionMask
from typing import Type, Sequence


class TuplesToGroups(RowsToGroups):

    def __init__(self,
                 type_question: Type[QuestionMask] = QuestionMask) -> None:
        RowsToGroups.__init__(self)
        self._type_question = type_question

    def _is_group_start(self, row: Sequence[str]) -> bool:
        return not row[1]

    def _extract_group_name(self, row: Sequence[str]) -> str:
        return row[0]

    def _create_item(self, row: Sequence[str]) -> QuestionMask:
        text = f'{self._group.name}: {row[0]}'
        return self._type_question(text=text, answer=row[1])
