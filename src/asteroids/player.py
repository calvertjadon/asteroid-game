from enum import Enum
import pygame
from pygame.color import Color
from pygame.math import Vector2

from asteroids.circle import Circle
from asteroids.config import PlayerConfig, ShotConfig
from asteroids.shot import Shot
from asteroids.types import Triangle
from asteroids.weapons import Arsenal, _MultiWeapon, _StandardWeapon, WeaponType


class Direction(int, Enum):
    FORWARD = 1
    BACKWARD = -1
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1


class Player(Circle):
    __color: pygame.Color
    __rotation: float
    # __shot_speed: float
    # __shot_radius: float
    # __shot_cooldown: float
    # __shot_color: Color
    __shot_timer: float
    __move_accel: float
    __move_decel: float
    __max_move_speed: float
    __current_move_speed: float
    __move_direction: Direction
    __arsenal: Arsenal

    def __init__(
        self,
        center: pygame.Vector2,
        config: PlayerConfig,
    ) -> None:
        super().__init__(center, config.radius)

        self.__color = config.color
        self.__rotation = 45
        # self.__shot_speed = config.shot.speed
        # self.__shot_radius = config.shot.radius
        # self.__shot_cooldown = config.shot.cooldown
        # self.__shot_color = config.shot.color
        self.__shot_timer = 0

        self.__move_accel = 10
        self.__move_decel = 5
        self.__current_move_speed = 0
        self.__max_move_speed = config.move_speed
        self.__move_direction = Direction.FORWARD

        self.__turn_accel = 30
        self.__turn_decel = 20
        self.__current_turn_speed = 0
        self.__max_turn_speed = config.turn_speed
        self.__turn_direction = Direction.CLOCKWISE

        self.__arsenal = Arsenal(self, config.shot.color)
        # self.__arsenal.equip(self.__arsenal.create(WeaponType.MULTI))
        # self.__arsenal.equip(self.__arsenal.create(WeaponType.SPRAY))
        #

    @property
    def arsenal(self) -> Arsenal:
        return self.__arsenal

    @property
    def rotation(self) -> float:
        return self.__rotation

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
        self.__rotation += (
            dt * self.__current_turn_speed * self.__turn_direction
        ) % 360

    def __move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.__rotation)
        self._center += forward * self.__current_move_speed * dt * self.__move_direction

    def update(self, dt: float) -> None:
        self.__arsenal.update(dt)

        keys = pygame.key.get_pressed()

        move_accel = self.__move_accel
        if keys[pygame.K_w]:
            if self.__current_move_speed == 0:
                self.__move_direction = Direction.FORWARD

            if self.__move_direction != Direction.FORWARD:
                move_accel = -self.__move_accel / 2

        elif keys[pygame.K_s]:
            if self.__current_move_speed == 0:
                self.__move_direction = Direction.BACKWARD

            if self.__move_direction != Direction.BACKWARD:
                move_accel = -self.__move_accel / 2
        else:
            move_accel = -self.__move_decel

        self.__current_move_speed = max(
            0, min(self.__max_move_speed, self.__current_move_speed + move_accel)
        )
        self.__move(dt)

        turn_accel = self.__turn_decel
        if keys[pygame.K_a]:
            if self.__current_turn_speed == 0:
                self.__turn_direction = Direction.COUNTER_CLOCKWISE

            if self.__turn_direction != Direction.COUNTER_CLOCKWISE:
                turn_accel = -self.__turn_accel * 2

        elif keys[pygame.K_d]:
            if self.__current_turn_speed == 0:
                self.__turn_direction = Direction.CLOCKWISE

            if self.__turn_direction != Direction.CLOCKWISE:
                turn_accel = -self.__turn_accel * 2

        else:
            turn_accel = -self.__turn_decel

        self.__current_turn_speed = max(
            0, min(self.__max_turn_speed, self.__current_turn_speed + turn_accel)
        )
        self.__rotate(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self) -> None:
        # if self.__shot_timer > 0:
        #     return
        #
        # velocity = pygame.Vector2(0, 1).rotate(self.__rotation) * self.__shot_speed
        # center = Vector2(self.center)
        # Shot(center, self.__shot_radius, velocity, self.__shot_color)
        # self.__shot_timer += self.__shot_cooldown
        self.__arsenal.active_weapon.shoot()
