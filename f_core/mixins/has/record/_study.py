from f_core.mixins.has.record.main import HasRecord


a = HasRecord.Factory.a()
b = HasRecord.Factory.b()

a.print()
a.print('I am A')
print(a.record)
print(a.str_record())

b.print()
b.print('I am B')
print(b.record)
print(b.str_record())
