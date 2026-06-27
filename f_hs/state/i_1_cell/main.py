from f_hs.state import StateBase
from f_ds.grids import CellMap

# StateCell is a pure type alias: a search state keyed on a CellMap.
# Identity only — equality / hash / order / str come from StateBase via
# HasKey; it carries no behavior of its own. State-to-state distance is
# ProblemGrid.distance; (row, col) extraction is state.key.to_tuple().
StateCell = StateBase[CellMap]
