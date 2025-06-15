import logging

class MyLogger:

    DEFAULT_FORMAT = '%(asctime)s [%(name)s][%(levelname)s] %(message)s'

    def __init__(self):
        self.configured = False

    def get_logger(self, name):
        if not self.configured:
            self._configure_logging()
        if not name:
            raise ValueError("Logger name must be provided")
        return logging.getLogger(name)
    
    def _configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format=MyLogger.DEFAULT_FORMAT
        )
        self.configured = True