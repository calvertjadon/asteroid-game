import pygame

from game import Game
from menu import Menu, MenuOption


class GameManager:
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    def __init__(self, width: int, height: int) -> None:
        pygame.init()

        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

    def display_title_screen(self): ...

    def start_game(self):
        while True:
            menu = Menu(self.__screen, self.__clock)
            selection = menu.show()

            if selection == MenuOption.QUIT:
                break

            if selection == MenuOption.PLAY:
                game = Game(self.__screen, self.__clock)
                game.run()

        pygame.quit()
        quit()
