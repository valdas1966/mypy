from __future__ import annotations
from f_abstract.components.groups.group import Listable
from f_google.big_query.structures.field import Field
from google.cloud.bigquery import SchemaField


class Schema(Listable[Field]):
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    def __init__(self, data: list[Field] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Listable.__init__(self, data=data)

    def to_schema_fields(self) -> list[SchemaField]:
        """
        ========================================================================
         Return BigQuery format of list Schema.
        ========================================================================
        """
        return [field.to_schema_field() for field in self]
