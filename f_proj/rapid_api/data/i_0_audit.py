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
    msg: str = Field(default=None)        
        

    class Gen:
        """
        ============================================================================
         Generator for DataAudit.
        ============================================================================
        """
        @classmethod
        def valid(cls,
                  params: dict[str, Any]) -> dict[str, Any]:
            """
            ========================================================================
             Generate a valid DataAudit.
            ========================================================================
            """
            data = DataAudit.model_validate(params)
            data.is_ok = True
            data.is_found = True
            data.is_broken = False
            return data.to_flat_dict()

        @classmethod
        def not_ok(cls,
                   status_code: int,
                   params: dict[str, Any]) -> dict[str, Any]:
            """
            ========================================================================
             Generate a non-ok DataAudit.
            ========================================================================
            """
            args = {"is_ok": False, "code": status_code}
            return cls._to_dict(args, params)
        
        @classmethod
        def not_found(cls,
                      params: dict[str, Any]) -> dict[str, Any]:
            """
            ========================================================================
             Generate a not-found DataAudit.
            ========================================================================
            """
            args = {'is_ok': True, 'is_found': False}
            return cls._to_dict(args, params)
        
        @classmethod    
        def broken(cls,
                   msg: str,
                   params: dict[str, Any]) -> dict[str, Any]:
            """
            ========================================================================
             Generate a broken DataAudit.
            ========================================================================
            """
            args = {'is_ok': True, 'is_found': True, 'is_broken': True, 'msg': msg}
            return cls._to_dict(args, params)

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
            data = DataAudit(**args)
            return data.model_dump(exclude_none=True)
    