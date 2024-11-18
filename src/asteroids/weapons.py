import random

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Protocol

from pygame.color import Color
from pygame.math import Vector2

from asteroids.shot import Shot


class Weilder(Protocol):
    @property
    def rotation(self) -> float: ...

    @property
    def center(self) -> Vector2: ...


class WeaponType(Enum):
    STANDARD = auto()
    MULTI = auto()
    SPRAY = auto()


class _Weapon(ABC):
    __shot_timer: float
    _arsenal: "Arsenal"
    _shot_color: Color
    __shot_cooldown: float

    def __init__(self, arsenal: "Arsenal", color: Color, cooldown: float) -> None:
        super().__init__()

        self._shot_color = color
        self._arsenal = arsenal
        self.__shot_timer = 0
        self.__shot_cooldown = cooldown

    def unequip(self) -> None:
        self._arsenal.unequip()

    def update(self, dt: float) -> None:
        self.__shot_timer = max(0, self.__shot_timer - dt)

    @abstractmethod
    def shoot(self) -> None: ...

    def _reset_timer(self) -> None:
        self.__shot_timer += self.__shot_cooldown

    @property
    def _can_shoot(self) -> bool:
        return self.__shot_timer == 0


class _StandardWeapon(_Weapon):
    _shot_speed: float
    _shot_radius: float

    def __init__(
        self, arsenal: "Arsenal", color: Color, cooldown=0.3, speed=500
    ) -> None:
        super().__init__(arsenal, color, cooldown)

        self._shot_speed = speed
        self._shot_radius = 5

    def shoot(self) -> None:
        if not self._can_shoot:
            return

        velocity = (
            Vector2(0, 1).rotate(self._arsenal.weilder.rotation) * self._shot_speed
        )
        center = Vector2(self._arsenal.weilder.center)

        Shot(center, self._shot_radius, velocity, self._shot_color)
        self._reset_timer()


class _SprayWeapon(_StandardWeapon):
    __rounds: int

    def __init__(self, arsenal: "Arsenal", color: Color) -> None:
        super().__init__(arsenal, color, cooldown=0.05, speed=300)

        self.__rounds = 50

    def __expense_round(self) -> None:
        self.__rounds -= 1

        if self.__rounds <= 0:
            self._arsenal.unequip()
            del self

    def shoot(self) -> None:
        if not self._can_shoot:
            return

        velocity = (
            Vector2(0, 1).rotate(self._arsenal.weilder.rotation + random.uniform(-5, 5))
            * self._shot_speed
        )
        center = Vector2(self._arsenal.weilder.center)

        Shot(center, self._shot_radius, velocity, self._shot_color)
        self._reset_timer()
        self.__expense_round()


class _MultiWeapon(_Weapon):
    __shot_speed: float
    __shot_radius: float
    __rounds: int

    def __init__(self, arsenal: "Arsenal", color: Color, cooldown=0.5) -> None:
        super().__init__(arsenal, color, cooldown)

        self.__shot_speed = 300
        self.__shot_radius = 3
        self.__rounds = 15

    def __expense_round(self) -> None:
        self.__rounds -= 1

        if self.__rounds <= 0:
            self._arsenal.unequip()
            del self

    def shoot(self) -> None:
        if not self._can_shoot:
            return

        v_middle = (
            Vector2(0, 1).rotate(self._arsenal.weilder.rotation) * self.__shot_speed
        )
        v_left = Vector2(v_middle).rotate(-20)
        v_right = Vector2(v_middle).rotate(20)

        Shot(
            center=Vector2(self._arsenal.weilder.center),
            radius=self.__shot_radius,
            velocity=v_middle,
            color=self._shot_color,
        )

        Shot(
            center=Vector2(self._arsenal.weilder.center),
            radius=self.__shot_radius,
            velocity=v_left,
            color=self._shot_color,
        )

        Shot(
            center=Vector2(self._arsenal.weilder.center),
            radius=self.__shot_radius,
            velocity=v_right,
            color=self._shot_color,
        )
        self._reset_timer()
        self.__expense_round()


class Arsenal:
    __weapons: list[_Weapon]
    __weilder: Weilder
    __color: Color

    def __init__(self, weilder: Weilder, color: Color) -> None:
        self.__weilder = weilder
        self.__color = color
        self.__weapons = [self.create(WeaponType.STANDARD)]

    def update(self, dt: float) -> None:
        for weapon in self.__weapons:
            weapon.update(dt)

    def equip(self, weapon: _Weapon) -> None:
        self.__weapons.append(weapon)

    def unequip(self) -> None:
        assert len(self.__weapons) > 1
        self.__weapons.pop()

    def create(self, type_: WeaponType) -> _Weapon:
        match type_:
            case WeaponType.STANDARD:
                return _StandardWeapon(self, self.__color)

            case WeaponType.MULTI:
                return _MultiWeapon(self, self.__color)

            case WeaponType.SPRAY:
                return _SprayWeapon(self, self.__color)

    @property
    def weilder(self) -> Weilder:
        return self.__weilder

    @property
    def active_weapon(self) -> _Weapon:
        return self.__weapons[-1]
