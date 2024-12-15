from f_google.services.big_query.structures.schema import Schema, Field


class SchemaPartial(Schema[Field]):
    """
    ============================================================================
     Partial-Schema (part of the table).
    ============================================================================
    """

    def __init__(self, name: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Schema.__init__(self, name=name)
