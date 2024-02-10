from f_google.big_query.structures.schema import Schema


schema = Schema()
schema.add(name='a', dt=Schema.INTEGER)
schema.add(name='b', dt=Schema.STRING)

for f in schema.build():
    print(f)
