from f_logging.c_loguru import LoGuru


filepath = 'd:\\temp\\loguru\\loguru.log'
header = ['a', 'b']
log = LoGuru(filepath=filepath)
log.log({'a': 1, 'b': 2})
log.log({'b': 22, 'a': 11})
