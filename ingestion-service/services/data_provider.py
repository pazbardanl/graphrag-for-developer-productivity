from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class DataProvider:
    def __init__(self, json_file_path: str):
        logger.info("initialized")
        self.json_file_path = json_file_path

    def provide(self):
        logger.info("providing data from %s", self.json_file_path)
        with open(self.json_file_path, "r", encoding="utf-8") as file:
            return file.read()