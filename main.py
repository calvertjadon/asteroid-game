import pygame
from asteriod import Asteroid
from asteroidfield import AsteroidField
from constants import COLOR_FOREGROUND, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND
from manager import GameManager
from player import Player
from shot import Shot


def main():
    print("Starting asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = updatable  # type: ignore
    _ = AsteroidField()

    Player.containers = (updatable, drawable)  # type: ignore
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (updatable, drawable, bullets)  # type: ignore

    dt = 0

    font = pygame.font.SysFont(None, 24)

    screen.fill(COLOR_BACKGROUND)
    greeting = font.render("hello", True, COLOR_FOREGROUND)
    screen.blit(greeting, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.is_colliding(player):
                print("Game over!")
                return

            for bullet in bullets:
                if asteroid.is_colliding(bullet):
                    asteroid.split()
                    bullet.kill()

        screen.fill(COLOR_BACKGROUND)

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


def main2():
    game = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.start_game()


if __name__ == "__main__":
    main2()
