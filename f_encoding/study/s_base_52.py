from f_encoding.base_52 import Base52


s = 'Hello!'
print(s)
e = Base52.encode(s)
print(e)
d = Base52.decode(e)
print(d)
