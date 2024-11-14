import pygame

from pygame.math import Vector2

from asteroids.entity import Entity


class Circle(Entity):
    _center: Vector2
    _velocity: Vector2
    _radius: float

    def __init__(self, center: Vector2, radius: float, velocity=None) -> None:
        super().__init__()

        self._center = center
        self._velocity = velocity or pygame.Vector2(0, 0)
        self._radius = radius

    @property
    def center(self) -> Vector2:
        return self._center

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    @property
    def radius(self) -> float:
        return self._radius
