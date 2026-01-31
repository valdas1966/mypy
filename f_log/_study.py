import logging
from f_log.config import setup_log

setup_log(enabled=True, level=logging.DEBUG, sink='both', path='debug.log')


log = logging.getLogger(__name__)
log.debug('debug message')
log.info('info message')
log.warning('warning message')
log.error('error message')
log.critical('critical message')
