from abc import abstractmethod
from typing import Generic, TypeVar
from f_abstract.components.groups.group import Group

Item = TypeVar('Item')


class Groupable(Generic[Item]):
    """
    ============================================================================
     Mixin for Classes that their content can be converted into Group.
    ============================================================================
    """

    @abstractmethod
    def to_group(self, name: str = None) -> Group[Item]:
        """
        ========================================================================
         Convert class content into List.
        ========================================================================
        """
        pass
