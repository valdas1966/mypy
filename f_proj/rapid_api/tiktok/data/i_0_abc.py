from f_core.components.data import Data, dataclass, field


@dataclass
class DataABC(Data):
    """
    ============================================================================
     ABC Data-Class for TikTok requests.
    ============================================================================
    """
    is_ok: bool = field(default=None)
    is_found: bool = field(default=None)