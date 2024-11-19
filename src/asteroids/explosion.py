import random
import pygame.draw

from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

from asteroids.circle import Circle


class Particle(Circle):
    __lifespan: float
    __speed: float

    def __init__(
        self,
        center: Vector2,
        velocity: Vector2,
        lifespan: float,
        speed: float,
        radius: float,
        color: Color,
    ) -> None:
        MIN_RADIUS = 3
        MAX_RADIUS = 15

        radius = random.uniform(MIN_RADIUS, min(MAX_RADIUS, radius))
        super().__init__(center, min(radius, 15), velocity)

        self.__lifespan = lifespan
        self.__speed = speed
        self.__color = color

    def update(self, dt: float) -> None:
        self.__lifespan -= dt

        if self.__lifespan <= 0:
            return self.kill()

        self.__speed -= 1.0 * dt
        self._radius -= self.radius * 0.5 * dt
        self._center += self.velocity * dt * self.__speed

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.__color, self.center, self.radius)


def create_explosion(circle: Circle, num_particles: int, colors: list[Color]) -> None:
    MIN_LIFESPAN = 1
    MAX_LIFESPAN = 3

    for _ in range(num_particles):
        angle = random.uniform(0, 360)
        velocity = Vector2(1, 0).rotate(angle)
        speed = random.uniform(30, 50)
        lifespan = random.uniform(MIN_LIFESPAN, MAX_LIFESPAN)
        distance_from_center = random.uniform(0, circle.radius)
        Particle(
            Vector2(circle.center) + velocity * distance_from_center,
            velocity,
            lifespan,
            speed,
            circle.radius * 0.1,
            random.choice(colors),
        )
