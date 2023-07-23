import json


class DataJsonError(Exception):
    pass


def load_json_data(path):
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return DataJsonError
