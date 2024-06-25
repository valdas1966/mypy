from f_encoding.base_52 import Base52


s = 'Hello!'
s = 'Hello, world! This string contains ASCII chars like 1234567890 and !@#$%^&*()'
print(s)
e = Base52.encode(s)
print(e)
d = Base52.decode(s)
print(d)
