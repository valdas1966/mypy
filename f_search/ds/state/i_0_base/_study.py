from f_search.ds.state.i_0_base import StateBase


zero = StateBase.Factory.zero()
one = StateBase.Factory.one()

print(zero.key())
print(one.key())

print(zero.key() == one.key())