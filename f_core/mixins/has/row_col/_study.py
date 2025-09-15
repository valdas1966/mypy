from f_core.mixins.has import HasRowCol


obj = HasRowCol.Factory.twelve()
for n in obj.neighbors():
    print(n)

obj_2 = HasRowCol.Factory.twelve()
print(obj == obj_2)


