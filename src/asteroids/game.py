import pygame

from asteroids.eventmanager import EventManager
from asteroids.guimanager import GuiManager
from asteroids.entitymanager import EntityManager
from asteroids.interfaces import IGameManager


class Game:
    __screen: pygame.Surface
    __entity_manager: EntityManager
    __event_manager: EventManager
    __gui_manager: GuiManager
    __game_manager: IGameManager
    __fps: int

    def __init__(
        self,
        entity_manager: EntityManager,
        gui_manager: GuiManager,
        screen: pygame.Surface,
        event_manager: EventManager,
        game_manager: IGameManager,
        fps: int,
    ) -> None:
        self.__entity_manager = entity_manager
        self.__gui_manager = gui_manager
        self.__screen = screen
        self.__event_manager = event_manager
        self.__game_manager = game_manager
        self.__fps = fps

    def __draw_background(self) -> None:
        self.__screen.fill(self.__gui_manager.bg_color)

    def run(self):
        clock = pygame.time.Clock()
        dt: float = 0.0

        self.__entity_manager.reset()

        while not self.__game_manager.round_over:
            for event in pygame.event.get():
                self.__event_manager.handle(event)

            if not self.__game_manager.round_over:
                self.__entity_manager.update(dt)

            self.__draw_background()
            self.__gui_manager.draw(self.__screen)
            self.__entity_manager.draw(self.__screen)

            pygame.display.flip()
            dt = clock.tick(self.__fps) / 1000

        if not self.__game_manager.game_over:
            self.__game_manager.start_round()
            return self.run()

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
            self.__game_manager.reset()
            return self.run()

        pygame.quit()
