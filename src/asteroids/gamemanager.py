from pygame.event import Event

from asteroids.events import CustomEvent


class GameManager:
    __score: int

    def __init__(self) -> None:
        self.__score = 0

    def handle(self, event: Event) -> None:
        assert event.type == CustomEvent.ASTEROID_KILLED

        self.__score += 1
        print(self.__score)

    @property
    def score(self) -> int:
        return self.__score
