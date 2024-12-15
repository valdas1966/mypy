from f_google.services.big_query.structures.schema import Schema


schema = Schema()
schema.add(name='a', dtype=Schema.BOOLEAN)
schema.add(name='b', dtype=Schema.INTEGER)
schema.add(name='c', dtype=Schema.STRING)
schema.add(name='d', dtype=Schema.DATETIME)

for f in schema.build():
    print(f)
