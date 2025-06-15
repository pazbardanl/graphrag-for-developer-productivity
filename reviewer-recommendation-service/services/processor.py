from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class Processor:
    def process(self, json_string: str):
        logger.info(f'incoming: {json_string}')
