from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataList(Flattenable):
    """
    ============================================================================
     Data-Class for List-Data.
    ============================================================================
    """

    has_more: bool = Field(default=None)
    cursor: int = Field(default=None)
    rows: list[Flattenable] = Field(..., alias=alias)
