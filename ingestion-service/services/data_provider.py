class DataProvider:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def provide(self):
        with open(self.json_file_path, "r", encoding="utf-8") as file:
            return file.read()