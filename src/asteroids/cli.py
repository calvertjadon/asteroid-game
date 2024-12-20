import pygame.math

from asteroids.asteroidfield import AsteroidField
from asteroids.config import Config
from asteroids.entityfactory import EntityFactory
from asteroids.entitymanager import EntityManager
from asteroids.eventmanager import EventManager
from asteroids.events import CustomEvent
from asteroids.game import Game
from asteroids.gamemanager import GameManager
from asteroids.guimanager import GuiManager
from asteroids.inputmanager import InputManager
from asteroids.itemmanager import ItemManager
from asteroids.stars import Star, StarField


def main():
    config = Config()

    pygame.init()

    window_rect = pygame.rect.Rect(0, 0, *config.window.size)

    entity_factory = EntityFactory(config.player)
    entity_manager = EntityManager(window_rect, entity_factory)
    game_manager = GameManager()
    gui_manager = GuiManager(
        game_manager=game_manager,
        screen_size=window_rect,
        bg_color=config.window.background_color,
        fg_color=config.window.foreground_color,
    )

    event_manager = EventManager()
    input_manager = InputManager()

    asteroid_field = AsteroidField(window_rect, config.asteroid)

    event_manager.register_handler(pygame.constants.KEYDOWN, input_manager)
    event_manager.register_handler(CustomEvent.ENTITY_CREATED, entity_manager)
    event_manager.register_handler(CustomEvent.ASTEROID_KILLED, game_manager)
    event_manager.register_handler(pygame.constants.QUIT, game_manager)
    event_manager.register_handler(CustomEvent.ASTEROID_KILLED, asteroid_field)
    event_manager.register_handler(CustomEvent.PLAYER_KILLED, game_manager)

    starfield = StarField(window_rect, config.window.star_colors)

    for _ in range(config.window.num_stars):
        starfield.create_star()

    _ = ItemManager(window_rect)

    window = pygame.display.set_mode(
        (config.window.width, config.window.height), pygame.BLEND_RGBA_MULT
    )

    game = Game(
        entity_manager=entity_manager,
        gui_manager=gui_manager,
        window=window,
        event_manager=event_manager,
        game_manager=game_manager,
        fps=config.game.fps,
    )
    game.run()


if __name__ == "__main__":
    main()
