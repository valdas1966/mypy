from __future__ import annotations
from f_core.mixins.has.name import HasName
from typing import Any, Callable, ClassVar, Dict

# A function that, given an object, returns the value for one record field.
RecordGetter = Callable[[Any], Any]


class HasRecord(HasName):
    """
    ============================================================================
     Mixin for objects that can be converted to a flat record (dict).
    ============================================================================
    """

    RECORD_SPEC: ClassVar[Dict[str, RecordGetter]] = {'name': lambda o: o.name}

    # Factory
    Factory = None

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)

    @property
    def record(self) -> dict[str, Any]:
        """
        ========================================================================
         Convert this instance to a record-dicr: {field_name: value} 
         (only values that are not None)
        ========================================================================
        """
        return {name: getter(self)
                for name, getter
                in self._record_spec().items()
                if getter(self) is not None}

    @staticmethod
    def spec(**fields: RecordGetter) -> Dict[str, RecordGetter]:
        """
        ========================================================================
         Helper for nicer syntax in subclasses.
        ========================================================================
        """
        return fields

    @classmethod
    def header_record(cls) -> list[str]:
        """
        ========================================================================
         Public: ordered list of field names (for CSV headers, tables, etc.).
        ========================================================================
        """
        return list(cls._record_spec().keys())

    @classmethod
    def _record_spec(cls) -> Dict[str, RecordGetter]:
        """
        ========================================================================
         INTERNAL: merged record spec for this class, including bases.
        ========================================================================
        """
        spec: Dict[str, RecordGetter] = {}
        for base in reversed(cls.__mro__):
            extra = getattr(base, "RECORD_SPEC", {})
            spec.update(extra)
        return spec
