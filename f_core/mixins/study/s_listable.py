from f_ds.groups.group import Listable


li = Listable(name='LIST')
li.append(1)
li.append(2)
print(li)
li += [3]
print(li)
