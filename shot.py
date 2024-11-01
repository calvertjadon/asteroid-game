from typing import Sequence
import pygame
from circleshape import CircleShape
from constants import COLOR_SHOT


class Shot(CircleShape):
    containers: Sequence[pygame.sprite.Group]

    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            surface=screen,
            color=COLOR_SHOT,
            center=self.position,
            radius=self.radius,
        )

    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float):
        self.position += self.velocity * dt
