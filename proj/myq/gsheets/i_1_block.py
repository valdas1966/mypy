from f_abstract.components.group import Listable
from proj.myq.questions.i_2_mask import QuestionMask
from proj.myq.gsheets.i_0_base import SheetBase
from typing import Type


class SheetBlock(SheetBase):
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

    def to_blocks(self) -> Listable[Listable[Type[QuestionMask]]]:
        """
        ========================================================================
         Return List of Questions extracted from the Questions-Sheet.
        ========================================================================
        """
        row = SheetBlock._ROW_FIRST
        blocks = Listable(name=self._sheet.title)
        block = None
        while not self._is_eof(row=row):
            if block:
                if self._is_title(row=row):
                    blocks.append(block)
                    name_block = self._get_block_name(row=row)
                    block = Listable(name=name_block)
                else:

                    block.append()
            if not block:
                name_block = self._get_block_name(row=row)
                block = Listable(name=name_block)
                continue


        return blocks

    def _is_eof(self, row: int) -> bool:
        return not self._sheet[row, SheetBlock._COL_LABEL]

    def _is_title(self, row: int) -> bool:
        return not self._sheet[row, SheetBlock._COL_LABEL]

    def _get_block_name(self, row: int) -> str:
        return self._sheet[row, SheetBlock._COL_LABEL].value


