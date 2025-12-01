from __future__ import annotations
from f_core.mixins.has.name import HasName
from typing import Any, Callable, ClassVar
from f_utils import u_datetime
from enum import Enum

class Color(Enum):
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    UNDERLINE = "\033[4m"

    GRAY    = "\033[90m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


# A function that, given an object, returns the value for one record field.
RecordGetter = Callable[[Any], Any]

class HasRecord(HasName):
    """
    ============================================================================
     Mixin for objects that can be converted to a flat record (dict).
    ============================================================================
    """

    RECORD_SPEC: ClassVar[dict[str, RecordGetter]] = {'name': lambda o: o.name}

    # Factory
    Factory = None

    def __init__(self,
                 name: str = None,
                 verbose: bool = False) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._verbose = verbose

    @property
    def verbose(self) -> bool:
        """
        ========================================================================
        Return the Verbose Attribute.
        ========================================================================
        """
        return self._verbose

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

    def str_record(self) -> str:
        """
        ========================================================================
         Convert this instance to a string representation of the record:
         '[field_name=value] [field_name=value] ...'
        ========================================================================
        """
        if not self.record:
            return str()
        return '[{}]'.format('] ['.join(f'{name}={value}' for name, value in self.record.items()))

    def print(self, msg: str = str()) -> None:
        """
        ========================================================================
        Print a message if verbose is True.
        ========================================================================
        """
        if self.verbose:
            s = f'{Color.GREEN.value}[{u_datetime.now()[11:]}]'
            s += f' {Color.RED.value}[{self._name}]'
            s += f' {Color.RESET.value}{msg}'
            print(s)

    @staticmethod
    def spec(**fields: RecordGetter) -> dict[str, RecordGetter]:
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
    def _record_spec(cls) -> dict[str, RecordGetter]:
        """
        ========================================================================
         INTERNAL: merged record spec for this class, including bases.
        ========================================================================
        """
        spec: dict[str, RecordGetter] = {}
        for base in reversed(cls.__mro__):
            extra = getattr(base, "RECORD_SPEC", {})
            spec.update(extra)
        return spec
