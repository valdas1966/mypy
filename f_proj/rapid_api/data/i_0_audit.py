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
    def gen_is_not_ok(cls,
                      status_code: int,
                      params: dict[str, Any]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a DataAudit with is_ok=False.
        ========================================================================
        """
        init_args = {"is_ok": False, "code": status_code}
        init_args.update(params)
        data = cls(**init_args)
        return data.model_dump()
    
    @classmethod
    def gen_is_not_found(cls,
                         params: dict[str, Any] = None) -> dict[str, Any]:
        """
        ========================================================================
         Generate a DataAudit with is_found=False.
        ========================================================================
        """
        init_args = {'is_ok': True, 'is_found': False}
        init_args.update(params)
        data = cls(**init_args)
        return data.model_dump()
    
    @classmethod
    def gen_is_broken(cls,
                      msg: str,
                      params: dict[str, Any]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a DataAudit with is_broken=True.
        ========================================================================
        """
        init_args = {'is_ok': True, 'is_found': True,
                     'is_broken': True, 'msg': msg}
        init_args.update(params)
        data = cls(**init_args)
        return data.model_dump()

    @classmethod
    def _to_dict(cls,
                 args: dict[str, Any],
                 params: dict[str, Any]) -> dict[str, Any]:
        """
        ========================================================================
         Convert a DataAudit to a dict without None-values.
        ========================================================================
        """
        args.update(params)
        data = cls(**args)
        return data.model_dump(exclude_none=True)
