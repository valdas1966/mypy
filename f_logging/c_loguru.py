from loguru import logger
import sys


class LoGuru:

    def __init__(self, filepath: str, verbose: bool=True):
        self._filepath = filepath
        logger.add(filepath, rotation='1 day', retention='7 days')
        if not verbose:
            logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

    def log(self, d: dict):
        logger.debug(d)
