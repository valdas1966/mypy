
class HasRecord:
    
    EXTRA_FIELDS: ClassVar[Iterable[str]] = ()

    @classmethod
    def record_fields(cls) -> list[str]:
        fields: list[str] = []
        for base in reversed(cls.__mro__):
            extra = getattr(base, "EXTRA_FIELDS", ())
            fields.extend(extra)
        return fields

    def to_record(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.record_fields()}
