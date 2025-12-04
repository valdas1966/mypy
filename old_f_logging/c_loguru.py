from loguru import logger
import sys


class LoGuru:

    def __init__(self, filepath: str):
        self._filepath = filepath
        logger.remove()
        logger.add(filepath, rotation='1 day', retention='7 days')

    def log(self, d: dict):
        logger.debug(d)
