from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataAudit(Flattenable):
    """
    ============================================================================
     Data-Class for Audit-Data.
    ============================================================================
    """
    is_ok: bool = Field(default=None)
    is_found: bool = Field(default=None)
    is_broken: bool = Field(default=None)
    status_code: int = Field(default=None, alias='code')
    msg: str = Field(default=None, alias='msg')
