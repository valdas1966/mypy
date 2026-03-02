from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.state import StateCell as State


data = DataBestFirst.Factory.cell_00()
state_00 = State.Factory.zero()
print(data.data_state(state_00))