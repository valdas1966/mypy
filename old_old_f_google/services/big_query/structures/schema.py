from __future__ import annotations
from f_ds.groups.main import Group
from old_old_f_google.services.big_query.structures.field import Field
from google.cloud.bigquery import SchemaField


class Schema(Group[Field]):
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    def __init__(self,
                 name: str,
                 data: list[Field] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Group.__init__(self, name=name, data=data)

    def to_schema_fields(self) -> list[SchemaField]:
        """
        ========================================================================
         Return BigQuery format of list Schema.
        ========================================================================
        """
        return [field.to_schema_field() for field in self]
