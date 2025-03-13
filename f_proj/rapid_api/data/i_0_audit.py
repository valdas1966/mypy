from __future__ import annotations
from f_psl.pydantic.mixins.flattenable import Flattenable
from pydantic import Field
from typing import Any


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

    @classmethod
    def is_not_ok(cls,
                  status_code: int = None,
                  msg: str = None,
                  params: dict[str, Any] = None) -> dict[str, Any]:
        """
        ========================================================================
         Check if the data is not ok.
        ========================================================================
        """
        init_args = {"is_ok": False, "code": status_code, "msg": msg}
        if params:
            init_args.update(params)
        data = cls(**init_args)
        return data.model_dump()
