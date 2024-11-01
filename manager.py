import pygame

from game import Game


class GameManager:
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    def __init__(self, width: int, height: int) -> None:
        pygame.init()

        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

    def display_title_screen(self): ...

    def start_game(self):
        game = Game(self.__screen, self.__clock)
        game.run()
