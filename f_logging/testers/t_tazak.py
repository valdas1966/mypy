from f_logging.tazak import LoggerTazak

logger = LoggerTazak(titles='id,value')
logger.write('1,list')
logger.write('2,b')
logger.write('3,c')
logger.close()

logger = LoggerTazak(titles='value', dir_logger='test')
logger.write('list')
logger.write('b')
logger.write('c')
logger.close()

