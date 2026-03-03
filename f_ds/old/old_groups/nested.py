from f_ds.groups.main import Group, Item


class NestedGroup(Group[Group[Item]]):
    """
    ============================================================================
     Group of Groups.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 data: list[Group[Item]] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(name=name, data=data)

    def flatten(self, name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return a flattened group of all Nested-Group items.
        ========================================================================
        """
        data = [item for group in self.data for item in group]
        return Group(name=name, data=data)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR.
         Ex: 'A[B[], C[]]'
        ========================================================================
        """
        str_data = ', '.join(str(group) for group in self.data)
        return f'{self.name}[{str_data}]'
