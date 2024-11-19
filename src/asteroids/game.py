import pygame

from asteroids.eventmanager import EventManager
from asteroids.guimanager import GuiManager
from asteroids.entitymanager import EntityManager
from asteroids.interfaces import IGameManager


class Game:
    __window: pygame.Surface
    __game_screen: pygame.Surface
    __gui_screen: pygame.Surface
    __entity_manager: EntityManager
    __event_manager: EventManager
    __gui_manager: GuiManager
    __game_manager: IGameManager
    __fps: int

    def __init__(
        self,
        entity_manager: EntityManager,
        gui_manager: GuiManager,
        window: pygame.Surface,
        event_manager: EventManager,
        game_manager: IGameManager,
        fps: int,
    ) -> None:
        self.__entity_manager = entity_manager
        self.__gui_manager = gui_manager
        self.__window = window
        self.__event_manager = event_manager
        self.__game_manager = game_manager
        self.__fps = fps
        self.__game_screen = pygame.Surface(self.__window.get_size())
        self.__gui_screen = pygame.Surface(self.__window.get_size())

    def __show_gui(self, new_game=True) -> bool:
        clock = pygame.time.Clock()

        running = True
        start = False
        while running:
            for event in pygame.event.get():
                self.__event_manager.handle(event)

                if event.type == pygame.constants.QUIT:
                    running = False

                if event.type == pygame.constants.KEYDOWN:
                    if event.key == pygame.constants.K_RETURN:
                        start = True
                        running = False
                    if event.key == pygame.constants.K_ESCAPE:
                        running = False

            if new_game:
                self.__gui_manager.new_game(self.__gui_screen)
            else:
                self.__gui_manager.game_over(self.__gui_screen)

            self.__window.blit(self.__gui_screen, (0, 0))
            pygame.display.flip()
            clock.tick(30)

        return start

    def run(self, skip_title=False):
        clock = pygame.time.Clock()
        dt: float = 0.0

        if not skip_title:
            self.__gui_manager.new_game(self.__gui_screen)
            start = self.__show_gui(new_game=True)

            if not start:
                return pygame.quit()

        self.__entity_manager.reset()
        while not self.__game_manager.round_over:
            for event in pygame.event.get():
                self.__event_manager.handle(event)

            if not self.__game_manager.round_over:
                self.__entity_manager.update(dt)

            self.__gui_manager.draw(self.__game_screen)
            self.__entity_manager.draw(self.__game_screen)

            self.__window.blit(self.__game_screen, (0, 0))
            pygame.display.flip()
            dt = clock.tick(self.__fps) / 1000

        if not self.__game_manager.game_over:
            self.__game_manager.start_round()
            return self.run(skip_title=True)

        self.__gui_manager.game_over(self.__gui_screen)
        restart = self.__show_gui(new_game=False)

        if restart:
            self.__game_manager.reset()
            return self.run(skip_title=True)

        pygame.quit()
