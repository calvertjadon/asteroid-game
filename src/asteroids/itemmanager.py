import random

from pygame import Vector2
from pygame.color import Color
from pygame.rect import Rect
from asteroids.entity import Entity
from asteroids.items import Item, WeaponItem
from asteroids.weapons import WeaponType


class ItemManager(Entity):
    __itemtimer: float
    __screen_size: Rect
    __item: Item | None
    COOLDOWN = 10

    def __init__(self, screen_size: Rect) -> None:
        super().__init__()

        self.__itemtimer = 0
        self.__screen_size = screen_size
        self.__item = None

    def spawn(self) -> None:
        weapon_type = random.choice(
            [type_ for type_ in WeaponType if type_ is not WeaponType.STANDARD]
        )
        x = random.uniform(0, self.__screen_size.width)
        y = random.uniform(0, self.__screen_size.height)
        center = Vector2(x, y)
        color = Color("yellow")

        self.__item = WeaponItem(center, color, weapon_type)
        self.__itemtimer = self.COOLDOWN

    def __can_spawn(self) -> bool:
        return self.__itemtimer == 0

    def update(self, dt: float) -> None:
        if not (self.__item is None or not self.__item.alive()):
            return

        self.__itemtimer = max(0, self.__itemtimer - dt)
        print(self.__itemtimer)
        if not self.__can_spawn():
            return

        self.spawn()
