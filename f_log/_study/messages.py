from f_log import setup_log, get_log

setup_log()
log = get_log(name='test')

log.debug('debug message')
log.info('info message')
log.warning('warning message')
log.error('error message')
log.critical('critical message')
