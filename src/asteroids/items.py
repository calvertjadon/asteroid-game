import pygame.draw

from abc import ABC, abstractmethod
from typing import Protocol
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

from asteroids.circle import Circle
from asteroids.weapons import Arsenal, WeaponType


class _Weilder(Protocol):
    @property
    def arsenal(self) -> Arsenal: ...


class Item(ABC, Circle):
    __color: Color

    def __init__(self, center: Vector2, color: Color) -> None:
        super().__init__(Vector2(center + (50, 0)), 5)

        self.__color = color

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.__color, self.center, self.radius)

    @abstractmethod
    def equip(self, weilder: _Weilder) -> None: ...


class WeaponItem(Item):
    __weapon_type: WeaponType

    def __init__(self, center: Vector2, color: Color, weapon_type: WeaponType) -> None:
        super().__init__(center, color)

        self.__weapon_type = weapon_type

    def equip(self, weilder: _Weilder) -> None:
        weapon = weilder.arsenal.create(self.__weapon_type)
        weilder.arsenal.equip(weapon)
        print(weilder.arsenal)
