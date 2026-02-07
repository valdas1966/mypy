from f_search.ds.state import StateCell as State

state_1 = State.Factory.zero()
state_2 = State.Factory.zero()
print(state_1.key_comparison())
print(state_2.key_comparison())
print(state_1.key_comparison() == state_2.key_comparison())
