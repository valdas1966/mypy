from pydantic import Field, model_validator
from typing import Generic, List, TypeVar, ClassVar, Any
from f_psl.pydantic.mixins.flattenable import Flattenable

Data = TypeVar('Data', bound=Flattenable)


class DataList(Flattenable, Generic[Data]):
    """
    ============================================================================
     Data-Class for List-Data.
    ============================================================================
    """
    has_more: bool = Field(default=None)
    cursor: int = Field(default=None)
    rows: List[Data] = Field(...)

    rows_key: ClassVar[str] = None

    @model_validator(mode="before")
    def remap_rows(cls, values: dict) -> dict:
        """
        ========================================================================
         Remap the rows key to rows.
        ========================================================================
        """
        if cls.rows_key and cls.rows_key in values:
            values["rows"] = values.pop(cls.rows_key)
        return values
    
    def to_list(self) -> list[dict[str, Any]]:
        """
        ========================================================================
         Convert the DataList to a list of dictionaries.
        ========================================================================
        """
        rows: list[dict[str, Any]] = list()
        for r in self.rows:
            row = r.to_flat_dict()
            row['is_ok'] = True
            row['is_found'] = True
            row['is_broken'] = False
            rows.append(row)
        return rows
