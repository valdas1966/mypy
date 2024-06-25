from f_encoding.base_64 import Base64


s = 'Hello!'
print(s)
e = Base64.encode(s)
print(e)
d = Base64.decode(e)
print(d)
