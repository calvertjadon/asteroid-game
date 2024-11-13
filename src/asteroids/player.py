from datetime import timedelta
import pygame

from asteroids.circle import Circle
from asteroids.config import PlayerConfig
from asteroids.types import Coordinate, Triangle


class Player(Circle):
    __color: pygame.Color
    __turn_speed: int
    __move_speed: int
    __rotation: float

    def __init__(
        self,
        center: Coordinate,
        config: PlayerConfig,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(center=center, radius=config.radius, *groups)

        self.__color = config.color
        self.__turn_speed = config.turn_speed
        self.__move_speed = config.move_speed
        self.__rotation = 45

    def __get_triangle(self) -> Triangle:
        forward = pygame.Vector2(0, 1).rotate(self.__rotation)
        right = pygame.Vector2(0, 1).rotate(self.__rotation + 90) * self._radius / 1.5
        a = self._center + forward * self._radius
        b = self._center - forward * self._radius - right
        c = self._center - forward * self._radius + right
        return (a, b, c)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(
            surface=surface, color=self.__color, points=self.__get_triangle(), width=2
        )

    def __rotate(self, dt: timedelta) -> None:
        self.__rotation += self.__turn_speed * dt.seconds / 1000
        print(self.__rotation)

    def __move(self, dt: timedelta) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.__rotation)
        self._center += forward * self.__move_speed * dt.seconds / 1000

    def update(self, dt: timedelta) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.__move(dt)
        if keys[pygame.K_a]:
            self.__rotate(-dt)
        if keys[pygame.K_s]:
            self.__move(-dt)
        if keys[pygame.K_d]:
            self.__rotate(dt)
