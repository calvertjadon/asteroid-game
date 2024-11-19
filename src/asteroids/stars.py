import random
import pygame.draw
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
import pygame.color

from asteroids.entity import Entity


class Star(Entity):
    _center: Vector2
    _width: float
    _height: float
    _color: pygame.color.Color

    def __init__(self, center: Vector2, color: pygame.color.Color, size: float) -> None:
        super().__init__()
        self._center = center
        self._width = size
        self._height = size
        self._color = color

    def draw(self, surface: Surface) -> None:
        rect = Rect(
            self._center.x - self._width / 2,
            self._center.y - self._height / 2,
            self._width,
            self._height,
        )
        pygame.draw.rect(surface, self._color, rect)


class BigStar(Star):
    def __init__(self, center: Vector2, color: pygame.color.Color, size: float) -> None:
        super().__init__(center, color, size)

    def draw(self, surface: Surface) -> None:
        super().draw(surface)

        distance = self._width * 1.5
        offsets = [
            (distance, 0),
            (-distance, 0),
            (0, distance),
            (0, -distance),
        ]

        for offset in offsets:
            pygame.draw.line(
                surface,
                self._color,
                self._center,
                Vector2(self._center + offset),
                width=int(self._width / 4),
            )


class StarField:
    __screen_size: Rect
    __colors: list[pygame.color.Color]

    def __init__(self, screen_size: Rect, colors: list[pygame.color.Color]) -> None:
        super().__init__()

        self.__screen_size = screen_size
        self.__star_types = [Star, BigStar]
        self.__colors = colors

    def create_star(self) -> None:
        # brightness = random.randint(1, 8) * 32 - 1
        # color = pygame.color.Color(brightness, brightness, brightness)

        color = random.choice(self.__colors)

        pos = Vector2(
            random.uniform(0, self.__screen_size.width),
            random.uniform(0, self.__screen_size.height),
        )

        star_type = random.choice(self.__star_types)
        size = random.uniform(2, 8)
        star = star_type(pos, color, size)
        print(star)
