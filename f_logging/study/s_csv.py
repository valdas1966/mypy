from f_logging.c_csv import CsvLogger


folder = 'd:\\temp\\study\\log'
name = 'study'
header = ['list', 'b', 'c']


logger = CsvLogger(folder=folder, name=name, header=header)
logger.append_list(row=[1, None, 3])
logger.append_dict(d={'b': 2, 'list': 1, 'd': 4})
