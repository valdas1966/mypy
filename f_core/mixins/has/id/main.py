from f_psl.datetime import UDateTime


class HasId:
    """
    ============================================================================
     Mixin of the Id-Birth.
    ============================================================================
    """
    
    def __init__(self,
                 id_group: str = None,
                 id_counter: int = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._id_birth: str = UDateTime.str_now(UDateTime.Format.NANO)
        self._id_group: str = id_group
        self._id_counter: int = id_counter
        
    @property
    def id_birth(self) -> str:
        """
        ========================================================================
         Getter of the Id-Birth of the Instance.
        ========================================================================
        """
        return self._id_birth
    
    @property
    def id_group(self) -> str:
        """
        ========================================================================
         Getter of the Id-Group of the Instance.
        ========================================================================
        """
        return self._id_group
    
    @property
    def id_counter(self) -> int:
        """
        ========================================================================
         Getter of the Id-Counter of the Instance.
        ========================================================================
        """     
        return self._id_counter
