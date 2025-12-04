from old_f_logging.c_loguru import LoGuru
from datetime import datetime

start = datetime.now()

filepath = 'd:\\temp\\loguru\\loguru.log'
header = ['list', 'b']
log = LoGuru(filepath=filepath)
for _ in range(1000):
    log.log({'list': 1, 'b': 2})

finish = datetime.now()
print(finish - start)
