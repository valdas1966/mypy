from f_proj.rapid_api.data.i_0_audit import DataAudit, Field
from typing import Any


class GenAudit:
    """
    ============================================================================
     Generator for Audit-Data.
    ============================================================================
    """

    @staticmethod
    def is_not_ok() -> dict[str, Any]:
        """
        ========================================================================
         Return a DataAudit with is_ok=False.
        ========================================================================
        """
        return DataAudit.is_not_ok()
    
    @staticmethod
    def is_not_ok_params() -> dict[str, Any]:
        """
        ========================================================================
         Return a DataAudit with is_ok=False and params.
        ========================================================================
        """
        return DataAudit.is_not_ok(status_code=400,
                                   msg='Bad Request',
                                   params={'is_found': True})

    @staticmethod
    def is_not_ok_derived() -> dict[str, Any]:
        """
        ========================================================================
         Return a derived class of DataAudit with is_ok=False.
        ========================================================================
        """
        class DataDerived(DataAudit):
            derived: str = Field(default=None)
        return DataDerived.is_not_ok()


data = GenAudit.is_not_ok_params()
print(data)
