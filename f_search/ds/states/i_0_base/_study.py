from f_search.ds.states.i_0_base import StateBase


zero = StateBase.Factory.zero()
one = StateBase.Factory.one()

print(zero.key_comparison())
print(one.key_comparison())

print(zero.key_comparison() == one.key_comparison())