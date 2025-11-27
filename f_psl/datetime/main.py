from datetime import datetime
from enum import Enum, auto


class UDateTime:
    """
    ========================================================================
     Class of the Utility of the Date-Time.
    ========================================================================
    """
    
    class Format(Enum):
        """
        ========================================================================
         Enum of the Formats of the Current-Date-Time.
        ========================================================================
        """
        # Standard Format: dd/mm/yyyy hh:mi:ss
        STD = auto()
        # Seconds Format: yyyymmddhhmiss
        SEC = auto()
        # Nanoseconds Format: yyyymmddhhmissnnnnnnnnn
        NANO = auto()
    
    @staticmethod
    def now() -> datetime:
        """
        ========================================================================
         Return the Current-Date-Time.
        ========================================================================
        """
        return datetime.now()
    
    @staticmethod
    def str_now(format: Format = Format.STD) -> str:
        """
        ============================================================================
         Return the Current-Date-Time in the given Format.
        ============================================================================
        """
        dt = UDateTime.now()
        if format == UDateTime.Format.STD:
            return dt.strftime('%d/%m/%Y %H:%M:%S')
        elif format == UDateTime.Format.SEC:
            return dt.strftime('%Y%m%d%H%M%S')
        elif format == UDateTime.Format.NANO:
            return dt.strftime('%Y%m%d%H%M%S%f')

