from typing import Any, ClassVar, Iterable


class HasRecord:
    """
    ============================================================================
     Mixin-Class for objects that can be converted to a Record.
    ============================================================================
    """

    # Fields of the Record.
    FIELDS_SPECIFIC: ClassVar[Iterable[str]] = ()

    # Factory
    Factory: type = None
    
    @classmethod
    def fields(cls) -> list[str]:
        """
        ========================================================================
         Getter of the Record-Fields of the Instance.
        ========================================================================
        """
        fields: list[str] = []
        for base in reversed(cls.__mro__):
            extra = getattr(base, "FIELDS_SPECIFIC", ())
            fields.extend(extra)
        return fields

    @property
    def record(self) -> dict[str, Any]:
        """
        ========================================================================
         Convert the Instance to a Record.
        ========================================================================
        """
        return {name: getattr(self, name)
                for name
                in self.fields()}
