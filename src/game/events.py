from typing import List
from enum import Enum


class EventType(Enum):

    USER_JOIN = 'user_join'
    USER_LEAVE = 'user_leave'


class Event:

    _type: EventType
    _data: any

    def __init__(self, type: EventType, data: any = None):
        self._type = type
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    def __str__(self):
        return f"Event: {self.type.name}, Data: {self.data}"


class EventManager:

    _listener: dict[EventType, List[callable]] = {}

    def __init__(self):
        self._events = []

    @property
    def listener(self):
        return self._listener

    def trigger(self, event: Event):
        if event.type in self.listener.keys():
            for listener in self.listener[event.type]:
                listener(event)

    def on(self, event_type: EventType, callback: callable):
        if event_type not in self.listener.keys():
            self.listener[event_type] = []
        self.listener[event_type].append(callback)
