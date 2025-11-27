from f_core.mixins.has.record.main import HasRecord


a = HasRecord.Factory.a()
b = HasRecord.Factory.b()

print(a.record)
print(b.record)
