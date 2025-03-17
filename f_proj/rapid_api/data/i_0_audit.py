from __future__ import annotations
from f_psl.pydantic.mixins.flattenable import Flattenable
from pydantic import Field
from typing import Any, Type


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
                  params: dict[str, Any],
                  type_data: Type[DataAudit]) -> dict[str, Any]:
            """
            ========================================================================
             Generate a valid DataAudit.
            ========================================================================
            """
            args = {'is_ok': True, 'is_found': True, 'is_broken': False}
            return cls._to_dict(args=args, params=params, type_data=type_data)

        @classmethod
        def not_ok(cls,
                   status_code: int,
                   params: dict[str, Any],
                   type_data: Type[DataAudit] = None) -> dict[str, Any]:
            """
            ========================================================================
             Generate a non-ok DataAudit.
            ========================================================================
            """
            args = {'is_ok': False, 'code': status_code}
            return cls._to_dict(args=args, params=params, type_data=type_data)
        
        @classmethod
        def not_found(cls,
                      params: dict[str, Any],
                      type_data: Type[DataAudit] = None) -> dict[str, Any]:
            """
            ========================================================================
             Generate a not-found DataAudit.
            ========================================================================
            """
            args = {'is_ok': True, 'is_found': False}
            return cls._to_dict(args=args, params=params, type_data=type_data)
        
        @classmethod    
        def broken(cls,
                   msg: str,
                   params: dict[str, Any],
                   type_data: Type[DataAudit] = None) -> dict[str, Any]:
            """
            ========================================================================
             Generate a broken DataAudit.
            ========================================================================
            """
            args = {'is_ok': True, 'is_found': True, 'is_broken': True, 'msg': msg}
            return cls._to_dict(args=args, params=params, type_data=type_data)
        
        @classmethod
        def _to_dict(cls,
                     args: dict[str, Any],
                     params: dict[str, Any],
                     type_data: Type[DataAudit] = None) -> dict[str, Any]:
            """
            ========================================================================
             Convert a DataAudit to a dict without None-values.
            ========================================================================
            """
            args.update(params)
            data = type_data(**args) if type_data else DataAudit(**args)
            return data.to_flat_dict()
