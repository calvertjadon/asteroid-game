import pygame

from asteroids.asteroidfield import AsteroidField
from asteroids.config import Config
from asteroids.eventmanager import EventManager
from asteroids.events import CustomEvent
from asteroids.player import Player
from asteroids.entitymanager import EntityManager
from asteroids.inputmanager import InputManager


class Game:
    __config: Config
    __screen: pygame.Surface
    __entity_manager: EntityManager
    __event_manager: EventManager

    def __init__(self, config: Config) -> None:
        self.__config = config

        self.__entity_manager = EntityManager(pygame.Vector2(config.window.size))

        self.__event_manager = EventManager()
        self.__event_manager.register_handler(pygame.constants.KEYDOWN, InputManager())
        self.__event_manager.register_handler(
            CustomEvent.ENTITY_CREATED, self.__entity_manager
        )

        self.__screen = pygame.display.set_mode(
            (
                self.__config.window.width,
                self.__config.window.height,
            )
        )

    def __draw_background(self) -> None:
        self.__screen.fill(pygame.Color(self.__config.window.background_color))

    def run(self):
        pygame.init()

        clock = pygame.time.Clock()
        dt: float = 0.0

        Player(
            center=self.__config.window.center,
            config=self.__config.player,
        )
        AsteroidField(
            pygame.Vector2(self.__config.window.size),
            self.__config.asteroid,
        )

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    game_over = True

                if event.type == CustomEvent.GAME_OVER:
                    game_over = True

                self.__event_manager.handle(event)

            if not game_over:
                self.__draw_background()
                self.__entity_manager.update(dt)
                self.__entity_manager.draw(self.__screen)

            pygame.display.flip()
            dt = clock.tick(self.__config.game.fps) / 1000

        self.__entity_manager.reset()

        running = True
        restart = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    running = False

                if event.type == pygame.constants.KEYDOWN:
                    if event.key == pygame.constants.K_RETURN:
                        restart = True
                        running = False
                    if event.key == pygame.constants.K_ESCAPE:
                        running = False

        if restart:
            return self.run()

        pygame.quit()
