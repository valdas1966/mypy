from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.state.i_0_base.main import StateBase as State


data = DataBestFirst.Factory.empty()
state_a = State.Factory.a()
state_b = State.Factory.b()
state_c = State.Factory.c()
data.frontier.push(state_a)
data.frontier.push(state_b)
data.frontier.push(state_c)
data.dict_parent[state_a] = None
data.dict_parent[state_b] = state_a
data.dict_parent[state_c] = state_b
assert data.path_to(state_a).key_comparison() == [state_a]