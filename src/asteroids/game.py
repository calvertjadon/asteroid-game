import pygame

from asteroids.config import Config


def run(config: Config):
    pygame.init()
    screen = pygame.display.set_mode((config.window.width, config.window.height))

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.constants.QUIT:
                    return

        screen.fill(pygame.Color("#333333"))
        pygame.display.flip()
