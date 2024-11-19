from typing import DefaultDict
from pygame.event import Event

from asteroids.interfaces import IEventHandler
from asteroids.types import EventType


class EventManager:
    __handlers: dict[EventType, list[IEventHandler]]

    def __init__(self) -> None:
        self.__handlers = DefaultDict(lambda: [])

    def register_handler(
        self,
        type_: EventType,
        handler: IEventHandler,
    ) -> None:
        self.__handlers[type_].append(handler)

    def handle(self, event: Event) -> None:
        for handler in self.__handlers[event.type]:
            handler.handle(event)
