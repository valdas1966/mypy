from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.queues.i_0_base.main import QueueBase

ULazy.install(globals(), {'QueueBase': 'f_ds.queues.i_0_base.main:QueueBase'})
