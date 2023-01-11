from f_logging.c_loguru import LoGuru

repo = 'd:\\temp\\loguru'
filepath_1 = f'{repo}\\loguru_1.log'
filepath_2 = f'{repo}\\loguru_2.log'
header = ['a']

log_1 = LoGuru(filepath=filepath_1, header=header)
log_2 = LoGuru(filepath=filepath_2, header=header)

log_1.log(d={'a': 1})
log_2.log(d={'a': 2})
