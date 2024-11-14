import pygame

from asteroids.circle import Circle


class Asteroid(Circle):
    __color: pygame.Color

    def __init__(
        self,
        center: pygame.Vector2,
        radius: float,
        color: pygame.Color,
    ) -> None:
        super().__init__(center, radius)

        self.__color = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.__color, self._center, self._radius, width=2)

    def update(self, dt: float) -> None:
        self._center += self._velocity * dt
