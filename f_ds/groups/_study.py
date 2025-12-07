from f_ds.groups import Group


group = Group.Factory.ab()
a = group.random.item()
print(a)
