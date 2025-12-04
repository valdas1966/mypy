import sys
import logging
from old_f_logging.dec import log_info


logging.basicConfig(level=logging.INFO,
                    encoding='utf-8',
                    stream=sys.stdout,
                    format='%(asctime)s: %(levelname)s: %(pathname)s: '
                           '%(funcName)s: %(message)s')


@log_info
def a(x):
    b(x, z=5)


@log_info
def b(y, z):
    pass


a(x=2)
