import pygame
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen) -> None:
        pygame.draw.circle(
            surface=screen,
            color=(255, 255, 255),
            center=self.position,
            radius=self.radius,
        )

    def update(self, dt) -> None:
        self.move(dt)

    def move(self, dt):
        self.position += self.velocity * dt
