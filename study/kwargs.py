
def f(a: int, b: int):
    print(a, b)

def f_2(**kwargs):
    if 'a' not in kwargs:
        a = 1
    print(a)

f(1, 2)
f(a=1, b=2)
f(**{'a': 1, 'b': 2})

f_2(a=2)

