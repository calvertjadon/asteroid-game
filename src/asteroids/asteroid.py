import pygame
from pygame.event import Event, post as post_event

from asteroids.circle import Circle
from asteroids.events import CustomEvent
from asteroids.explosion import create_explosion


class Asteroid(Circle):
    __color: pygame.Color

    def __init__(
        self,
        center: pygame.Vector2,
        radius: float,
        color: pygame.Color,
        velocity: pygame.Vector2,
    ) -> None:
        super().__init__(center, radius, velocity)

        self.__color = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.__color, self._center, self._radius, width=2)

    def update(self, dt: float) -> None:
        super().update(dt)
        self._center += self._velocity * dt

    def split(self) -> None:
        self.kill()
        create_explosion(self, 30)

        event = Event(CustomEvent.ASTEROID_KILLED, asteroid=self)
        post_event(event)
