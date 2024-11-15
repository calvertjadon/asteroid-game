import pygame.constants
from pygame.event import Event

from asteroids.events import CustomEvent


class GameManager:
    __DEFAULT_LIVES = 3

    __score: int
    __lives: int

    __game_over: bool
    __round_over: bool

    def __init__(self) -> None:
        self.__score = 0
        self.__lives = 3
        self.__game_over = False
        self.__round_over = False

    def __handle_player_killed(self) -> None:
        print("player killed")
        if not self.__round_over:
            self.__lives -= 1

        if self.__lives <= 0:
            self.__game_over = True

        self.__round_over = True

    def handle(self, event: Event) -> None:
        match event.type:
            case CustomEvent.ASTEROID_KILLED:
                self.__score += 1

            case CustomEvent.PLAYER_KILLED:
                self.__handle_player_killed()

            case pygame.constants.QUIT:
                self.__stop()

            case _:
                raise AssertionError("Invalid event type", event.type)

    def __stop(self) -> None:
        self.__game_over = True
        self.__round_over = True

    @property
    def score(self) -> int:
        return self.__score

    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def game_over(self) -> bool:
        return self.__game_over

    @property
    def round_over(self) -> bool:
        return self.__round_over

    def reset(self) -> None:
        self.__game_over = False
        self.__lives = self.__DEFAULT_LIVES
        self.__score = 0

    def start_round(self) -> None:
        self.__round_over = False
