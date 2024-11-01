import pygame

from asteriod import Asteroid
from asteroidfield import AsteroidField
from constants import COLOR_BACKGROUND
from player import Player
from shot import Shot


class Game:
    __screen: pygame.Surface
    __clock: pygame.time.Clock
    __dt: float

    __player: Player
    __game_over: bool

    __updatable: pygame.sprite.Group
    __drawable: pygame.sprite.Group
    __asteroids: pygame.sprite.Group
    __bullets: pygame.sprite.Group

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.__initialize_containers()

        self.__screen = screen
        self.__clock = clock
        self.__dt = 0.0
        self.__game_over = False
        self.__player = Player(
            self.__screen.get_width() / 2, self.__screen.get_height() / 2
        )

    def __initialize_containers(self):
        self.__updatable = pygame.sprite.Group()
        self.__drawable = pygame.sprite.Group()
        self.__asteroids = pygame.sprite.Group()
        self.__bullets = pygame.sprite.Group()

        Player.containers = (self.__updatable, self.__drawable)
        Asteroid.containers = (self.__asteroids, self.__updatable, self.__drawable)
        AsteroidField.containers = (self.__updatable,)
        Shot.containers = (self.__updatable, self.__drawable, self.__bullets)

    def __update(self) -> None:
        for obj in self.__updatable:
            obj.update(self.__dt)

    def __draw(self):
        self.__screen.fill(COLOR_BACKGROUND)
        for obj in self.__drawable:
            obj.draw(self.__screen)

    def __handle_collisions(self):
        assert self.__player is not None

        for asteroid in self.__asteroids:
            if asteroid.is_colliding(self.__player):
                self.__game_over = True
                return

            for bullet in self.__bullets:
                if asteroid.is_colliding(bullet):
                    asteroid.split()
                    bullet.kill()

    def run(self):
        _ = AsteroidField()

        while not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.__update()
            self.__handle_collisions()
            self.__draw()

            pygame.display.flip()
            self.__dt = self.__clock.tick(60) / 1000
