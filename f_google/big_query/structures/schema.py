from f_google.big_query.structures.field import Field
from google.cloud.bigquery import SchemaField


class Schema:
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    # Field-Types
    BOOLEAN = 'BOOLEAN'
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    DATETIME = 'DATETIME'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._fields = list()

    def add(self, name: str, dtype: str = STRING) -> None:
        """
        ========================================================================
         Add list Field to the Schema.
        ========================================================================
        """
        self._fields.append(Field(name=name, dt=dtype))

    def build(self) -> list[SchemaField]:
        """
        ========================================================================
         Return BigQuery format of list Schema.
        ========================================================================
        """
        return [SchemaField(name=field.name, field_type=field.dt)
                for field in self._fields]
