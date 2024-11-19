from pygame.math import Vector2
from asteroids.asteroid import Asteroid
from asteroids.asteroidfield import AsteroidField
from asteroids.config import AsteroidConfig, PlayerConfig
from asteroids.player import Player


class EntityFactory:
    __player_config: PlayerConfig

    def __init__(self, player_config: PlayerConfig) -> None:
        self.__player_config = player_config

    def create_player(self, center: Vector2) -> Player:
        return Player(center=center, config=self.__player_config)
