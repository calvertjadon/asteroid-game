import pygame
from pygame.math import Vector2

from asteroids.circle import Circle
from asteroids.config import PlayerConfig, ShotConfig
from asteroids.shot import Shot
from asteroids.types import Triangle


class Player(Circle):
    __color: pygame.Color
    __turn_speed: int
    __move_speed: int
    __rotation: float
    __shot_speed: float
    __shot_radius: float
    __shot_cooldown: float
    __shot_timer: float

    def __init__(
        self,
        center: pygame.Vector2,
        config: PlayerConfig,
    ) -> None:
        super().__init__(center, config.radius)

        self.__color = config.color
        self.__turn_speed = config.turn_speed
        self.__move_speed = config.move_speed
        self.__rotation = 45
        self.__shot_speed = config.shot.speed
        self.__shot_radius = config.shot.radius
        self.__shot_cooldown = config.shot.cooldown
        self.__shot_timer = 0

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

    def __rotate(self, dt: float) -> None:
        self.__rotation += (self.__turn_speed * dt) % 360

    def __move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.__rotation)
        self._center += forward * self.__move_speed * dt

    def update(self, dt: float) -> None:
        self.__shot_timer = max(0, self.__shot_timer - dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.__move(dt)
        if keys[pygame.K_a]:
            self.__rotate(-dt)
        if keys[pygame.K_s]:
            self.__move(-dt)
        if keys[pygame.K_d]:
            self.__rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self) -> None:
        if self.__shot_timer > 0:
            return

        velocity = pygame.Vector2(0, 1).rotate(self.__rotation) * self.__shot_speed
        center = Vector2(self.center)
        Shot(center, self.__shot_radius, velocity)
        self.__shot_timer += self.__shot_cooldown
