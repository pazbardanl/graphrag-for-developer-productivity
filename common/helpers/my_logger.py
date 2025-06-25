import logging
import sys

class MyLogger:

    DEFAULT_FORMAT = '%(asctime)s [%(name)s][%(levelname)s] %(message)s'

    def __init__(self):
        self.configured = False

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(MyLogger.DEFAULT_FORMAT))
        logger.handlers = [handler]
        return logger