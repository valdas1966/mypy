from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_math.percentiles.utils import UPercentiles
    from f_math.percentiles.bin import Bin

ULazy.install(globals(), {
    'UPercentiles': 'f_math.percentiles.utils:UPercentiles',
    'Bin': 'f_math.percentiles.bin:Bin',
})
