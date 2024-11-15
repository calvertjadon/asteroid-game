from pygame.color import Color
import pygame.font

from pygame.rect import Rect
from pygame.surface import Surface
from pygame.math import Vector2
from asteroids.interfaces import IGameManager


class GuiManager:
    __game_manager: IGameManager
    __font: pygame.font.Font
    __screen_size: Rect
    __bg_color: Color
    __fg_color: Color

    def __init__(
        self,
        game_manager: IGameManager,
        screen_size: Rect,
        bg_color: Color,
        fg_color: Color,
    ) -> None:
        self.__game_manager = game_manager
        self.__font = pygame.font.SysFont(None, 24)
        self.__screen_size = screen_size
        self.__fg_color = fg_color
        self.__bg_color = bg_color

    @property
    def fg_color(self) -> Color:
        return self.__fg_color

    @property
    def bg_color(self) -> Color:
        return self.__bg_color

    def draw(self, surface: Surface) -> None:
        score_text = self.__font.render(
            f"Score: {self.__game_manager.score}", False, self.__fg_color
        )
        surface.blit(
            score_text,
            [Vector2(self.__screen_size.center).x, 20],
            score_text.get_rect(),
        )
