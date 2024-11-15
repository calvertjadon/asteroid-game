from typing import Protocol

from pygame import Surface
from pygame.event import Event
from pygame.sprite import Sprite


class IUpdatable(Protocol):
    def update(self, dt: float) -> None: ...


class IDrawable(Protocol):
    def draw(self, surface: Surface) -> None: ...


class IEventHandler(Protocol):
    def handle(self, event: Event) -> None: ...


class ISpriteManager(Protocol):
    def register(self, sprite: Sprite) -> None: ...


class IGameManager(Protocol):
    @property
    def score(self) -> int: ...

    @property
    def lives(self) -> int: ...

    @property
    def game_over(self) -> bool: ...

    @property
    def round_over(self) -> bool: ...

    def reset(self) -> None: ...

    def start_round(self) -> None: ...
