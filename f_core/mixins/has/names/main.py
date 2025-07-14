from collections import UserList
from f_core.mixins.has.name import HasName


class HasNames(UserList[HasName]):
    """
    ============================================================================
     Mixin-Class for Objects with List of HasName Objects.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, items: list[HasName]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        UserList.__init__(self, items)
    
    def names(self) -> list[str]:
        """
        ========================================================================
         Return the names of the HasName objects in the List.
        ========================================================================
        """
        return [item.name for item in self]
    
    def __contains__(self, name: str) -> bool:
        """
        ========================================================================
         Check if a name exists in the List.
        ========================================================================
        """
        return name in self.names()
    
    def __getitem__(self, item: str | int | slice) -> HasName:
        """
        ========================================================================
         Get a HasName object by name or index.
        ========================================================================
        """
        if isinstance(item, str):
            for obj in self:
                if obj.name == item:
                    return obj
            raise ValueError(f"Object with name {item} not found")
        else:
            return UserList.__getitem__(self, item)
