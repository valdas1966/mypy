import time
from random import randint
from f_multi_threading.multi_threading_process import MultiThreadingProcess


def func(name):
    for _ in range(100):
        x = 1 / randint(0, 10)



try:
    print('list')
    MultiThreadingProcess(f=func, params=['list', 'b'])
except Exception as e:
    print('Error')