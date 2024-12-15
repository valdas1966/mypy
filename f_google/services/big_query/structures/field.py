from __future__ import annotations
from google.cloud.bigquery import SchemaField
from f_core.mixins.has_name import HasName


class Field(HasName):
    """
    ============================================================================
     Field (Column) in BigQuery Table.
    ============================================================================
    """

    # Field-Types
    BOOLEAN = 'BOOLEAN'
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    DATETIME = 'DATETIME'

    def __init__(self, name: str, dtype: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._dtype = dtype

    def to_schema_field(self) -> SchemaField:
        return SchemaField(name=self.name, field_type=self.dtype)

    @property
    def dtype(self) -> str:
        return self._dtype

    def __str__(self) -> str:
        return f'{self.dtype}: {self.name}'

    @classmethod
    def boolean(cls, name: str) -> Field:
        return Field(name=name, dtype=Field.BOOLEAN)

    @classmethod
    def integer(cls, name: str) -> Field:
        return Field(name=name, dtype=Field.INTEGER)

    @classmethod
    def string(cls, name: str) -> Field:
        return Field(name=name, dtype=Field.STRING)

    @classmethod
    def datetime(cls, name: str) -> Field:
        return Field(name=name, dtype=Field.DATETIME)
