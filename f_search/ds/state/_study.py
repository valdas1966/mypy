from f_search.ds.state import State


zero = State.Factory.zero()
one = State.Factory.one()

print(zero.key_comparison())
print(one.key_comparison())

print(zero.key_comparison() == one.key_comparison())