from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.state.i_0_base import StateBase
    from f_hs.state.i_1_cell import StateCell
    from f_hs.state.i_1_resource import StateResource
    from f_hs.state.i_1_resource import NodeResource

ULazy.install(globals(), {
    'StateBase': 'f_hs.state.i_0_base:StateBase',
    'StateCell': 'f_hs.state.i_1_cell:StateCell',
    'StateResource': 'f_hs.state.i_1_resource:StateResource',
    'NodeResource': 'f_hs.state.i_1_resource:NodeResource',
})
