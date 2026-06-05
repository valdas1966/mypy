from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_graph.nodes.i_0_key import NodeKey
    from f_graph.nodes.i_0_key import Key
    from f_graph.nodes.i_1_parent import NodeParent

ULazy.install(globals(), {
    'NodeKey': 'f_graph.nodes.i_0_key:NodeKey',
    'Key': 'f_graph.nodes.i_0_key:Key',
    'NodeParent': 'f_graph.nodes.i_1_parent:NodeParent',
})
