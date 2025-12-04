import sys
import logging
from old_f_logging.dec import log_all_methods, log_info_without_self


logging.basicConfig(level=logging.INFO,
                    encoding='utf-8',
                    stream=sys.stdout,
                    format='%(asctime)s: %(levelname)s: %(pathname)s: '
                           '%(funcName)s: %(message)s')


@log_all_methods(decorator=log_info_without_self)
class C:

    def __init__(self):
        self.a(x=2)

    def a(self, x):
        self.b(x, z=5)

    def b(self, y, z):

        def bb(w):
            w = 0

        bb(z)


c = C()
