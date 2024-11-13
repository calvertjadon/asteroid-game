from datetime import timedelta
import pygame

from asteroids.config import Config
from asteroids.player import Player


def run(config: Config):
    pygame.init()
    screen = pygame.display.set_mode((config.window.width, config.window.height))
    clock = pygame.time.Clock()
    dt: timedelta = timedelta()

    player = Player(center=config.window.center, config=config.player)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.constants.QUIT:
                    return pygame.quit()
                case pygame.constants.KEYDOWN:
                    if event.key == pygame.constants.K_ESCAPE:
                        return pygame.quit()

        screen.fill(pygame.Color("#333333"))

        player.update(dt)
        player.draw(screen)

        pygame.display.flip()
        dt = timedelta(seconds=clock.tick(config.game.fps))
