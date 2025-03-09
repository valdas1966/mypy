from pydantic import BaseModel
from typing import Any, Dict


class Flattenable(BaseModel):
    """
    ============================================================================
     Mixin for flattenable pydantic models.
    ============================================================================
    """

    def to_flat_dict(self) -> Dict[str, Any]:
        """
        ============================================================================
         Convert the model to a dict (with internal field names) and then
         flatten any nested dictionaries.
        ============================================================================
        """
        # Convert the model to a dict using internal names and excluding None values.
        data = self.dict(by_alias=False, exclude_none=True)
        return self._flatten_dict(data)

    def _flatten_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """
        ============================================================================
         Recursively flattens a dictionary by merging any nested dictionaries.
        ============================================================================
        """
        flat: Dict[str, Any] = {}
        for key, value in d.items():
            if isinstance(value, dict):
                # Recursively flatten nested dictionaries.
                nested = self._flatten_dict(value)
                flat.update(nested)
            else:
                flat[key] = value
        return flat
