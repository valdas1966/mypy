import logging
from f_log.config import setup_log
import time


def log_enabled(times: int) -> float:
    log = logging.getLogger(__name__)
    setup_log(enabled=True, level=logging.DEBUG, sink='file', path='debug.log')
    start = time.time()
    for _ in range(times):
        log.debug('debug message')
    return time.time() - start


def log_disabled(times: int) -> float:
    log = logging.getLogger(__name__)
    setup_log(enabled=False, level=logging.DEBUG, sink='file', path='debug.log')
    start = time.time()
    for _ in range(times):
        log.debug('debug message')
    return time.time() - start


def without_log(times: int) -> float:
    start = time.time()
    for _ in range(times):
        pass
    return time.time() - start


for times in (100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000):
    log_enabled_time = log_enabled(times)
    log_disabled_time = log_disabled(times)
    without_log_time = without_log(times)   
    str_times = f'times: {times}'
    str_log_enabled_time = f'log_enabled: {log_enabled_time}'
    str_log_disabled_time = f'log_disabled: {log_disabled_time}'
    str_without_log_time = f'without_log: {without_log_time}'
    str_diff_enabled_disabled = f'diff enabled vs disabled: {log_disabled_time - log_enabled_time}'
    str_diff_disabled_without = f'diff disabled vs without: {without_log_time - log_disabled_time}'
    print(str_times, str_log_enabled_time, str_log_disabled_time, str_without_log_time, str_diff_enabled_disabled, str_diff_disabled_without)
    