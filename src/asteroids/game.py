import pygame
from pygame.event import Event

from asteroids.eventmanager import EventManager
from asteroids.events import CustomEvent
from asteroids.guimanager import GuiManager
from asteroids.entitymanager import EntityManager


class Game:
    __screen: pygame.Surface
    __entity_manager: EntityManager
    __event_manager: EventManager
    __gui_manager: GuiManager
    __fps: int

    __game_over: bool

    def __init__(
        self,
        entity_manager: EntityManager,
        gui_manager: GuiManager,
        screen: pygame.Surface,
        event_manager: EventManager,
        fps: int,
    ) -> None:
        self.__entity_manager = entity_manager
        self.__gui_manager = gui_manager
        self.__screen = screen
        self.__event_manager = event_manager
        self.__fps = fps
        self.__game_over = False

        self.__event_manager.register_handler(pygame.constants.QUIT, self)
        self.__event_manager.register_handler(CustomEvent.GAME_OVER, self)

    def __draw_background(self) -> None:
        self.__screen.fill(self.__gui_manager.bg_color)

    def handle(self, event: Event) -> None:
        assert event.type in (pygame.constants.QUIT, CustomEvent.GAME_OVER)

        self.__game_over = True

    def run(self):
        clock = pygame.time.Clock()
        dt: float = 0.0

        self.__entity_manager.reset()

        self.__game_over = False
        while not self.__game_over:
            for event in pygame.event.get():
                self.__event_manager.handle(event)

            self.__draw_background()
            self.__entity_manager.update(dt)
            self.__entity_manager.draw(self.__screen)
            self.__gui_manager.draw(self.__screen)

            pygame.display.flip()
            dt = clock.tick(self.__fps) / 1000

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
