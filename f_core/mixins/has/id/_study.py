from f_core.mixins.has.id import HasId


a = HasId()
b = HasId()

print(a.id_birth)
print(b.id_birth)

c = HasId()
print(c.id_birth)
