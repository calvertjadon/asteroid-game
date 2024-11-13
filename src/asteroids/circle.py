import pygame

from datetime import timedelta

from asteroids.types import Coordinate


class Circle(pygame.sprite.Sprite):
    _center: Coordinate
    _velocity: Coordinate
    _radius: float

    def __init__(
        self, center: Coordinate, radius: float, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)

        self._center = center
        self._velocity = pygame.Vector2(0, 0)
        self._radius = radius

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def update(self, dt: timedelta) -> None:
        pass
