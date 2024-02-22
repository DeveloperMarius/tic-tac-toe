from json import JSONEncoder
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper


class ModelEncoder(JSONEncoder):
    def default(self, o):
        data = {}
        for key, value in o.__dict__.items():
            if key.startswith('_'):
                key = key[1:]
            data[key] = value
        return data


class EventHandler:

    @staticmethod
    @listens_for(Mapper, "before_insert")
    def receive_before_insert(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    @listens_for(Mapper, "before_update")
    def receive_before_update(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    def _validate(data, columns):
        for column in columns:
            if column.name not in data:
                continue
            value = data[column.name]
            if isinstance(column.type, String):
                length = column.type.length
                if value is None:
                    if not column.nullable:
                        raise ValueError(f"{column.name} cannot be null.")
                    continue
                if len(value) > length:
                    raise ValueError(f"{column.name} is to long. {len(value)} > {length}")


class Base(DeclarativeBase):
    pass
