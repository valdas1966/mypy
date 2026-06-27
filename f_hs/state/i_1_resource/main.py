from f_hs.state import StateBase
from f_hs.state.i_1_resource.node_resource import NodeResource
from typing import TypeVar

Node = TypeVar('Node')

# StateResource is a pure (generic) type alias: a search state keyed on a
# NodeResource (node, resource) pair — the V×R identity that runs RCSPP on
# stock AStar / Dijkstra. Identity only via StateBase; the node / resource
# components are read off the key (state.key.node / state.key.resource).
# NodeResource holds the behavior; the state is pure identity.
StateResource = StateBase[NodeResource[Node]]
