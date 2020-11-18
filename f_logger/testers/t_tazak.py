from f_logger.tazak import LoggerTazak

logger = LoggerTazak(titles='value')
logger.write('a')
logger.write('b')
logger.write('c')
logger.close()

logger = LoggerTazak(titles='value', dir_logger='test')
logger.write('a')
logger.write('b')
logger.write('c')
logger.close()

