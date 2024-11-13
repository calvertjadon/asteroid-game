from datetime import timedelta
from pydantic import BaseModel, Field


class GameConfig(BaseModel):
    pass


class WindowConfig(BaseModel):
    width: int = Field(default=1280)
    height: int = Field(default=720)


class AsteroidConfig(BaseModel):
    min_radius: int = Field(default=20)
    kinds: int = Field(default=3)
    spawn_rate: timedelta = Field(default_factory=lambda: timedelta(seconds=0.8))

    @property
    def max_radius(self) -> int:
        return self.min_radius * self.kinds


class PlayerConfig(BaseModel):
    pass


class Config(BaseModel):
    game: GameConfig = Field(default_factory=lambda: GameConfig())
    window: WindowConfig = Field(default_factory=lambda: WindowConfig())
    asteroid: AsteroidConfig = Field(default_factory=lambda: AsteroidConfig())
    player: PlayerConfig = Field(default_factory=lambda: PlayerConfig())
