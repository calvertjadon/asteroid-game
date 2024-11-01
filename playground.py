import pygame
from enum import Enum
from dataclasses import dataclass
from typing import Callable


class Colors(pygame.Color, Enum):
    DARK = pygame.Color("#131313")
    LIGHT = pygame.Color("#fafafa")


@dataclass
class Config:
    display_size: tuple[int, int]
    font_name: str
    font_size: int


class Event:
    __handlers: list[Callable]

    def __init__(self) -> None:
        self.__handlers = []

    def invoke(self) -> None:
        for handler in self.__handlers:
            handler()

    def add_handler(self, handler: Callable) -> None:
        self.__handlers.append(handler)


def draw_text(
    display: pygame.Surface,
    text: str,
    font_name: str,
    font_size: int,
    center_pos: tuple[int, int],
) -> None:
    font = pygame.font.Font(font_name, font_size)
    text_surface = font.render(text, True, Colors.LIGHT)
    text_rect = text_surface.get_rect()
    text_rect.center = center_pos
    display.blit(text_surface, text_rect)


class Menu:
    __config: Config
    __display: pygame.Surface
    # __running: bool
    __cursor_rect: pygame.Rect  # for selecting menu items

    blit_screen: Event

    def __init__(self, display: pygame.Surface, config: Config) -> None:
        self.__config = config
        self.__display = display
        # self.__running = True
        self.__cursor_rect = pygame.Rect(0, 0, 20, 20)
        # self.__offset = -100
        self.blit_screen = Event()

    def __draw_cursor(self) -> None:
        draw_text(
            display=self.__display,
            text="*",
            font_name=self.__config.font_name,
            font_size=15,
            center_pos=self.__cursor_rect.center,
        )

    def __blit_screen(self) -> None:
        self.blit_screen.invoke()


class MainMenu: ...


class Game:
    __running: bool
    __playing: bool
    __config: Config
    __display: pygame.Surface
    __window: pygame.Surface

    __enter_pressed: Event
    __backspace_pressed: Event
    __up_pressed: Event
    __down_pressed: Event

    def __init__(self, config: Config) -> None:
        pygame.init()

        self.__config = config
        self.__running = True
        self.__playing = False

        self.__enter_pressed = Event()
        self.__backspace_pressed = Event()
        self.__up_pressed = Event()
        self.__down_pressed = Event()

        self.__enter_pressed.add_handler(self.__on_enter_pressed)
        self.__backspace_pressed.add_handler(self.__on_backspace_pressed)
        self.__up_pressed.add_handler(self.__on_up_pressed)
        self.__down_pressed.add_handler(self.__on_down_pressed)

        self.__display = pygame.Surface(config.display_size)
        self.__window = pygame.display.set_mode(config.display_size)

    @property
    def is_running(self) -> bool:
        return self.__running

    def __on_enter_pressed(self) -> None:
        self.__playing = False

    def __on_backspace_pressed(self) -> None:
        print("backspace pressed")

    def __on_up_pressed(self) -> None:
        print("up pressed")

    def __on_down_pressed(self) -> None:
        print("down pressed")

    def __handle_keypress(self, key: int) -> None:
        match key:
            case pygame.constants.K_RETURN:
                self.__enter_pressed.invoke()

    def __check_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.constants.QUIT:
                    self.__running, self.__playing = False, False
                case pygame.constants.KEYDOWN:
                    self.__handle_keypress(event.key)

    def __game_loop(self) -> None:
        while self.__playing:
            self.__check_events()
            self.__display.fill(Colors.DARK)
            draw_text(
                display=self.__display,
                text="Thanks for playing!",
                font_name=self.__config.font_name,
                font_size=20,
                center_pos=(
                    int(self.__display.get_width() / 2),
                    int(self.__display.get_height() / 2),
                ),
            )
            self.__blit_screen()

    def __blit_screen(self) -> None:
        self.__window.blit(self.__display, (0, 0))
        pygame.display.update()

    def play(self) -> None:
        self.__playing = True
        self.__game_loop()


if __name__ == "__main__":
    config = Config(
        display_size=(480, 270), font_name=pygame.font.get_default_font(), font_size=24
    )
    game = Game(config)

    while game.is_running:
        game.play()
