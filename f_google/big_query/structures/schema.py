from f_google.big_query.structures.field import Field
from google.cloud.bigquery import SchemaField


class Schema:
    """
    ============================================================================
     Schema of the BigQuery Table (Cols names and types).
    ============================================================================
    """

    # Field-Types
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    DATETIME = 'DATETIME'

    def __init__(self) -> None:
        self._fields = list()

    def add(self, name: str, dt: str) -> None:
        """
        ========================================================================
         Add a Field to the Schema.
        ========================================================================
        """
        self._fields.append(Field(name=name, dt=dt))

    def build(self) -> list[SchemaField]:
        """
        ========================================================================
         Return a BigQuery format of a Schema.
        ========================================================================
        """
        return [SchemaField(name=field.name, field_type=field.dt)
                for field in self._fields]
