from f_search.ds.generated import Generated
from f_search.ds.states import StateBase
from f_search.ds.cost import Cost


generated = Generated()
state_1 = StateBase(key=1)
state_2 = StateBase(key=2)
cost_1 = Cost(key=1, g=4, h=2, is_cached=False, is_bounded=False)
cost_2 = Cost(key=2, g=3, h=3, is_cached=False, is_bounded=False)
generated.push(state_2, cost_2)
generated.push(state_1, cost_1)
best = generated.pop()
print(best.key)