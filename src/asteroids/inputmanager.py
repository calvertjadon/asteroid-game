import pygame.constants
from pygame.event import Event


class InputManager:
    def handle(self, event: Event) -> None:
        assert event.type == pygame.constants.KEYDOWN

        if event.key == pygame.constants.K_ESCAPE:
            quit_event = Event(pygame.constants.QUIT)
            pygame.event.post(quit_event)
