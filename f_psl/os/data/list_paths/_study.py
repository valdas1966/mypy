from f_psl.os.data.list_paths import ListPaths

li = ListPaths.Factory.ab()
print(li)
print(li.data)
print(li.record)
for x in li:
    print(x)