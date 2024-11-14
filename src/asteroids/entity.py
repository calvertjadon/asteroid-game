import pygame
from pygame.event import Event, post as post_event
from pygame.surface import Surface

from asteroids.events import CustomEvent


class Entity(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        event = Event(CustomEvent.ENTITY_CREATED, entity=self)
        post_event(event)

    def draw(self, surface: Surface) -> None: ...
    def update(self, dt: float) -> None: ...
