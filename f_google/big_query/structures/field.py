from typing import NamedTuple


class Field(NamedTuple):
    """
    ============================================================================
     Field (Column) in BigQuery Table.
    ============================================================================
    """
    name: str
    dtype: str
