from f_logging.c_loguru import LoGuru
from datetime import datetime

start = datetime.now()

filepath = 'd:\\temp\\loguru\\loguru.log'
header = ['a', 'b']
log = LoGuru(filepath=filepath)
for _ in range(1000):
    log.log({'a': 1, 'b': 2})

finish = datetime.now()
print(finish - start)
