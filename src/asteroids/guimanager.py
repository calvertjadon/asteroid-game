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

    def __render_score(self) -> Surface:
        return self.__font.render(
            f"Score: {self.__game_manager.score}", True, self.__fg_color
        )

    def __render_lives(self) -> Surface:
        return self.__font.render(
            f"Lives Remaining: {self.__game_manager.lives}", True, self.fg_color
        )

    def draw(self, surface: Surface) -> None:
        score_text = self.__render_score()
        surface.blit(
            score_text,
            [20, 20],
            score_text.get_rect(),
        )

        lives_text = self.__render_lives()
        surface.blit(
            lives_text,
            [20, 40],
            lives_text.get_rect(),
        )
