import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.color import Color
from asteroids.circle import Circle


class Shot(Circle):
    __color: Color

    def __init__(
        self, center: Vector2, radius: float, velocity: Vector2, color: Color
    ) -> None:
        super().__init__(center, radius, velocity)

        self.__color = color

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(
            surface,
            self.__color,
            self.center,
            self.radius,
            width=2,
        )

    def update(self, dt: float) -> None:
        super().update(dt)
        self._center += self.velocity * dt
