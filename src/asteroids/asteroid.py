import pygame.draw
from pygame.event import Event, post as post_event
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

from asteroids.circle import Circle
from asteroids.events import CustomEvent
from asteroids.explosion import create_explosion


class Asteroid(Circle):
    __color: Color
    __particle_colors: list[Color]

    def __init__(
        self,
        center: Vector2,
        radius: float,
        color: Color,
        velocity: Vector2,
        particle_colors: list[Color],
    ) -> None:
        super().__init__(center, radius, velocity)

        self.__color = color
        self.__particle_colors = particle_colors

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(
            surface,
            self.__color,
            self._center,
            self._radius,
            width=int(self.radius**0.5 / 1.5),
        )

    def update(self, dt: float) -> None:
        super().update(dt)
        self._center += self._velocity * dt

    def split(self) -> None:
        self.kill()
        create_explosion(self, 30, self.__particle_colors)

        event = Event(CustomEvent.ASTEROID_KILLED, asteroid=self)
        post_event(event)
