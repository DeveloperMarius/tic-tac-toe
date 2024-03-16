from typing import List
from enum import Enum


class EventType(Enum):

    # Sent to frontend when a user joins a server
    USER_JOIN = 'user_join'
    # Sent to frontend when a user leaves a server
    USER_LEAVE = 'user_leave'
    # Sent to frontend when a user is updated
    USER_UPDATE = 'user_update'
    # Sent to backend when a user changes his username
    USER_UPDATE_USERNAME = 'user_update_username'
    # Sent from server or can be requested from client to update player cache etc.
    SYNC = 'sync'
    # Sent from the frontend when a user clicked the ready button
    LOBBY_READY = 'lobby_ready'
    # Sent from the lobby when both users pressed ready. When this event is received, the play field should be spawned
    GAMEPLAY_START = 'gameplay_start'
    # Sent from the server when a move is requested from a user. The user can now interact with the play field and select a box
    GAMEPLAY_MOVE_REQUEST = 'gameplay_move_request'
    # Sent from the frontend when a user made a move
    GAMEPLAY_MOVE_RESPONSE = 'gameplay_move_response'
    # Sent from server when move was accepted
    GAMEPLAY_MOVE_ACCEPTED = 'gameplay_move_accepted'
    # Sent from server when move was accepted
    GAMEPLAY_MOVE_DENIED = 'gameplay_move_denied'
    # Remove the play field because the game is over
    GAMEPLAY_STOP = 'gameplay_stop'
    # Sent from the server when a player has won
    GAMEPLAY_WINNER = 'gameplay_winner'
    # Send / receive a message
    CHAT_MESSAGE = 'chat_message'


class Event:

    _type: EventType
    _data: any

    def __init__(self, type: EventType, data: any = None):
        self._type = type
        self._data = data if data is not None else {}

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

    def clear_events(self):
        self._listener = {}
