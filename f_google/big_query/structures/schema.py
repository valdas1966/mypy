from __future__ import annotations
from f_abstract.mixins.iterable import Iterable, Item
from f_google.big_query.structures.field import Field
from google.cloud.bigquery import SchemaField


class Schema(Iterable[Field]):
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    def __init__(self) -> None:
        self._fields: list[Field] = list()

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return Schema's Fields.
        ========================================================================
        """
        return self._fields

    def append(self,
               field: Field = None,
               name: str = None,
               dtype: str = Field.STRING) -> None:
        """
        ========================================================================
         Append a given Field to the Schema.
        ========================================================================
        """
        if not field:
            field = Field(name=name, dtype=dtype)
        self._fields.append(field)

    def build(self) -> list[SchemaField]:
        """
        ========================================================================
         Return BigQuery format of list Schema.
        ========================================================================
        """
        return [field.to_schema_field() for field in self._fields]
