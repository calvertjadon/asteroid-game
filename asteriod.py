from typing import Sequence
import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, COLOR_ASTEROID


class Asteroid(CircleShape):
    containers: Sequence[pygame.sprite.Group]

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen) -> None:
        pygame.draw.circle(
            surface=screen,
            color=COLOR_ASTEROID,
            center=self.position,
            radius=self.radius,
            width=2,
        )

    def update(self, dt) -> None:
        self.move(dt)

    def move(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        child_a = Asteroid(
            self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS
        )
        child_b = Asteroid(
            self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS
        )

        child_a.velocity = self.velocity.rotate(random_angle) * 1.2
        child_b.velocity = self.velocity.rotate(-random_angle)
