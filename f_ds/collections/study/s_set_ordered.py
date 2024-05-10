from f_data_structure.collections.set_ordered import SetOrdered

s = SetOrdered()
s.add(2)
s.add(1)

for x in s:
    print(x)

print(1 in s)

print(s)