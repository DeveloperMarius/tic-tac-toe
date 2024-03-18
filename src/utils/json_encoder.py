from json import JSONEncoder


class ModelEncoder(JSONEncoder):
    def default(self, o):
        data = {}
        for key, value in o.__dict__.items():
            if key.startswith('_'):
                key = key[1:]
            data[key] = value
        return data
