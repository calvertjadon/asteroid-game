import pygame
from pygame.event import Event, post as post_event
from pygame.surface import Surface

from asteroids.events import CustomEvent


class Entity(pygame.sprite.Sprite):
    __age: float

    def __init__(self) -> None:
        super().__init__()
        self.__age = 0

        event = Event(CustomEvent.ENTITY_CREATED, entity=self)
        post_event(event)

    def update(self, dt: float) -> None:
        self.__age += dt

    def draw(self, surface: Surface) -> None: ...

    @property
    def age(self) -> float:
        return self.__age
