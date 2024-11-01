from abc import ABC, abstractmethod
from enum import Enum, auto
import re
from typing import Sequence
import pygame
from pygame.color import Color
from pygame.rect import Rect

from constants import COLOR_BACKGROUND, COLOR_FOREGROUND, PLAYER_TURN_SPEED


_FG = pygame.Color(COLOR_FOREGROUND)
_BG = pygame.Color(COLOR_BACKGROUND)


class MenuOption(Enum):
    PLAY = auto()
    QUIT = auto()


class Node(pygame.sprite.Sprite, ABC):
    containers: Sequence[pygame.sprite.Group]

    def __init__(self) -> None:
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # type: ignore
        else:
            super().__init__()

    @abstractmethod
    def draw(self, screen: pygame.Surface): ...

    def update(self, invert=False): ...


class TextNode(Node):
    __node: pygame.Surface
    __rect: pygame.Rect

    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        centerx: int,
        centery: int,
        fg: pygame.Color = _FG,
        bg: Color = _BG,
    ) -> None:
        super().__init__()

        self.__node = font.render(text, True, fg, bg)
        self.__rect = self.__node.get_rect()
        self.__rect.centerx = centerx
        self.__rect.centery = centery

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__node, self.__rect)


class ButtonNode(Node):
    __rect: pygame.Rect
    __font: pygame.font.Font
    __text: str
    __inverted: bool

    def __init__(self, text: str, font: pygame.font.Font, rect: pygame.Rect) -> None:
        super().__init__()
        self.__inverted = True

        self.__rect = rect
        self.__font = font
        self.__text = text

    def draw(self, screen: pygame.Surface):
        if not self.__inverted:
            label = self.__font.render(self.__text, True, _BG)
            border_width = 0
        else:
            label = self.__font.render(self.__text, True, _FG)
            border_width = 2

        pygame.draw.rect(screen, _FG, self.__rect, border_width)
        screen.blit(label, label.get_rect(center=self.__rect.center))

    def update(self, invert: bool = False) -> None:
        self.__inverted = invert


class Menu:
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    __updatable: pygame.sprite.Group
    __drawable: pygame.sprite.Group
    __buttons: pygame.sprite.Group

    __selected_idx: int

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.__screen = screen
        self.__clock = clock

        self.__updatable = pygame.sprite.Group()
        self.__drawable = pygame.sprite.Group()
        self.__buttons = pygame.sprite.Group()

        self.__selected_idx = 0

        TextNode.containers = (self.__drawable,)
        ButtonNode.containers = (self.__drawable, self.__updatable, self.__buttons)

    def __update(self) -> None:
        for i, obj in enumerate(self.__updatable):
            obj.update(not i == self.__selected_idx)

    def __draw(self) -> None:
        self.__screen.fill(COLOR_BACKGROUND)

        for obj in self.__drawable:
            obj.draw(self.__screen)

    def show(self):
        font = pygame.font.SysFont(None, 24)

        # title = font.render("Asteroids", True, COLOR_FOREGROUND, COLOR_BACKGROUND)
        # title_rect = title.get_rect()
        # title_rect.center = self.__screen.get_rect().center

        _ = TextNode(
            "Asteroids",
            font,
            self.__screen.get_rect().centerx,
            self.__screen.get_rect().centery,
        )

        BUTTON_WIDTH = 256
        BUTTON_HEIGHT = 32
        BUTTON_MARGIN = BUTTON_HEIGHT / 4

        play_btn = ButtonNode(
            "Play",
            font,
            pygame.Rect(
                self.__screen.get_rect().centerx - BUTTON_WIDTH / 2,
                self.__screen.get_rect().centery
                - BUTTON_HEIGHT / 2
                + (BUTTON_HEIGHT + BUTTON_MARGIN) * 1,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        )
        quit_btn = ButtonNode(
            "Quit",
            font,
            pygame.Rect(
                pygame.Rect(
                    self.__screen.get_rect().centerx - BUTTON_WIDTH / 2,
                    self.__screen.get_rect().centery
                    - BUTTON_HEIGHT / 2
                    + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT,
                ),
            ),
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    return

                if event.type == pygame.constants.KEYDOWN:
                    if event.key == pygame.constants.K_k:
                        self.__selected_idx = max(0, self.__selected_idx - 1)
                    if event.key == pygame.constants.K_j:
                        self.__selected_idx = min(
                            len(self.__buttons) - 1, self.__selected_idx + 1
                        )
                    if event.key == pygame.constants.K_RETURN:
                        if self.__selected_idx == [b for b in self.__buttons].index(
                            quit_btn
                        ):
                            return MenuOption.QUIT

                        if self.__selected_idx == [b for b in self.__buttons].index(
                            play_btn
                        ):
                            return MenuOption.PLAY

            self.__update()
            self.__draw()

            pygame.display.update()
            _ = self.__clock.tick(60) / 1000
