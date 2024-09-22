from __future__ import annotations
from f_google.big_query.structures.field import Field
from f_abstract.mixins.indexable import Indexable
from google.cloud.bigquery import SchemaField


class Schema(Indexable[Field]):
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Indexable.__init__(self)

    def add(self,
            field: Field = None,
            name: str = None,
            dtype: str = Field.STRING) -> None:
        """
        ========================================================================
         Add list Field to the Schema.
        ========================================================================
        """
        if not field:
            field = Field(name=name, dtype=dtype)
        self._items.append(field)

    def build(self) -> list[SchemaField]:
        """
        ========================================================================
         Return BigQuery format of list Schema.
        ========================================================================
        """
        return [field.to_schema_field() for field in self._items]

    def __add__(self, other: Schema) -> Schema:
        """
        ========================================================================
         Return a new Schema resulted by addition of self + current fields.
        ========================================================================
        """
        schema = Schema()
        for field in self:
            schema.add(field)
        for field in other:
            schema.add(field)
        return schema
