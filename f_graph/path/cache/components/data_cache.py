from f_core.components.data_frozen import DataFrozen, dataclass
from typing import Callable


@dataclass(frozen=True)
class DataCache(DataFrozen):
