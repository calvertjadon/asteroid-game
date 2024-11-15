import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from asteroids.circle import Circle


class Shot(Circle):
    def __init__(self, center: Vector2, radius: float, velocity: Vector2) -> None:
        super().__init__(center, radius, velocity)

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(
            surface,
            "white",
            self.center,
            self.radius,
            width=2,
        )

    def update(self, dt: float) -> None:
        super().update(dt)
        self._center += self.velocity * dt
